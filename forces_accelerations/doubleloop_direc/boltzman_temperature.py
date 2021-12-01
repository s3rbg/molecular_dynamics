import numpy as np

def boltzman_temperature(vel, Nat):
    v2=0
    v=0
    R=8,314 #JK**-1mol**-1
    Na=6.023*10**(23) #mol**-1
    m=1 #¡ATENTION!
    for i in range(1,Nat+1):
        for j in range(1,4):
            v2 = v2 + vel[i][j]**2
        v = v + np.sqrt(v2)
        v2=0
    vm = v/Nat
    T=m*np.pi*np.sqrt(vm)*Na/(8*R)
    return T
