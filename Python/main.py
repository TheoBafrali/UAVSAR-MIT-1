'''
Runs the entire workflow, taking motion capture data (a .csv) and radar data (a binary file), 
aligns data, calculates backprojected image, deconvolutes image, and plots.  

@author: Mason + David 
'''

#Import required modules
from pulson440_unpack import unpack 
from read_files import read_radar_data, read_motion_data
from radar_movement import find_point_one_radar, find_i_of_first_motion, find_i_of_last_motion
from data_align import align_data
from GeneralAlignedRangeTimeGraph import AlignedGraph 
from FastLinInt import BackProjection
from read_intensity import read_intensity
from Deconvolution import deconvolute
from backprojection import interp_approach, main #Ramu's backprojection

#Converts motion and RADAR data to the right data structures
unpack("../Raw_Data/uavsar1flight1") #Currently commented out because unused

#Loads data from the RADAR
motion_data = read_motion_data("../Raw_Data/UAVSAR1Flight1.csv","UAVSAR1")
radar_data = read_radar_data("../Raw_Data/data.pkl")

#Finds the first point of the motion data that it starts to move
#motion_start = find_i_of_first_motion(motion_data)

#Finds the last point of the motion data that it moves
#motion_end = find_i_of_last_motion(motion_data)

#Finds the first point in the radar data that it starts to move
#radar_start = find_point_one_radar(radar_data)

radar_start = 600
motion_start = 6600
motion_end = 29545

#Aligns data, currently using frames given in function definition
aligned_data = align_data(radar_data,motion_data,radar_start,motion_start, motion_end)

#Plots aligned graph
#AlignedGraph(aligned_data,radar_data)

#Calculates and plots BackProjected Image
IntensityList = BackProjection(aligned_data,radar_data,[-5,-5],[5,5],0.5)

#IntensityList = read_intensity('../Raw_Data/intensity2.csv')
#Deconvolutes image and plots images
#deconvolute(IntensityList, IterationNumber = 3, PercentageMin = 1/5.5)

'''
#Currently unused code

#Calculates backprojected image using Ramu's algorithm
interp_approach(aligned_data,radar_data,[-3,3],[-3,3],.1)

#Reads in an intensity list and saves it as an intensity list
IntensityList = read_intensity('../Raw_Data/intensity2.csv')

'''
