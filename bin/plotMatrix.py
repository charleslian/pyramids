# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 09:01:38 2016

@author: clian
"""
import numpy as np
from pyramids.plot.setting import setProperty, getPropertyFromPosition
import matplotlib.pyplot as plt

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

matrix = readMatrix('siesta.psiTmp')

numBlocks = matrix.shape[0]/matrix.shape[1]
iblock = 0
psiTmp1 = matrix[iblock*matrix.shape[1]:(iblock+1)*matrix.shape[1],:]

iblock = 1
psiTmp2 = matrix[iblock*matrix.shape[1]:(iblock+1)*matrix.shape[1],:]


matrix = readMatrix('siesta.SBerryInv')
numBlocks = matrix.shape[0]/matrix.shape[1]
iblock = 0
Sinv1 = matrix[iblock*matrix.shape[1]:(iblock+1)*matrix.shape[1],:]

iblock = 1
Sinv2 = matrix[iblock*matrix.shape[1]:(iblock+1)*matrix.shape[1],:]

vcap = (Sinv1*psiTmp1 - Sinv2*psiTmp2)[:,0]*1j

#print readMatrix('siesta.vcap')
vec = readMatrix('siesta.psi')[0:2,1]
print np.outer(vcap, vec)
print readMatrix('siesta.wie')[:2,:] + readMatrix('siesta.wie')[2:4,:]

print readMatrix('siesta.Saux')[:2,:] + readMatrix('siesta.Sraux')[:2,:]
#print (np.vdot(vec,(readMatrix('siesta.Smat').dot(vec))))
#block = matrix]
#print block
#fig = plt.figure(figsize=[10.0, 4.0])
#ax = plt.subplot(1, 2, 1)
#cax = ax.imshow(np.real(block), interpolation='none',cmap='bwr')
#cbar = fig.colorbar(cax)
#setProperty(ax,**getPropertyFromPosition(index=0,title='Real Part')) 
#
#ax = plt.subplot(1, 2, 2)
#cax = ax.imshow(np.imag(block), interpolation='none',cmap='bwr')
#cbar = fig.colorbar(cax)
#setProperty(ax,**getPropertyFromPosition(index=1,title='Imag Part')) 
#plt.tight_layout()