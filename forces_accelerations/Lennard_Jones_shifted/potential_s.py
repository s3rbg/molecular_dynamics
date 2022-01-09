import numpy as np
import matplotlib.pyplot as plt

def potential_lj_shifted (sigma, distance, rc):
    """
    Potential energy for a given distance between atoms, for a double shifted Lennnard-Jones potential.

    Parameters
    ----------
    sigma : float
        the parameter sigma of the leonard-jones potential
        
    epsilon : float
        the parameter epsilon of the leonard-jones potential
        
    distance: float
        the distance between the two particles
        
    rc: float
        the cut off distance
    Returns
    -------
    float
        the potencial energy (original leonard jones potential)
        of particle 1 due to particle 2 (the same of 2 due to 1)
    """
    
    r_twelve = rc ** 12 
    r_six = rc ** 6
    distance = distance*sigma

    if distance <= rc:
        e = 4 * ( (1/distance)**12 - (1/distance)**6)
        ec = 4 * ( (1/r_twelve) - (1/r_six))
        dec =(-48/rc) * (1/(r_twelve) - 0.5/(r_six)) * (distance - rc)
        energy = e - ec - dec
    else:
        energy = 0
    return energy


