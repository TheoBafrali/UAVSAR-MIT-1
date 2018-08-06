from numpy import genfromtxt,average, array, real, arange, reshape
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import scatter, xlabel, ylabel, xlim, ylim, show, plot
import pickle
import numpy as np
import math

data = pickle.load(open('5Points_data.pkl','rb'))
Platform = data[0] #Platform
PlatformX = Platform[:, 0]
Pulses = data[1] #Pulses
RangeAxis = data[2] #RangeAxis
PulsesAbs = np.absolute(Pulses)
PulsesReal = real(Pulses)
def actualRange(x, y):
   return math.sqrt((x-y[0])**2.0+(-15-y[1])**2.0+25)

def bin(x):
    bin = int (x/0.0185)
    if x % 0.0185 >= 0.00925:
        realbin = bin + 1
    else: 
        realbin = bin
    return realbin

intensityx = 0+0j
rangebins = np.zeros(len(PlatformX))
xlist = []
ylist = []
intensitylist = []
fig = plt.figure()
resolution = 0
for x in arange(-3,3,.1):
    for y in arange(-3,3,.1):
        intensityx = 0+0j 
        for i in range(len(PlatformX)):
            PixelCoord = [x,y]   
            rangebins[i] = int(bin(actualRange(PlatformX[i], PixelCoord)))
            intensityx += float(np.absolute(Pulses[i, int(bin(actualRange(PlatformX[i], PixelCoord)))]) )
        intensitylist.append(real(intensityx))
        xlist.append(x)
        ylist.append(y)
        print(real(intensityx))
        print(x)
        print(y)

print(len(intensitylist))
intensitylist = reshape(intensitylist, (60,60))
plt.imshow(intensitylist)           
plt.show()
