import matplotlib.pyplot as plt
import numpy as np
from numpy import real, arange, reshape
def BackProjection(aligned_data,radar_data,LeftInterval,RightInterval,StepSize):

    WrongRadarPosition = aligned_data[1] #Actual position of radar in 3D space
    PulseData = np.array(aligned_data[0]) #Data of all pulses in file
    RangeBins = np.array(radar_data[2]) #Distance in meters between the sampling rate of PulseData
    #print(RangeBins)
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
    y_length = arange(LeftInterval[1],RightInterval[1]+StepSize,StepSize)
    x_length = arange(LeftInterval[0],RightInterval[0]+StepSize,StepSize)
    x_pixel, y_pixel = np.meshgrid(x_length,y_length)
    IntensityList = np.zeros(np.shape(x_pixel))
    PulseData = PulseData[0:len(RadarPosition)-1]
    RadarPosition = np.array(RadarPosition)
    #print(RadarPosition)
    #print(PulseData)
    for i in range(len(PulseData)):
        squared = np.sqrt(np.square(x_pixel-RadarPosition[i][0])+np.square(y_pixel-RadarPosition[i][1])+np.square(RadarPosition[i][2]))
        if np.isnan(RadarPosition[i][0]):
            return "Wrong"
        IntensityList += np.interp(squared,RangeBins,PulseData[i])        
    


    #Reshapes IntensityList into proper format and plots
    ImageSizeX = len(arange(LeftInterval[0],RightInterval[0],StepSize))  #Calculates proper image size
    ImageSizeY = len(arange(LeftInterval[1],RightInterval[1],StepSize)) #Calculates proper image size

    #IntensityList = np.flip(reshape(IntensityList, (ImageSizeY,ImageSizeX)),0) #Reshapes IntensityList to the right size
    #plt.imsave('LinIntBP.png',IntensityList)
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
    #plt.colorbar()

    plt.show() #Shows the image in a new window for Mason
    np.savetxt("intensity.csv", IntensityList, delimiter=",", fmt='%s')

    return IntensityList
