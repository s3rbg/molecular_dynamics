# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 10:52:46 2021
@author: Sergio
"""
import numpy as np

def histogram(array, bins=100, sigma=1, wide=2.5):
    """
    Prints in a file a histogram according to the data given in the input array
    It should be a Gaussian distribution
    Parameters
    ----------
    array : array
        data to evaluate.
    bins : int, optional
        Number of bins. The default is 100.
    sigma: float, optional
        Standard deviation. The default is 1
    """
    
    num, edge = np.histogram(array, bins, (-wide*sigma, wide*sigma))
    
    return num, edge