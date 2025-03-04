'''
Aligns RADAR and position  data

@author: David + Mason
'''
#Import required  modules
import numpy as np
import math
import matplotlib.pyplot as plt
from spline2 import interp_3

def align_data(radar_data,motion_data,radar_point_one,motion_point_one,motion_point_last, lefttrim, righttrim):
    '''
    Inputs: 
        radar_data: contains pulses, timestamps, and range bins
        motion_data: contains position data for a set of times
        radar_point_one, motion_point_one, motion_point_last: currently unused
        lefttrim: leftmost pulse outputted in data
        righttrim: rightmost pulse outputted in data
        
    Outputs: 
        Returns aligned data
        
    Summary:
        RADAR data and motion data have different sampling rates (Motion: 360, RADAR: ?), so the data needs to be aligned
    '''
    #Takes relevant RADAR data
    Pulses = radar_data[0][radar_point_one:20000]
    radar_time = radar_data[1][radar_point_one-1:] - (radar_data[1][radar_point_one-1])
    starting_radar_time = radar_time[1]
    
    #Takes relevant motion data
    new_motion_data = motion_data[motion_point_one:motion_point_last] 
    new_motion_data = np.array(interp_3(new_motion_data))
    motion_time = range(0,len(new_motion_data)) 
    
    '''
    motion_time = []
    for i in range(len(new_motion_data)):
        motion_time.append(1000*i*1/360)  
    '''
    #Calculates aligned data
    iterated_radar_time = starting_radar_time
    final_motion_list = []
    count = 0
    for i in range(len(motion_time)):
            if radar_time[count] <= motion_time[i]:
                count += 1
                iterated_radar_time += starting_radar_time
                final_motion_list.append(new_motion_data[i])
                
    #Truncate data
    final_motion_list = final_motion_list[lefttrim:righttrim]
    Pulses = Pulses[lefttrim:righttrim ,:]
    Final = [Pulses,final_motion_list,len(final_motion_list)+radar_point_one]
    
    #Return outputs
    print(len(Pulses))
    print(len(final_motion_list))
    #print(final_motion_list)
    return Final

'''
    #Linear Interpolation
    for i in range(len(Pulses)):
        floor_val = (constant*i) - math.floor(constant*i)
        ceil_val = 1 - floor_val
        temp_list = []
        for x in range(0,3):
            #print(math.floor(constant*i))
            floored = floor_val * new_motion_data[math.floor(constant*i)][x]
            ceiling = ceil_val * new_motion_data[math.ceil(constant*i)][x]
            temp_list.append(floored+ceiling)
        aligned_motion_data.append(temp_list)
'''
