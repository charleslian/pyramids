# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 12:12:31 2016

@author: cl-iop
"""


from scipy import linalg
import numpy as np
import matplotlib.pyplot as plt

numBands = 2
Ep = 2
t  = 4 
t1 = 2 ; t2 = 3 ; t3 = 2

kxs = [1,1]
H = np.zeros([numBands,numBands],dtype=complex)

H[0,0] = Ep
H[1,1] = Ep


for kx in np.linspace(0,np.pi,40): 
  for ky in np.linspace(0,np.pi,40): 
    H[0,1] = t1*np.exp(-1j*kx) + t2*np.exp(-1j*(-0.5*kx+np.sqrt(3)*ky)) + t3*np.exp(-1j*(-0.5*kx-np.sqrt(3)*ky)) 
    H[1,0] = np.conj(H[0,1])
    eigenvalues, eigvectors = linalg.eigh(H)
    
    #for band in range(start,end): 
    plt.scatter([kx,kx],eigenvalues[:],color='g',linewidths = 0.0, alpha=0.8)