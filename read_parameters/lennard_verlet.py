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

    obj.crea_entrada('Sigma parameter (lennard-jones potential). Every distance in the output file is displayed in units of this parameter', "Sigma", 0.341)
    obj.crea_entrada('Epsilon parameter (lennard-jones potential). Every energy in the output file is displayed in units of this parameter', "Epsilon", 1.654438e-21)

    obj.crea_entrada('Cutoff distance used to consider the neighbours in the potential, in units of sigma' , "Cutoff distance", 2.5)
    obj.crea_entrada('Cutoff distance used to update the neighbour list, in units of sigma', "Cutoff list", 2.7)

    obj.crea_combo('Units of the sigma parameter', 'Sigma units', distance_units, default=False, clmn=2, rw=0, wdth=10)
    obj.crea_combo('Units of the epsilon parameter', 'Epsilon units', energy_units, default=False, clmn=2, rw=1, wdth=10)

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


