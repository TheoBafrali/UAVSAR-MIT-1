'''
Debug file that plots RTI  graph with RADAR data pre-alignment

@author: Mason
'''
#Import required modules
import matplotlib.pyplot as plt
import numpy as np
import math
from read_files import read_radar_data, read_motion_data

#Loads data
data = read_radar_data('../Raw_Data/railTestDiagonal.pkl')
Pulses = data[0]
Range_Bins = data[2]
RangeBinDistance = Range_Bins[2]-Range_Bins[1]
position = read_motion_data('../Raw_Data/MC-RailSAR.csv')

def rti_graph(radar_data,motion_data,pulse_start,motion_start,motion_end,pulse_end):
    
    Pulses = radar_data[0]
    Range_Bins = radar_data[2]
    RangeBinDistance = Range_Bins[2]-Range_Bins[1]
    position = motion_data
    #Define box positions and calculate expected distances
    distance = []
    total_distance = []
    box_position = [[.33,.168,-.149],[2.44,.168,-2.168],[.233,.168,-2.69],[2.48,.168,.859]]
    for x in range(len(box_position)):
        for i in range(len(Pulses)):
            distance.append(math.sqrt((position[i][0]-box_position[x][0])**2+(position[i][1]-box_position[x][1])**2+(position[i][2]-box_position[x][2])**2))
        total_distance.append(distance)
        distance = []
        plt.plot(total_distance[x],range(len(total_distance[0])))

    RangeBinX = []
    for i in np.arange(0,len(Range_Bins),50):
        RangeBinX.append(round(i*RangeBinDistance+Range_Bins[0],2))


    #Plots the data as well as the expected data
    plt.set_cmap('jet')
    #plt.yticks(np.arange(0,len(Pulses),1000),np.flip(np.arange(0,len(Pulses),1000),0))
    print(pulse_start)
    plt.plot([Range_Bins[1],Range_Bins[-1]], [pulse_start,pulse_start],c='g')
    plt.plot([Range_Bins[1],Range_Bins[-1]], [pulse_end,pulse_end],c='g')
    plt.xlabel("Distance (m)")
    plt.ylabel("Pulse Number")
    plt.imshow(np.flip(np.abs(Pulses),0),np.arange(0,len(Pulses),1/radar_data[1],np.extent=[Range_Bins[1],Range_Bins[len(Range_Bins)-1],1,len(Pulses)])
    plt.axis('tight')
    plt.show()

