from numpy import genfromtxt,average, array, real, arange, reshape
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import scatter, xlabel, ylabel, xlim, ylim, show, plot
import pickle
import numpy as np
from scipy.constants import speed_of_light
data = pickle.load(open('5Points_data.pkl','rb'))
Platform = data[0] #Platform
PlatformX = Platform[:, 0]
Pulses = data[1] #Pulses
RangeAxis = data[2] #RangeAxis
PulsesAbs = np.absolute(Pulses)
PulsesReal = real(Pulses)

h_width = 3
h_height = 3
pxl_d = .1
p_width = int(2 * h_width / pxl_d)
p_height = int(2 * h_height / pxl_d)


def euc_norm(v1, v2):
   return np.linalg.norm([v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]])

def bin(x):
    bin = int (x/0.0185)
    if x % 0.0185 >= 0.00925:
        realbin = bin - 1
    else:
        realbin = bin
    return realbin

xlist = []
ylist = []
intensitylist = []
fig = plt.figure()

pixels = np.zeros((p_width, p_height))


align_rangebins_at_this = 500


def roll(array, current_bin, desired_bin):
    array = np.insert(array, 0, np.zeros(500))
    array = np.append(array, np.zeros(500))
    return np.roll(array, current_bin - desired_bin)

def test():
    intensity_vec = np.zeros((p_width * p_height, 2084))
    for x in range(0, p_width):
        for y in range(0, p_height):
            # for each pxl
            pxl_coord = [x*pxl_d - h_width, y*pxl_d - h_height, 0]

        for ii in range(0, len(PlatformX)):
            rangebin = int(bin(euc_norm(Platform[ii], pxl_coord)))
            intensity_vec[x * y] += np.absolute(roll(Pulses[ii], rangebin, 500))

    for i in range(0, p_height * p_width):
        plt.plot(intensity_vec[i])

    plt.show()




def plotSAR():
    for x in range(0, p_width):
        for y in range(0, p_height):
            intensity = 0
            for i in range(len(PlatformX)):
                pxl_coord = [x*pxl_d - h_width, y*pxl_d - h_height, 0]
                rangebin = int(bin(euc_norm(Platform[i], pxl_coord)))
                intensity += Pulses[i, int(bin(euc_norm(Platform[i], pxl_coord)))]

            pixels[x][y] = np.absolute(intensity)

    plt.imshow(pixels)
    plt.show()


def plotFourierSAR():
    for x in range(0, p_width):
        for y in range(0, p_height):
            # per pxl
            pxl_coord = [x*pxl_d - h_width, y*pxl_d - h_height, 0]
            ref_signal_d = euc_norm(Platform[50], pxl_coord)
            signal_sum = np.zeros(1084, dtype = complex)

            for i in range(len(PlatformX)):
                # per pulse
                og_sig = Pulses[i]
                this_signal_d = euc_norm(Platform[i], pxl_coord)
                delta_d = ref_signal_d - this_signal_d
                time_delta = 2 * delta_d / speed_of_light
                freq_rep = np.fft.fft(og_sig)
                plt.plot(freq_rep)
                plt.show()
                #np.exp(-1j *2*np.pi*4.06*(10**9)*time_delta))
                phi_shifted_sig = np.fft.ifft()
                signal_sum += phi_shifted_sig

            pixels[x][y] = np.max(np.absolute(signal_sum))


    plt.imshow(pixels)
    plt.show()


#test()
#plotSAR()
plotFourierSAR()
