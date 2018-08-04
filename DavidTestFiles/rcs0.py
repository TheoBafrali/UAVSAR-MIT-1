#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 09:05:02 2018

@author: David
"""
import math
import decimal

antenna_gain = 5 #dBi
transmit_power = 0.00005 #appoximately 50 uW, in watts
#transmit_frequency = 4.3 gHz, use this to find lambda
Lambda = 0.07 #meters, 0.06976744186, aka transmit wavelength
#power received = it varies
c = 3*(10**8)
k = 1.38*(10**23)

#aka Boltzmann's constant, Watt*sec/°Kelvin
def radar_range(power_received, t):
    Range = 1.5*(10**8)*t #t = measured running time in sec
    a = k*(Range**4)
    b = (power_received)*(64*(math.pi**3))
    c = (transmit_power*antenna_gain*(Lambda**2))
    return a*b/c #is the radar cross section, sigma
print(radar_range(7,1))

