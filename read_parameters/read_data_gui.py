#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 00:20:17 2021

@author: dgiron
"""

# Mejorar la descripcion
from read_parameters.lectura_modified import Lectura
from read_parameters.lennard_verlet import read_lennard_verlet_parameters
from read_parameters.check_input_errors import check_type_gui
from common_modules.imports import *
from common_modules.units_dicts import *
from common_modules.errors import InputError



density_units = list(density_units_upp.keys())
cell_types = list(number_atoms_cell_upp.keys())

def create_gui():
    
    
    # Step 1: create an object of the "Lectura" class
    lec = Lectura("Initial values")

    # Step 2: create the conditions for the initial entries

    lec.crea_entrada('Density of the material', "Density", 0.09e-3)
    lec.crea_entrada('Number of cells inside the supercell in one direction', "Number of cells", 3)
    lec.crea_entrada('Temperature of the system', "Temperature", 20)
    lec.crea_entrada('Total simulation steps', "Max steps", 1000)
    lec.crea_entrada('Step for each simulation', "Step", 0.001)
    lec.crea_entrada('Directory for the output files. Last bar is included', "Directory", 'output')
    
    lec.crea_combo('Type of cubic cell', 'Cell type', cell_types)
    lec.crea_combo('Two body potential to be used', 'Potential type', potential_types_upp)
    lec.crea_combo('ODE solving algorithm to be used', 'ODE algorithm', ode_algos_upp)
    lec.crea_combo('Velocities distribution model', 'Velocities distribution', vels_dist_upp)

    lec.crea_combo('Units of density' , 'Density units', density_units, default=False, clmn=2, rw=0, wdth=10)
    lec.crea_combo('Units of temperature', 'Temp units', temperature_units_upp, default=False, clmn=2, rw=2, wdth=10)
    # Wait until user fills the entries
    lec.espera()
    
    # Read the values
    
    # Read the float values
    try:
        density = lec.lee_float("Density")
        n_cells = lec.lee_int("Number of cells")
        temperature = lec.lee_float("Temperature")
        tot_t = lec.lee_int('Max steps')
        delt_t = lec.lee_float('Step')
    except ValueError:
        check_type_gui(lec)
    # Read the string values
    
    density_unit = lec.lee_string('Density units')    
    temperature_unit = lec.lee_string('Temp units')
    cell_type = lec.lee_string('Cell type')
    potential_type = lec.lee_string('Potential type')
    algo_ode = lec.lee_string('ODE algorithm')
    vels_dist = lec.lee_string('Velocities distribution')
    directory = lec.lee_string('Directory')
    
    # Check if output path exists
    if not os.path.exists(directory):
        print('Output path provided does not exists. Using default fordel for output file')
        directory = 'output'
    
    
    lec.destruye()
    
    lec2 = Lectura('Specific parameters')
    
    # Group of algorithms with the same parameters to be inputed
    verlet_algos = ['velocity-verlet', 'verlet', 'leap-frog']
    lj_algos = ['lennard-jones', 'lennard-jones double shifted']

    # Conditions to introduce different parameters
    if potential_type in lj_algos and algo_ode in verlet_algos:
        sigma, sigma_unit, epsilon, epsilon_unit, cutoff_distance, cutoff_list = read_lennard_verlet_parameters(lec2)
        
        data = np.array([density, n_cells, epsilon, temperature, cell_type, potential_type, 
                         algo_ode, tot_t, delt_t, sigma, cutoff_distance, cutoff_list, vels_dist, directory, density_unit, sigma_unit,
                         epsilon_unit, temperature_unit])

        df = pd.DataFrame(data, index=keywords)
        df = df.T
        return df
    
    # Meter mas condiciones con los nuevos inputs 
    
    else:
        raise InputError('Those selections are not programmed yet')
    


