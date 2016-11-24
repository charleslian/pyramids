import numpy as np
from ase.calculators.siesta.import_functions import xv_to_atoms
import pandas as pd 
import pyramids.io.result as dp

class snapshot():
  from ase.dft.kpoints import special_paths
  from ase.dft.kpoints import get_special_points, get_bandpath
  atoms = dp.getStructrue()
  points = get_special_points('Orthorhombic', atoms.cell)
  specialKPoints = 'GSXGY'
  cut, data = dp.findBandPath(atoms,points,specialKPoints)
  #print data
  kpath = np.array(data.values[:,1],dtype=int)
  #print kpath
  selectedTimeStep = [0, 197, 447, 997]
  x = data.values[:,2]
  norm = 1000
  drawfill = False
  ylimits = [-5, 5]

  
  
norm = 2000.0
drawfill = False


lines = [(301,12),(12,185),(185,289)]

class selectedKPoints():
  kSet = np.array([12,  94, 237]) - 1
  ylimits = [-10, 25]
  names = [r'$\Gamma$',r'$K_1$',r'$K_2$']
  norms = [50.0, 5, 5.0, 10, 10.0, 10, 10.0, 10, 10.0]