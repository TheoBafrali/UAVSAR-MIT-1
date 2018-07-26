from read_files import read_radar_data, read_motion_data
import numpy as np
data = read_radar_data()
motion_data = np.array(read_motion_data("../Raw_Data/MC-RailSAR.csv"))
radar_collection_time_hz = .011/1
motion_collection_hz = 360
constant = motion_collection_hz/radar_collection_time
radar_aligned_val = 10
motion_aligned_val = 12
Pulses = data[0][radar_aligned_val:]
aligned_motion_data = []
for i in range(len(Pulses)):
	floor_val = (constant*i) - floor(constant*i)
	ceil_val = 1 - floor_val
	floored = floor_val * motion_data[floor(constant*i)]
	ceiling = ceil_val * motion_data[ceil(constant*i)]
	aligned_motion_data(floored+ceiling)
print(aligned_motion_data)
