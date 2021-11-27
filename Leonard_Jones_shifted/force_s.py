import numpy as np

def force_lj_shifted(sigma, epsilon, distance, rc):
    """

    Parameters
    ----------
    sigma : float
        the parameter sigma of the leonard-jones otential
        
    epsilon : float
        the parameter epsilon of the leonard-jones otential
        
    distance: float
        the distance between the two particles
        
    rc: float
        the cut off distance

    Returns
    -------
    float
        force that makes particles 1 to particle 2 due to original leonrd-jones potential
    """
    if distance<=rc:
        
        force = (48*(epsilon/distance))*((sigma/distance)^(12)-0.5*(sigma/distance)^6)
    else:
        force=0
    return force
