#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 15:25:50 2021

@author: dgiron
"""

from common_modules.imports import *

from forces_accelerations.doubleloop import doubleloop 
from forces_accelerations.neighbour_list.verlet_list import list_neighbour

# from output.save_text_file import to_txt # Cambiar por nombre real

# Calcular energias en el de alain

def velocity_verlet(positions, velocities, accelerations, old_neigh_point, old_neigh_list, n_at, delta_t, cutoff_for_disp, cutoff_for_neigh,
                    potential_type, number_of_cells, lat_con, sigma, epsilon):
    
    # Sustituir con el nombre de la funcion real
    initial_positions = positions # Save initial positions to compute the displacements
    
    positions = positions + velocities * delta_t + 0.5 * accelerations * delta_t ** 2
    inter_velocities = velocities + 0.5 * accelerations * delta_t
    
    # Compute new accelerations
    displacements = np.abs([aux(i[0], i[1], i[2]) - aux(j[0], j[1], j[2])  
                            for i, j in zip(initial_positions, positions)])
    
    if max(displacements) >= cutoff:
        neigh_point, neigh_list = list_neighbour(sigma, lat_con, n_at, number_of_cells, cutoff_for_neigh)
        accelerations = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                  n_at, positions, velocities, number_of_cells, lat_con, epsilon, cutoff_for_neigh)
    else:
        neigh_point = old_neigh_point
        neigh_list = old_neigh_list
        accelerations, potential, kinetic, total = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                                              n_at, positions, velocities, number_of_cells, 
                                                              lat_con, epsilon, cutoff_for_neigh)
    velocities = inter_velocities + 0.5 * accelerations * delta_t
    
    # to_txt(positions, potential, kinetic, total) # Save in a text file the new coordinates

    return positions, velocities, accelerations, neigh_point, neigh_list

def leap_frog(positions, velocities, accelerations, old_neigh_point, old_neigh_list, n_at, delta_t, cutoff_for_disp, cutoff_for_neigh, 
              potential_type, number_of_cells, lat_con, sigma, epsilon):
    
    initial_positions = positions # Save initial positions to compute the displacements
    
    inter_velocities = velocities + accelerations * delta_t
    positions = positions + inter_velocities * delta_t
    
    velocities = (inter_velocities + velocities) / 2
    
    # Compute new accelerations
    displacements = np.abs([aux(i[0], i[1], i[2]) - aux(j[0], j[1], j[2]) 
                            for i, j in zip(initial_positions, positions)])
    
    if max(displacements) >= cutoff:
        neigh_point, neigh_list = list_neighbour(sigma, lat_con, n_at, number_of_cells, cutoff_for_neigh)
        accelerations = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                  n_at, positions, velocities, number_of_cells, lat_con, epsilon, cutoff_for_neigh)
    else:
        neigh_point = old_neigh_point
        neigh_list = old_neigh_list
        accelerations, potential, kinetic, total = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                                              n_at, positions, velocities, number_of_cells, 
                                                              lat_con, epsilon, cutoff_for_neigh)
    # to_txt(positions, potential, kinetic, total) # Save in a text file the new coordinates

    return positions, velocities, accelerations, neigh_point, neigh_list


def verlet(positions, old_positions, velocities, accelerations, old_neigh_point, old_neigh_list, 
           n_at, delta_t, cutoff_for_disp, cutoff_for_neigh, potential_type, number_of_cells, lat_con, sigma, epsilon): # Here f(t) always
    
    initial_positions = positions # Save initial positions to compute the displacements
    
    
    positions = 2 * positions - old_positions + accelerations * delta_t ** 2 # Next step
    
    velocities = (positions - old_positions) / (2 * delta_t ** 2) # Next step
    
    # Compute new accelerations
    displacements = np.abs([aux(i[0], i[1], i[2]) - aux(j[0], j[1], j[2]) 
                            for i, j in zip(initial_positions, positions)])
    
    if max(displacements) >= cutoff:
        neigh_point, neigh_list = list_neighbour(sigma, lat_con, n_at, number_of_cells, cutoff_for_neigh)
        accelerations = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                  n_at, positions, velocities, number_of_cells, lat_con, epsilon, cutoff_for_neigh)
    else:
        neigh_point = old_neigh_point
        neigh_list = old_neigh_list
        accelerations, potential, kinetic, total = doubleloop(sigma, potential_type, neigh_point, neigh_list, 
                                                              n_at, positions, velocities, number_of_cells, 
                                                              lat_con, epsilon, cutoff_for_neigh)
    
    # to_txt(positions, potential, kinetic, total) # Save in a text file the new coordinates

    return positions, velocities, accelerations, neigh_point, neigh_list
 
    
# def RK4(f, a, b, r0, N):
#     # Calcularemos la solución dr/dt=f(t,r) con valor inicial r(a)=r0, y con paso h=(b-a)/N, usando RK4. Nótese que r0 tiene que ser un vector, esto es, un np.array, en cuyo caso r(t) será una función vectorial, de la que nos devolverá el método: r(0), r(h), r(2h),...r(Nh=b). Por lo tanto, lo que nos devuelve el método es una matriz "T" con N+1 filas y número de columnas igual a la dimensión de r0.
#     T = np.zeros((N+1,r0.size)) #  Fijamos el tamaño de T y la iremos rellenando
#     T[0,:] = r0 # la primera fila de T es los elementos de r0
#     contador = 0 # Para llevar la cuenta de en qué fila estamos
#     h = (b-a)/N # El valor de h
#     t0 = a + contador*h # El valor del tiempo en este momento

#     while contador<N:

#         k_1 = h*f(t0,r0)
#         k_2 = h*f(t0+h/2, r0+k_1/2)
#         k_3 = h*f(t0+h/2, r0+k_2/2)
#         k_4 = h*f(t0+h, r0+k_3)
#         r0 = r0+1/6*(k_1+2*k_2+2*k_3+k_4)
        
#         contador = contador+1
#         t0 = t0+h # actualizamos el tiempo
#         T[contador,:] = r0 # El valor actualizado

#     tt = np.linspace(a, b, N+1) # Que nos devuelva también el vector de tiempos
    
    
#     return tt, T

# def segundo_orden(f, a, b, r0, rdot0, N):
#     # Dada una función f(t,r,rdot) que nos da el valor de d^2 r/dt^2, y dado un intervalo temporal [a,b], calcula una aproximación de la función r(t) que satisface la ecuación con valores iniciales r(t=0)=r0, dr/dt(t=0)=rdot0, mediante el procedimiento de reducirlo a un problema de primer orden y resolver con el método de RK4. Nos devolverá tt (los tiempos donde se aproxima la solución, correspondientes a "a", "a+h", "a+2h", ..., "a+Nh=b$ donde h=(b-a)N), además de el valor de r en cada uno de esos tiempos y  también el valor de dr/dt en cada uno de esos tiempos, porque ya que los generamos en el proceso pues los acumulamos.
#     # Construimos el problema de primer orden (y doble de dimensión) correspondiente a f: consideraremos una nueva función inventada w(t)=(r,dr/dt). Con ello,
#     p = r0.size*2 # luego el tamaño de r es p/2, y el de dr/dt también
#     def f_aux(t, w):
#         r = w[0:p//2] # Extraemos las primeras p/2 coordenadas: tenemos r
#         rdot = w[p//2:] # O sea desde d/2 hasta el final: tenemos dr/dt
#         # La derivada de r es dr/dt:
#         deri_r = rdot
#         # La derivada de dr/dt viene dada por la función f original:
#         deri_rdot = f(t, r, rdot)
#         # Finalmente, acumulamos deri_r y deri_rdot en un solo array y devolvemos:
#         wdot = np.concatenate((deri_r,deri_rdot))
        
#         return wdot
#     # Ahora resolvemos este problema de primer orden. Primero definimos el valor inicial para este nuevo problema:
#     w0 = np.concatenate((r0, rdot0))
#     tt, T = RK4(f_aux, a, b, w0, N)
#     # Con ello, T será una matriz de N+1 filas y p columnas. Las primeras p/2 corresponden a r(tt) y las últimas p/2 corresponden a dr/dt(tt):
#     R = T[:, 0:p//2]
#     Rdot = T[:, p//2:]
#     return tt, R, Rdot
    
    
def aux(x, y, z):
    return np.sqrt(x**2 + y**2 + z**2)
    
    
    
    

