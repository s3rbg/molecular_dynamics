import numpy as np

def list_neighbour(sigma, LATCON, nat, nf, atoms, rl):
    """
    
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
        DESCRIPTION.
    LIST : List
        DESCRIPTION.

    """
    
    BOXL=(nf*LATCON)/sigma 
    NLIST=0 #counter
    POINT=[nat]
    LIST=[]
    for iat in range(1,nat):
        POINT[iat] = NLIST + 1
        position = atoms[iat] #position of the atom iat r(iat)
        for j in range(iat+1,nat):
            rel_pos = position-atoms[j]
            rel_pos = rel_pos - round(rel_pos/BOXL,1)*BOXL #rel_pos=relative position with the iat atom: R(j)=r(j)-position
            rel_dis = np.sqrt( rel_pos[1]^2 + rel_pos[2]^2 + rel_pos[3]^2 )
            if rel_dis < rl:
                NLIST = NLIST + 1
                LIST.append(j)
            
    return (POINT, LIST)
