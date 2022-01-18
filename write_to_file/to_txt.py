#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:43:44 2022

@author: dgiron
"""

from common_modules.imports import *

def energy_to_txt(kinetic, potential, direc):
    """
    Append kinetic, potential and total energy at the end of the output file

    Parameters
    ----------
    kinetic : float
        kinetic energy.
    potential : float
        potential energy.
    direc : str
        directory to save the file.

    Returns
    -------
    None.

    """
    append_new_line(direc + '/energy_each_step.txt', '{:.4f}, {:.5f}, {:.4f}'.format(kinetic, potential, kinetic+potential))
    

def positions_to_txt(positions, step, direc, n_at):
    """
    Creates a .axfs file with the positions for every time step
    
    Parameters:
        positions: array(array)
            positions of every atom, in angstrom
        step: int
            step of the simulation
        directory: string
            Directory where the file is going to be saved without the last bar.
            The default is where the output folder file is.
        n_at: int
            Total number of atoms
            
    """
    append_new_line(direc + '/positions.axsf', 'PRIMCOORD         {}'.format(step))
    append_new_line(direc + '/positions.axsf', '       {}         1'.format(n_at))

    for i in positions:
        append_new_line(direc + '/positions.axsf', '        {}    {:.5f}    {:.5f}    {:.5f}'.format(18, i[0], i[1], i[2]))
    
    

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
        
