#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:43:44 2022

@author: dgiron
"""

from common_modules.imports import *

def energy_to_txt(kinetic, potential, direc):
    append_new_line(direc + '/energy_each_step.txt', '{:.2f}, {:.2f}, {:.2f}'.format(kinetic, potential, kinetic+potential))
    

def positions_to_txt(time, itime, pos, directory='.'):
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
    file = directory + '/positions'+str(itime)+'.dat'
    columns  = ['x', 'y', 'z']
    index = np.arange(len(pos))+1
    df = pd.DataFrame(data=pos, index=index, columns=columns)
    
    if os.path.exists(file):
        os.remove(file)
    with open(file, 'a+') as f:
        f.write('Positions of the atoms at time '+str(time)+'\n\n')
        f.close()
    df.to_csv(file, sep='\t', mode='a+')
    
    

def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)
        
