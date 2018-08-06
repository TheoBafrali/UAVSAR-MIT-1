'''
Runs the entire workflow, taking motion capture data (a .csv) and radar data (a binary file), 
aligns data, calculates backprojected image, deconvolutes image, and plots.  

@author: Mason + David 
'''
#Import required modules
from pulson440_unpack import unpack 
from read_files import read_radar_data, read_motion_data
from rcs import rcs
from data_align import align_data
from GeneralAlignedRangeTimeGraph import AlignedGraph 
from LinInt import BackProjection
from Deconvolution import deconvolute
from plotRTI import plotRTI
from FastLinInt import FastBackProjection
from helper_functions import linear_interp_nan
import matplotlib.pyplot as plt

#Converts motion and RADAR data to the right data structures
unpack("../Raw_Data/uavsar3flight5")

#Loads data from the RADAR
motion_data = read_motion_data("../Raw_Data/UAVSAR3Flight5.csv","UAVSAR3")
motion_data = linear_interp_nan(motion_data[1],motion_data[0])
radar_data = read_radar_data("data.pkl", 580, 2) #580, 0.25 is probably good

#Performs RCS correction
radar_data = rcs(radar_data)

#Plot RTI for radar_data
plotRTI(radar_data)

#Set parameters
#Take motion_start and  motion_end from .tak file video
#Estimate radar_start from the plotRTI above, initially comment out code below
radar_start = 1 #Flight4: 510, FLight3: 135, Flight2: 113
motion_start = 3100 #Flight2: 3300, Flight3: 2400, FLight4: 3450, Flight5: 4477, 4803
motion_end = motion_start + 3400#Flight2: 24000, Flight3: 15382, Flight4: 14462, Flight5: 14201, 12670

#Aligns data
aligned_data = align_data(radar_data,motion_data,radar_start,motion_start, motion_end, 0, 1300) #100, 3500

#Plots aligned graph with known data point
AlignedGraph(aligned_data,radar_data, [[.746,.1,-1.95548],[.942713,.1,1.019],[2.48,.1,-.238],[2.648,.1,2.227]]) # (-2.751455492	, 1.076340894, 0.533231786)
'''
#Calculates and plots BackProjected Image
IntensityList = FastBackProjection(aligned_data,radar_data,[-3,1.5],[0,4],0.0002)

#Deconvolutes image and plots images
Image = deconvolute(IntensityList, IterationNumber = 2, PercentageMin = 1/5)


plt.figure(5)
plt.imshow(Image)
cbar = plt.colorbar()
plt.show()
'''
