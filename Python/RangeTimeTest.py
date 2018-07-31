from read_files import read_radar_data, read_motion_data
import matplotlib.pyplot as plt
radar_data = read_radar_data("../Raw_Data/data.pkl")
plt.imshow(radar_data[0],extent=[radar_data[2][1],radar_data[2][-1],1,len(radar_data[0])])
plt.show()

