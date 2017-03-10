# -*- coding: utf-8 -*-
"""
Created on Mon May 23 14:47:00 2016

@author: cl-iop
"""
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import os

def readW90hr(filename='wannier90_hr.dat'):
  # read the Wannier function hr file, organize the data 
  W90hrFile = open(filename)
  W90hrFile.readline()
  nOrb = int(W90hrFile.readline().split()[0])
  nCell = int(W90hrFile.readline().split()[0])
  for i in range(nCell/15+1):
    W90hrFile.readline()
  nElement = nCell*nOrb*nOrb
  Rij = np.zeros([nElement,3],dtype=int) 
  Orb = np.zeros([nElement,2],dtype=int)
  Hsp = np.zeros([nElement],dtype=complex)
  for i in range(nElement):
    line = W90hrFile.readline().split()
    Rij[i,0] = int(line[0])
    Rij[i,1] = int(line[1])
    Rij[i,2] = int(line[2])
    Orb[i,0] = int(line[3])-1
    Orb[i,1] = int(line[4])-1
    Hsp[i] = complex(float(line[5]),float(line[6]))
  return Rij, Orb, Hsp, nOrb, nCell
    
def buildHamiltonian(Rij, Orb, Hsp, nOrb, nCell, cell, kpoint):
  # build the Hamiltonian Hk at k = (kpoint[0],kpoint[1],kpoint[2])
  H = np.zeros([nOrb,nOrb],dtype=complex)
  for index,rij in enumerate(Rij):
    H[Orb[index,0],Orb[index,1]] += Hsp[index]*np.exp(1.0j*np.dot(kpoint,np.dot(rij,cell)))
  return H
  
def getMPKpts(atoms, grid):
  """
  Generate the Monkhorst-Pack k point with grid[0] \times grid[1] \times grid[2]
  """
  from ase.dft.kpoints import monkhorst_pack
  reciprocal_vectors = 2*np.pi*atoms.get_reciprocal_cell()
  return np.dot(monkhorst_pack(grid),reciprocal_vectors)
  
def getBandKpoints(atoms, npoints=50, selectedPath = ['G','M','K','G','A','L','H'],shape='Hexagonal'):
  """
  Generate the line mode k along the selected path
  not very kind ase interface lead to a puzzling input parameters
  """
  from ase.dft.kpoints import get_bandpath, get_special_points
  points = get_special_points(shape,atoms.get_cell())
  #print points
  GXW = [points[k] for k in selectedPath]
  kpts,rk,rspk = get_bandpath(GXW, atoms.get_cell(), npoints=npoints)
  reciprocal_vectors = 2*np.pi*atoms.get_reciprocal_cell()
  return np.dot(kpts,reciprocal_vectors)
               
def susFunc(eigall,ik,iq,Ef,T):
  nb = eigall.shape[0]
  fdk = 1.0/((eigall[:,ik]-Ef)/8.61E-5*T+1.0)
  fdq = 1.0/((eigall[:,iq]-Ef)/8.61E-5*T+1.0)
  sus = np.sum([(fdk[i]*(1-fdq[j]))/(eigall[i,ik]-eigall[j,iq] + 1j*1E-6)
                for i in range(nb) for j in range(nb)])
  return sus
  
def calculateEigenPairs(atoms, kpts=[],filename='wannier90_hr.dat'):
  """
  calculate the eigen pairs with the set of kpoints, 
  return Xs, eigenvalues, eigenvectors of all kpoints,
  For a MxM Hamiltonian and N kpoints, 
  the dimensions of the first array (X) is N, 
  the second (eigenvalues) is MxN, 
  the third (eigenvalues) is eigenvector MxMxN
  """
  # If there are saved files, read from them instead of re-calculating
  if not os.path.isfile('EigValue.npy'):
    eigValueAllK = np.zeros([1,1])
  else:
    eigValueAllK = dP.loadSaved('EigValue')
  if not os.path.isfile('EigVector.npy'):  
    eigVectorAllK = np.zeros([1,1])
  else:
    eigVectorAllK = dP.loadSaved('EigVector')  
  if not os.path.isfile('X.npy'):  
    xall = np.zeros([1,1])
  else:
    xall = dP.loadSaved('X')
    
  rk = range(len(kpts))
  nk = len(kpts)
  
  print eigValueAllK.shape[1]
  if eigValueAllK.shape[1] != nk:
    Rij, Orb, Hsp, nOrb, nCell = readW90hr(filename)
    eigValueAllK = np.zeros([nOrb,len(kpts)],dtype=float)
    eigVectorAllK = np.zeros([nOrb,nOrb,len(kpts)],dtype=complex)
    xall = np.zeros([nOrb,len(kpts)])
    for ik, kpoint in enumerate(kpts):
      print "Calculating the ",ik,kpoint,"K point of ", nk, 'K points'
      H = buildHamiltonian(Rij, Orb, Hsp, nOrb, nCell, atoms.get_cell(), kpoint)
      from scipy.linalg import norm, eig, eigh
      x = np.ones([nOrb]) * norm(rk[ik])
      eigVector = np.zeros([nOrb,nOrb])
      eigValue,eigVector = eig(H)
      xall[:,ik] = x
      
      eigValueAllK[:,ik] = eigValue
      eigVectorAllK[:,:,ik] = eigVector
    np.save('X',xall)
    np.save('EigValue',eigValueAllK)
    np.save('EigVector',eigVectorAllK)
  return xall, eigValueAllK, eigVectorAllK

def plotBands(xall,eigValueAllK):
  from pyramids.plot.setting import setProperty, getPropertyFromPosition
  fig, ax = plt.subplots(1,1)
  #Plot the eigenvalues 
  for index in range(eigValueAllK.shape[0]):
    ax.plot(xall[index,:],eigValueAllK[index,:],'ob',lw=1)
  setProperty(ax,**getPropertyFromPosition(title='Energy Bands',xlabel=r'',ylabel=r'Energy(eV)',xticklabels=[]))
  #Set tight layout and output 
  plt.axis('tight')
  plt.tight_layout()
  plt.savefig('Bands.pdf',dpi=600)
  plt.show()
  #plt.close()

def plotKpoints(kpts):
  #Plot the K points
  from pyramids.plot.setting import setProperty, getPropertyFromPosition
  fig, ax = plt.subplots(1,1)
  ax.plot(kpts[:,0],kpts[:,1],'o')
  setProperty(ax,**getPropertyFromPosition(title='K points',xlabel=r'$k_x(1/\AA)$',ylabel=r'$k_y(1/\AA)$'))
  plt.axis('equal')
  plt.tight_layout()
  plt.savefig('Kpoints.pdf',dpi=600)
  plt.show()
  #plt.close()
  
#unit = reciprocal_vectors/grid
#KIndex = np.dot(kpts,np.linalg.inv(unit)) + [nkx/2, nky/2, nkz/2]
#kIndex = np.array(KIndex, dtype=int)
#skpts = np.array([kpts + np.dot([i,j,k],reciprocal_vectors)
#         for i in [0,-1,1] for j in [0,-1,1] for k in [0,-1,1]])
#skIndex = np.array(np.dot(skpts,np.linalg.inv(unit)) + [0.5,0.5,0], dtype=int)            
#print kIndex.shape, #skIndex.shape
#print kIndex

#Ef = 6.0
#T = 300
#qOrder = 2     
#susp = np.zeros([qOrder,qOrder,qOrder],dtype=float) 
#
#
#for ik, ikpt in enumerate(kpts):
#  kxy = kIndex[ik] 
#  for i in range(-qOrder,qOrder):
#    for j in range(-qOrder,qOrder):
#      for k in range(-qOrder,qOrder):
#        qxy = (kxy + np.array([i,j,k])) % np.array([nkx,nky,nkz])
#        iq = qxy[0]*nky*nkz + qxy[1]*nkz + qxy[2]
#        #susp[i,j,k] = susFunc(eigValueAllK,ik,iq,Ef,T)
#        pass
#print susp

#if __name__ == "__main__":
#  nkx = 12
#  nky = 12
#  nkz = 1
#  # Read the structure information from POSCAR
#  from ase.io import read
#  atoms = read('POSCAR')  
#  # Generate K points, 
#  # Selection: Monkhorst-Pack or Line-Mode
#  grid = np.array([nkx,nky,nkz],dtype=int)
#  kpts = getMPKpts(atoms,grid)
#  #kpts = getBandKpoints(atoms,npoints=50)
#  x, v, u = calculateEigenPairs(kpts)
#  plotBands(x, v)
#  plotKpoints(kpts)