import ase.build as ab
from pyramids.io.output import writeSiesta
from ase.visualize import view

atom = ab.mx2()
view(atom)
writeSiesta('structure.fdf',atom)