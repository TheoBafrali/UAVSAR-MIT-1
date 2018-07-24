from numpy import genfromtxt,average, array, real, arange, reshape
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import scatter, xlabel, ylabel, xlim, ylim, show, plot
import pickle
import numpy as np
import math

data = pickle.load(open('mandrill_no_aliasing_data.pkl','rb'))
Platform = data[0] #Platform
PlatformX = Platform[:, 0]
Pulses = data[1] #Pulses
RangeAxis = data[2] #RangeAxis
PulsesAbs = np.absolute(Pulses)
PulsesReal = real(Pulses)

#for i in PulsesAbs:
#   scatter(RangeAxis,i)
#   xlim(25,40)
#show()

def actualRange(x, y):
    return np.sqrt((x-y[0])**2.0+(-15-y[1])**2.0+25)

def bin(x):
    bin_ = int (x/0.0185)
    return bin_
    #print(x % 0.0185)
    #if x % 0.0185 >= 0.00925:
    #    realbin = bin_ + 1
    #else: 
    #    realbin = bin_
    #return realbin

IMAGE_SIZE = (len(arange(-4,4,0.01)),len(arange(-4,4,0.01)))

intensityx = 0+0j
otherrange = np.zeros(len(PlatformX))
xlist = []
ylist = []
intensitylist = []
fig = plt.figure()
resolution = 0
for y in arange(-4,4,0.01):
    for x in arange(-4,4,0.01):
        intensityx = 0+0j 
        for i in range(len(PlatformX)):
            PixelCoord = [x,y]   
            #rangebins[i] = int(bin(actualRange(PlatformX[i], PixelCoord)))
            otherrange[i] = np.argmin(np.abs(2*actualRange(PlatformX[i], PixelCoord)-RangeAxis))
            #intensityx += float(np.absolute(Pulses[i, int(otherrange[i])]) )
            #intensityx += float(np.absolute(Pulses[i,  int(bin(actualRange(PlatformX[i], PixelCoord)))]) )
            Weight1 = (1-(actualRange(PlatformX[i], PixelCoord)%0.0185)/0.0185)
            Weight2 = (actualRange(PlatformX[i], PixelCoord)%0.0185)/0.0185
            #intensityx += Pulses[i,  int(bin(actualRange(PlatformX[i], PixelCoord)))] 
            intensityx += Weight1*Pulses[i,  int(bin(actualRange(PlatformX[i], PixelCoord)))] + Weight2*Pulses[i,  int(bin(actualRange(PlatformX[i], PixelCoord)))+1]
        intensitylist.append(real(np.absolute(intensityx)))
        xlist.append(x)
        ylist.append(y)
#        print(real(intensityx))
#        print(x)
#        print(y)

#print(len(intensitylist))
intensitylist = np.flip(reshape(intensitylist, IMAGE_SIZE),0)
plt.imshow(intensitylist, extent = (-4, 4, -4, 4))           
plt.show()
