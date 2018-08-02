# -*- coding: utf-8 -*-
"""
PulsON 440 radar data unpacking module 
"""

# Import the required modules
import os
import sys
import argparse
import pickle
import matplotlib.pyplot as plt
import numpy as np
from pulson440_formats import CONFIG_MSG_FORMAT
from pulson440_constants import SPEED_OF_LIGHT, T_BIN
from matplotlib.ticker import Formatter

# Constants
DT_0 = 10 # Path delay through antennas (ns)

class value_formatter(Formatter):
    """
    Tick label formatter.
    """
    
    def __init__(self, values):
        """
        Add set of values to use in ticks.
        """
        self.values = values
        
    def __call__(self, x, pos=0):
        """
        Return formatted tick label.
        """
        ind = int(np.round(x))
        if ind >= len(self.values) or ind < 0:
            return ''
        return '%3.1f  [%d]' % (self.values[ind], ind)

def read_config_data(file_handle, legacy=False):
    """
    Read in configuration data based on platform.
    """
    config = dict.fromkeys(CONFIG_MSG_FORMAT.keys())
    
    if legacy:
        config_msg = file_handle.read(44)
        config['node_id'] = np.frombuffer(config_msg[4:8], dtype='>u4')[0]
        config['scan_start'] = np.frombuffer(config_msg[8:12], dtype='>i4')[0]
        config['scan_stop'] = np.frombuffer(config_msg[12:16], dtype='>i4')[0]
        config['scan_res'] = np.frombuffer(config_msg[16:18], dtype='>u2')[0]
        config['pii'] = np.frombuffer(config_msg[18:20], dtype='>u2')[0]
        config['ant_mode'] = np.uint16(config_msg[32])
        config['tx_gain_ind'] = np.uint16(config_msg[33])
        config['code_channel'] = np.uint16(config_msg[34])
        config['persist_flag'] = np.uint16(config_msg[35])
        
    else:
        config_msg = file_handle.read(32)
        byte_counter = 0
        for config_field in CONFIG_MSG_FORMAT.keys():
            num_bytes = CONFIG_MSG_FORMAT[config_field].itemsize
            config_data = config_msg[byte_counter:(byte_counter + num_bytes)]
            config[config_field] = np.frombuffer(config_data,
                  dtype=CONFIG_MSG_FORMAT[config_field])[0]
            config[config_field] = config[config_field].byteswap()
            byte_counter += num_bytes
            
    return config

def unpack(file, legacy=False):
    """
    Unpacks PulsOn 440 radar data from input file
    """
    with open(file, 'rb') as f:
        
        # Read configuration part of data
        config = read_config_data(f, legacy)
        
        # Compute range bins in datas
        scan_start_time = float(config['scan_start'])
        start_range = SPEED_OF_LIGHT * ((scan_start_time * 1e-12) - DT_0 * 1e-9) / 2
        
        # Read data
        data = dict()
        data= {'scan_data': [],
               'time_stamp': [],
               'packet_ind': [],
               'packet_pulse_ind': [],
               'range_bins': [],
               'config': config}
        single_scan_data = []
        packet_count = 0
        pulse_count = 0
        
        while True:
            
            # Read a single data packet and break loop if not a complete packet
            # (in terms of size)
            packet = f.read(1452)
            if len(packet) < 1452:
                break            
            
            # Get information from first packet about how scans are stored and 
            # range bins collected
            if packet_count == 0:
                num_range_bins = np.frombuffer(packet[44:48], dtype='>u4')[0]
                num_packets_per_scan = np.frombuffer(packet[50:52], dtype='>u2')[0]
                drange_bins = SPEED_OF_LIGHT * T_BIN * 1e-9 / 2
                range_bins = start_range + drange_bins * np.arange(0, num_range_bins, 1)
            packet_count += 1
            
            # Number of samples in current packet and packet index
            num_samples = np.frombuffer(packet[42:44], dtype='>u2')[0]
            data['packet_ind'].append(np.frombuffer(packet[48:50], dtype='>u2')[0])
            
            # Extract radar data samples from current packet; process last 
            # packet within a scan seperately to get all data
            packet_data = np.frombuffer(packet[52:(52 + 4 * num_samples)], 
                                               dtype='>i4')
            single_scan_data.append(packet_data)
            
            if packet_count % num_packets_per_scan == 0:
                data['scan_data'].append(np.concatenate(single_scan_data))
                data['time_stamp'].append(np.frombuffer(packet[8:12], 
                    dtype='>u4')[0])
                single_scan_data = []
                pulse_count += 1
            
        # Add last partial scan if present
        if single_scan_data:
            single_scan_data = np.concatenate(single_scan_data)
            num_pad = data['scan_data'][0].size - single_scan_data.size
            single_scan_data = np.pad(single_scan_data, (0, num_pad), 
                                      'constant', constant_values=0)
            data['scan_data'].append(single_scan_data)
                
        # Stack scan data into 2-D array 
        # (rows -> pulses, columns -> range bins)
        data['scan_data'] = np.stack(data['scan_data'])
        
        # Finalize entries in data
        data['time_stamp'] = np.asarray(data['time_stamp'])
        data['range_bins'] = range_bins
        
        with open('../Raw_Data/data.pkl', 'wb') as o:
            pickle.dump(data, o)
        return data

def parse_args(args):
    """
    Input argument parser.
    """
    parser = argparse.ArgumentParser(
            description='PulsON 440 radar data unpacker')
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')
    parser.add_argument('-o', '--output', nargs='?', const='data.dat', default='',
                        dest='output', help='Output file; data will be pickled')
    parser.add_argument('-v', '--visualize', action='store_true', dest='visualize',
                        help='Plot RTI of unpacked data; will block computation')
    parser.add_argument('-l --legacy', action='store_true', dest='legacy',
                        help='Load legacy format of file')
    
    return parser.parse_args(args)

def main(args):
    """
    Top-level function; parses input arguments, unpacks, data, visualizes, and
    saves as specified.
    """
    args = parse_args(args)
    
    data = unpack(args.file, args.legacy)
    
    # Save (pickle) unpacked data
    if args.output:
        with open(args.output, 'wb') as o:
            pickle.dump(data, o)

    # Visualize RTI of unpacked data
    plt.ioff()
    if args.visualize:
        range_formatter = value_formatter(data['range_bins'])
        pulse_formatter = value_formatter((data['time_stamp'] - data['time_stamp'][0])/ 1000)
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        h_img = ax.imshow(20 * np.log10(np.abs(data['scan_data'])))
        ax.set_aspect('auto')
        ax.set_title('Range-Time Intensity')
        ax.set_xlabel('Range (m) [Range Bin Number]')
        ax.set_ylabel('Time Elapsed (s) [Pulse Number]')
        ax.xaxis.set_major_formatter(range_formatter)
        ax.yaxis.set_major_formatter(pulse_formatter)
        cbar = fig.colorbar(h_img)
        cbar.ax.set_ylabel('dB')
        
        # Try to display to screen if available otherwise save to file
        try:
            plt.show()
        except:
            plt.savefig('%s.png' % os.path.splitext(args.file)[0])

if __name__ == "__main__":
    """
    Standard Python alias for command line execution.
    """
    main(sys.argv[1:])
