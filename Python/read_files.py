'''
This file is meant to read the data from the motion capture system, as well as from unpacked, pickle data from the PulsON 440 unpack script.

@author: Mason
'''

#Import required modules
import pandas as pd
import pickle
import numpy


def read_motion_data(filename,rigid_body_name='Mason UAV-SAR 1'):

    '''
    Inputs:
        filename = literally file name  of motion data, should be a .csv
        rigid_body_name = rigid body you want to extract data for
    
    Outputs:
        final_data: array containing x, y, and z positions for all time points of given marker
    
    Summary:
        Will return a list that holds x, y and z data from the motion capture system
    '''
    
    #Reads in .csv
    data = []
    path = '../Raw_Data/' + str(filename) #This is the path to the file
    parsedData = pd.read_csv(path,low_memory=False,skiprows=3) #Reading the CSV file
    
    #Only adding data for the desired marker
    for name in list(parsedData):
        #Determining if the parsed data is part of the rigid body

        if rigid_body_name in name and "Marker" not in name: 
            data.append(list(parsedData[name][2:]))
            
    #Adding only the X, Y, Z data to the final list
    x = []
    y = []
    z = []
    for i in range(1,len(data[4])):
        x.append(float(data[4][i]))
    for i in range(1,len(data[5])):
        y.append(float(data[5][i]))
    for i in range(1,len(data[6])):
        z.append(float(data[6][i]))
    final_data = []
    for i in range(len(x)):
        final_data.append([x[i],y[i],z[i]])
    return final_data

def read_radar_data(filename='../Raw_Data/data.pkl'):

    '''
    Inputs: 
        filename: name of .pkl containing RADAR data
    Outputs:
        data: restructured set of arrays containing scan data, time stamps, and range bins
    Summary:
        Will return a list with scan data, time stamp, 
        and range bins from the pickled data
    '''
    #Load data
    path = '../Raw_Data/' + str(filename) #This is the path to the file
    data = pickle.load(open(path,'rb')) #Loading the pickle file
    time_stamp = data['time_stamp']
    scan_data = data['scan_data']
    range_bins = data['range_bins']
    
    #Adding only the scan, time stamp, and range bin data to the final list
    new_time_stamp = []

    start_time = time_stamp[0]
    for i in range(len(time_stamp)):
        time_stamp[i] = time_stamp[i]-start_time

    data = [scan_data,time_stamp,range_bins]
    return data

