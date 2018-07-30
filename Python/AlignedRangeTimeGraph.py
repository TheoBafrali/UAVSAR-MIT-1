import matplotlib.pyplot as plt
import numpy as np
from Unpack import unpack
from read_files import read_radar_data, read_motion_data
from motion_capture import motion_point_one
from radar_movement import radar_point_one
from data_align import align_data
from LinInt import BackProjection
from backprojection import interp_approach, main
import math
unpack("../Raw_data/RailSAR-record1")
motion_data = read_motion_data("../Raw_Data/MC-RailSAR.csv")

radar_data = read_radar_data()

motion_start = motion_point_one(motion_data)

radar_start = radar_point_one(radar_data)

aligned_data = align_data(radar_data,motion_data,radar_start,motion_start)
distance = []
new_motion_data = aligned_data[1]
Front_Triangle = [.33,.168,-.14959]
for i in range(len(new_motion_data)):
    distance.append(math.sqrt((new_motion_data[i][0]-Front_Triangle[0])**2+(new_motion_data[i][1]-Front_Triangle[1])**2+(new_motion_data[i][2]-Front_Triangle[2])**2))
plt.plot(distance,len(distance))
Pulses = np.flip(aligned_data[0],0)
Range_Bins = radar_data[2]
RangeBinDistance = Range_Bins[2]-Range_Bins[1]
RangeBinX = []
for i in np.arange(0,len(Range_Bins),50):
    RangeBinX.append(round(i*RangeBinDistance+Range_Bins[0],2))
plt.set_cmap('nipy_spectral')
plt.xticks(np.arange(0,len(Range_Bins),50),RangeBinX)
#plt.yticks(np.arange(0,len(Pulses),1000),np.flip(np.arange(0,len(Pulses),1000),0))
plt.xlabel("Distance (m)")
plt.ylabel("Pulse Number")
plt.imshow(np.abs(Pulses))
plt.axis('tight')
plt.show()
