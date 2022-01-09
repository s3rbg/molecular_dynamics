import numpy as np

from forces_accelerations.Lennard_Jones.force import *
from forces_accelerations.Lennard_Jones.kinetic import *
from forces_accelerations.Lennard_Jones.potential import *
from forces_accelerations.Lennard_Jones_shifted.force_s import *
from forces_accelerations.Lennard_Jones_shifted.potential_s import *
from forces_accelerations.neighbour_list.verlet_list import *
from forces_accelerations.doubleloop_direc.boltzman_temperature import *

from write_to_file.to_txt import energy_to_txt


def doubleloop(sigma, type_potential, point, lista, Nat, atoms, vel, nf, LATCON, epsilon, rc, direc):
    """
    Accelerations and total potential energy for the given positions of the atoms.
    
    Parameters
    ----------
    sigma : float
        the parameter sigma of the lennard-jones otential
    type_potential : string
        the variable contains the type of potential to implement
    point : list
        the list POINT of the function neighbour list(contains the indices of the neighbours
                                                      in the list LIST)
    lista : list
        the list LIST of the function neighbour list(contains the number of the neighbours)
    Nat : int
        the total number of atoms 
    atoms : array
        an array with the positions of the atoms
    vel : array
        an array with the velocities of the atoms
    LATCON (lattice constant) : float
        latice constant of the fcc cell
    nf (nfcc) : int
        the number of fcc unit cells in a supercell
        
    Returns  (fuerza, potencial, cinetica, total)
    -------
    TYPE
        the function returns an arrays  with the forces and the
        potential energy of the system
    """
    BOXL=(nf*LATCON)/sigma 
    force=0*np.copy(atoms)
    potential = np.zeros(Nat)    
            
    for iat in range(Nat-1):
        position = atoms[iat]
        JBEG=point[iat]
        if iat != Nat-2:           
            JEND=point[iat+1]
        else:
            JEND = len(lista)
        if JEND<JBEG:
            return print('last neighbour atom lower than first')
        for jneig in range(JBEG,JEND):
            J=lista[jneig]
            position_neig=atoms[J]
            rel_pos = position-position_neig
            rel_pos = rel_pos - np.round(rel_pos/BOXL, 0)*BOXL #rel_pos=relative position with the iat atom: R(j)=r(j)-position
            
            # Transform distances in cartesian to spherical
            rel_dis = np.sqrt( rel_pos[0]**2 + rel_pos[1]**2 + rel_pos[2]**2 )
            theta = np.arccos(rel_pos[2]/rel_dis)
            phi = np.arctan2(rel_pos[1], rel_pos[0]) # Special arctan, that takes into account the cuadrant.
            
            if type_potential == 'lennard-jones double shifted':
                mod_force = force_lj_shifted(sigma, rel_dis, rc)
            
            elif type_potential == 'lennard-jones':
                mod_force = force_lj(sigma, rel_dis, rc)
            
            # Once the force is calculated, it is transformed back to cartesian
            force_x = mod_force * np.cos(phi) * np.sin(theta)
            force_y = mod_force * np.sin(phi) * np.sin(theta)
            force_z = mod_force * np.cos(theta)
            
            array_force = np.array([force_x, force_y, force_z])
            for x in range(3):
                force[iat][x]=force[iat][x] + array_force[x]
                force[J][x]= force[J][x] - array_force[x]

            potential[iat]= potential[iat] + potential_lj_shifted(sigma, rel_dis, rc)
    potential = np.sum(potential)
        
    return force, potential