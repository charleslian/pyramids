#/usr/bin/python
from ase.calculators.siesta.import_functions import xv_to_atoms
from ase.visualize import view
import pyramids.io.output as tdio
from ase.io import write

atoms = xv_to_atoms('siesta.XV')
import numpy as np
#atoms.rotate([1,0,0],-0.5*np.pi,rotate_cell=True)
#atoms.pbc = [True, True, True]
#ase.build.niggli_reduce(atoms)
#
#tdio.writeQE('structure.in',atoms)
#write('struture.pdb',atoms,format='pdb')

atomsSC = atoms*[1,1,10]
position = atomsSC.get_positions()
#atomsSC.cell[2,:] += 10
#atomsSC.position = position
view(atomsSC)
write('POSCAR',atomsSC)
tdio.writeSiesta('structure.fdf',atomsSC)