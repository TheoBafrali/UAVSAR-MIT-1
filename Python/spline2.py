#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 08:13:53 2018

@author: Hannah
"""
import matplotlib.pyplot as plt
from scipy import interpolate
from Unpack import unpack
from read_files import read_motion_data
import numpy as np

motion_data = read_motion_data("../Raw_Data/MC-RailSAR2.csv")

def interp(motion_data):
    a = len(motion_data)*(1000/360)
    

    x = []
    for i in range(len(motion_data)):
        time1 = (1/360)*1000 #360 hertz to milliseconds
        x.append(time1*i)
    xnew = np.arange(0, a, 1)

    xx = []
    for ii in motion_data:
        xx.append(ii[0])

#y = np.exp(-x/3.0)
    f = interpolate.CubicSpline(x, xx)

    xxnew = f(xnew)   # use interpolation function returned by `interp1d`
    plt.plot(x, xx, 'b--', xnew, xxnew, 'r--')
    plt.show()

    y = []
    for ii in motion_data:
        y.append(ii[0])

#y = np.exp(-x/3.0)
    f1 = interpolate.CubicSpline(x, xx)

  
    ynew = f1(xnew)   # use interpolation function returned by `interp1d`
    plt.plot(x, y, 'g^', xnew, ynew, 'o')
    plt.show()

    z = []
    for ii in motion_data:
        z.append(ii[0])

#y = np.exp(-x/3.0)
    f2 = interpolate.CubicSpline(x, z)

  
    znew = f2(xnew)   # use interpolation function returned by `interp1d`
    plt.plot(x, xx, 'r^', xnew, znew, 'p--')
    plt.show()
print (interp(motion_data))