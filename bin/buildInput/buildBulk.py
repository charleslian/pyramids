# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 10:44:16 2016

@author: cl-iop
"""

from ase.build import molecule
import os
import numpy as np
from ase.visualize import view
from pyramids.io.output import writeSiesta
Name = 'NO2' 

# Sodium dime
atoms = molecule(Name)
atoms.center(vacuum=8)
atoms.positions -= atoms.positions[0]
#atoms.cell = np.array([[8,0,0],[0,8,0],[0,0,8]])
view(atoms)
writeSiesta('structure.fdf',atoms)