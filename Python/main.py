'''
Runs the entire workflow, taking motion capture data (a .csv) and radar data (a binary file), 
aligns data, calculates backprojected image, deconvolutes image, and plots.  

@author: Mason + David 
'''

#Import required modules
from Unpack import unpack 
from read_files import read_radar_data, read_motion_data
from radar_movement import find_point_one_radar, find_i_of_first_motion, find_i_of_last_motion
from data_align import align_data
from AlignedRangeTimeGraph import AlignedGraph 
from LinInt import BackProjection
from read_intensity import read_intensity
from Deconvolution import deconvolute
from backprojection import interp_approach, main #Ramu's backprojection

#Converts motion and RADAR data to the right data structures
#unpack("../Raw_data/RailSAR-record1") #Currently commented out because unused
motion_data = read_motion_data("../Raw_Data/UASSAR4_rail_diagonal.csv","UASSAR4")
radar_data = read_radar_data("../Raw_Data/railTestDiagonal.pkl")

#Calculates the right frames to perform alignment on
#Currently using manual alignment,  instead of these functions
motion_start = find_i_of_first_motion(motion_data)
print(motion_start)
motion_end = find_i_of_last_motion(motion_data)
print(motion_end)
radar_start = find_point_one_radar(radar_data)
print(radar_start)

#Aligns data, currently using frames given in function definition
aligned_data = align_data(radar_data,motion_data,radar_start,motion_start, motion_end)

#Plots aligned graph
AlignedGraph(aligned_data,radar_data)

#Calculates and plots BackProjected Image
IntensityList = BackProjection(aligned_data,radar_data,[-5,-5],[5,5],0.005)

#Deconvolutes image and plots images
deconvolute(IntensityList, IterationNumber = 3, PercentageMin = 1/5.5)

'''
#Currently unused code

#Calculates backprojected image using Ramu's algorithm
interp_approach(aligned_data,radar_data,[-3,3],[-3,3],.1)

#Reads in an intensity list and saves it as an intensity list
IntensityList = read_intensity('../Raw_Data/intensity2.csv')

'''
