#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:58:44 2016

@author: cl-iop
"""

from graphene import *
import pyramids.plot.setting as ma
import matplotlib.pyplot as plt
fig, axs = plt.subplots(2,1,sharex=False,sharey=False,figsize=(12,10))

k = (0.0,1.0) #(np.sqrt(0.5),np.sqrt(0.5))
numSample = 20
thetas = np.linspace(0,np.pi/2,numSample)
intensities = 0.2*np.sin(thetas)
colors = ma.getColors(intensities.shape[0])

args={'t0':20.0,'sigma': 8.0, 'omega':2.0, 'phi':0.0, 'parity':1, 'vFermi' : 1}

args['times'] = np.linspace(0.0, 50.0, 500.0)
args['kpoint'] = k

function = []
for index, A in enumerate(intensities):
  ax = axs[1]
  args['A'] = A
  #label = r'$A = $ %2.1f eV'% (A)
  ax.plot(args['times'], HCoeff(args['times'],args), color=colors[index])
  
  result, proj0, proj1 = excitation(args)
  ax = axs[0]
  #title = r'k$_x$ = %2.1f, k$_y$ = %2.1f'% (k[0],k[1])
  ax.plot(result.times, proj1, '-', color=colors[index])
  
  function.append(proj1[-1])
  
np.save('intense',np.array(function))
#axs[2].plot(thetas,np.cos(thetas),'-') 

kargs=ma.getPropertyFromPosition(ylabel=r'', xlabel='Time $t$ (1/ev)',title='')
ma.setProperty(axs[0],**kargs)

kargs = ma.getPropertyFromPosition(ylabel=r'', xlabel='Time $t$ (1/ev)',title='')
ma.setProperty(axs[1],**kargs)

plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0] 
for save_type in ['.pdf']:
  plt.savefig(SaveName+save_type,transparent=True,dpi=600)