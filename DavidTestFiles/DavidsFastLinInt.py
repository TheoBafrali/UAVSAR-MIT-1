import matplotlib.pyplot as plt
import numpy as np
from numpy import real, arange, reshape

def FastBackProjection(aligned_data,radar_data,LeftInterval,RightInterval,StepSize):

RadarPosition = []
    
WrongRadarPosition = aligned_data[1] #Actual position of radar in 3D space
PulseData = aligned_data[0] #Data of all pulses in file
RangeBins = radar_data[2] #Distance in meters between the sampling rate of PulseData

#This loop changes the xyz data (x is actually z) to z x y data
for i in range(len(WrongRadarPosition)):
    y = WrongRadarPosition[i][0]
    x = WrongRadarPosition[i][2]
    z = WrongRadarPosition[i][1]
    RadarPosition.append([x,y,z])


#Initialize variable grids
y_intervals = np.arange(LeftInterval[1], RightInterval[1], StepSize)
x_intervals = np.arange(LeftInterval[0], RightInterval[0], StepSize)
x_grid, y_grid = np.meshgrid(x_intervals,y_intervals)  
    
IntensityList = np.zeros((32,32))

for i in range(0, len(PulseData[:,0])):
    # Calculate the range between position and image points
    range_grid = np.sqrt((x_grid - RadarPosition[i][0])**2 + (y_grid - RadarPosition[i][1])**2 +RadarPosition[i][2]**2)
    
    Fun = np.interp(range_grid, RangeBins, PulseData[i, :])
    
    # Do linear interpolation
    IntensityList = IntensityList + np.array(Fun)
    
plt.set_cmap('jet')
logarithmic_intensity = 20*np.log10(IntensityList)
max_log_intensity = max(logarithmic_intensity.flatten())

plt.figure(1)
plt.subplot(121) 
plt.title("Logaritmic")
plt.imshow(logarithmic_intensity, extent = (LeftInterval[0], RightInterval[0], LeftInterval[1], RightInterval[1])) #Plots the image 
plt.clim(max_log_intensity-20,max_log_intensity)
plt.axis('equal')
    

plt.subplot(122)
plt.set_cmap('jet')
plt.title("Linear")
plt.imshow(IntensityList, extent = (LeftInterval[0], RightInterval[0], LeftInterval[1], RightInterval[1])) #Plots the image
plt.axis('equal')


#Initializes otherrange and calculates range using argmin
otherrange = np.zeros(len(PlatformX))
otherrange[i] = np.argmin(np.abs(2*actualRange(PlatformX[i], PixelCoord)-RangeAxis))

#Initializes rangebins and calculates range using modular arithmetic
rangebins = np.zeros(len(PlatformX))
rangebins[i] = int(bin(actualRange(PlatformX[i], PixelCoord)))

#Defines xlist and ylist and stores coordinates
xlist = [] #Array of x-coordinates
ylist = [] #Array of y-coordinates
xlist.append(x) #Appends the iterated x value to the xlist
ylist.append(y) #Appends the iterated y value to the ylist
'''
