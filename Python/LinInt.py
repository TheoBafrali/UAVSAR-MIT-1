'''
Performs backprojection to generate SAR image. Plots in logarithmic and linear scale.

@author: David +  Mason
'''

#Import required modules
import matplotlib.pyplot as plt
import numpy as np
from numpy import real, arange, reshape

def BackProjection(aligned_data,radar_data,LeftInterval,RightInterval,StepSize):
    '''
    Inputs:
        aligned_data: Properly aligned_data
        radar_data: RADAR data
        LeftInterval: vector of bounds on x and y from the left
        RightInterval: vector of bounds on x and y from the right
        StepSize: interval which backprojection steps through
    '''
    
    #Extracts data
    WrongRadarPosition = aligned_data[1] #Actual position of radar in 3D space
    PulseData = aligned_data[0] #Data of all pulses in file
    RangeBins = radar_data[2] #Distance in meters between the sampling rate of PulseData
   
    #LeftInterval = Left boundary of interval of pixels to iterate over
    #RightInterval = Right boundary of interval of pixels to iterate over
    #StepSize = Step size between left and right boundaries of interval. Must be less than RightInterval-LeftInterval
    bin_constant = float(RangeBins[1])-float(RangeBins[0])
    RadarPosition = []
    
    #This loop changes the xyz data (x is actually z) to z x y data
    for i in range(len(WrongRadarPosition)):
        y = WrongRadarPosition[i][0]
        x = WrongRadarPosition[i][2]
        z = WrongRadarPosition[i][1]
        RadarPosition.append([x,y,z])

    '''Define Useful Functions'''
    def actualRange(Position, PixelPosition): #calculutes the range form the position x to the vector y
        return np.sqrt((Position[0]-PixelPosition[0])**2.0+(Position[1]-PixelPosition[1])**2.0+(Position[2])**2)
    def bin(x): #new bin function that returns floored bin
        return int((x-RangeBins[0])/bin_constant)
        #return np.argmin(np.abs(x - RangeBins))
    
    #Iterate over pixels
    graphingx = []
    graphingy = []
    graphingz = []
    IntensityList = [] #Intializes list of intensities
    
    #Iterates over pixels
    for y in arange(LeftInterval[1], RightInterval[1]+StepSize, StepSize):
        print("Computing  y coordinate: " + str(y))
        for x in arange(LeftInterval[0], RightInterval[0]+StepSize, StepSize):
            intensityx = 0+0j #Initializes intensities
            for i in range(len(RadarPosition)): #Iterates over platform positions
                PixelCoord = [x,y]  #Defines Pixel Coordinates
                if actualRange(RadarPosition[i],PixelCoord) > RangeBins[0] and actualRange(RadarPosition[i],PixelCoord) < RangeBins[-1] :
                    
                    Weight1 = (1-(actualRange(RadarPosition[i], PixelCoord)%bin_constant)/bin_constant) #Calculates weight on the left bin
                    Weight2 = (actualRange(RadarPosition[i], PixelCoord)%bin_constant)/bin_constant #Calculates weight on the right bin
                #Adds weighted average of pulse bins to calculate intensity
                    intensityx += Weight1*PulseData[i,int(bin(actualRange(RadarPosition[i], PixelCoord)))] + Weight2*PulseData[i,  int(bin(actualRange(RadarPosition[i], PixelCoord)))+1]
                    #intensityx += PulseData[i,  int(bin(actualRange(RadarPosition[i], PixelCoord)))]
            IntensityList.append(real(np.absolute(intensityx))) #Appends the correct intensity value to the list of intensities

    #Reshapes IntensityList into proper format and plots
    ImageSizeX = len(arange(LeftInterval[0],RightInterval[0]+StepSize, StepSize))  #Calculates proper image size
    ImageSizeY = len(arange(LeftInterval[1],RightInterval[1]+StepSize, StepSize)) #Calculates proper image size

    IntensityList = np.flip(reshape(IntensityList, (ImageSizeY,ImageSizeX)),0) #Reshapes IntensityList to the right size
    #plt.imsave('LinIntBP.png',IntensityList)
    plt.figure(2)
    plt.set_cmap('jet')
    logarithmic_intensity = 20*np.log10(IntensityList)
    max_log_intensity = max(logarithmic_intensity.flatten())

    plt.subplot(121) 
    plt.title("Logaritmic")
    plt.imshow(logarithmic_intensity, extent = (LeftInterval[0], RightInterval[0], LeftInterval[1], RightInterval[1])) #Plots the image 
    plt.clim(max_log_intensity-20,max_log_intensity)
    #plt.axis('equal')
    
    plt.subplot(122)
    plt.set_cmap('jet')
    plt.title("Linear")
    plt.imshow(IntensityList, extent = (LeftInterval[0], RightInterval[0], LeftInterval[1], RightInterval[1])) #Plots the image
    #plt.axis('equal')
    #plt.colorbar()

    plt.show() #Shows the image in a new window for Mason
    np.savetxt("intensity.csv", IntensityList, delimiter=",", fmt='%s')
    return IntensityList
    
'''
#Old Code!

#This code plots the scatter plot for the absolute values over pulses.
PulsesAbs = np.absolute(Pulses)
for i in PulsesAbs:
  scatter(RangeAxis,i)
  xlim(25,40)

#Old bin function that returns nearest bin
def bin(x):
    bin_ = int (x/0.0185)
    if x % 0.0185 >= 0.00925:
        realbin = bin_ + 1
    else:
        realbin = bin_
    return realbin

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
