import numpy as np
import matplotlib.pyplot as plt
from scipy import mgrid,exp
from numpy.fft import *
from PIL import Image
from skimage import color, data, restoration
def deconvolve(Input, psf, epsilon):
    InputFFT = fftn(Input)
    psfFFT = fftn(psf)+epsilon
    deconvolved = ifftn(InputFFT/psfFFT)
    deconvolved = np.abs(deconvolved)
    return(deconvolved)
plt.imshow(deconvolve("LinIntBP.png",2,1))
plt.show()
