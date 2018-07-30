import numpy as np
import math

def align_data(radar_data,motion_data,radar_point_one,motion_point_one):
    radar_collection_hz = 1/.008 #Need to confirm
    motion_collection_hz = 360
    constant = motion_collection_hz/radar_collection_hz
    Pulses = radar_data[0][radar_point_one:1775]
    radar_time = radar_data[1][radar_point_one-1:] - (radar_data[1][radar_point_one-1])
    starting_radar_time = radar_time[1]
    new_motion_data = motion_data[motion_point_one:9992] 
    motion_time = []
    for i in range(len(new_motion_data)):
        motion_time.append(1000*i*1/360)  
   
    iterated_radar_time = starting_radar_time
    final_motion_list = []
    count = 0
    for i in range(len(motion_time)):
            if radar_time[count] <= motion_time[i]:
                count += 1
                iterated_radar_time += starting_radar_time
                final_motion_list.append(new_motion_data[i])
    Final = [Pulses,final_motion_list]
    #print(new_motion_data)
    #print(final_motion_list)
    return Final


    '''
    aligned_motion_data = []
    too_long = True 
    while too_long:
        if (len(Pulses) * constant) > len(new_motion_data):
            Pulses = Pulses[:(len(Pulses)-1)]
            #print("Too Long Ran")
        else:
            too_long = False
  
    for i in range(len(Pulses)):
        temp_list = []
        for x in range(0,3):
            list_data = new_motion_data[math.floor(constant*i)][x]
            temp_list.append(list_data)
        aligned_motion_data.append(temp_list)
        #[[x,y,z],[x,y,z]]
        final = [Pulses, aligned_motion_data]
    return final  
'''

'''
    def takeClosest(time, value): #returns the index of where this value belongs
   for i in range(len(time)):
       #print(time[i])
       if value >= time[i] and i + 1 < len(time):
           if value < time[i+1]:
               return i
   return len(time) - 1
'''
    
'''

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
