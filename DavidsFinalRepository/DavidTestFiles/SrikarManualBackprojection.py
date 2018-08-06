# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 11:00:15 2018

@author: dbli2
"""

import csv
import pandas as pd
import numpy as np
from numpy import real, arange, reshape
import matplotlib.pyplot as plt


#Parses Position  Data
parsedData = pd.read_csv('SrikarPositionModified.csv',low_memory=False, delimiter=',', header=0, encoding='ascii')
X = parsedData['X']
Y = parsedData['Y']
Z = parsedData['Z']
motion_data = []
for i in range(len(X)):
    temp_list = []
    temp_list.append(X[i])
    temp_list.append(Y[i])
    temp_list.append(Z[i])
    motion_data.append(temp_list)
    
#Parses Pulses Data
Pulses = []
with open('SrikarPulseDataModified.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        Pulses.append(np.array(row))

        
#Parses Range Axis Data
RangeAxis = []
with open('SrikarRangeAxisModified.csv','r') as csvfile:
    reader = csv.reader(csvfile,delimiter= ' ', quotechar = '|')
    for row in reader:
        RangeAxis.append(float(row[0]))
   
#Defined formatting to simulate aligned data
formatting = [Pulses,motion_data]

#Setting inputs to the function
aligned_data = formatting
radar_data = RangeAxis
LeftInterval = -5
RightInterval = 5
StepSize = 0.1

#Computing function stuff
WrongRadarPosition = aligned_data[1] #Actual position of radar in 3D space
PulseData = aligned_data[0] #Data of all pulses in file
RangeBins = radar_data #Distance in meters between the sampling rate of PulseData
#LeftInterval = Left boundary of interval of pixels to iterate over
#RightInterval = Right boundary of interval of pixels to iterate over
#StepSize = Step size between left and right boundaries of interval. Must be less than RightInterval-LeftInterval
bin_constant = float(RangeBins[1])-float(RangeBins[0])
RadarPosition = []
#This loop changes the xyz data (x is actually z) to z x y data
for i in range(len(WrongRadarPosition)):
    x = WrongRadarPosition[i][2]
    y = WrongRadarPosition[i][0]
    z = WrongRadarPosition[i][1]
    RadarPosition.append([x,y,z])

    #Define Useful Functions
def actualRange(Position, PixelPosition): #calculutes the range form the position x to the vector y
    return np.sqrt((Position[0]-PixelPosition[0])**2.0+(Position[1]-PixelPosition[1])**2.0+(Position[2])**2)
def bin(x): #new bin function that returns floored bin
    return int((float(x)-float(RangeBins[0]))/bin_constant)
    #return np.argmin(np.abs([float(y) - float(x) for y in RangeBins]))

#print(PulseData[1])
#print(float(PulseData[1][int(bin(actualRange(RadarPosition[1], [-4.0, -4.0])))]))
#print(RangeBins[0])
#print(RangeBins[(np.argmax(RangeBins))])

#Iterate over pixels
IntensityList = [] #Intializes list of intensities
for y in arange(LeftInterval, RightInterval, StepSize):
    print("Computing  y coordinate: " + str(y))
    for x in arange(LeftInterval, RightInterval, StepSize):
        intensityx = 0 #Initializes intensityz
        for i in range(len(RadarPosition)): #Iterates over platform positions
            PixelCoord = [x,y]  #Defines Pixel Coordinates
          #  print(actualRange(RadarPosition[i],PixelCoord))
            if float(actualRange(RadarPosition[i],PixelCoord)) > float(RangeBins[0]) and float(actualRange(RadarPosition[i],PixelCoord)) < float(RangeBins[np.argmax(RangeBins)]) :
                Weight1 = (1-(actualRange(RadarPosition[i], PixelCoord)%bin_constant)/bin_constant) #Calculates weight on the left bin
                Weight2 = (actualRange(RadarPosition[i], PixelCoord)%bin_constant)/bin_constant #Calculates weight on the right bin
                #Adds weighted average of pulse bins to calculate intensity
                intensityx += Weight1*float(PulseData[i][int(bin(actualRange(RadarPosition[i], PixelCoord)))]) + Weight2*float(PulseData[i][int(bin(actualRange(RadarPosition[i], PixelCoord)))+1])
                #print(float(PulseData[i][int(bin(actualRange(RadarPosition[i],PixelCoord)))]))
                #intensityx += float(PulseData[i][int(bin(actualRange(RadarPosition[i], PixelCoord)))])
        IntensityList.append(real(np.absolute(intensityx))) #Appends the correct intensity value to the list of intensities

#Reshapes IntensityList into proper format and plots
ImageSize = len(arange(LeftInterval,RightInterval,StepSize)) #Calculates proper image size
IntensityList = np.flip(reshape(IntensityList, (ImageSize,ImageSize)),0) #Reshapes IntensityList to the right size
#plt.imsave('LinIntBP.png',IntensityList)
plt.imshow(IntensityList, extent = (LeftInterval, RightInterval, LeftInterval, RightInterval)) #Plots the image
plt.show() #Shows the image in a new window for Mason
   # return IntensityList

