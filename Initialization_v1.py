# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 23:59:39 2021

@author: Sergio
"""
import numpy as np
import matplotlib.pyplot as plt
from Atom import Atom
import os
# from tqdm import tqdm

class Initialization():
    
    def __init__(self, N):
        
        self.atoms = []
        self.N = N
        self.ac = 1/N
        
    def unit_cell(self, tipe = 'FCC'):
        """
        Defines the position of the atoms in the unit cell. The default is 
        an FCC lattice.

        Parameters
        ----------
        type : TYPE, optional
            type of lattice. The default is 'FCC', currently the only one 
            available
        """
        if tipe != 'FCC':
            print('Other initial positions not implemented')
        else:
            pos = np.genfromtxt('FCC.txt', delimiter='\t', skip_header=1)
            for i in pos:
                self.atoms.append(Atom(i*self.ac))
        self.size = len(self.atoms)
        
    def supercell(self):
        """Given the position of the atoms in the unit cell, it moves them 
        to build the supercell made of N^dim unit cells.
       """
        #Loop along the cartesian axis in the dimensions defined
        
        for ix in range(len(self.atoms[0].get_pos())):      
            #Loop for all the replicas of the unit cell along direction ix
            replicas = []
            for i in range(1, self.N):
                #Loop for all the atoms defined
                for j in self.atoms:
                    # print(j.get_pos())                    
                    #Get the position of the periodic replica
                    #It adds ac*i along direction ix to the position of atom j
                    # print(j.get_pos())
                    pos = j.move_direction(ix, self.ac*i)
                    #Add the replica to the list
                    replicas.append(Atom(pos))
            self.atoms.extend(replicas)
                    
    def velocities(atoms, temp):
        """Defines the velocity of the atoms in the supercell according to a Maxwell-Boltzmann distribution.
        Returns the atoms that were given with velocity defined."""
        pass
        
    def correction(atoms):
        """Corrects the velocities so that the net momentum is 0"""
        pass
        
    def tests(self, file1 = 'Initial_positions'):
        """
        Creates a file with the initial positions and plots a 
        histogram with the initial velocities
        """
        # Deletes the file if already exists
        if os.path.exists(file1):
            os.remove(file1)
        
        #Create the file
        with open(file1, 'a+') as f:
            #loop for all the atoms
            for i, j in enumerate(self.atoms):
                #Write position of atom 
                f.write(str(j.get_pos())+'\n')
                #Check if unit cell was completed
                if (i+1)%self.size == 0:
                    f.write('\n')
            f.close()
                
    
    def get_atoms(self):
        return self.atoms
    

    
