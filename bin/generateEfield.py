#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma

def timeEvol(t,omega,phi,t0,delta):
  return np.sin(omega*t+phi)*np.exp(-((t-t0)/delta)**2)
  


m  = 0    # Propagation direction
N  = 1000  # Total steps
ts = 0.05 # Lenght of time step, unit in fs 

# Omega of the first and second direction, unit in eV
w = 4.0, 4.0 
# Phi of the first direction and second direction, unit in pi
p = 0.0, 0.5 
# Amplitude of the first direction and second direction, unit in Ry/Bohr/e
A = 0.05, 0.05     

t0 = N/2
delta = N/5


field = np.zeros([N,3])
for i in range(2):
  direction = (m+i+1)%3
  steps = np.arange(N)*ts
  T = 1245.0/(w[i]*300.0)
  omega = 1/T
  field[:,direction] = A[i]*timeEvol(steps,omega,p[i]*np.pi,t0*ts,delta*ts)



f = open('TDEFIELD.in','w')
for values in field:
  line = '%6.3f  %6.3f  %6.3f'% (values[0]*1E5,  values[1]*1E5,  values[2]*1E5)
  f.write(line+'\n')
  
f.close()

#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure(figsize=(10,6))
#ax = fig.add_subplot(111, projection='3d')
#
#ax.scatter(steps, field[:,(m+1)%3],field[:,(m+2)%3],linewidths=0.0)
#
#labels = [r'$\varepsilon_x$',r'$\varepsilon_y$',r'$\varepsilon_z$']
#ax.set_ylim([-max(A),max(A)])
#ax.set_zlim([-max(A),max(A)])
#ax.tick_params(labelsize='large')
#ax.set_xlabel('Time(fs)',fontsize='x-large')
#ax.set_ylabel(labels[(m+1)%3]+'(a.u.)',fontsize='x-large')
#ax.set_zlabel(labels[(m+2)%3]+'(a.u.)',fontsize='x-large')
#
#plt.tight_layout()
#SaveName = __file__.split('/')[-1].split('.')[0]
#c = ma.getColors(3,cmap='brg')


