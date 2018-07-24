#Import Packages
import matplotlib.pyplot as plt
import pickle
import numpy as np
from numpy import real, arange, reshape

#Load Data
data = pickle.load(open('mandrill_no_aliasing_data.pkl','rb'))
Platform = data[0] #Platform
PlatformX = Platform[:, 0] #X values for Platform 
Pulses = data[1] #Pulses
RangeAxis = data[2] #RangeAxis

#Define Parameters
LeftInterval = -3 #Left boundary of interval of pixels to iterate over
RightInterval = 3 #Right boundary of interval of pixels to iterate over
StepSize = 0.05 #Step size between left and right boundaries of interval. Must be less than RightInterval-LeftInterval

#Define Useful Functions
def actualRange(x, y): #calculutes the range form the position x to the vector y
    return np.sqrt((x-y[0])**2.0+(-15-y[1])**2.0+25)

def bin(x): #new bin function that returns floored bin
    bin_ = int (x/0.0185)
    return bin_
    
#Iterate over pixels
IntensityList = [] #Intializes list of intensities
for y in arange(LeftInterval,RightInterval,StepSize): #Iterates over y-coordinates
    print("Over y coordinate: " + str(y))
    for x in arange(LeftInterval,RightInterval,StepSize): #Iterates over x-coordinates
        intensityx = 0+0j #Initializes intensityz
        for i in range(len(PlatformX)): #Iterates over platform positions
            PixelCoord = [x,y]  #Defines Pixel Coordinates 
            Weight1 = (1-(actualRange(PlatformX[i], PixelCoord)%0.0185)/0.0185) #Calculates weight on the left bin
            Weight2 = (actualRange(PlatformX[i], PixelCoord)%0.0185)/0.0185 #Calculates weight on the right bin
            #Adds weighted average of pulse bins to calculate intensity 
            intensityx += Weight1*Pulses[i,  int(bin(actualRange(PlatformX[i], PixelCoord)))] + Weight2*Pulses[i,  int(bin(actualRange(PlatformX[i], PixelCoord)))+1] 
        IntensityList.append(real(np.absolute(intensityx))) #Appends the correct intensity value to the list of intensities


#Reshapes IntensityList into proper format and plots 
ImageSize = len(arange(LeftInterval,RightInterval,StepSize)) #Calculates proper image size
IntensityList = np.flip(reshape(IntensityList, (ImageSize,ImageSize)),0) #Reshapes IntensityList to the right size
plt.imsave('LinIntBP.png',IntensityList)
#plt.imshow(IntensityList, extent = (LeftInterval, RightInterval, LeftInterval, RightInterval)) #Plots the image    
#plt.show() #Shows the image in a new window for Mason

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
