# -*- coding: utf-8 -*-
"""
Helper functions for UAS-SAR.
"""

import numpy as np
from warnings import warn
    
def linear_interp_nan(coords, data):
    """
    Linear 1-D interpolation of data that may have missing data and/or 
    coordinates. Assumes that coordinates are uniformly spaced.
    """
    # Initialize outputs; make a deep copy to ensure that inputs are directly
    # modified
    coords_out = np.copy(coords)
    data_out = np.copy(data)
    
    # Store inputs original shapes
    coords_shape = coords_out.shape
    
    # Convert inputs to numpy arrays
    coords_out = np.asarray(coords_out).squeeze()
    data_out = np.asarray(data_out)
    
    # Check inputs
    if coords_out.ndim != 1:
        raise ValueError('Coordinates are not 1-D!')
        
    if data_out.ndim > 2:
        raise ValueError('Data must be a 2-D matrix!')
    elif data_out.ndim == 1:
        data_out = np.reshape(data_out, (-1, 1))
        
    dim_match = coords_out.size == np.asarray(data_out.shape)
    transpose_flag = False
    if not np.any(dim_match):
        raise IndexError('No apparent agreement')
    elif np.all(dim_match):
        warn(('Ambiguous dimensionalities; assuming columns of data are to ' + 
              'be interpolated'), Warning)
    elif dim_match[0] != 1:
        data_out = data_out.transpose()
        transpose_flag = True
        
    # Determine where NaN coordinates are replace them using linear 
    # interpolation assuming uniform spacing
    uniform_spacing = np.arange(0, coords_out.size)
    coords_nan = np.isnan(coords_out)
    coords_out[coords_nan] = np.interp(uniform_spacing[coords_nan], 
          uniform_spacing[~coords_nan], coords_out[~coords_nan])
    
    # Iterate over each dimension of data
    for ii in range(0, data_out.shape[1]):
        
        # Determine where the NaN data and replace them using linear 
        # interpolation
        data_nan = np.isnan(data_out[:, ii])
        data_out[data_nan, ii] = np.interp(coords_out[data_nan], 
                coords_out[~data_nan], data_out[~data_nan, ii])
        
    # Reshape results to match inputs
    coords_out = np.reshape(coords_out, coords_shape)
    if transpose_flag:
        data_out = np.transpose(data_out)
    
    # Return coordinates and data with NaN values replaced
    return coords_out, data_out