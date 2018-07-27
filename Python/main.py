from Unpack import unpack
from read_files import read_radar_data, read_motion_data
from motion_capture import motion_point_one
from radar_movement import radar_point_one
from data_align import align_data
from LinInt import BackProjection

unpack("../Raw_data/RailSAR-record2")
motion_data = read_motion_data("../Raw_Data/MC-RailSAR2.csv")
radar_data = read_radar_data()
motion_start = motion_point_one(motion_data)
radar_start = radar_point_one(radar_data)
aligned_data = align_data(radar_data,motion_data,radar_start,motion_start)
BackProjection(aligned_data,radar_data,-10,10,.5)
