import numpy as np

def kinetic(velocities):
    """
    Kinetic energy for a given atom
    
    Parameters
    ----------
    velocities : float
        an array with the cardinate components of the velocity

    Returns
    -------
    float
        the kinetic energy of the particle

    """
    vel_2 =  velocities[0]**2 + velocities[1]**2 + velocities[2]**2 
    energy = vel_2/2
    return energy
