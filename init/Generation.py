# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 10:35:55 2021

@author: Sergio
"""
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.stats import maxwell
class Generation():
    
    def __init__(self, T):
        self.T = T
     
        
  
    
    def gen_random(self, num, var = None, mu=0):
        if var is None:
            var = np.sqrt(self.T)
            
        vx = np.random.normal(mu, np.sqrt(var), num)*var
        vy = np.random.normal(mu, np.sqrt(var), num)*var
        vz = np.random.normal(mu, np.sqrt(var), num)*var
        #Generate velocities (norm)
        return vx, vy, vz
        
    def correction(self, v):
        
        v = np.array(v)        
        s = sum(v)
        # v -= s/len(v)
        return v - s/len(v)
    
    
def main():
    T = 100
    a = Generation(T)
    N = 2
    vx, vy, vz = a.gen_random(N**3)
    vx = a.correction(vx)
    vy = a.correction(vy)
    vz = a.correction(vz)
    
    print(sum(vx))
    print(sum(vy))
    print(sum(vz))
    

        
        