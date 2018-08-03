# -*- coding: utf-8 -*-
"""
Plots the RTI graphs for some RADAR data

@author: David
"""

import numpy as np
import matplotlib.pyplot as plt

def plotRTI(radar_data):
    '''
    Inputs:
        radar_data: contains pulse data, time stamps, and range bins
    Outputs:
        Displays an RTI plot of the RADAR data
    '''
    plt.figure(0)
    plt.set_cmap('jet')
    plt.imshow(np.abs(radar_data[0])) #Plots the image
    plt.title('Range-Time Intensity')
    plt.xlabel('Range Bins')
    plt.ylabel('Pulse Index')
    plt.axis('tight')
    ax = plt.gca()
    ax.invert_yaxis()
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('dB')
    plt.show() #Shows the image in a new window for Mason
