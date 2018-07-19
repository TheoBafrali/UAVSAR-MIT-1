from numpy import genfromtxt,average, array, real, arange, reshape
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import scatter, xlabel, ylabel, xlim, ylim, show, plot
import pickle
import numpy as np
from scipy.constants import speed_of_light
import argparse
from utility import euc_norm, bin, roll


class ImageFormer():

    # inputs are filename, image size in m, and pixel width and height in m
    def __init__(self, filename, IMAGE_SIZE, pxl_d):
        self.data = pickle.load(open(filename,'rb'))
        self.Platform = self.data[0] #Platform
        self.Pulses = self.data[1] #Pulses
        self.RangeAxis = self.data[2] #RangeAxis
        self.pxl_d = pxl_d
        self.IMAGE_SIZE = IMAGE_SIZE
        self.IMAGE_PIXEL_SIZE = (np.array(IMAGE_SIZE) / pxl_d).astype(int)
        self.image = np.zeros((self.IMAGE_PIXEL_SIZE[0], self.IMAGE_PIXEL_SIZE[1]))


    def test(self):
        intensity_vec = np.zeros((self.IMAGE_PIXEL_SIZE[0] * self.IMAGE_PIXEL_SIZE[1], 2084))
        for x in range(0, self.IMAGE_PIXEL_SIZE[0]):
            for y in range(0, self.IMAGE_PIXEL_SIZE[1]):
                # for each pxl
                pxl_coord = [x*self.pxl_d - self.IMAGE_SIZE[0], y*self.pxl_d - self.IMAGE_SIZE[1], 0]

            for ii in range(0, len(self.Platform)):
                rangebin = int(bin(euc_norm(self.Platform[ii], pxl_coord)))
                intensity_vec[x * y] += np.absolute(roll(self.Pulses[ii], rangebin, 500))

        for i in range(0, self.IMAGE_PIXEL_SIZE[1] * self.IMAGE_PIXEL_SIZE[0]):
            plt.plot(intensity_vec[i])

        plt.show()


    def plotSAR(self):
        for x in range(0, self.IMAGE_PIXEL_SIZE[0]):
            if x % 10 == 0:
                print("Loading: %f" % (100 * x / self.IMAGE_PIXEL_SIZE[0]))
            for y in range(0, self.IMAGE_PIXEL_SIZE[1]):
                intensity = 0
                for i in range(len(self.Platform)):
                    pxl_coord = [x*self.pxl_d - self.IMAGE_SIZE[0] / 2, y*self.pxl_d - self.IMAGE_SIZE[1] / 2, 0]
                    range_bin = bin(euc_norm(self.Platform[i], pxl_coord))

                    weight_1 = (range_bin - np.floor(range_bin))
                    weight_2 = 1 - weight_1
                    if i is not 99:
                        intensity += weight_1 * self.Pulses[i, int(range_bin)] + weight_2 * self.Pulses[i + 1, int(range_bin)]
                    else:
                        intensity += self.Pulses[i, int(range_bin)]

                self.image[x][y] = np.absolute(intensity)

        self.image = np.rot90(np.array(self.image), 1)
        plt.imshow(self.image, cmap = 'gray')
        plt.show()

    def plotFourierSAR(self):
        for x in range(0, self.IMAGE_PIXEL_SIZE[0]):
            if x % 10 == 0:
                print("Loading: %f" % (100 * x / self.IMAGE_PIXEL_SIZE[0]))
            for y in range(0, self.IMAGE_PIXEL_SIZE[1]):
                # per pxl
                pxl_coord = [x*self.pxl_d - self.IMAGE_SIZE[0] / 2, y*self.pxl_d - self.IMAGE_SIZE[1] / 2, 0]
                ref_signal_d = euc_norm(self.Platform[50], pxl_coord)
                signal_sum = np.zeros(1084, dtype = complex)

                for i in range(len(self.Platform)):
                    # per pulse
                    og_sig = self.Pulses[i]
                    this_signal_d = euc_norm(self.Platform[i], pxl_coord)
                    delta_d = ref_signal_d - this_signal_d
                    time_delta = 2 * delta_d / speed_of_light
                    freq_rep = np.fft.fft(og_sig)
                    plt.plot(freq_rep)
                    plt.show()
                    #np.exp(-1j *2*np.pi*4.06*(10**9)*time_delta))
                    phi_shifted_sig = np.fft.ifft()
                    signal_sum += phi_shifted_sig

                self.image[x][y] = np.max(np.absolute(signal_sum))


        plt.imshow(self.image, cmap = 'gray')
        plt.show()


former = ImageFormer("data_complex.pkl", (6,6), .05)

former.plotSAR()

