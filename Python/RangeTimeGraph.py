import matplotlib.pyplot as plt
import numpy as np
from read_files import read_radar_data
data = read_radar_data()
Pulses = np.flip(data[0],0)
Range_Bins = data[2]
RangeBinDistance = Range_Bins[2]-Range_Bins[1]
RangeBinX = []
for i in np.arange(0,len(Range_Bins),50):
    RangeBinX.append(round(i*RangeBinDistance+Range_Bins[0],2))
plt.set_cmap('nipy_spectral')
plt.xticks(np.arange(0,len(Range_Bins),50),RangeBinX)
#plt.yticks(np.arange(0,len(Pulses),1000),np.flip(np.arange(0,len(Pulses),1000),0))
plt.xlabel("Distance (m)")
plt.ylabel("Pulse Number")
plt.imshow(np.abs(Pulses))
plt.axis('tight')
plt.show()
