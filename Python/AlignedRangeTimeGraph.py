import matplotlib.pyplot as plt
import numpy as np
import math
'''
unpack("../Raw_data/RailSAR-record1")
motion_data = read_motion_data("../Raw_Data/MC-RailSAR.csv")

radar_data = read_radar_data()

motion_start = motion_point_one(motion_data)

radar_start = radar_point_one(radar_data)

aligned_data = align_data(radar_data,motion_data,radar_start,motion_start)
'''
def AlignedGraph(aligned_data,radar_data):
    
    Pulses = aligned_data[0]
    Range_Bins = radar_data[2]
    RangeBinDistance = Range_Bins[2]-Range_Bins[1]
    RangeBinX = []
    position = aligned_data[1]
    box_position = [[.33,.168,-.149],[2.44,.168,-2.168],[.233,.168,-2.69],[2.48,.168,.859]]
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
        #plt.plot(total_distance[x],range(len(total_distance[0])))

    print(distance)
    plt.set_cmap('nipy_spectral')
    #plt.xticks(np.arange(0,len(Range_Bins),50),RangeBinX)
#plt.yticks(np.arange(0,len(Pulses),1000),np.flip(np.arange(0,len(Pulses),1000),0))
    plt.xlabel("Distance (m)")
    plt.ylabel("Pulse Number")
    plt.imshow(np.abs(Pulses),extent=[Range_Bins[1],Range_Bins[len(Range_Bins)-1],1,len(Pulses)])
    plt.axis('tight')
    plt.show()
