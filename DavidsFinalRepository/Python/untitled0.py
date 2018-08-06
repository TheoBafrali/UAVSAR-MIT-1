# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 18:47:12 2018

@author: dbli2
"""
import numpy as np

def entropycalculation(SAR_image):
    NormalizedSARimage = SAR_image 
    EntropyArray = np.select([NormalizedSARimage <= 0, NormalizedSARimage > 0], [0, -np.log2()]  )