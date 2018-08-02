# -*- coding: utf-8 -*-
"""
Scales Pulse data by RADAR cross section
@author: dbli2
"""
from read_files import read_radar_data
import numpy as np
#radar_data = read_radar_data("../Raw_Data/UAVSAR4Flight1.pkl")

def rcs(radar_data):
    '''
    Inputs:
        radar_data: contains pulses, timestamps, and range bins
    Outputs:
        corrected_radar_data: contains corrected pulses, timestamps, and range bins
    Summary:
        does a sketchy RCS correction
    '''
    #Parses input data
    range_bins = radar_data[2]
    time_stamp = radar_data[1]
    pulses = radar_data[0]
    numpulses = len(pulses)
    numrangebins = len(range_bins)

    #Implements RCS correction
    corrected_pulses = np.zeros((numpulses, numrangebins))

    for p in range(0, numpulses): #Iterate over pulses
        for r in range(0, numrangebins): #Iterate over range bins
            corrected_pulses[p,  r] = pulses[p, r]*((range_bins[r])**4)
    
    #Redefines corrected_radar_data
    corrected_radar_data = [corrected_pulses,time_stamp,range_bins]
    return corrected_radar_data

#newdata = rcs(radar_data)

