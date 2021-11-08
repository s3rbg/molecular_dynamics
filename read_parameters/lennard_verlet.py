#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 22:56:17 2021

@author: dgiron
"""
from common_modules.units_dicts import distance_units_upp, energy_units_upp
from common_modules.errors import InputError

distance_units = list(distance_units_upp.keys())
energy_units = list(energy_units_upp.keys())

def read_lennard_verlet_parameters(obj):

    obj.crea_entrada('Sigma parameter used in the lennard jones potential', "Sigma", 0.231e-9)
    obj.crea_entrada('Epsilon parameter', "Epsilon", 8.6e-18)

    obj.crea_entrada('Cutoff distance used to consider the neighbours in the potential' , "Cutoff distance", 2.5)
    obj.crea_entrada('Cutoff distance used to update the neighbour list', "Cutoff list", 2.7)

    obj.crea_combo('Sigma distance units', 'Sigma units', distance_units, default=False, clmn=2, rw=0, wdth=10)
    obj.crea_combo('Epsilon energy units', 'Epsilon units', energy_units, default=False, clmn=2, rw=1, wdth=10)

    obj.espera()
    # Read float values
    try:
        sigma = obj.lee_float("Sigma")
        epsilon = obj.lee_float('Epsilon')
        cutoff_distance = obj.lee_float("Cutoff distance")
        cutoff_list = obj.lee_float("Cutoff list")

    except ValueError:
        for i in ("Sigma", "Epsilon", "Cutoff distance", 'Cutoff list'):
            try:
                obj.lee_float(i)
            except ValueError:
                raise InputError('Invalid type introduced in "{}"'.format(i))
    
    
    sigma_units = obj.lee_string('Sigma units')
    epsilon_units = obj.lee_string('Epsilon units')
    
    
    
    obj.destruye()
    return sigma, sigma_units, epsilon, epsilon_units, cutoff_distance, cutoff_list
