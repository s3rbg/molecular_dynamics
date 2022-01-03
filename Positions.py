# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 11:12:27 2022

@author: Sergio
"""

import numpy as np
import pandas as pd
import os

def positions(time, itime, pos, directory='.'):
    """
    Creates a .dat file with the positions for a given time step
    
    Parameters:
        time: float
            time of the simulated positions
        itime: int
            index of the time step to create the file
        pos: array
            positions of the atoms for the given time step
        directory: string
            Directory where the file is going to be saved without the last bar.
            The default is where this .py file is.
            
    """
    file = str(directory)+'/positions'+str(itime)+'.dat'
    columns  = ['x', 'y', 'z']
    index = np.arange(len(pos))+1
    df = pd.DataFrame(data=pos, index=index, columns=columns)
    
    
    
    if os.path.exists(file):
        os.remove(file)
    with open(file, 'a+') as f:
        f.write('Positions of the atoms at time '+str(time)+'\n\n')
        f.close()
    df.to_csv(file, sep='\t', mode='a+')
    
