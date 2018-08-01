# -*- coding: utf-8 -*-
"""
Contains the deconvolute() function, which deconvolutes a backprojected image passed in as an intensity list using the Richardson-Lucy algorithm. 

Created on Tue Jul 31 09:11:07 2018
@author: dbli2000
"""
#Import required modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve, convolve

def RichardsonLucy(image, psf, iterations=50, clip=False):
    """
    Richardson-Lucy deconvolution, modified from skimage to deal with 0s
   
    Inputs:
        image : ndarray that is starting image
        psf : ndarraym, the point spread function.
        iterations : number of iterations
        clip : boolean, optional. False by default. If true, pixel value of the result above 1 or
                under -1 are thresholded for skimage pipeline compatibility.
    Outputs: 
        im_deconv : deconvolved image
        
    Summary:
        Performs the Richardson-Lucy algorithm
    """
    # compute the times for direct convolution and the fft method. The fft is of
    # complexity O(N log(N)) for each dimension and the direct method does
    # straight arithmetic (and is O(n*k) to add n elements k times)
    direct_time = np.prod(image.shape + psf.shape)
    fft_time =  np.sum([n*np.log(n) for n in image.shape + psf.shape])

    # see whether the fourier transform convolution method or the direct
    # convolution method is faster (discussed in scikit-image PR #1792)
    time_ratio = 40.032 * fft_time / direct_time

    if time_ratio <= 1 or len(image.shape) > 2:
        convolve_method = fftconvolve
    else:
        convolve_method = convolve

    image = image.astype(np.float)
    psf = psf.astype(np.float)
    im_deconv = 0.5 * np.ones(image.shape)
    psf_mirror = psf[::-1, ::-1]

    for _ in range(iterations):
        relative_blur = image / convolve_method(im_deconv, psf, 'same')
        relative_blur[np.isnan(relative_blur)] = 0
        im_deconv *= convolve_method(relative_blur, psf_mirror, 'same')

    if clip:
        im_deconv[im_deconv > 1] = 1
        im_deconv[im_deconv < -1] = -1

    return im_deconv

def deconvolute(IntensityList, IterationNumber = 30, PercentageMin = 1/5.5):
    '''
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
    '''
    
    #Define point spread function
    psf = np.array([[1/37, 1/37, 1/37,1/37 ,1/37], [1/37, 2/37, 2/37, 2/37 ,1/37], [1/37, 2/37, 5/37, 2/37 ,1/37], [1/37, 2/37, 2/37, 2/37 ,1/37], [1/37, 1/37, 1/37, 1/37 ,1/37]])  
   
    # Restore image using Richardson-Lucy algorithm
    DefaultDeconvoluted = RichardsonLucy(IntensityList, psf, iterations=10, clip = False)
    DeconvolutedIntensityList = RichardsonLucy(IntensityList, psf, iterations=IterationNumber, clip  = False)

    #Plot deconvoluted images
    plt.set_cmap('jet')
    #Plot default deconvoluted image
    plt.figure(2)
    plt.imshow(DefaultDeconvoluted,vmin=DefaultDeconvoluted.max()*PercentageMin, vmax=DefaultDeconvoluted.max())
    plt.show()
    #Plot user deconvoluted image
    plt.figure(3)
    plt.imshow(DeconvolutedIntensityList,vmin=DeconvolutedIntensityList.max()*PercentageMin, vmax=DeconvolutedIntensityList.max())
    #Returns intensity list with user inputted number of iterations
    return DeconvolutedIntensityList
