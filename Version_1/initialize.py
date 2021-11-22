# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 16:10:18 2021

@author: Sergio
"""

from Initialization import Initialization

    
def initialize(T, N, sigma, a, directory='.'):
    """
    Using the Initialization class, it generates the initial positions and 
    velocities required for a molecular dynamics simulation

    Parameters
    ----------
    T : float
        Reduced temperature.
    N : int
        Number of unit cells in the supercell along one axis.
    sigma : float
        Sigma parameter in Lennard-Jones potential.
    a : float
        lattice constant.

    Returns
    -------
    Two arrays with positions and velocities in cartesian coordiantes 
    (see .dat files for more info)

    """
    #Create object
    b = Initialization(T, N, sigma, a, directory)
    
    #Position initialization
    b.unit_cell()
    b.supercell()
    b.final_change()
    
    #Velocities initialization
    b.velocities()
    
    #Run tests
    b.tests()
    
    #return arrays
    return b.get_pos(), b.get_vel()
    

