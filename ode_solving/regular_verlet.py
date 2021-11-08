#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 16:39:25 2021

@author: dgiron
"""

from common_modules.imports import *
from neighbour_list import neighbour
from forces import compute_forces 
from common_modules.errors import NeighListError

# def solve_ode_step(initial_forces, point, neigh_list, positions):
    
#     for i in range(tot_time/step):
#         neigh_list, point = neighbour(positions) 
#         forces = compute_forces(point, neigh_list, positions)
#         acceleration = forces/mass
        
#         for iat in range(len(dN_at - 1)):
#             j_beg = point(iat)
#             j_end = point(iat) - 1
            
#             if jbeg > jend:
#                 raise NeighListError('Neighbour list (point) is not correctly defined')
            
#             for jneigh in range(jbeg, jend):
#                 j = neigh_list(jneig)
#                 new_position_array = 2 * positions - old_positions * step + acceleration * step ** 2
    