'''
Runs the entire workflow, taking motion capture data (a .csv) and radar data (a binary file), 
aligns data, calculates backprojected image, deconvolutes image, and plots.  

@author: Mason + David 
'''
#Import required modules
from pulson440_unpack import unpack 
from read_files import read_radar_data, read_motion_data
from rcs import rcs
from interp_data_align import interp_align_data
from data_align import align_data
from GeneralAlignedRangeTimeGraph import AlignedGraph 
from FastLinInt import FastBackProjection
from LinInt import BackProjection
from Deconvolution import deconvolute
from plotRTI import plotRTI
from helper_functions import linear_interp_nan

#Converts motion and RADAR data to the right data structures
unpack("../Raw_Data/uavsar1flight1")

#Loads data from the RADAR
motion_data = read_motion_data("../Raw_Data/UAVSAR1Flight1.csv","UAVSAR1")
motion_data = linear_interp_nan(motion_data[1],motion_data[0])
radar_data = read_radar_data("data.pkl", 580, 0.30) #580, 0.30 is probably good

#Performs RCS correction
radar_data = rcs(radar_data)

#Plot RTI for radar_data
plotRTI(radar_data)

#Set parameters
#Take motion_start and  motion_end from .tak file video
#Estimate radar_start from the plotRTI above, initially comment out code below
radar_start = 500 #Initiall600
motion_start = 6000 #6600
motion_end = 30000 #29545

#Aligns data
aligned_data = interp_align_data(radar_data,motion_data,radar_start,motion_start, motion_end, 100, 3500) #100, 3500

#Plots aligned graph with known data point
AlignedGraph(aligned_data,radar_data, [[.942713,.1,1.019]])

#Calculates and plots BackProjected Image
#IntensityList = BackProjection(aligned_data,radar_data,[-4,0],[4,4],0.1)
IntensityList2 = FastBackProjection(aligned_data, radar_data, [-4,0],[4,4], 0.005)

#Deconvolutes image and plots images
Image = deconvolute(IntensityList2, IterationNumber = 2, PercentageMin = 1/15)
