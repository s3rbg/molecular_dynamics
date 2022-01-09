#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 15:25:50 2021

@author: dgiron
"""

from common_modules.imports import *

from forces_accelerations.doubleloop import doubleloop 
from forces_accelerations.neighbour_list.verlet_list import list_neighbour
from forces_accelerations.Lennard_Jones_shifted.kinetic import kinetic

# Functions to save calculated variables in txt files
from write_to_file.to_txt import energy_to_txt


def velocity_verlet(positions, velocities, accelerations, old_neigh_point, old_neigh_list, displacements, n_at, delta_t, cutoff_for_disp, cutoff_for_neigh,
                    potential_type, number_of_cells, lat_con, sigma, epsilon, direc, save=True):
    """
    Compute the t+delta t positions, velocities, accelerations, neighbours and displacements

    Parameters
    ----------
    positions : array(array)
        initial positions
    velocities :  array(array)
        initial velocities
    accelerations :  array(array)
        initial accelerations
    old_neigh_point : array
        initial neighbour list (POINT).
    old_neigh_list : array
        initial neighbour list (LIST).
    displacements : array
        displacements from the previous step. 
    n_at : int
        total number of atoms.
    delta_t : float
        reduced time step.
    cutoff_for_disp : float
        cutoff used to compute the neighbour list.
    cutoff_for_neigh : float
        cutoff that limits the potential.
    potential_type : str
        type of potential used.
    number_of_cells : int
        number of cells in each direction.
    lat_con : float
        lattice constant, in units of sigma.
    sigma : float
        sigma parameter.
    epsilon : float
        epsilon parameter.
    direc : str
        directory to save the calculated positions and energies
        
    Returns
    -------
    positions : array(array)
        new positions.
    velocities : array(array)
        new velocities.
    accelerations : array(array)
        new accelerations.
    neigh_point : array
        new neighbour list (POINT).
    neigh_list : array
        new neighbour list (LIST).
    displacements : array
        new array with displacements for each atom.
    save : bool (optional)
        if False, energies are not saved in a file. Designed to avoid saving the v(t+delta t/2) energy
        in leap frog algorithm

    """
    initial_positions = positions  # Save initial positions to compute the displacements
    
    positions = positions*sigma + velocities * delta_t + 0.5 * accelerations * delta_t ** 2
    inter_velocities = velocities + 0.5 * accelerations * delta_t
    
    # Compute displacements
    displacements = displacements + np.abs([aux((i*sigma-j)) for i, j in zip(initial_positions, positions)])
    disp_sorted = np.sort(displacements)
    
    # Choose to compute a new neighbour list (or not)
    if disp_sorted[-1] + disp_sorted[-2] >= (cutoff_for_disp-cutoff_for_neigh):
        neigh_point, neigh_list = list_neighbour(sigma, lat_con, n_at, number_of_cells, cutoff_for_disp, positions/sigma)
        displacements = 0
    else:
        neigh_point = old_neigh_point
        neigh_list = old_neigh_list

    # Compute accelerations and potential energy
    accelerations, potential = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                           n_at, positions/sigma, velocities, number_of_cells, 
                                           lat_con, epsilon, cutoff_for_neigh, direc)
    # Final velocities
    velocities = inter_velocities + 0.5 * accelerations * delta_t
    
    # Kinetic energy
    if save:
        kin = np.sum([kinetic(i) for i in velocities])
        energy_to_txt(kin, potential, direc)

    return positions/sigma, velocities, accelerations, neigh_point, neigh_list, displacements

def leap_frog(positions, velocities, accelerations, old_neigh_point, old_neigh_list, displacements, n_at, delta_t, cutoff_for_disp, cutoff_for_neigh, 
              potential_type, number_of_cells, lat_con, sigma, epsilon, direc):
    
    initial_positions = positions # Save initial positions to compute the displacements
    
    inter_velocities = velocities + accelerations * delta_t
    positions = positions*sigma + inter_velocities * delta_t
    
    velocities_current = (inter_velocities + velocities) / 2
    
    # Compute new accelerations
    displacements = displacements + np.abs([aux((i*sigma-j)) for i, j in zip(initial_positions, positions)])
    disp_sorted = np.sort(displacements)
    
    # Compute new accelerations
    if disp_sorted[-1] + disp_sorted[-2] >= (cutoff_for_disp-cutoff_for_neigh):
        neigh_point, neigh_list = list_neighbour(sigma, lat_con, n_at, number_of_cells, cutoff_for_disp, positions/sigma)
        displacements = 0
    else:
        neigh_point = old_neigh_point
        neigh_list = old_neigh_list


    accelerations, potential = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                           n_at, positions/sigma, inter_velocities, number_of_cells, 
                                           lat_con, epsilon, cutoff_for_neigh, direc)

    kin = np.sum([kinetic(i) for i in velocities_current])
    energy_to_txt(kin, potential, direc)
    
    return positions/sigma, inter_velocities, accelerations, neigh_point, neigh_list, displacements


def verlet(positions, old_positions, velocities, accelerations, old_neigh_point, old_neigh_list, displacements,
           n_at, delta_t, cutoff_for_disp, cutoff_for_neigh, potential_type, number_of_cells, lat_con, sigma, epsilon, direc): # Here f(t) always
    
    initial_positions = positions # Save initial positions to compute the displacements
    
    
    positions = 2 * positions*sigma - old_positions*sigma + accelerations * delta_t ** 2 # Next step
    
    velocities = (positions - old_positions*sigma) / (2 * delta_t) # Next step
    
     # Compute new accelerations
    displacements = displacements + np.abs([aux((i*sigma-j)) for i, j in zip(initial_positions, positions)])
    disp_sorted = np.sort(displacements)
    
    if disp_sorted[-1] + disp_sorted[-2] >= (cutoff_for_disp-cutoff_for_neigh):
        neigh_point, neigh_list = list_neighbour(sigma, lat_con, n_at, number_of_cells, cutoff_for_disp, positions/sigma)
        displacements = 0
    else:
        neigh_point = old_neigh_point
        neigh_list = old_neigh_list
        
    accelerations, potential = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                               n_at, positions/sigma, velocities, number_of_cells, 
                                               lat_con, epsilon, cutoff_for_neigh, direc)

    kin = np.sum([kinetic(i) for i in velocities])
    energy_to_txt(kin, potential, direc)
    
    return positions/sigma, initial_positions, velocities, accelerations, neigh_point, neigh_list, displacements
    
    
def aux(x):
    return np.sqrt(x[0]**2 + x[1]**2 + x[2]**2)
    
    
    
    

