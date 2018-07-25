import numpy as np
import matplotlib.pyplot as plt
import imageio
from scipy.signal import convolve2d as conv2

from skimage import color, data, restoration
def deconvolve(img):
     image = imageio.imread(img)
     psf = np.ones((5, 5)) / 25
     test = restoration.richardson_lucy(image,psf,iterations=30)
     plt.imshow(test)
     plt.show()
deconvolve("imageio:chelsea.png")
