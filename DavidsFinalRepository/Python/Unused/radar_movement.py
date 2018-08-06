'''
Calculates frames that RADAR data start/end and the frame that motion data starts from

@author: Mason + Theo
'''

#Import required modules
import matplotlib.pyplot as plt
import numpy as np
import pandas
from scipy.stats import chi2_contingency
from read_files import read_radar_data, read_motion_data


'''
distance between n  dimensional vecotrs in a list [a,b]
'''
def euc_norm(x):

    if np.array(x).ndim == 1:
       return np.linalg.norm(x)

    _x = np.array(x[0])
    _y = np.array(x[1])
    return np.linalg.norm(_x - _y)

'''
returns a list of the peaks and their indices, as [peak_val, og_index]
'''
def find_peaks(nums):
    returnable = []
    for ii in range(1, len(nums) - 1):
        if nums[ii] > nums[ii + 1] and nums[ii] > nums[ii - 1]:
             returnable.append([nums[ii], ii])
    return returnable

'''
returns pulse index of first motion, only works for railSAR as of now
'''
def find_point_one_radar(data):

    Pulses = np.flip(data[0],0)
    Time = np.array(data[1])*.001
    Pulses = Pulses + 2**17
    
    p_vals = []
    nums = 3
    for i in range(len(Pulses)-nums):
        chi2, p, dof, ex = chi2_contingency(Pulses[i:i+nums])
        p_vals.append(p)
    whitespace = 300
    in_a_row = 0
    start_motion_pulse = []
    has_peaked = False
    last_peak = 0
    for i in range(len(p_vals)):
        if p_vals[i] > .85:
            has_peaked = True
        if p_vals[i] < .85 and has_peaked:
            in_a_row = in_a_row + 1
            if last_peak == 0:
                last_peak = i
        else:
            in_a_row = 0
            last_peak = 0
        if in_a_row == whitespace:
            start_motion_pulse.append(last_peak)
            last_peak = 0
        
    #plt.plot(np.flip(p_vals,0),range(len(p_vals)))
    #plt.show()
    #print(start_motion_pulse[0])
    return start_motion_pulse[0]


def delta_detector(data):
    v = np.array([])
    vs = np.array([])
    d = np.array([])
    ds = np.array([])
    std_dev = np.array([])
    indices_of_first_motion = []

    s_k = 50
    std_dev_win = 100

    # compute velocities from position data
    for ii in range(0, len(data) - 1):
        d = np.append(d, euc_norm(data[ii]))
        if ii != 0:
            v = np.append(v, [d[ii] - d[ii - 1]])

    # compute smoothed distance and velocity
    for ii in range(int(s_k / 2), len(data) - int(s_k / 2)):
        ds = np.append(ds, np.mean(d[ii - int(s_k / 2):ii + int(s_k / 2)]))
        vs = np.append(vs, np.mean(v[ii - int(s_k / 2):ii + int(s_k / 2)]))

    # compute standard deviation of windowed dataset
    for ii in range(int(0 *  std_dev_win), len(vs) - int(1 * std_dev_win)):
        std_dev = np.append(std_dev, np.std(vs[ii - int(std_dev_win * 0):ii + int(std_dev_win * 1)]))


    #plt.plot(d)
    #plt.plot(ds)
    '''
    plot velocity, smoothed velocity, std_dev
    '''
    #plt.plot(v)
    #plt.plot(vs)
    '''
    scale and cube std_dev to improve SNR
    '''
    std_dev = np.array(std_dev) * 4000
    std_dev = np.power(std_dev, np.full((len(std_dev)), 3))
    #plt.plot(std_dev)

    '''
    compute the local maxima peaks of the sigma_squared sata
    '''
    peak_sigma_sq = find_peaks(std_dev)

    '''
    compute the avg, untainted by large spikes
    '''
    running_avgs = []

    fuckingHey = []
    goddamnit = []

    for ii in range(0, len(peak_sigma_sq)):
        fuckingHey.append(peak_sigma_sq[ii][0])


    for ii in range(0, len(peak_sigma_sq)):
        goddamnit.append(peak_sigma_sq[ii][1])

    for ii in range(0, len(peak_sigma_sq)):
        running_avgs.append(np.mean(fuckingHey[0:ii]))


    running_avgs = 100 * np.array(running_avgs)
    #plt.plot(goddamnit, running_avgs)
    #print("running_avgs::")
    #print(running_avgs)


    total_std_peaks = 0
    for ii in range(0, len(peak_sigma_sq)):
        if not peak_sigma_sq[ii][0] > 3 * total_std_peaks / (ii + 1):
            total_std_peaks += peak_sigma_sq[ii][0]


    for ii in range(0, len(peak_sigma_sq)):
        if peak_sigma_sq[ii][0] > running_avgs[ii]:
            indices_of_first_motion.append(int(peak_sigma_sq[ii][1]))
    '''
    for ii in range(0, len(indices_of_first_motion)):
        plt.plot([indices_of_first_motion[ii], indices_of_first_motion[ii]], [0,1])
    '''

    #print("indices_of_first_motion::")
    #plt.ylim(-.0015, 10)
    '''
    for ii in range(0, len(peak_sigma_sq)):
        plt.plot([peak_sigma_sq[ii][1], peak_sigma_sq[ii][1]], [0,1])
    '''
    #plt.plot([indices_of_first_motion[0], indices_of_first_motion[0]], [0,10])
    #plt.show()
    return indices_of_first_motion[0]


def find_i_of_first_motion(motion_data):
    data = np.array(motion_data)
    return delta_detector(data)

def find_i_of_last_motion(motion_data):
    data = np.flip(np.array(motion_data),0)
    return len(data) - delta_detector(data)




