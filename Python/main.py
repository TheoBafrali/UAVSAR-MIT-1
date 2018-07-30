from Unpack import unpack
from read_files import read_radar_data, read_motion_data
from motion_capture import motion_point_one
from radar_movement import radar_point_one, find_i_of_first_motion
from data_align import align_data
from LinInt import BackProjection
from backprojection import interp_approach, main
#unpack("../Raw_data/RailSAR-record1")

motion_data = read_motion_data("../Raw_Data/MC-RailSAR.csv")

radar_data = read_radar_data("../Raw_Data/data.pkl")

motion_start = find_i_of_first_motion(motion_data)

radar_start = radar_point_one(radar_data)

aligned_data = align_data(radar_data,motion_data,radar_start,motion_start)

#interp_approach(aligned_data,radar_data,[-3,3],[-3,3],.1)

BackProjection(aligned_data,radar_data,-5,3,.1)
