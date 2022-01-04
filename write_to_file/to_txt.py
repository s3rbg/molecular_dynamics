#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:43:44 2022

@author: dgiron
"""

from common_modules.imports import *

def energy_to_txt(kinetic, potential, direc):
    append_new_line(direc + '/energy_each_step.txt', '{:.2f}, {:.2f}, {:.2f}'.format(kinetic, potential, kinetic+potential))
    
    
def positions_to_txt(position, direc):
    append_new_line(direc + '/positions_each_step.txt', ' ')

    for i, j, k in zip(position[:, 0], position[:, 1], position[:, 2]):
        append_new_line(direc + '/positions_each_step.txt', '{:.2f}, {:.2f}, {:.2f}'.format(i, j, k))

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
        
