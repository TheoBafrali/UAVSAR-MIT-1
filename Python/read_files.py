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
Will return a list with scan data, time stamp, and range bins from the pickled data
    '''

    path = '../Raw_Data/' + str(filename) #This is the path to the file
    data = pickle.load(open(path,'rb')) #Loading the pickle file
    time_stamp = numpy.concatenate(data['time_stamp'])
    scan_data = data['scan_data']
    range_bins = data['range_bins']
    config = data['config']

    #Adding only the scan, time stamp, and range bin data to the final list
    new_time_stamp = []

    start_time = time_stamp[0]
    for i in range(len(time_stamp)):
        time_stamp[i] = time_stamp[i]-start_time

    data = [scan_data,time_stamp,range_bins,config]
    return data

