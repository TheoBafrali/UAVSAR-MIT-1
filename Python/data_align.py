import numpy as np
import math

def align_data(radar_data,motion_data,radar_point_one,motion_point_one):
    radar_collection_hz = 1/.011
    motion_collection_hz = 1/.002778
    constant = motion_collection_hz/radar_collection_hz
    Pulses = radar_data[0][radar_point_one:]
    new_motion_data = motion_data[motion_point_one:] 
    aligned_motion_data = []
    too_long = True
    while too_long:
        if (len(Pulses) * constant) > len(new_motion_data):
            Pulses = Pulses[:(len(Pulses)-1)]
        else:
            too_long = False

    for i in range(len(Pulses)):
        temp_list = []
        for x in range(0,3):
            list_data = new_motion_data[math.floor(constant*i)][x]
            temp_list.append(list_data)
        aligned_motion_data.append(temp_list)
        final = [Pulses, aligned_motion_data]
   
    return final

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
