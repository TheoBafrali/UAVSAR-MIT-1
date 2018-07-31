# -*- coding: utf-8 -*-
"""
Inputs: 
    IntensityList: list of intensities reshaped into an array from backprojection
    IterationNumber: User-inputted integer that is the number of iterations the Richardson-Lucy algorithm iterates through
    PercentageMin: percentage, as a decimal, of the maximum intensity in your images that you want to use as the minimum cutoff
     
Outputs: 
    Figure1: Image after deconvolution with iteration number 10
    Figure2: Image after deconvolution with iteration number IterationNumber, a user input
    DeconvolutedIntensityList: List of intensities reshaped into an array after deconvolution
    
Summary:
    Uses the Richardson-Lucy algorithm to deconvolute the backprojected image, given as an array of intensities
    
Created on Tue Jul 31 09:11:07 2018

@author: dbli2000
"""
import skimage
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage import color, data, restoration, io
from scipy.signal import convolve2d as conv2
import csv

def deconvolute(IntensityList, IterationNumber = 30, PercentageMin = 1/5.5):
    #Define point spread function
    psf = np.array([[1/37, 1/37, 1/37,1/37 ,1/37], [1/37, 2/37, 2/37, 2/37 ,1/37], [1/37, 2/37, 5/37, 2/37 ,1/37], [1/37, 2/37, 2/37, 2/37 ,1/37], [1/37, 1/37, 1/37, 1/37 ,1/37]])  
   
    # Restore image using Richardson-Lucy algorithm
    DefaultDeconvoluted = restoration.richardson_lucy(IntensityList, psf, iterations=10, clip = False)
    DeconvolutedIntensityList = restoration.richardson_lucy(IntensityList, psf, iterations=IterationNumber, clip  = False)

    #Plot deconvoluted images
    plt.set_cmap('jet')
    #Plot default deconvoluted image
    plt.imshow(DefaultDeconvoluted,vmin=DefaultDeconvoluted.max()*PercentageMin, vmax=DefaultDeconvoluted.max())
    plt.figure()
    #Plot user deconvoluted image
    plt.imshow(DeconvolutedIntensityList,vmin=DeconvolutedIntensityList.max()*PercentageMin, vmax=DeconvolutedIntensityList.max())
    
    #Returns intensity list with user inputted number of iterations
    return DeconvolutedIntensityList
