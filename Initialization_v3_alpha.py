# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 23:59:39 2021

@author: Sergio
"""
import numpy as np
import matplotlib.pyplot as plt
from Atom import Atom
import os
from pandas import DataFrame
from Generation import Generation
# from tqdm import tqdm

class Initialization():
    
    def get_pos(self):
        return self.pos
    
    def __init__(self, T, N, sigma, a):
        
        self.atoms = []
        self.N = N
        self.ac = 1/N
        self.sigma = sigma
        self.a = a
        self.T = T
        
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
            self.pos = np.genfromtxt('FCC.txt', delimiter='\t', skip_header=1)*self.ac
        
    
            
    def supercell(self):
        """Given the position of the atoms in the unit cell, it moves them 
        to build the supercell made of N^dim unit cells.
       """
        #Loop along the cartesian axis in the dimensions defined
        # self.pos = self.pos.tolist()
        # print(self.pos)
        # print(len(self.pos[0]))
        for ix in range(len(self.pos[0])):      
            #Loop for all the replicas of the unit cell along direction ix
            replicas = []
            for i in range(1, self.N):
                #Loop for all the atoms defined
                for j in np.copy(self.pos):
                    #It adds ac*i along direction ix to the position of atom j
                    # pos = j.move_direction(ix, self.ac*i)
                    # pos = np.copy(self.pos)
                    j[ix] += self.ac*i
                    #Add the replica to the list
                    replicas.append(j.tolist())
            # replicas = np.array(replicas)
            pos = np.copy(self.pos).tolist()
            pos.extend(replicas)
            self.pos = np.array(pos)
            # print(self.pos)
            # self.pos = np.array(pos.extend(replicas))
            
            
            # self.pos = np.array(self.pos.tolist().extend(replicas))
            # print(self.pos)
        
                    
    def velocities(self):
        """Defines the velocity of the atoms in the supercell according to a Maxwell-Boltzmann distribution.
        Returns the atoms that were given with velocity defined."""
        a = Generation(self.T)
        vx, vy, vz = a.gen_random(len(self.atoms))
        vx = a.correction(vx)
        vy = a.correction(vy)
        vz = a.correction(vz)
        
        for i in range(len(self.atoms)):
            self.atoms[i].input_vel([vx[i], vy[i], vz[i]])
        
    
        
    def tests(self):
        """
        Creates a file with the initial positions and plots a 
        histogram with the initial velocities
        """
        # Deletes the file if already exists
        file1 = 'Initial_positions.txt'
        if os.path.exists(file1):
            os.remove(file1)
        
        #Create the file
        with open(file1, 'a+') as f:
            #loop for all the atoms
            f.write(str(['x', 'y', 'z'])+'\n')
            for i, j in enumerate(self.atoms):
                #Write position of atom 
                f.write(str(j.get_pos())+'\n')
                #Check if unit cell was completed
                if (i+1)%self.size == 0:
                    f.write('\n')
            f.close()
                
    def final_change(self):
        for i in self.atoms:
            i.input_pos(i.move_all(-0.5))
            i.input_pos(i.len_unit(self.N*self.a/self.sigma))
            
    # def get_atoms(self):
    #     pos = [x.get_pos() for x in self.atoms]
    #     vel = [x.get_vel() for x in self.atoms]
    #     return pos, vel
    
def main():
    T = 100
    N = 2
    ct = 1/N
    sigma=2
    a = Initialization(T, N, sigma, ct)
    a.unit_cell()
    
    a.supercell()
    
    # a.tests()
    # a.final_change()
    # a.velocities()
    # pos, vel = a.get_atoms()
    # sx = 0
    # sy = 0
    # sz = 0
    # for i in b:
    #     v = i.get_vel()
    #     sx+=v[0]
    #     sy+=v[1]
    #     sz+=v[2]
    # print(sx,'\n',sy,'\n',sz)
    # a.tests()
    # b = a.get_atoms()
    # for i in b:
    #     print(i.get_pos())
    # positions = [i.get_pos().tolist() for i in a.get_atoms()]
    
    # b = a.get_atoms()
    # for i in b:
    #     print(i.get_pos())
    # a = [1, 2, 4]
    # b = [5, 6]
    # a.extend(b)
    # print(a)
main()
    
