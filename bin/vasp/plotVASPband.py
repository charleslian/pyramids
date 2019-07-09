#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
import os

from ase.io import read

atoms = read('POSCAR',format='vasp')

rcell = atoms.get_reciprocal_cell()


fig, ax = plt.subplots(1,1,figsize=(6,8),sharex=True)

def getBandVasp():
    fileContext = open('DOSCAR','r').readlines()
    emax,emin,ne,ef,weight=(float(i) for i in fileContext[5].split())
    
    print emax,emin,ne,ef,weight
    
    
    fileContext = open('EIGENVAL','r').readlines()
    #f=open('EIGENVAL','r')
    #for i in range(5): f.readline()
    
    x,nk,nb=(int(i) for i in fileContext[5].split())
    print nk,nb
    
    bands=np.zeros([nk,nb])
    kpoints=np.zeros([nk,3])
    
    dataBlock = fileContext[6:]
    for i in range(nk):
        block = dataBlock[i*(nb+2):(i+1)*(nb+2)]
        kpoints[i,:] = np.array([float(k) for k in block[1].split()[:3]]).dot(rcell)
        bands[i,:]= [float(block[j+2].split()[1]) for j in range(nb)]
            
    
    #x=range(nk)
    deltaLength = np.zeros(nk)
    for i in range(1,nk):
        rep = kpoints[i,:] - kpoints[i-1,:]
        dl = np.dot(rep, rcell)
        deltaLength[i] = np.linalg.norm(dl)
    x = np.zeros(nk)
    for i in range(1,nk):
        x[i] = np.sum(deltaLength[:i])
    return x, bands-ef 


x, bands = getBandVasp()
ax.plot(x,bands,'-k')
kargs=ma.getPropertyFromPosition(
        xlimits=[0,x.max()], xticklabels=[], hline= [0.0],
        ylimits=[-4,5], ylabel = 'Energy (eV)',
        #vline=[x[i] for i in range(0,nk,50)]
        
)
ma.setProperty(ax,**kargs)
plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]
for save_type in ['.pdf','.png']:
    filename = SaveName + save_type
    plt.savefig(filename,orientation='portrait',dpi=600)
#plt.show()        
#f.close()



