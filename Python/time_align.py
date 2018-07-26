import numpy
from read_files import read_motion_data, read_radar_data

'''
reads radar and motion data files, generates a new file which
establishes a one to one correspondence between pulses and position data, yay
'''

def ingest(motion_filename, radar_filename, rigid_body_name):
    motion_data = read_motion_data(motion_filename)
    radar_data = read_radar_data(radar_filename)


    '''find when motion starts'''
    # get distances between points

    motion_deltas = []np.array(motion_data))

    # find index when we start really movin'
    # de-noise by taking running averages of last 20 values and then look for
    # the large change, recall we begin at index = 20

    smoothed_motion_deltas = np.array([])

    for ii in range(, len(motion_deltas) - 20):
        np.append(motion_deltas, np.sum(motion_deltas[ii:ii + 20])


    
