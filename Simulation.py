#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 16:01:22 2021

@author: dgiron
"""
# Input imports
from read_parameters.read_data_gui import create_gui
from read_parameters.read_data_file import read_data_txt
from read_parameters.check_input_errors import check_type

# Initialization imports
from init.initialize import initialize

# Potential calculation imports
from forces_accelerations.doubleloop import doubleloop 
from forces_accelerations.neighbour_list.verlet_list import list_neighbour
from forces_accelerations.Lennard_Jones_shifted.kinetic import kinetic
from forces_accelerations.Lennard_Jones_shifted.potential_s import potential_lj_shifted

# ODE solving imports
from solve_ode.ode_algorithms import verlet, velocity_verlet, leap_frog

# Output writing functions
from write_to_file.to_txt import positions_to_txt, energy_to_txt, append_new_line

# Other imports
from common_modules.imports import *
from common_modules.units_dicts import *
from common_modules.errors import InputError, PackageError

k = 8.63125e-5 # eV * K

how_many_units = 4 # starting from end. How many elements of the list are units

class simulation(): 
    def __init__(self, data_file):
        
        try:
            import tqdm
        except:
            raise PackageError('Needed package "tqdm" is not installed. For installation type:'+ 
                '"conda install -c conda-forge tqdm" in the shell/Anaconda prompt')
            
        if not data_file:
            df = create_gui()
        else:
            df = read_data_txt(data_file)
            
        units = df.iloc[:, -how_many_units:]
        # Save the parameters as attributes and check if their type is correct
        try:
            self.density = float(df['density'].iloc[0]) * density_units[units.iloc[:, 0].item()]
            self.n_cells = int(df['number_of_units'].iloc[0]) # IF N is float uses closest integer
            
            self.cell_type = df['cell_type'].iloc[0]
            self.potential_type = df['potential_type'].iloc[0]
            self.algo_ode = df['algo_ode'].iloc[0]
            self.vels_dist = df['velocities_dist'].iloc[0]
          
            
            self.delta_t = float(df['delta_t'].iloc[0])    
            self.tot_t = float(df['tot_t'].iloc[0])
            
            # Specific parameters of Lennard-Jones potential
            if self.potential_type == 'lennard-jones double shifted' or self.potential_type == 'lennard-jones':
                self.sigma = float(df['sigma'].iloc[0]) * distance_units[units.iloc[:, 1].item()]
                self.epsilon =  float(df['epsilon'].iloc[0]) * energy_units[units.iloc[:, 2].item()]
            
            self.cutoff_distance = float(df['cutoff_distance'].iloc[0])
            self.cutoff_list = float(df['cutoff_list'].iloc[0])
        
        except ValueError:
            check_type(df)
            
        self.directory = df['directory'].iloc[0]

        self.temperature = float(self.transform_to_kelvin(float(df['temperature'].iloc[0]), df['temperature_units'].iloc[0]))      
        self.n_at = number_atoms_cell[self.cell_type]
        
        self.reduced_density = self.density * (self.sigma * 10**-7) ** 3
        self.reduced_temperature = k * self.temperature/self.epsilon
                
        self.lattice_constant = self.get_constant() * self.sigma
        
        # Create the output folder if it is deleted
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)


    def simulate(self):
        """
        Computes the simulation for the number of steps given as atributte. Saves
        the energy and the positions for every time steps in different files, saved in
        the folder given as atributte.

        Returns
        -------
        None.

        """
        
        # Initialize positions/velocities
        positions, velocities = initialize(self.reduced_temperature, self.n_cells, self.sigma, self.lattice_constant, self.directory)

        # Create data files to store the data. If the files exist, they are removed.
        energy_file_name = self.directory + '/energy_each_step.txt'
        positions_file_name = self.directory + '/positions.axsf'

        if os.path.exists(energy_file_name):
            os.remove(energy_file_name)
            
        if os.path.exists(positions_file_name):
            os.remove(positions_file_name)
            

        # Create the headers for the files
        append_new_line(energy_file_name, 'Kinetic, Potential, Total')
        
        # Length of the supercell in Angstrom
        len_supercell = self.lattice_constant * 10 * self.n_cells
        
        append_new_line(positions_file_name, 'ANIMSTEPS       {}'.format(int(self.tot_t + 1)))
        append_new_line(positions_file_name, 'CRYSTAL')
        append_new_line(positions_file_name, 'PRIMVEC')
        append_new_line(positions_file_name, '    {:.5f}     {:.5f}     {:.5f}'.format(len_supercell, 0.0, 0.0))
        append_new_line(positions_file_name, '     {:.5f}    {:.5f}     {:.5f}'.format(0.0, len_supercell, 0.0))
        append_new_line(positions_file_name, '     {:.5f}     {:.5f}    {:.5f}'.format(0.0, 0.0, len_supercell))

            
        # Total number of atoms
        self.n_tot_at = len(positions)
        
        # Save initial positions
        positions_to_txt(positions*self.sigma*10, 1, self.directory, self.n_tot_at)
       
        # Total number of atoms
        
        # Parameters that remain constant in each iteration of the ODE solving algorithm
        common_parameters = (self.n_tot_at, self.delta_t, self.cutoff_list, self.cutoff_distance, 
                             self.potential_type, self.n_cells, self.lattice_constant, self.sigma, self.epsilon, self.directory)
        
        # Initial neighbour list and accelerations. Saves the initial neighbours for each atom
        neigh_point, neigh_list = list_neighbour(self.sigma, self.lattice_constant, self.n_tot_at, self.n_cells, self.cutoff_list, positions, self.directory)
        accelerations, potential = doubleloop(self.sigma, self.potential_type, neigh_point, neigh_list, 
                                  self.n_tot_at, positions, velocities, self.n_cells, self.lattice_constant, self.epsilon, self.cutoff_distance, self.directory)
        
        # Append initial energies in the file
        energy_to_txt(np.sum([kinetic(i) for i in velocities]), potential, self.directory)

        # Solve ode
        displacements = 0
        step = 0
        j = 1 # Counter to name the positions file
        if self.algo_ode == 'velocity-verlet':
            old_parameters = [positions, velocities, accelerations, neigh_point, neigh_list, displacements]
            while step <= self.tot_t*self.delta_t:
                j = j+1 
                old_parameters = velocity_verlet(*old_parameters, *common_parameters)
                step = step + self.delta_t
                positions_to_txt(old_parameters[0] * self.sigma * 10, j, self.directory, self.n_tot_at)

        elif self.algo_ode == 'leap-frog':
            # Calculate v(t + delta_t/2)
            initial_parameters = [positions, velocities, accelerations, neigh_point, neigh_list, displacements,
                                  self.n_tot_at, self.delta_t/2, self.cutoff_list, self.cutoff_distance,
                                  self.potential_type, self.n_cells, self.lattice_constant, self.sigma, self.epsilon, self.directory]

            velocities_half_time = velocity_verlet(*initial_parameters, save=False)[1]
            
            initial_parameters = [positions, velocities, accelerations, neigh_point, neigh_list, displacements,
                                  self.n_tot_at, self.delta_t, self.cutoff_list, self.cutoff_distance,
                                  self.potential_type, self.n_cells, self.lattice_constant, self.sigma, self.epsilon, self.directory]
            
            new_positions, new_velocities, new_accelerations, new_point, new_list, new_disp = velocity_verlet(*initial_parameters, save=False)
            
            
            old_parameters = [new_positions, velocities_half_time, new_accelerations, new_point, new_list, new_disp]
            
            while step <= self.tot_t*self.delta_t:
                j = j+1
                old_parameters = leap_frog(*old_parameters, *common_parameters)
                step = step + self.delta_t
                positions_to_txt(old_parameters[0] * self.sigma * 10, j, self.directory, self.n_tot_at) # Save in a text file the new coordinates

        elif self.algo_ode == 'verlet':
            initial_parameters = [positions, velocities, accelerations, neigh_point, neigh_list, displacements,
                                  self.n_tot_at, self.delta_t, self.cutoff_list, self.cutoff_distance,
                                  self.potential_type, self.n_cells, self.lattice_constant, self.sigma, self.epsilon, self.directory]

            next_step_positions, new_vel, next_step_accelerations, new_point, new_list, new_disp = velocity_verlet(*initial_parameters, save=False)
            # Check if putting the same position on old an new works
            old_parameters = [next_step_positions, positions, velocities, next_step_accelerations, new_point, new_list, new_disp]
            while step <= self.tot_t*self.delta_t:
                j = j+1
                old_parameters = verlet(*old_parameters, *common_parameters)
                step = step + self.delta_t

                positions_to_txt(old_parameters[0] * self.sigma * 10, j, self.directory, self.n_tot_at) # Save in a text file the new coordinates
        self.plot_energy_cons()
        
        
    def transform_to_kelvin(self, temp, unit):
        """
        Transform any of the admitted units to Kelvin

        Parameters
        ----------
        temp : float
            temperature.
        unit : str
            unit.

        Returns
        -------
        temp
            temperature in kelvin.

        """
        if unit == 'celsius' or unit == 'c':
            return 273.15 + temp
        elif unit == 'fahrenheit' or unit == 'f':
            return (temp - 32) * 5/9 + 273.15
        else:
            return temp

    def get_constant(self):
        """
        Calculate the lattice constant, in units of sigma

        Returns
        -------
        lattice_constant
        
        """
        return (self.n_at/self.reduced_density) ** (1/3)
    
    def plot_energy_cons(self):
        """
        Plots a graph with the total energy for every time step

        Returns
        -------
        None.

        """
        
        energy = np.genfromtxt(self.directory + '/energy_each_step.txt', delimiter=',')
        energy = energy[2:]
        total = energy[:, 2]
        mean = np.mean(total)
        
        plt.clf()
        plt.plot(total, 'b-', alpha=0.7, label='Energy/time step')
        plt.plot([0, self.tot_t], [mean, mean], 'r--', label='Mean energy')
        plt.ylim(mean-mean/30, mean+mean/30)
        plt.xlabel('Step number')
        plt.ylabel('Total energy (reduced units)')
        plt.title('Energy conservation')
        plt.grid()
        plt.legend()
        plt.savefig(self.directory+'/energy_conservation_plot.png', dpi=720)
        
    def get_parameters(self):
        """
        Get the parameters of the simulation (to check the input)

        Returns
        -------
        dict
            dictionary with the parameters given to the class.

        """
        
        return {'density':self.density, 'number_of_units':self.n_cells, 'epsilon':self.epsilon, 
                'temperature':self.temperature, 'cell_type':self.cell_type, 'potential_type':self.potential_type,
                'algo_ode':self.algo_ode, 'tot_t':self.tot_t, 'delta_t':self.delta_t, 'sigma':self.sigma,
                'cutoff_distance':self.cutoff_distance, 'cutoff_list':self.cutoff_list, 'vel_dist':self.vels_dist, 
                'reduced_density':self.reduced_density, 'reduced_temperature':self.reduced_temperature,
                'lattice_constant (sigma units)': self.lattice_constant, 'directory': self.directory}
    
        
        
