from numpy import genfromtxt,average, array, real, arange, reshape
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import scatter, xlabel, ylabel, xlim, ylim, show, plot
import pickle
import numpy as np
import math

data = pickle.load(open('2Points_data.pkl','rb'))
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
    bin = int (x/0.0185)
    if x % 0.0185 >= 0.00925:
        realbin = bin + 1
    else: 
        realbin = bin
    return realbin

intensityx = 0+0j
rangebins = np.zeros(len(PlatformX))
fig = plt.figure()

intensityx = 0+0j 
for i in range(len(PlatformX)):
    PixelCoord = [0,2]   
    rangebins[i] = int(bin(actualRange(PlatformX[i], PixelCoord)))
    intensityx += float(np.absolute(Pulses[i, int(bin(actualRange(PlatformX[i], PixelCoord)))]) )

#        print(real(intensityx))
#        print(x)
#        print(y)

def addingZeros(x, y):
    sumList = []
    for i in range(0, int(y)):
        sumList.append(0)
    for i in range(0,1084):
        sumList.append(x[i])
    for i in range(0,1084-y):
        sumList.append(0)
    return sumList

totalsum = np.zeros(2168)

for i in range(len(PlatformX)):
    appended = addingZeros(np.absolute(Pulses[i,:]), int(rangebins[i]-rangebins[50]))
    totalsum += appended 
    
plt.plot(range(len(totalsum)), totalsum)
show()
#print(len(intensitylist))
#ntensitylist = reshape(intensitylist, (600,600))
#plt.imshow(intensitylist)           
#plt.show()
