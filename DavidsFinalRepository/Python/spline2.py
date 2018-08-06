#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 08:13:53 2018
@author: Hannah
"""
import matplotlib.pyplot as plt
from scipy import interpolate
#from Unpack import unpack
#from read_files import read_motion_data
import numpy as np

#motion_data = read_motion_data("../Raw_Data/MC-RailSAR2.csv")

def interp_3(motion_data):
    a = len(motion_data)*(1000/360)
    time = []
    
    for i in range(len(motion_data)):
        time.append((1/360)*1000*i) #Hz to Milliseconds
    resolution = np.arange(0, a, 1)
    
    x = []
    for i in motion_data:
        x.append(i[0])
    x_function = interpolate.CubicSpline(time, x)
    x_interp = x_function(resolution)   # use interpolation function returned by `interp1d`
    
    y = []
    for i in motion_data:
        y.append(i[1])
    y_function = interpolate.CubicSpline(time, y)
    y_interp = y_function(resolution)   # use interpolation function returned by `interp1d`
    
    z = []
    for i in motion_data:
        z.append(i[2])
    z_function  = interpolate.CubicSpline(time, z)
    z_interp = z_function(resolution)   # use interpolation function returned by `interp1
    
    final_motion_list = []
    for i in range(len(x_interp)):
        final_motion_list.append([x_interp[i],y_interp[i],z_interp[i]])
    
    print('lengths')
    print(len(motion_data))
    print(len(final_motion_list))
    
    return final_motion_list