#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 15:58:24 2021

@author: dgiron
"""
# Default units Angstrom, eV, g/cm3

from Simulation import *
from common_modules.errors import *
import argparse
import os

    
def main(): 
    
    parser = argparse.ArgumentParser(description='Runs a simulation of the movement of a solid with a given initial conditions')
    parser.add_argument('--data_file', required=False,
                        help='Input file with requested parameters. If no data file is given, a GUI is displayed.')
    inargs = parser.parse_args()
    data_file = inargs.data_file


    if type(data_file) != None:
       pass
    else:
        data_file = False
    
    
    sim = simulation(data_file)
    
    
    sim.simulate()    
    del sim

main()

