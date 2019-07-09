# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 14:28:56 2017

@author: cl-iop
"""

import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu

import numpy as np
from ase.atoms import Atoms, Atom
from ase import units
from ase.calculators.singlepoint import SinglePointCalculator
from ase.utils import basestring



images = dp.read_espresso_out('result')
#print images.pop(0)

from ase.visualize import view
from ase.io import read, write
polar = [atom.positions[1,:] - atom.positions[0,:] for atom in images]
polar = np.array(polar)

#view(images)
#print images[-1]


atoms = images[-1]
print images

print atoms.positions
#atoms.positions[:,2]+=0.29694265
#print atoms.positions[:,2]

from pyramids.io.output import writeQE

for s, line in zip(atoms.get_chemical_symbols(), atoms.get_scaled_positions()):
  print s, line
#print atoms.get_positions()

write('final.xsf',atoms)
writeQE('struct.part',atoms)

