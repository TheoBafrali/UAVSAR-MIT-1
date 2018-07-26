import matplotlib.pyplot as plt
import numpy as np
from read_files import read_motion_data
import math
data = read_motion_data("MC-RailSAR.csv")
x = data[0]
y = data[1]
z = data[2]
sampling_rate = 360
velocities = []
for i in range(1,len(data[0])):
    distance = math.sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2+(z[i]-z[i-1])**2)
    velocity = distance * sampling_rate
    velocities.append(velocity)
movement = []
list_pos = 0
for i in range(1,len(velocities)):
    if abs(velocities[i])+abs(velocities[i-1]) > .7:
        movement.append(velocities[i-1])
        list_pos = i
        break
x = data[0][i:]
y = data[1][i:]
z = data[2][i:]
