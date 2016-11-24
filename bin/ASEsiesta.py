#/usr/bin/python
"""
Created on Fri Jul 22 09:54:42 2016
@author: Chao (Charles) Lian
@email: Charleslian@126.com
"""
import ase.calculators.siesta.import_functions as sinter
import ase.calculators.vasp as vinter
from ase.visualize import view
import dataProcess as dp

atoms = sinter.xv_to_atoms('siesta.XV')
dp.writeSiesta('structure.fdf',atoms)
view(atoms)