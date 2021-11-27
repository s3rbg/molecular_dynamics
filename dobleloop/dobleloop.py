import numpy as np

def dobleloop(sigma, type_potential, point, lista, Nat, atoms, vel, nf, LATCON):
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
    BOXL=(nf*LATCON)/sigma 
    fuerza=0*np.copy(atoms)
    potencial = np.zeros(Nat)
    cinetica= np.zeros(Nat)
    total= np.zeros(Nat)
    if type_potential == 'lj':

        for iat in range(1,Nat):
            position = atoms[iat]
            JBEG=point[iat]
            JEND=point[iat+1]-1
            if JEND<JBEG:
                return print('last neighbour atom lower than first')
            for jneig in range(JBEG,JEND):
                J=lista[jneig]
                position_neig=atoms[J]
                rel_pos = position-position_neig
                rel_pos = rel_pos - round(rel_pos/BOXL,1)*BOXL #rel_pos=relative position with the iat atom: R(j)=r(j)-position
                rel_dis = np.sqrt( rel_pos[1]^2 + rel_pos[2]^2 + rel_pos[3]^2 )
                for x in range(1,4):
                    d = position[x]-position_neig[x]
                    fuerza[iat][x]=fuerza[iat][x] + force_lj(sigma, d)
                    fuerza[jneig][x]=fuerza[jneig][x] - force_lj(sigma, d)
            
                potencial[iat]= potencial[iat] + potential_lj(sigma, rel_dis)
                potencial[J]= potencial[J] + potential_lj(sigma, rel_dis)
                
            cinetica[iat]= cinetica[iat] + kinetic(vel[iat]) 
        total = cinetica + potencial
        
    elif type_potential == 'lj_shifted':
        
        for iat in range(1,Nat):
            position = atoms[iat]
            JBEG=point[iat]
            JEND=point[iat+1]-1
            if JEND<JBEG:
                return print('last neighbour atom lower than first')
            for jneig in range(JBEG,JEND):
                J=lista[jneig]
                position_neig=atoms[J]
                rel_pos = position-position_neig
                rel_pos = rel_pos - round(rel_pos/BOXL,1)*BOXL #rel_pos=relative position with the iat atom: R(j)=r(j)-position
                rel_dis = np.sqrt( rel_pos[1]^2 + rel_pos[2]^2 + rel_pos[3]^2 )
                for x in range(1,4):
                    d = position[x]-position_neig[x]
                    fuerza[iat][x]=fuerza[iat][x] + force_lj_shifted(sigma, d)
                    fuerza[jneig][x]=fuerza[jneig][x] - force_lj_shifted(sigma, d)
            
                potencial[iat]= potencial[iat] + potential_lj_shifted(sigma, rel_dis)
                potencial[J]= potencial[J] + potential_lj_shifted(sigma, rel_dis)
                
            cinetica[iat]= cinetica[iat] + kinetic(vel[iat])
        total = cinetica + potencial
        
    else:
        print('wrong tipe of potential')     
        
    return (fuerza, potencial, cinetica, total)    
