# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 23:59:39 2021
@author: Sergio
"""
import numpy as np
import matplotlib.pyplot as plt
import os
from pandas import DataFrame
from init.Generation import Generation
from init.Histogram import histogram
from tqdm import tqdm

class Initialization():
    
    def get_pos(self):
        return self.pos
    
    def get_vel(self):
        return self.vel
    
    
    
    def __init__(self, T, N, sigma, a, directory='.'):
        
        self.N = N
        self.ac = 1/N
        self.sigma = sigma
        self.a = a
        self.T = T
        self.dir = directory
        
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
            self.pos = np.genfromtxt('init/FCC.txt', delimiter='\t', skip_header=1)*self.ac
        
        self.unit_size = len(self.pos)
    
            
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
            #Copy positions as a list
            pos = np.copy(self.pos).tolist()
            #Add replicas to position list
            pos.extend(replicas)
            #Update positions array
            self.pos = np.array(pos)
        self.size = len(self.pos)
        
    def final_change(self):
        """
        Final corrections to the system from which positions are defined for
        efficiency
        """
        #Change the origin of the system to the center of the supercell
        self.pos -= 0.5
        #Change the system of units so that sigma = 1
        self.pos *= self.N*self.a/self.sigma

                
    def velocities(self):
        """Defines the velocity of the atoms in the supercell according to a Maxwell-Boltzmann distribution.
        Returns the atoms that were given with velocity defined."""
        #Create object of generation class
        a = Generation(self.T)
        #Generate random velocities according to a Gaussian distribution for
        #each of the cartesian axis
        vx, vy, vz = a.gen_random(len(self.pos))
        
        #Correct the velocities so that net momentum is 0 (system doesn't move)
        vx = a.correction(vx)
        vy = a.correction(vy)
        vz = a.correction(vz)
        
        self.vel = np.array([vx, vy, vz]).T
        
        
    
        
    def tests(self):
        """
        Creates a file with the initial positions and plots a 
        histogram with the initial velocities
        """
        # Positions file
        # Deletes the file if already exists
        file1 = str(self.dir+'/initial_positions.dat')
        
        if os.path.exists(file1):
            os.remove(file1)
        
        #Create the file
        with open(file1, 'a+') as f:
            f.write('Initial position of the atoms in the supercell divided in unit cell\n'
                'blocks in a system of units where sigma is 1 and the origin\n'
                'is placed at the center of the supercell, in cartesian coordinates \n\n')
            #loop for all the atoms
            print('Writing positions in file')
            for i, j in enumerate(tqdm(self.pos)):
                #Write position of atom
                f.write(str(i+1)+ ' '+str(j)+'\n')
                #Check if unit cell was completed
                if (i+1)%self.unit_size == 0:
                    f.write('\n')
            f.close()
            
        #Histogram
        
        num, edges = histogram(np.concatenate((self.vel[:,0], self.vel[:,1],
                                              self.vel[:,2])),
                               10*self.N, sigma=self.T**0.5, wide=10)
        
        file2 = str(self.dir+'/velocity_histogram.dat')
        
        
        # Deletes the file if already exists
        if os.path.exists(file2):
            os.remove(file2)
        #Create the file    
        with open(file2, 'a+') as g:
            g.write('Histogram for the initial velocities\n'
                    'the velocities are generated according to a Gaussian distribution\n'
                    'for each of the cartesian axis\n'
                    'The variance is '+ str(round(np.sqrt(self.T), 3))+'\n\n')
            g.write('Velocity (reduced units)\t Number of atoms with one component'
                    ' being between that velocity and the next one\n')
            
            print('Writing histogram')
            for i in tqdm(range(len(num))):
                edge = f'{edges[i]:.10f}'
                #Make file look good
                if edge[0]=='-':
                    g.write(f'{edge} \t\t\t\t\t\t\t\t {num[i]:.0f}\n')
                else:
                    g.write(f' {edge} \t\t\t\t\t\t\t\t {num[i]:.0f}\n')
                        
                        
                # if len(edge)<7 and edge[0]=='-':
                #     g.write(f'{edge} \t\t\t\t\t\t\t\t\t {num[i]:.0f}\n')
                # elif len(edge)>=7 and edge[0]!='-':
                #     g.write(f' {edge} \t\t\t\t\t\t\t\t {num[i]:.0f}\n')
                # elif len(edge)<7 and edge[0]!='-':
                #     g.write(f' {edge} \t\t\t\t\t\t\t\t\t {num[i]:.0f}\n')
                # else:
                #     g.write(f'{edge} \t\t\t\t\t\t\t\t {num[i]:.0f}\n')
            g.close()