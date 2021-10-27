# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:32:36 2021

@author: Sergio
"""
import numpy as np
import os
import time

class Atom():
    
    
    def __init__(self, pos=[], vel=[], force=[]):
        """
        An atom
        
        Parameters
        ----------
        pos : List
            Position of the atom. The default is empty List.
        vel : List
            Velocity of the atom. The default is empty List.
        force : List
            Force of the atom. The default is empty List.

        """
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.force = np.array(force)
    
    #Get the values that define an atom
    def get_pos(self):
        return self.pos
    
    def get_vel(self):
        return self.vel
    
    def get_force(self):
        return self.force
    
    
    # Input the arguments to defined atom
    def input_pos(self, pos):
        self.pos = np.array(pos)
    
    def input_vel(self, vel):
        self.vel = np.array(vel)
        
    def input_force(self, force):
        self.force = np.array(force)
        
        
    #Modify position
    
    def move_all(self, d):
        """
        
        Moves the 3 coordinates of the position a distance d
        Parameters
        ----------
        d : float
            distance moved

        """
        if len(self.pos)!=0:
            return self.pos + d
        else:
            print('Position not defined')
   
        
    def move_direction(self, i, d):
        """
        Gives the position of the moved in one direction (x, y, z)

        Parameters
        ----------
        i : int
            Direction index (x=0, y=1, z=2)
        d : float
            Distance moved
        
        ----------
        Returns:
            Position of the atom moved a distance d along direction i
        """
        if len(self.pos)!=0:
            pos = np.copy(self.pos)
            pos[i] += d
            return pos
        else:
            print('Position not defined')
     
            
    def len_unit(self, factor):
        """
        Multiplies the position by a factor to change its units

        Parameters
        ----------
        factor : float 
            Factor to change the units
        """
        
        if len(self.pos)!=0:
            return self.pos * factor 
        else:
            print('Position not defined')    
            
    #Modify velocity
    
    def change_vel(self, i, val):
        """
        Changes the velocity of the atom along one direction

        Parameters
        ----------
        i : int
            Direction index (x=0, y=1, z=2)
        val : float
            modification value
            
        ----------
        Returns:
            modified velocity

        """
        vel = np.copy(self.vel)
        vel[i] += val
        return vel
        
    
    #Modify force
    
    def add_force(self, val):
        """
        Adds a force to the atom

        Parameters
        ----------
        val : List
            Force added to the atom
        """
        if len(val)==len(self.force):
            self.force += np.array(val)
        else:
            print('Dimension not valid, force was not changed')
        
            

def main():
    a = Atom()
    pos = [1, 2, 3]
    a.input_force(pos)
    # print(a.get_pos())
    # a.len_unit(5)
    # print(a.get_pos())
    force = [1, 0, 1]
    a.add_force(force)
    print(a.get_force())
# main()
    











