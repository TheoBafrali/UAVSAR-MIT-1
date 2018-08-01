'''
Reads in IntensityList from a .csv

@author: Mason
'''
#Import required modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_intensity(filename="../Raw_Data/intensity.csv"):
    '''
    Inputs:
        filename: path of the .csv you want to parse
    
    Outputs: 
        resized_intensities: outputs the intensity list as an array
    '''
    #Intialize things
    df = pd.read_csv(filename)
    Intensities = df.as_matrix()
    sizes = df.shape
    
    #Plot Intensity List
    plt.set_cmap('jet')
    resized_intensities = np.reshape(Intensities,(sizes[0],sizes[1]))
    plt.imshow(resized_intensities)
    plt.show()
    
    #Plot logarithmic Intensity List
    log_intensity = 20*np.log10(resized_intensities)
    max_log_intensity = max(log_intensity.flatten())
    plt.imshow(log_intensity)
    plt.clim(max_log_intensity-20,max_log_intensity)
    plt.axis('equal')
    plt.show()
    
    #Return Intensity List
    return resized_intensities
