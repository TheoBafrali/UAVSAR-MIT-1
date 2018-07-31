from Unpack import unpack
from read_files import read_radar_data, read_motion_data
from motion_capture import motion_point_one
from radar_movement import find_point_one_radar, find_i_of_first_motion, find_i_of_last_motion
from data_align import align_data
from LinInt import BackProjection
from backprojection import interp_approach, main
from AlignedRangeTimeGraph import AlignedGraph
#unpack("../Raw_data/RailSAR-record1")

motion_data = read_motion_data("../Raw_Data/UASSAR4_rail_diagonal.csv","UASSAR4")

radar_data = read_radar_data("../Raw_Data/railTestDiagonal.pkl")

motion_start = find_i_of_first_motion(motion_data)
print(motion_start)
motion_end = find_i_of_last_motion(motion_data)
print(motion_end)
radar_start = find_point_one_radar(radar_data)
print(radar_start)
aligned_data = align_data(radar_data,motion_data,radar_start,motion_start, motion_end)

#AlignedGraph(aligned_data,radar_data)
#interp_approach(aligned_data,radar_data,[-3,3],[-3,3],.1)

BackProjection(aligned_data,radar_data,[-5,-5],[5,5],.05)
