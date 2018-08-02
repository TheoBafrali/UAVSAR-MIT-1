'''
Runs the entire workflow, taking motion capture data (a .csv) and radar data (a binary file), 
aligns data, calculates backprojected image, deconvolutes image, and plots.  

@author: David 
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
from rcs import rcs
import numpy as np
import matplotlib.pyplot as plt

#Converts motion and RADAR data to the right data structures
#unpack("../Raw_data/RailSAR-record1") #Currently commented out because unused
motion_data = read_motion_data("../Raw_Data/UAVSAR4Flight1.csv","UASSAR4")
radar_data = read_radar_data("../Raw_Data/UAVSAR4Flight1.pkl")

#Does RCS correction
new_radar_data = rcs(radar_data)

#Plots RTI graph
plt.figure(0)
plt.set_cmap('jet')
rti_ax = plt.imshow(20 * np.log10(np.abs(new_radar_data[0])))
rti_ax.axes.set_aspect('auto')
plt.title('Range-Time Intensity')
plt.xlabel('Range Bins')
plt.ylabel('Pulse Index')
cbar = plt.colorbar()
cbar.ax.set_ylabel('dB')
plt.show()

'''
#Calculates the right frames to perform alignment on
#Currently using manual alignment,  instead of these functions
motion_start = find_i_of_first_motion(motion_data)
print(motion_start)
motion_end = find_i_of_last_motion(motion_data)
print(motion_end)
radar_start = find_point_one_radar(radar_data)
print(radar_start)
'''

radar_start = 1
motion_start = 1
motion_end = 1

#Aligns data, currently using frames given in function definition
# motion_point_one = 5100, motion_point_last = 29545,  radar_point_one = 1110
aligned_data = align_data(new_radar_data,motion_data,radar_start,motion_start, motion_end)

#Plots aligned graph
AlignedGraph(aligned_data,new_radar_data)

#Calculates and plots BackProjected Image
IntensityList = BackProjection(aligned_data,radar_data,[-5,-5],[5,5],0.25)

#Deconvolutes image and plots images
deconvolute(IntensityList, IterationNumber = 3, PercentageMin = 1/5.5)


#Currently unused code
'''
#Calculates backprojected image using Ramu's algorithm
interp_approach(aligned_data,radar_data,[-3,3],[-3,3],.1)

#Reads in an intensity list and saves it as an intensity list
IntensityList = read_intensity('../Raw_Data/intensity2.csv')

'''
