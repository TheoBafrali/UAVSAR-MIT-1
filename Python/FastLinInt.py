'''
Performs backprojection using Numpy operations to generate SAR image. Plots in logarithmic and linear scale.
@author: David +  Mason
'''

#Import required modules
import matplotlib.pyplot as plt
import numpy as np
from numpy import real, arange, reshape

def FastBackProjection(aligned_data,radar_data,LeftInterval,RightInterval,StepSize):
    '''
    Inputs:
        aligned_data: Properly aligned_data
        radar_data: RADAR data
        LeftInterval: vector of bounds on x and y from the left
        RightInterval: vector of bounds on x and y from the right
        StepSize: interval which backprojection steps through
        
    Outputs:
        Plots backprojected SAR image, in linear and logarithmic scale
        IntensityList: numpy array of image data
    '''
    
    #Extracts data
    WrongRadarPosition = aligned_data[1] #Actual position of radar in 3D space
    PulseData = np.array(aligned_data[0]) #Data of all pulses in file
    RangeBins = np.array(radar_data[2]) #Distance in meters between the sampling rate of PulseData
    
    #Parameters:
    #LeftInterval = Left boundary of interval of pixels to iterate over
    #RightInterval = Right boundary of interval of pixels to iterate over
    #StepSize = Step size between left and right boundaries of interval. Must be less than RightInterval-LeftInterval
    
    #Initialize RadarPosition
    RadarPosition = []
    
    #This loop changes the (x, y, z) data to (z, x, y) data
    for i in range(len(WrongRadarPosition)):
        y = WrongRadarPosition[i][0]
        x = WrongRadarPosition[i][2]
        z = WrongRadarPosition[i][1]
        RadarPosition.append([x,y,z])
        
    #Defines distance grid
    y_length = arange(LeftInterval[1],RightInterval[1]+StepSize,StepSize)
    x_length = arange(LeftInterval[0],RightInterval[0]+StepSize,StepSize)
    x_pixel, y_pixel = np.meshgrid(x_length,y_length)
    
    #Initialize IntensityList
    IntensityList = np.zeros(np.shape(x_pixel))
    
    #Further extract data
    PulseData = PulseData[0:len(RadarPosition)-1]
    RadarPosition = np.array(RadarPosition)
    PulseData = np.array(PulseData)

    #Iterate over pulses
    for i in range(len(PulseData)):
        squared = np.sqrt(np.square(x_pixel-RadarPosition[i][0])+np.square(y_pixel-RadarPosition[i][1])+np.square(RadarPosition[i][2]))
        if np.isnan(RadarPosition[i][0]):
            return "Wrong"
        #Gives some indication the program is running
        if np.mod(i, 200) == 0:
            print("Calculating pulse "+str(i)+ " which is "+str(i/len(PulseData)*100) +"% of the data" )
        #Adds interpolated data to IntensityList
        IntensityList += np.interp(squared, RangeBins,PulseData[i,:], left = 0, right = 0) 
    
    IntensityList = np.flip(IntensityList,0) #Reshapes IntensityList to the right size
    #plt.imsave('LinIntBP.png',IntensityList)
    plt.figure(2)
    plt.subplot(122)
    plt.set_cmap('jet')
    plt.title("Linear")
    plt.imshow(abs(IntensityList), extent = (LeftInterval[0], RightInterval[0], LeftInterval[1], RightInterval[1])) #Plots the image
    plt.axis('equal')
    cbar = plt.colorbar()
    #plt.colorbar()

    logarithmic_intensity = 20*np.log10(abs(IntensityList))
    max_log_intensity = max(logarithmic_intensity.flatten())


    plt.subplot(121) 
    plt.title("Logaritmic")
    plt.imshow(logarithmic_intensity, extent = (LeftInterval[0], RightInterval[0], LeftInterval[1], RightInterval[1])) #Plots the image 
    plt.clim(max_log_intensity-20,max_log_intensity)
    plt.axis('equal')  
    plt.show() #Shows the image in a new window for Mason
    np.savetxt("intensity.csv", IntensityList, delimiter=",", fmt='%s')
    
    #Takes absolute value of IntensityList for deconvolution
    IntensityList = np.absolute(IntensityList)
    return IntensityList
