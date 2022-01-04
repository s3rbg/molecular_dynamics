#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 15:25:50 2021

@author: dgiron
"""

from common_modules.imports import *

from forces_accelerations.doubleloop import doubleloop 
from forces_accelerations.neighbour_list.verlet_list import list_neighbour

from write_to_file.to_txt import positions_to_txt

# from output.save_text_file import to_txt # Cambiar por nombre real

# Calcular energias en el de alain

def velocity_verlet(positions, velocities, accelerations, old_neigh_point, old_neigh_list, n_at, delta_t, cutoff_for_disp, cutoff_for_neigh,
                    potential_type, number_of_cells, lat_con, sigma, epsilon, direc):
    # Sustituir con el nombre de la funcion real
    initial_positions = positions # Save initial positions to compute the displacements

    positions = positions + velocities * delta_t + 0.5 * accelerations * delta_t ** 2
    inter_velocities = velocities + 0.5 * accelerations * delta_t
    
    # Compute new accelerations
    displacements = np.abs([aux(i[0], i[1], i[2]) - aux(j[0], j[1], j[2])  
                            for i, j in zip(initial_positions, positions)])
    
    if max(displacements) >= cutoff_for_disp/sigma:
        neigh_point, neigh_list = list_neighbour(sigma, lat_con, n_at, number_of_cells, cutoff_for_neigh, positions)
        accelerations = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                  n_at, positions, velocities, number_of_cells, lat_con, epsilon, cutoff_for_neigh, direc)[0]
    else:
        neigh_point = old_neigh_point
        neigh_list = old_neigh_list
        accelerations = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                   n_at, positions, velocities, number_of_cells, 
                                   lat_con, epsilon, cutoff_for_neigh, direc)[0]
    velocities = inter_velocities + 0.5 * accelerations * delta_t
    
    positions_to_txt(positions, direc) # Save in a text file the new coordinates
    return positions, velocities, accelerations, neigh_point, neigh_list

def leap_frog(positions, velocities, accelerations, old_neigh_point, old_neigh_list, n_at, delta_t, cutoff_for_disp, cutoff_for_neigh, 
              potential_type, number_of_cells, lat_con, sigma, epsilon, direc):
    
    initial_positions = positions # Save initial positions to compute the displacements
    
    inter_velocities = velocities + accelerations * delta_t
    positions = positions + inter_velocities * delta_t
    
    velocities = (inter_velocities + velocities) / 2
    
    # Compute new accelerations
    displacements = np.abs([aux(i[0], i[1], i[2]) - aux(j[0], j[1], j[2]) 
                            for i, j in zip(initial_positions, positions)])
    
    if max(displacements) >= cutoff_for_disp/sigma:
        neigh_point, neigh_list = list_neighbour(sigma, lat_con, n_at, number_of_cells, cutoff_for_neigh)
        accelerations = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                  n_at, positions, velocities, number_of_cells, lat_con, epsilon, cutoff_for_neigh, direc)
    else:
        neigh_point = old_neigh_point
        neigh_list = old_neigh_list
        accelerations, potential, kinetic, total = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                                              n_at, positions, velocities, number_of_cells, 
                                                              lat_con, epsilon, cutoff_for_neigh, direc)
    positions_to_txt(positions, direc) # Save in a text file the new coordinates

    return positions, velocities, accelerations, neigh_point, neigh_list


def verlet(positions, old_positions, velocities, accelerations, old_neigh_point, old_neigh_list, 
           n_at, delta_t, cutoff_for_disp, cutoff_for_neigh, potential_type, number_of_cells, lat_con, sigma, epsilon, direc): # Here f(t) always
    
    initial_positions = positions # Save initial positions to compute the displacements
    
    
    positions = 2 * positions - old_positions + accelerations * delta_t ** 2 # Next step
    
    velocities = (positions - old_positions) / (2 * delta_t ** 2) # Next step
    
    # Compute new accelerations
    displacements = np.abs([aux(i[0], i[1], i[2]) - aux(j[0], j[1], j[2]) 
                            for i, j in zip(initial_positions, positions)])
    
    if max(displacements) >= cutoff:
        neigh_point, neigh_list = list_neighbour(sigma, lat_con, n_at, number_of_cells, cutoff_for_neigh)
        accelerations = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                  n_at, positions, velocities, number_of_cells, lat_con, epsilon, cutoff_for_neigh, direc)
    else:
        neigh_point = old_neigh_point
        neigh_list = old_neigh_list
        accelerations, potential, kinetic, total = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                                              n_at, positions, velocities, number_of_cells, 
                                                              lat_con, epsilon, cutoff_for_neigh, direc)
    
    positions_to_txt(positions, direc) # Save in a text file the new coordinates

    return positions, velocities, accelerations, neigh_point, neigh_list
    
    
def aux(x, y, z):
    return np.sqrt(x**2 + y**2 + z**2)
    
    
    
    

