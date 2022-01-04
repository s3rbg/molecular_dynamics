import numpy as np

def force_lj(sigma, epsilon, distance, rc):
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
    if distance == 0:
        return 0 
    if distance<=rc/sigma:
        force = (48 * (1/distance) * ((1 / distance) ** (12) - 0.5 * (1 / distance) ** 6))       
    else:
        force = 0
    return force

