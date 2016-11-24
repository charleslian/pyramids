#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma

def timeEvol(t,omega,phi,t0,delta):
  return np.sin(omega*t+phi)*np.exp(-((t-t0)/delta)**2)
  
m  = 0    # Propagation direction
N  = 5000  # Total steps
ts = 0.002 # Lenght of time step, unit in fs 

# Omega of the first and second direction, unit in eV
w = 21.84
# Phi of the first direction and second direction, unit in pi
p = 0.0
# Amplitude of the first direction and second direction, unit in Ry/Bohr/e
A = 0.01

t0 = N/2
delta = N/5

field = np.zeros([N,3])
for i in [2]:
  direction = (m+i+1)%3
  steps = np.arange(N)*ts
  T = 4.15/w
  omega = 2.0*np.pi/T
  field[:t0,i] = A*timeEvol(steps[:t0],omega,p*np.pi,t0*ts,delta*ts)
  field[t0:,i] = A*timeEvol(steps[t0:],omega,p*np.pi,t0*ts,1E30*ts)

f = open('TDEFIELD.in','w')
for values in field:
  line = '%6.3f  %6.3f  %6.3f'% (values[0]*1E5,  values[1]*1E5,  values[2]*1E5)
  f.write(line+'\n')
  
f.close()
fig, axs = plt.subplots(1,1,sharex=True,sharey=True)
ax = axs

# print Efield
# Plot Block #
ax.plot(steps,field[:,0],'-o',label='x')
ax.plot(steps,field[:,1],'-o',label='y')
ax.plot(steps,field[:,2],'-o',label='z')
#ax.plot(Efield)

kargs=ma.getPropertyFromPosition(ylabel=r'E(a.u.)',xlabel='',title='', 
                               xticks=None, yticks=None, 
                               xticklabels=None, yticklabels=None,
                               xlimits=None, ylimits=None)

ma.setProperty(ax,**kargs)

plt.tight_layout()

SaveName = __file__.split('/')[-1].split('.')[0]
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)