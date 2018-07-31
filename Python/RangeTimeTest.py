from read_files import read_radar_data, read_motion_data
import matplotlib.pyplot as plt
import numpy as np
import math
radar_data = read_radar_data("../Raw_Data/data.pkl")
position = read_motion_data('../Raw_Data/MC-RailSAR.csv')
distance = []
total_distance = []
box_position = [[.33,.168,-.149],[2.44,.168,-2.168],[.233,.168,-2.69],[2.48,.168,.859]]
for x in range(len(box_position)):
        for i in range(len(radar_data[0])):
            distance.append(math.sqrt((position[i][0]-box_position[x][0])**2+(position[i][1]-box_position[x][1])**2+(position[i][2]-box_position[x][2])**2))
        total_distance.append(distance)
        distance = []
        plt.plot(total_distance[x],range(len(total_distance[0])))
plt.set_cmap('nipy_spectral')
plt.imshow(np.abs(radar_data[0]),extent=[radar_data[2][1],radar_data[2][-1],1,len(radar_data[0])])
plt.axis('tight')
plt.show()

