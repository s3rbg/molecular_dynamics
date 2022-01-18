#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 15:58:24 2021

@author: dgiron
"""

from Simulation import *
from common_modules.errors import *
import argparse
import os

from read_parameters.lectura_modified import Lectura
from read_parameters.lennard_verlet import read_lennard_verlet_parameters
from read_parameters.check_input_errors import check_type_gui
from common_modules.imports import *
from common_modules.units_dicts import *
from common_modules.errors import InputError

    
def main(): 
    
    lec = Lectura('input')
    lec.crea_label('Welcome to the molecular dynamics simulator!', 1, 0)
    lec.crea_combo('Select a way to introduce the data', 'Select the input', ['GUI', 'Data file'],
                   clmn=1, rw=1, last=True)
    lec.espera()

    data_file = lec.lee_string('Select the input')
    lec.destruye()

    if data_file == 'data file':
        lec = Lectura('read_route')
        lec.crea_entrada('Select a the path to the input file', 'Route', 'data.txt')
        lec.espera()

        route = lec.lee_string('Route')

        lec.destruye()
    else:
        route = False
    
    sim = simulation(route)
    
    
    sim.simulate()    
    del sim

main()

