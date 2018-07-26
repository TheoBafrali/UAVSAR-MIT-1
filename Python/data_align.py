from read_files import read_radar_data, read_motion_data
import numpy as np
data = read_radar_data()
radar_time = np.array(data[1])*.001
print(radar_time)
