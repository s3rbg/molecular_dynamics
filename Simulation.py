#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 16:01:22 2021

@author: dgiron
"""
# Input imports
from read_parameters.read_data_file import read_data_txt
from read_parameters.read_data_gui import create_gui
from read_parameters.check_input_errors import check_type

# Initialization imports
from init.initialize import initialize

# Potential calculation imports

# ODE solving imports
from solve_ode.ode_algorithms import verlet, velocity_verlet, leap_frog

# Other imports
from common_modules.imports import *
from common_modules.units_dicts import *
from common_modules.errors import InputError

#Total simulation time. Añadir opciones para los 
# demas parametros

# uses eV, ang, g/cm3, K

k = 8.62e-5 # eV * K

how_many_units = 4 # starting from end. How many elements of the list are units

class simulation():
    def __init__(self, data_file):
        if not data_file:
            df = create_gui()
        else:
            df = read_data_txt(data_file)
            
        units = df.iloc[:, -how_many_units:]
        try:
            self.density = float(df['density'].iloc[0]) * density_units[units.iloc[:, 0].item()]
            self.n_cells = int(df['number_of_units'].iloc[0]) # IF N is float uses closest integer
            
            self.cell_type = df['cell_type'].iloc[0]
            self.potential_type = df['potential_type'].iloc[0]
            self.algo_ode = df['algo_ode'].iloc[0]
            self.vels_dist = df['velocities_dist'].iloc[0]
            
            self.tot_t = float(df['tot_t'].iloc[0])
            self.delta_t = float(df['delta_t'].iloc[0])
            
            # Parameters Verlet-Lennard
            if self.potential_type == 'lennard-jones':
                self.sigma = float(df['sigma'].iloc[0]) * distance_units[units.iloc[:, 1].item()]
                self.epsilon =  float(df['epsilon'].iloc[0]) * energy_units[units.iloc[:, 2].item()]
    
            self.cutoff_distance = float(df['cutoff_distance'].iloc[0])
            self.cutoff_list = float(df['cutoff_list'].iloc[0])
            a = float(df['temperature'].iloc[0])
        
        except ValueError:
            check_type(df)
            
        
        self.temperature = float(self.transform_to_kelvin(float(df['temperature'].iloc[0]), df['temperature_units'].iloc[0]))      
        self.n_at = number_atoms_cell[self.cell_type]
            
        self.reduced_density = self.density * self.sigma ** 3
        self.reduced_temperature = k * self.temperature/self.epsilon
                
        self.lattice_constant = self.get_constant()
         
    def transform_to_kelvin(self, temp, unit):
        if unit == 'celsius' or unit == 'c':
            return 273.15 + temp
        elif unit == 'fahrenheit' or unit == 'f':
            return (temp - 32) * 5/9 + 273.15
        else:
            return temp

    def get_constant(self):
        """
        Units of sigma

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return (self.n_at/self.reduced_density) ** 1/3


    def simulate(self):
        
        # Initialize cosas
        
        positions, velocities = initialize(self.reduced_temperature, self.n_cells, self.sigma, self.lattice_constant)

        # Solve ode
        # step = 0
        
        # if self.algo_ode == 'velocity-verlet':
        #     f = velocity_verlet
        # while step <= self.tot_t:
        #     positions, velocities, accelerations = f(positions, velocities, accelerations, self.n_at, self.delta_t, self.cutoff_list)
        #     step = step + self.delta_t
    
    def get_parameters(self):
        
        return {'density':self.density, 'number_of_units':self.n_cells, 'epsilon':self.epsilon, 
                'temperature':self.temperature, 'cell_type':self.cell_type, 'potential_type':self.potential_type,
                'algo_ode':self.algo_ode, 'tot_t':self.tot_t, 'delta_t':self.delta_t, 'sigma':self.sigma,
                'cutoff_distance':self.cutoff_distance, 'cutoff_list':self.cutoff_list, 'vel_dist':self.vels_dist, 
                'reduced_density':self.reduced_density, 'reduced_temperature':self.reduced_temperature,
                'lattice_constant (sigma units)': self.lattice_constant}
    
