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
        the function resturns for arrays one with the forces, another one with the
        potential energy, another one with the kinetic energy and lastly the total energy
        of each atom
    """
    BOXL=(nf*LATCON)/sigma 
    fuerza=0*np.copy(atoms)
    potencial = np.zeros(Nat)
    cinetica= np.zeros(Nat)
    total= np.zeros(Nat)
    
    if type_potential == 'lennard-jones double shifted':
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
                rel_dis = np.sqrt( rel_pos[0]**2 + rel_pos[1]**2 + rel_pos[2]**2 )
                
                theta = np.arccos(rel_pos[2]/rel_dis)
                phi = np.arctan2(rel_pos[1], rel_pos[0])
                
                mod_fuerza = force_lj_shifted(sigma, rel_dis, rc)

                fuerza_x = mod_fuerza * np.cos(phi) * np.sin(theta)
                fuerza_y = mod_fuerza * np.sin(phi) * np.sin(theta)
                fuerza_z = mod_fuerza * np.cos(theta)
                
                array_fuerza = np.array([fuerza_x, fuerza_y, fuerza_z])
                for x in range(3):
                    fuerza[iat][x]=fuerza[iat][x] + array_fuerza[x]
                    fuerza[J][x]= fuerza[J][x] - array_fuerza[x]

                aux = potential_lj_shifted(sigma, rel_dis, rc)
                potencial[iat]= potencial[iat] + aux
                potencial[J]= potencial[J] + aux
            cinetica[iat]= cinetica[iat] + kinetic(vel[iat])
        cinetica = np.sum(cinetica)
        potencial = np.sum(potencial)
    elif type_potential == 'lennard-jones':

        for iat in range(Nat):
            position = atoms[iat]
            JBEG=point[iat]
            JEND=point[iat+1]-1
            if JEND<JBEG:
                return print('last neighbour atom lower than first')
            for jneig in range(JBEG,JEND):
                J=lista[jneig]
                position_neig=atoms[J]
                rel_pos = position-position_neig
                rel_pos = rel_pos - np.round(rel_pos/BOXL,1)*BOXL #rel_pos=relative position with the iat atom: R(j)=r(j)-position
                rel_dis = np.sqrt( rel_pos[0]**2 + rel_pos[1]**2 + rel_pos[2]**2 )
                
                mod_fuerza = force_lj(sigma, rel_dis, rc)

                fuerza_x = mod_fuerza * np.cos(phi) * np.sin(theta)
                fuerza_y = mod_fuerza * np.sin(phi) * np.sin(theta)
                fuerza_z = mod_fuerza * np.cos(theta)
                
                array_fuerza = np.array([fuerza_x, fuerza_y, fuerza_z])
                for x in range(3):
                    fuerza[iat][x]=fuerza[iat][x] + array_fuerza[x]
                    fuerza[J][x]= fuerza[J][x] - array_fuerza[x]
            
                potencial[iat]= potencial[iat] + potential_lj(sigma, epsilon, rel_dis, rc)
                potencial[J]= potencial[J] + potential_lj(sigma, epsilon, rel_dis, rc)
                
                aux = potential_lj(sigma, rel_dis, rc)
                potencial[iat]= potencial[iat] + aux
                potencial[J]= potencial[J] + aux
                
            cinetica[iat]= cinetica[iat] + kinetic(vel[iat]) 
        total = cinetica + potencial
        
        
    else:
        print('wrong tipe of potential') 
    print(cinetica+potencial)
    energy_to_txt(cinetica, potencial, direc)
    return fuerza, potencial, cinetica