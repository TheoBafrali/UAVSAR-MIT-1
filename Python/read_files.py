import pandas as pd
import pickle
import numpy

'''
This file is meant to read the data from the motion capture system, as well as from unpacked, pickle data from the PulsON 440 unpack script.
'''

def read_motion_data(filename,rigid_body_name='Mason UAV-SAR 1'):

    '''
Will return a list that holds x, y and z data from the motion capture system
    '''

    data = []
    path = '../Raw_Data/' + str(filename) #This is the path to the file
    parsedData = pd.read_csv(path,low_memory=False,skiprows=3) #Reading the CSV file
    for name in list(parsedData):
        #Determining if the parsed data is part of the rigid body

        if rigid_body_name in name and "Marker" not in name: 
            data.append(list(parsedData[name][2:]))

    #Adding only the X, Y, Z data to the final list
    Finaldata = [data[4],data[5],data[6]]
    return Finaldata

def read_radar_data(filename='../Raw_Data/data.pkl'):

    '''
Will return a list with scan data, time stamp, and range bins from the pickled data
    '''

    path = '../Raw_Data/' + str(filename) #This is the path to the file
    data = pickle.load(open(path,'rb')) #Loading the pickle file
    time_stamp = numpy.concatenate(data['time_stamp'])
    scan_data = data['scan_data']
    range_bins = data['range_bins']
    config = data['config']

    #Adding only the scan, time stamp, and range bin data to the final list
    for i in range(1,len(time_stamp)):

        if i != (len(time_stamp)-1):
            if time_stamp[i] == time_stamp[i-1]:
                time_stamp[i] = (time_stamp[i-1]+time_stamp[i+1])/2.0
    data = [scan_data,time_stamp,range_bins,config]
    return data
#read_motion_data("MC-RailSAR.csv",'Mason UAV-SAR 1'
