import pandas as pd
import csv
path = '../Raw_Data/DavidPosition.csv' 
parsedData = pd.read_csv(path,low_memory=False, delimiter=',', header=0, encoding='ascii')
X = parsedData['X']
Y = parsedData['Y']
Z = parsedData['Z']

path = '../Raw_Data/DavidPulseData.csv'
Pulses = [] 
with open(path, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        Pulses.append(row)
path = '../Raw_Data/DavidRangeAxis.csv'
rangeAxis = [] 
with open(path,'r') as csvfile:
    reader = csv.reader(csvfile,delimiter= ' ', quotechar = '|')
    for row in reader:
        rangeAxis.append(int(row[0]))
print(rangeAxis)
