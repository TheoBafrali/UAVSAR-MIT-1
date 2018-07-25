from read_files import read_radar_data, read_motion_data
import matplotlib.pyplot as plt
data = read_radar_data() 
motion = read_motion_data("MC-RailSAR.csv")
for i in data:
    plt.plot(i)
plt.show()
