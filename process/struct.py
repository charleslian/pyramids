# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import os
from pyramids.io.fdf import tdapOptions
from pyramids.io.result import getTrajactory
from pyramids.io.result import loadSaved
#-------------------------------------------------------------------
def calculateRMSD(selectedStep=None,atomsOrigin=None,init=0, selectedAtoms=None):
  """ 
  return the radius mean square displacements of the selected steps 
  compared with the init step
  """
  from ase.io.trajectory import Trajectory
  traj = Trajectory("Trajectory")
  options = tdapOptions()
  
  timestep = options.mdTimeStep[0]
  if atomsOrigin is None:
    atomsOrigin = traj[init]
    #print 'no'
  if selectedStep == None:
    selectedStep = range(len(traj))
  #print  selectedStep, timestep
  time = np.array(selectedStep) * timestep

  SaveName = 'RMSD'
  distance = loadSaved(SaveName)

  if len(distance) != len(selectedStep):
    #print 'Calculation'
    distance = np.array([np.mean(calculateDisplacement(traj[step],atomsOrigin,selectedAtoms)**2)**0.5
                for step in selectedStep])
    np.save(SaveName,distance)
  return time,distance
  
#-------------------------------------------------------------------
def calculateDisplacement(atoms,atomsOrigin, selectedAtoms=None):
  """ 
  return the displacements as a dimension of Natoms
  """
  if selectedAtoms == None:
    selectedAtoms = range(atomsOrigin.get_number_of_atoms())
    
  return np.array([
          np.min([np.linalg.norm(atoms.get_positions()[index] - 
                  atomsOrigin.get_positions()[index] + np.dot([i,j,k],atoms.get_cell())) 
                  for i in range(-1,2) 
                  for j in range(-1,2) 
                  for k in range(-1,2)
                  ])
          for index in selectedAtoms])
#-------------------------------------------------------------------  
def calculateRDF(step, b = 98, lb = 0.1, hb = 5.0):
  """ 
  return the radius distribution function of a certain step
  calculate the histogram, devide bins segments between lowbound and highbound
  """
  from ase.io.trajectory import Trajectory
  traj = Trajectory("Trajectory")
  
  atoms = traj[step]
  SaveName = 'RDF' + str(step)
  hist = loadSaved(SaveName+'hist')
  bin_edges = loadSaved(SaveName+'bin_edges')
  if len(hist) == 0 or os.path.getmtime(SaveName+'hist.npy') < os.path.getmtime('Trajectory'):
    bondLength = atoms.get_all_distances(mic=True).flatten()
    hist,bin_edges = np.histogram(bondLength,bins=b,range=(lb,hb))
    np.save(SaveName+'hist',hist)
    np.save(SaveName+'bin_edges',bin_edges)
  return hist,bin_edges 
   
#-------------------------------------------------------------------
if __name__ == '__main__':        
  import matplotlib.pyplot as plt
  
  fig,ax=plt.subplots(2,1)
  time,distance = calculateRMSD()
  ax[0].plot(time,distance,linewidth=3.0,label='RMSD')
  
  hist,bin_edges = calculateRDF(500,b=3000, hb=2.0,lb=0.8)
  ax[1].plot(bin_edges[:-1],hist)
