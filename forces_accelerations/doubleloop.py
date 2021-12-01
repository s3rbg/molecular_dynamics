import numpy as np

from forces_accelerations.Lennard_Jones.force import *
from forces_accelerations.Lennard_Jones.kinetic import *
from forces_accelerations.Lennard_Jones.potential import *
from forces_accelerations.Lennard_Jones_shifted.force_s import *
from forces_accelerations.Lennard_Jones_shifted.potential_s import *
from forces_accelerations.neighbour_list.verlet_list import *
from forces_accelerations.doubleloop_direc.boltzman_temperature import *


def doubleloop(sigma, type_potential, point, lista, Nat, atoms, vel, nf, LATCON, epsilon, rc):
    """
    

    Parameters
    ----------
    sigma : float
        the parameter sigma of the leonard-jones otential
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
    lATCON( laticeconstant) : float
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
    print(point)
    print(len(lista))
    BOXL=(nf*LATCON)/sigma 
    fuerza=0*np.copy(atoms)
    potencial = np.zeros(Nat)
    cinetica= np.zeros(Nat)
    total= np.zeros(Nat)
    if type_potential == 'lennard-jones':

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
                for x in range(3):
                    d = position[x]-position_neig[x]
                    fuerza[iat][x]=fuerza[iat][x] + force_lj(sigma, epsilon, d, rc)
                    fuerza[J][x]=fuerza[J][x] - force_lj(sigma, epsilon, d, rc)
            
                potencial[iat]= potencial[iat] + potential_lj(sigma, epsilon, rel_dis, rc)
                potencial[J]= potencial[J] + potential_lj(sigma, epsilon, rel_dis, rc)
                
            cinetica[iat]= cinetica[iat] + kinetic(vel[iat]) 
        total = cinetica + potencial
        
    elif type_potential == 'lennard-jones double shifted':
        
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
                rel_pos = rel_pos - np.round(rel_pos/BOXL,1)*BOXL #rel_pos=relative position with the iat atom: R(j)=r(j)-position
                rel_dis, theta, phi = to_spherical(rel_pos[0], rel_pos[1], rel_pos[2])

                force = force_lj_shifted(sigma, epsilon, rel_dis, rc) 

                for x in range(3):
                    fuerza[iat][x]=fuerza[iat][x] + coords[x]
                    fuerza[J][x]=fuerza[J][x] - coords[x]

                potencial[iat]= potencial[iat] + potential_lj_shifted(sigma, epsilon, rel_dis, rc)
                potencial[J]= potencial[J] + potential_lj_shifted(sigma, epsilon, rel_dis, rc)
            cinetica[iat]= cinetica[iat] + kinetic(vel[iat])
        total = cinetica + potencial
    else:
        print('wrong tipe of potential')     
    return (np.array(fuerza), potencial, cinetica, total)   

