import pickle
from Unpack import unpack
from read_files import read_radar_data, read_motion_data
from data_align import align_data
motion_data = read_motion_data("../Raw_Data/UASSAR4_rail_diagonal.csv","UASSAR4")
radar_data = read_radar_data("../Raw_Data/railTestDiagonal.pkl")

aligned_data = align_data(radar_data,motion_data,272,1844,5368)

Pulses = aligned_data[0]

Final_Motion = aligned_data[1]
print(Final_Motion)
aligned_data[2] = radar_data[2]
with open('parrot.pkl', 'wb') as f:
    pickle.dump(aligned_data,f)
    f.close()
