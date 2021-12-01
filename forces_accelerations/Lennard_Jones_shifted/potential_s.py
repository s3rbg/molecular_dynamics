import numpy as np

def potential_lj_shifted (sigma, epsilon, distance, rc):
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
        the potencial energy (original leonard jones potential)
        of particle 1 due to particle 2 (the same of 2 due to 1)
    """
    if distance <= rc:
            
        v=4*epsilon*((sigma/distance)**(12)-(sigma/distance)**6)  
        vc=4*epsilon*((sigma/rc)**(12)-(sigma/rc)**6)  
        dvc= (48*(epsilon/rc))*((sigma/rc)**(12)-0.5*(sigma/rc)**6)
        energy= v - vc -dvc
    else:
        energy = 0
    
    
    return energy
