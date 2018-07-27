import matplotlib.pyplot as plt
import numpy as np
import pandas
from scipy.stats import chi2_contingency

def radar_point_one(data):
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
    return start_motion_pulse[0]
