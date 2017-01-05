from ase.calculators.siesta.import_functions import xv_to_atoms
from ase.visualize import view
import pyramids.io.output as tdio
import pyramids.io.result as dp
from ase.io import write
import os
import numpy as np
import matplotlib.pyplot as plt


def findBandPath(atoms, points, kLine):
  reciprocal_vectors = 2*np.pi*atoms.get_reciprocal_cell()
  if os.path.exists('input.fdf'):
    kcoor, kweight = readKpoints()
    kall, klist = recoverAllKPoints(kcoor, reciprocal_vectors)
    #ax.plot(kcoor[:,0], kcoor[:,1],'o')
    #ax.plot(kall[:,0], kall[:,1],'.')
    
  selectedPoints = [(points[name], name) for name in kLine]
  
  lines = [(selectedPoints[i],selectedPoints[i+1]) 
            for i in range(len(selectedPoints) - 1)] 
  kpath = []     
  import pandas as pd
  
  last = 0.0
  xticks = []
  xticks.append(last)
  for a, b in lines:
    coorA = np.dot(a[0],reciprocal_vectors)
    coorB = np.dot(b[0],reciprocal_vectors)
    #ax.plot(coorB[0], coorB[1],'or',ms=20)
    #ax.plot(coorA[0], coorA[1],'or',ms=20)
    reVect =  coorB - coorA
    kpath_alongAB = []
    
    for index, (k, ucellK) in enumerate(zip(kall, klist)):
      vect = k - coorA
      normVect = np.linalg.norm(vect)
      normReVect = np.linalg.norm(reVect)
      normProd = np.linalg.norm(vect)*np.linalg.norm(reVect)
      dotProd = np.dot(reVect, vect)
      if np.abs(dotProd - normProd) < 0.001 and normVect < normReVect:
        kpath_alongAB.append((index, ucellK, normVect + last))
    last += normReVect
    xticks.append(last)
    kpath.extend(kpath_alongAB)
   
  kpath = pd.DataFrame(kpath, columns=['sc-index','uc-index','distance'])
  kpath = kpath.sort_values(['distance'])
  #kpts = np.array(kpath.values[:,0],dtype=int)

  #kpath.to_csv('selectedKPath.csv')
  
  return xticks, kpath
#  fig, ax = plt.subplots(1,1,figsize=(5,8))
#  ax.plot(kall[kpts,0], kall[kpts,1],'-o',label=str(i))


