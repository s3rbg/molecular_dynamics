#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 17:23:12 2021

@author: dgiron
"""

distance_units_upp = {"nm": 1, "m": 10**9,  "mm": 10**6,  "cm": 10**7,  
                  "microm": 10**3, 'Angstrom': 0.1, 'Bohr rad': 0.0529177}

density_units_upp = {"m**-3": 10**-6, "cm**-3": 1}

energy_units_upp = {'J':1/1.6e-19, 'erg': 6.242e+11, 'eV':1, 'cal': 26131936951817052000}

number_atoms_cell_upp = {'FCC': 4}

temperature_units_upp = ('Kelvin', 'Celsius', 'C', 'K', 'F', 'Fahrenheit')

temperature_units_special_upp = ('Kelvin', 'Celsius', 'Fahrenheit')

ode_algos_upp = ('Velocity-Verlet', 'Verlet', 'Leap-Frog')
potential_types_upp = ('Lennard-Jones double shifted', 'Lennard-Jones')
vels_dist_upp = ('M-B', 'Coming soon...')

keywords = ('density', 'number_of_units', 'epsilon', 'temperature',
            'cell_type', 'potential_type', 'algo_ode', 'tot_t', 'delta_t', 'sigma',
            'cutoff_distance', 'cutoff_list', 'velocities_dist', 'directory', 'density_units', 
            'sigma_unit', 'epsilon_units', 'temperature_units')

default_data = [2.1290321e28, 3, 1.654438e-21, 86.4956, 'fcc', 'lennard-jones double shifted', 'velocity-verlet',
                        100, 0.005, 0.341, 2.5, 2.7, 'm-b', 'output', 'm**-3', 'nm', 'j', 'k']

distance_units =  {k.lower(): v for k, v in distance_units_upp.items()}

density_units =  {k.lower(): v for k, v in density_units_upp.items()}

energy_units =  {k.lower(): v for k, v in energy_units_upp.items()}

number_atoms_cell =  {k.lower(): v for k, v in number_atoms_cell_upp.items()}

temperature_units = (i.lower() for i in temperature_units_upp)

ode_algos = (i.lower() for i in ode_algos_upp)

potential_types = (i.lower() for i in potential_types_upp)

vels_dist = (i.lower() for i in vels_dist_upp)