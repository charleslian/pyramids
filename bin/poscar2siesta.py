#!/usr/bin/python

import numpy as np
from phonopy.structure.atoms import Atoms
from phonopy.interface.vasp import write_vasp
from phonopy.interface.vasp import read_vasp
from dataProcess import writeSiesta

atoms=read_vasp('POSCAR')
writeSiesta('siesta_from_POSCAR',atoms)