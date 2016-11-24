# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 13:54:16 2016

@author: cl-iop
"""
from ase.build import molecule, mx2
from ase.collection import g2, s22
from ase.visualize import view
import os
import shutil
from pyramids.io.output import writeSiesta

for name in g2.names:
  atom = molecule(name)
  atom.cell *= 10 
  if os.path.exists(name): 
    shutil.rmtree(name)
  os.mkdir(name)
  os.chdir(name)
  for element in set(atom.get_chemical_symbols()):
    os.popen('siestapot_LDA.sh '+element)
  writeSiesta('structure.fdf',atom)
  os.chdir('..')  

  
#for name in s22.names:
#  #atom = molecule(name)
#  #atom.cell *= 8 
#  print name
#atom = molecule('trans-butane')
#atom = mx2()
#view(atom*(4,4,1))
