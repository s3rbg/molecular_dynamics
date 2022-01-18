import numpy as np

def force_lj_shifted(sigma, distance, rc):
    """
    Accelerations (and forces, as m = 1) considering a double shifted Lennard-Jones potential 
    (continous until the force's first derivative).
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
    r_twelve = rc ** 12 
    r_six = rc ** 6

    if distance == 0:
        return 0 
    if distance <= rc:
        f = (24 / distance) * (2 * (1/distance) ** 12 - (1/distance) ** 6)
        dfc = (48 / rc) *( (1/r_twelve) - 0.5 * (1/r_six) )
        force = f - dfc
    else:
        force=0
        
    return force
