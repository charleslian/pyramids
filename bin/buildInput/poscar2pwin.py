#/usr/bin/python
from ase.calculators.siesta.import_functions import xv_to_atoms
from ase.visualize import view
import pyramids.io.output as tdio
from ase.io import write, read

atoms = read('POSCAR')
import numpy as np
#atoms.rotate([1,0,0],-0.5*np.pi,rotate_cell=True)
#atoms.pbc = [True, True, True]
#ase.build.niggli_reduce(atoms)
#tdio.writeSiesta('structure.fdf',atoms)
atoms*=[2,2,1]
tdio.writeQE('structure.in',atoms)

write('struture_super.vasp',atoms)
#write('POSCAR',atoms)

#view(atoms*[2,2,2])