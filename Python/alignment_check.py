'''
Allows for checking of automatic data alignment, and is flexible for manual editing of data.

@author: Mason
'''

#Import required modules
from Unpack import unpack
from read_files import read_radar_data, read_motion_data
from radar_movement import find_point_one_radar, find_i_of_first_motion, find_i_of_last_motion
from data_align import align_data
from AlignedRangeTimeGraph import AlignedGraph
#from RangeTimeGraph import rti_graph
import numpy as np
import matplotlib.pyplot as plt
unpack("../Raw_data/uavsar1flight1") #Currently commented out because unused
motion_data = read_motion_data("../Raw_Data/UASSAR4_rail_diagonal.csv","UASSAR4")
radar_data = read_radar_data("../Raw_Data/data.pkl")
motion_start = find_i_of_first_motion(motion_data)
motion_end = find_i_of_last_motion(motion_data)

radar_start = find_point_one_radar(radar_data)

#Aligns data, currently using frames given in function definition
aligned_data = align_data(radar_data,motion_data,radar_start,motion_start, motion_end)
radar_end = aligned_data[2]
rti_graph(radar_data,motion_data,radar_start,motion_start,motion_end,radar_end)

#Plots aligned graph
#AlignedGraph(aligned_data,radar_data)
