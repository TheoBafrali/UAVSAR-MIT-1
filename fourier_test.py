from numpy import genfromtxt,average, array, real, arange, reshape
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import scatter, xlabel, ylabel, xlim, ylim, show, plot
import pickle
import numpy as np
from scipy.constants import speed_of_light

data = pickle.load(open('data_complex.pkl','rb'))
Platform = data[0] #Platform
PlatformX = Platform[:, 0]
Pulses = data[1] #Pulses

sig = Pulses[50]

freq_rep = np.fft.fft(sig)
plt.plot(freq_rep)
plt.show()

h_width = 3
h_height = 3
pxl_d = .1
p_width = int(2 * h_width / pxl_d)
p_height = int(2 * h_height / pxl_d)
