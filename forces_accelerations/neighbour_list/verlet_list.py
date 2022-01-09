import numpy as np
import os

from write_to_file.to_txt import append_new_line

def list_neighbour(sigma, LATCON, nat, nf, rc, atoms, direc=None):
    """
    Calculate the two lists with information about the neighbours of every atom, in
    order to calculate the potential.
    
    Parameters
    ----------
    sigma : float
        parameter sigma of the Lennard-Jons potential
    lATCON( laticeconstant) : float
        latice constant of the fcc cell
    nat (Nat) : int
        the number of atoms in a supercell
    nf (nfcc) : int
        the number of fcc unit cells in a supercell
    atoms : array
        an array wich has the cordenates of each atom
    rl : float
        the cut off distance

    Returns
    -------
    POINT : List
    LIST : List
        
    """
    # If a path is given, it saves the neighbour list in a file (designed to save the initial neigh_list)
    if direc != None:
        if os.path.exists(direc + '/ini_neigh.txt'):
            os.remove(direc + '/ini_neigh.txt')
        append_new_line(direc + '/ini_neigh.txt', 'x, y, z, rel_dis (sigma units)')
        
    BOXL=(nf*LATCON)/sigma
    NLIST=0 #counter
    point=np.zeros(nat-1)
    POINT=point.tolist()
    LIST=[]
    for iat in range(nat-1):
        POINT[iat] = NLIST
        position = atoms[iat] #position of the atom iat r(iat)
        
        # If a path is given, it saves the position of the atom and the position of its neighbours
        if direc != None:
            append_new_line(direc + '/ini_neigh.txt', 'Next atom:')
            append_new_line(direc + '/ini_neigh.txt', '{:.3f}, {:.3f}, {:.3f}'.format(position[0]*sigma, position[1]*sigma, position[2]*sigma))
            append_new_line(direc + '/ini_neigh.txt', 'Neighbours:')

        for j in range(iat+1, nat):
            x = atoms[j]
            rel_pos = position-atoms[j]
            rel_pos = rel_pos - np.round(rel_pos/BOXL, 0)* BOXL #rel_pos=relative position with the iat atom: R(j)=r(j)-position
            rel_dis = np.sqrt( rel_pos[0]**2 + rel_pos[1]**2 + rel_pos[2]**2 )
            if rel_dis <= rc/sigma:
                if direc != None:
                    append_new_line(direc + '/ini_neigh.txt', '{:.3f}, {:.3f}, {:.3f}, {:.3f}'.format(x[0]*sigma, x[1]*sigma, x[2]*sigma, sigma*rel_dis))
                LIST.append(j)
                NLIST = NLIST + 1   
    return np.array(POINT), np.array(LIST)




