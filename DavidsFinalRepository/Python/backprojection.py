# -*- coding: utf-8 -*-
"""
Ramu's SAR backprojection image formation.

@author: Ramu
"""

# Import the required modules
import sys
import os
import numpy as np
import argparse
import pickle
import matplotlib.pyplot as plt
from scipy.misc import imsave
from pulson440_constants import SPEED_OF_LIGHT

def shift_approach(pulses, range_axis, platform_pos, x_vec, y_vec):
    """
    Backprojection using only discrete shifts.
    """
    
def interp_approach(aligned_data,radar_data, x_bounds, y_bounds,pixel_res):
    """
    Backprojection using interpolated shifts.
    """
    range_axis = radar_data[2]
    pulses = aligned_data[0]
    WrongRadarPosition = aligned_data[1]
    platform_pos = []
    for i in range(len(WrongRadarPosition)):
        y = WrongRadarPosition[i][0]
        x = WrongRadarPosition[i][2]
        z = WrongRadarPosition[i][1]
        platform_pos.append([x,y,z])
    # Ensure that the range_axis is a 1-D vector
    range_axis = np.squeeze(range_axis)
     
    # Determine dimensions of data
    num_pulses = pulses.shape[0]
        
    x_vec = np.arange(x_bounds[0], x_bounds[1], 
                        pixel_res)
    y_vec = np.arange(y_bounds[0], y_bounds[1], 
                        pixel_res)
    
    x_grid, y_grid = np.meshgrid(x_vec,y_vec)    
 
    # Initialize SAR image
    complex_image = np.zeros_like(x_grid, dtype=np.complex)
    print(platform_pos[0][0])
    # Iterate over each pulse
    for ii in range(0, num_pulses):
        
        # Compute the 2-way range between current platform position and each 
        # point in the image grid
        two_way_range_grid = np.sqrt((x_grid - platform_pos[ii][0])**2 + 
                                         (y_grid - platform_pos[ii][1])**2 +
                                         platform_pos[ii][2]**2)
        
        # Interpolate the current pulse's return to each range in the image 
        # grid using linear interpolation
        complex_image += np.interp(two_way_range_grid, range_axis, 
                                   pulses[ii, :])
    
    image_extent = (x_vec[0], x_vec[-1], y_vec[0], y_vec[-1])
    plt.figure()
    plt.subplot(121)
    plt.imshow(np.abs(complex_image), origin='lower', extent=image_extent)
    plt.title('Linear Scale')
    plt.colorbar()
    plt.subplot(122)
    plt.imshow(20 * np.log10(np.abs(complex_image)), origin='lower', extent=image_extent)
    plt.title('Logarithmic Scale')
    plt.colorbar()
    plt.show()

    return complex_image
    
def fourier_approach(pulses, range_axis, platform_pos, x_vec, y_vec, 
                     center_freq):
    """
    Backprojection using shifts implemented through linear phase ramps.
    """
    # Determine dimensions of data
    (num_pulses, num_range_bins) = pulses.shape
    num_x_pos = len(x_vec)
    num_y_pos = len(y_vec)
    
    # Compute the fast-time or range-bin times
    fast_time = np.transpose(range_axis / SPEED_OF_LIGHT)
    delta_fast_time = fast_time[1] - fast_time[0]
    
    # Compute the unwrapped angular frequency
    ang_freq = np.transpose(2 * np.pi * 
                            np.arange(-num_range_bins / 2, num_range_bins / 2) / 
                            (delta_fast_time * num_range_bins))
    
    # X-Y locations of image grid
    x_grid, y_grid = np.meshgrid(x_vec, y_vec)
    
    # Initialize SAR image
    complex_image = np.zeros_like(x_grid, dtype=np.complex)
    
    # Iterate over each X-position in image grid and focus all the pixels 
    # across the Y-span of the image grid, i.e., a column
    for ii in range(0, num_x_pos):
        print('%d of %d' % (ii, num_x_pos))
        
        # Initialize current column's sum of aligned pulses
        sum_aligned_pulses = np.zeros(num_y_pos, dtype=np.complex)
        
        # Iterate over each pulse
        for jj in range(0, num_pulses):
            
            # Calculate the 2-way time delay to each point in the current 
            # column of the image grid
            two_way_time = 2 * np.sqrt(
                    (x_grid[:, ii] - platform_pos[jj, 0])**2 + 
                    (y_grid[:, ii] - platform_pos[jj, 1])**2 +
                    platform_pos[jj, 2]**2) / SPEED_OF_LIGHT
                    
            # Demodulate the current pulse
            demod_pulse = (np.transpose(np.atleast_2d(pulses[jj, :])) * 
                           np.exp(-1j * 2 * np.pi * center_freq * 
                                  (fast_time - two_way_time)))
            
            # Align the current pulses contribution to current column
            demod_pulse_freq = np.fft.fftshift(np.fft.fft(demod_pulse, axis=0),
                                               axes=0)
            phase_shift = np.exp(1j * np.outer(ang_freq, two_way_time))
            demod_pulse_freq_aligned = phase_shift * demod_pulse_freq
            pulse_aligned = np.fft.ifft(
                    np.fft.ifftshift(demod_pulse_freq_aligned, 0), axis=0)
            
            # Update current column's sum of aligned pulses
            sum_aligned_pulses += np.transpose(pulse_aligned[0])
            
        # Update complex image with latest column's result
        complex_image[:, ii] = sum_aligned_pulses
        
    return complex_image

def parse_args(args):
    """
    Input argument parser.
    """
    parser = argparse.ArgumentParser(
            description=('SAR image formation via backprojection'))
    parser.add_argument('input', nargs='?', type=str,
                        help='Pickle containing data')
    parser.add_argument('x_bounds', nargs=2, type=float, 
                        help=('Minimum and maximum bounds of the X coordinates'
                              ' of the image (m)'))
    parser.add_argument('y_bounds', nargs=2, type=float, 
                        help=('Minimum and maximum bounds of the Y coordinates'
                              ' of the image (m)'))
    parser.add_argument('pixel_res', type=float, help='Pixel resolution (m)')
    parser.add_argument('-o', '--output', nargs='?', const=None, default=None, 
                        type=str, help='File to store SAR image to')
    parser.add_argument('-m', '--method', nargs='?', type=str,
                        choices=('shift', 'interp', 'fourier'),
                        default='fourier', const='fourier', 
                        help='Backprojection method to use')
    parser.add_argument('-fc', '--center_freq', type=float, 
                        help=('Center frequency (Hz) of radar; must be '
                              'specified if using fourier method'))
    parser.add_argument('-nv', '--no_visualize', action='store_true', 
                        help='Do not show SAR image')
    parsed_args = parser.parse_args(args)
    
    # Do some additional checks
    if parsed_args.output is None:
        root, ext = os.path.splitext(parsed_args.input)
        parsed_args.output = '%s.png' % root
    
    return parsed_args

def main(args):
    """
    Top level methods
    """
    # Parse input arguments
    parsed_args = parse_args(args)
    
    # Load data
    with open(parsed_args.input, 'rb') as f:
        data = pickle.load(f)
    platform_pos = data[0]
    pulses = data[1]
    range_axis = data[2]
    
    # Determine X-Y coordinates of image pixels
    x_vec = np.arange(parsed_args.x_bounds[0], parsed_args.x_bounds[1], 
                      parsed_args.pixel_res)
    y_vec = np.arange(parsed_args.y_bounds[0], parsed_args.y_bounds[1], 
                      parsed_args.pixel_res)
    
    # Form SAR image
    if parsed_args.method == 'shift':
        complex_image = shift_approach(
                pulses, range_axis, platform_pos, x_vec, y_vec)
    elif parsed_args.method == 'interp':
        complex_image = interp_approach(
                pulses, range_axis, platform_pos, x_vec, y_vec)
    elif parsed_args.method == 'fourier':
        complex_image = fourier_approach(
                pulses, range_axis, platform_pos, x_vec, y_vec, 
                parsed_args.center_freq)
    else:
        raise ValueError('Unknown method %s specified' % parsed_args.method)    
        
    # Convert to magnitude image for visualization
    image = np.abs(complex_image)
        
    # Show SAR image
    if not parsed_args.no_visualize:
        image_extent = (x_vec[0], x_vec[-1], y_vec[0], y_vec[-1])
        plt.figure()
        plt.subplot(121)
        plt.imshow(image, origin='lower', extent=image_extent)
        plt.title('Linear Scale')
        plt.colorbar()
        plt.subplot(122)
        plt.imshow(20 * np.log10(image), origin='lower', extent=image_extent)
        plt.title('Logarithmic Scale')
        plt.colorbar()
        plt.show()
        
    # Save image
    imsave(parsed_args.output, image)
    
if __name__ == "__main__":
    """
    Standard Python alias for command line execution.
    """
    main(sys.argv[1:])
