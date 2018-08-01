'''
Reads in CSVs from David's manual alignment

@author: David + Mason
'''
#Import required modules
import pandas as pd
import csv

#Reads in Position data, generates list
path = '../Raw_Data/DavidPosition.csv' 
parsedData = pd.read_csv(path,low_memory=False, delimiter=',', header=0, encoding='ascii')
X = parsedData['X']
Y = parsedData['Y']
Z = parsedData['Z']

#Reads in pulse data from CSV
path = '../Raw_Data/DavidPulseData.csv'
Pulses = [] 
with open(path, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        Pulses.append(row)
        
#Reads in range axis data from csv
path = '../Raw_Data/DavidRangeAxis.csv'
rangeAxis = [] 
with open(path,'r') as csvfile:
    reader = csv.reader(csvfile,delimiter= ' ', quotechar = '|')
    for row in reader:
        rangeAxis.append(int(row[0]))
