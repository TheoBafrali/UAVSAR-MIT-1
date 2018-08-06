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
unpack("../Raw_Data/uavsar1flight4")

#Loads data from the RADAR
motion_data = read_motion_data("../Raw_Data/UAVSAR1Flight4.csv","UAVSAR1")
motion_data = linear_interp_nan(motion_data[1],motion_data[0])
radar_data = read_radar_data("data.pkl", 580, 0.25) #580, 0.25 is probably good

#Performs RCS correction
radar_data = rcs(radar_data)

#Plot RTI for radar_data
plotRTI(radar_data)

#Set parameters
#Take motion_start and  motion_end from .tak file video
#Estimate radar_start from the plotRTI above, initially comment out code below
radar_start = 510 #Flight4: 510, FLight3: 135, Flight2: 113
motion_start = 3450 #Flight2: 3300, Flight3: 2400, FLight4: 3450, Flight5: 4477
motion_end = 14462 #Flight2: 24000, Flight3: 15382, Flight4: 14462, Flight5: 14201

#Aligns data
aligned_data = align_data(radar_data,motion_data,radar_start,motion_start, motion_end, 100, 1200) #100, 3500

#Plots aligned graph with known data point
AlignedGraph(aligned_data,radar_data, [[2.920519426,	0.089892255,	-1.116615139]]) # (2.920519426,	0.089892255,	-1.116615139)


#Calculates and plots BackProjected Image
IntensityList = FastBackProjection(aligned_data,radar_data,[-3,1.5],[0,4],0.02)

#Deconvolutes image and plots images
Image = deconvolute(IntensityList, [-3,1.5],[0,4], IterationNumber = 2, PercentageMin = 1/5, )

'''
plt.figure(5)
plt.imshow(Image)
cbar = plt.colorbar()
plt.show()
'''
