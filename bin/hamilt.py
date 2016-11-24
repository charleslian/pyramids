# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:10:54 2016

@author: cl-iop
"""
import numpy as np
from pyramids.plot.setting import setProperty, getPropertyFromPosition

def readMatrix(filename):
  fileContext=open(filename).readlines()
  matrix = []
  for line in fileContext:
    #sep = line[:-1].replace(')','').split('(')
    sep = line[:-1].split('(')[1:]
    #print sep
    from ast import literal_eval
    b = [complex(literal_eval('(  '+i)[0],literal_eval('(  '+i)[1]) for i in sep]
    matrix.append(b)
  return np.array(matrix)
  
c=['b','r','g']
import matplotlib.pyplot as plt
import os  

fig, axs = plt.subplots(1,1) 
ax = axs
HAll = []
struct = 'Si'
folders = (struct+'_gauge',struct+'_gauge')
for index,fold in enumerate(folders):
  x = []
  y = []
  z = []
  os.chdir(fold)
  allFolder = os.popen('ls |sort -n').readlines()
  scanFolder = [intense[:-1] for intense in allFolder 
                if intense[0] in [str(j) for j in range(0,10)]]
  Hcase = []
  for iEield, efield in enumerate(scanFolder):
    print efield
    os.chdir(str(efield))
    from pyramids.io.result import  readEigFile
    comp,ef = readEigFile('siesta3td.EIG')
    
    #H = readMatrix('siesta.Hmat')
    #S = readMatrix('siesta.Smat')
  
    #iblock = H.shape[0] - 1 
    #print H
    #numBlocks = H.shape[0]/H.shape[1]
    #iblock = numBlocks - 1
    
    #Sk = S[iblock*S.shape[1]:(iblock+1)*S.shape[1],:]
    #Hk = H[iblock*H.shape[1]:(iblock+1)*H.shape[1],:]
    #Hcase.append(Hk)
    
    #eig=np.sort(np.linalg.eigvals(np.linalg.inv(Sk).dot(Hk))*13.60580)
    #eig -= ef
    comp -= ef
    if index == 1:
      x.append(float(efield)*1.0)
    else:
      x.append(float(efield))

    z.append(comp.flatten())
    os.chdir('..')
    
  HAll.append(Hcase)
  ax.plot(x,z,'-o',c=c[index],alpha=0.7)
  os.chdir('..')

ax.plot([],[],'-o',c=c[0],alpha=0.7,label=folders[0])
ax.plot([],[],'-o',c=c[1],alpha=0.7,label=folders[1])

setProperty(ax,**getPropertyFromPosition(title=struct,
                                         xlabel=r'$\varepsilon$(Ry/Bohr/e)',
                                         ylabel='Eigenvalues(eV)',
                                         ylimits=[-2,2]))
saveTypes = ['.pdf']
plt.tight_layout()
for save_type in saveTypes:
  plt.savefig(struct+save_type,transparent=True,dpi=600)                                    
                                         