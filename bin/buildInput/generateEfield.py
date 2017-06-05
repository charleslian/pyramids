#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma



import laserparam

ep = laserparam.photonenergy
A = laserparam.field
N = laserparam.nstep
ts = laserparam.timestep
t0 = laserparam.peakstep
delta = laserparam.widthstep
p = laserparam.phase

efs = 2*np.pi*0.6562
tt = N*ts
w = [i/efs for i in ep]
t0 = t0*ts
delta = delta*ts

def timeEvol(t,omega,phi,t0,delta):
  return np.sin(2.0*np.pi*omega*t+phi)*np.exp(-((t-t0)/delta)**2)


field = np.zeros([N,3])
for i in range(3):
  direction = i
  steps = np.arange(N)*ts
  #T = 1245.0/(w[i]*300.0)
  omega = w[i]
  field[:,direction] = A[i]*timeEvol(steps,omega,p[i]*np.pi,t0,delta)

f = open('TDEFIELD.in','w')
for values in field:
  line = '%6.3f  %6.3f  %6.3f'% (values[0]*1E5,  values[1]*1E5,  values[2]*1E5)
  f.write(line+'\n')
f.close()

fig, ax = plt.subplots(1,1,sharex=True,sharey=True)
for i in range(3):
  if np.max(np.abs(field[:,i])) > 1E-7:  
    ax.plot(np.arange(N)*ts,field[:,i],label=str(i))
    
kargs=ma.getPropertyFromPosition(ylabel=r'E(a.u.)',xlabel='',title='', 
                               xticks=None, yticks=None, 
                               xticklabels=None, yticklabels=None,
                               xlimits=None, ylimits=None)

ma.setProperty(ax,**kargs)  


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


