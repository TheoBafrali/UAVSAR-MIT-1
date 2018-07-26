import matplotlib.pyplot as plt
import numpy as np
from numpy import real, arange, reshape
from read_files import read_radar_data,read_motion_data
def BackPropogate(radar_data,RadarPosition,LeftInterval,RightInterval,StepSize):

    #RadarPosition = Actual position of radar in 3D space
    PulseData = radar_data[0] #Data of all pulses in file
    TimeStamp = radar_data[1] #Time of each pulse
    RangeBins = radar_data[2] #Distance in meters between the sampling rate of PulseData
    #LeftInterval = Left boundary of interval of pixels to iterate over
    #RightInterval = Right boundary of interval of pixels to iterate over
    #StepSize = Step size between left and right boundaries of interval. Must be less than RightInterval-LeftInterval

    bin_constant = float(float(RangeBins[1])/2.0)

    '''Define Useful Functions'''
    def actualRange(Position, PixelPosition): #calculutes the range form the position x to the vector y
        return np.sqrt((Position[0]-PixelPosition[0])**2.0+(Position[1]-y[1])**2.0+(Position[2])**2)

    def bin(x): #new bin function that returns floored bin
        bin_ = int (x/bin_constant)
        return bin_

    #Iterate over pixels
    IntensityList = [] #Intializes list of intensities
    for y in arange(LeftInterval, RightInterval, StepSize):
        print("Computing  y coordinate: " + str(y))
        for x in arange(LeftInterval, RightInterval, StepSize):
            intensityx = 0+0j #Initializes intensityz
            for i in range(len(RadarPosition)): #Iterates over platform positions
                PixelCoord = [x,y]  #Defines Pixel Coordinates
                Weight1 = (1-(actualRange(RadarPosition[i], PixelCoord)%bin_constant)/bin_constant) #Calculates weight on the left bin
                Weight2 = (actualRange(RadarPosition[i], PixelCoord)%bin_constant)/bin_constant #Calculates weight on the right bin
                #Adds weighted average of pulse bins to calculate intensity
                intensityx += Weight1*PulseData[i,  int(bin(actualRange(RadarPosition[i], PixelCoord)))] + Weight2*PulseData[i,  int(bin(actualRange(RadarPosition[i], PixelCoord)))+1]
            IntensityList.append(real(np.absolute(intensityx))) #Appends the correct intensity value to the list of intensities


#Reshapes IntensityList into proper format and plots
    ImageSize = len(arange(LeftInterval,RightInterval,StepSize)) #Calculates proper image size
    IntensityList = np.flip(reshape(IntensityList, (ImageSize,ImageSize)),0) #Reshapes IntensityList to the right size
    plt.imsave('LinIntBP.png',IntensityList)
    #plt.imshow(IntensityList, extent = (LeftInterval, RightInterval, LeftInterval, RightInterval)) #Plots the image
    #plt.show() #Shows the image in a new window for Mason
    return IntensityList

BackPropogate(read_radar_data(),read_motion_data("MC-RailSAR.csv"),3,3,.1)
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
