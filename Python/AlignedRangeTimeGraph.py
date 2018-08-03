'''
Plots aligned graph

@author: David + Mason
'''

#Import required modules
import matplotlib.pyplot as plt
import numpy as np
import math
def AlignedGraph(aligned_data,radar_data):
    '''
    Inputs:
        aligned_data: Contains arrays of pulses and positions for each pulse
        radar_data: Contains a lot of stuff, but only the range bins are useful
    
    Outputs/Summary:
        Plots RTI graph with aligned data
    '''
    Pulses = aligned_data[0]
    Range_Bins = radar_data[2]
    RangeBinDistance = Range_Bins[2]-Range_Bins[1]
    RangeBinX = []
    position = aligned_data[1]
    plt.figure(1)
    #Positions for each point
    box_position = [[.746,.1,-1.95548],[.942713,.1,1.019],[2.48,.1,-.238],[2.648,.1,2.227]]
    for i in np.arange(0,len(Range_Bins),50):
        RangeBinX.append(round(i*RangeBinDistance+Range_Bins[0],2))
    distance = []
    total_distance = []
    Pulses = Pulses[:len(position)]
    for x in range(len(box_position)):
        for i in range(len(Pulses)):
            distance.append(math.sqrt((position[i][0]-box_position[x][0])**2+(position[i][1]-box_position[x][1])**2+(position[i][2]-box_position[x][2])**2))    
        total_distance.append(distance)
        distance = []
        plt.plot(total_distance[x],range(len(total_distance[0])))

    print(distance)
    plt.set_cmap('nipy_spectral')
    #plt.xticks(np.arange(0,len(Range_Bins),50),RangeBinX)
    #plt.yticks(np.arange(0,len(Pulses),1000),np.flip(np.arange(0,len(Pulses),1000),0))
    plt.title('Aligned Range-Time Intensity')
    plt.xlabel("Distance (m)")
    plt.ylabel("Pulse Number")
    #plt.imshow(np.flip(np.abs(Pulses),0),extent=[Range_Bins[1],Range_Bins[len(Range_Bins)-1],1,len(Pulses)])
    plt.imshow(np.flip(np.abs(Pulses[:,0:580]),0),extent=[Range_Bins[0],Range_Bins[-1],1,len(Pulses)])
    plt.axis('tight')
    plt.show()
