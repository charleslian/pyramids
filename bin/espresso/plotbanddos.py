#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 11:06:46 2017

@author: clian
"""
import numpy as np

def readData(): 
    f=open('bands.out.gnu')
    data = []
    nband = 0
    for line in f.readlines():
        if len(line) != 1:
            data.append([float(i) for i in line.split()])
        else:
            nband += 1
    data = np.array(data)
    nkpt = data.shape[0]/nband 
    band = np.zeros([nkpt,nband+1])
    band[:,0] = data[:nkpt,0]
    band[:,1:] = data[:,1].reshape([nband,nkpt]).T
    #print band
    return band

def readDOS(): 
    f=open('pwscf.dos')
    data = []
    content = f.readlines()
    efermi = float(content[0].split()[-2])
    for line in content[1:]:
        data.append([float(i) for i in line.split()])
    data = np.array(data)
    #print efermi
    data[:,0] -= efermi
    return  data, efermi

import os
#homo, lumo = [float(i) for i in os.popen('grep "highest occupied" result').readline().split()[-2:]]
#print homo

skpt = []
for line in os.popen('grep "high-symmetry point:" result').readlines():
    skpt.append(float(line.split()[-1]))



data = readData()
dos, efermi = readDOS()

data[:,1:] -= efermi

import matplotlib.pyplot as plt
import pyramids.plot.setting as ma
SaveName = __file__.split('/')[-1].split('.')[0]


fig, axs = plt.subplots(1,2,sharex=False, sharey=True,figsize=(8,6))#,figsize=(10,6)

ax = axs[1]
xcon = np.linspace(1E15,1E15,dos.shape[0])
ax.fill_between(dos[:,1], dos[:,0], xcon)

ax.plot(dos[:,1], dos[:,0], '-k')
#ax.plot(xcon, dos[:,0])


args = ma.getPropertyFromPosition(1, 
                                  title = 'DOS', 
                                  xticklabels=[], 
                                  xlimits=[0,None], 
                                  hline=[0.0]
                                  )
ma.setProperty(ax,**args)




ax = axs[0]
ax.plot(data[:,0],data[:,1:],'-', mfc='w',ms=3.0)
args = ma.getPropertyFromPosition(0, 
                                  title = 'Band', 
                                  ylabel = 'E (eV)', 
                                  xlimits=[data[:,0].min(),data[:,0].max()], 
                                  ylimits=[-6,dos[:,0].max()], 
                                  xticklabels=[],
                                  hline=[0.0],
                                  vline=skpt[:-1]
                                  )
ma.setProperty(ax,**args)
plt.tight_layout()


plt.tight_layout()
for save_type in ['.png']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)


