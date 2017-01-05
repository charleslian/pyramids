# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 09:31:02 2016

@author: cl-iop
"""

from ase.io.cube import read_cube_data
from ase.io import write
from ase.visualize import view
from ase.data import covalent_radii
from ase.data.colors import cpk_colors


import numpy as np
from mayavi import mlab
    
def plot(atoms, data, contours, index):
    """Plot atoms, unit-cell and iso-surfaces using Mayavi.
    
    Parameters:
        
    atoms: Atoms object
        Positions, atomiz numbers and unit-cell.
    data: 3-d ndarray of float
        Data for iso-surfaces.
    countours: list of float
        Contour values.
    """
    
    # Delay slow imports:
    from mayavi import mlab

    mlab.figure(1, bgcolor=(1, 1, 1))  # make a white figure

    # Plot the atoms as spheres:
    for pos, Z in zip(atoms.positions, atoms.numbers):
        mlab.points3d(*pos,
                      scale_factor=covalent_radii[Z],
                      resolution=20,
                      color=tuple(cpk_colors[Z]))

    # Draw the unit cell:
    A = atoms.cell
    for i1, a in enumerate(A):
        i2 = (i1 + 1) % 3
        i3 = (i1 + 2) % 3
        for b in [np.zeros(3), A[i2]]:
            for c in [np.zeros(3), A[i3]]:
                p1 = b + c
                p2 = p1 + a
                mlab.plot3d([p1[0], p2[0]],
                            [p1[1], p2[1]],
                            [p1[2], p2[2]],
                            tube_radius=0.1)

    cp = mlab.contour3d(data, contours=contours, transparent=True,
                        opacity=1, colormap='hot')
    # Do some tvtk magic in order to allow for non-orthogonal unit cells:
    polydata = cp.actor.actors[0].mapper.input
    pts = np.array(polydata.points) - 1
    # Transform the points to the unit cell:
    polydata.points = np.dot(pts, A / np.array(data.shape)[:, np.newaxis])
    
    # Apparently we need this to redraw the figure, maybe it can be done in
    # another way?
    mlab.view(azimuth=155, elevation=70, distance='auto')
    # Show the 3d plot:
    mlab.show()
    
dataAndAtoms = [read_cube_data(str(i)+'/siesta.RHO.cube') for i in range(5,155,30)]
for index, image in enumerate(dataAndAtoms): 
  #if index == 0:
  #  pho0, atoms0 = dataAndAtoms[0]
  #else:
  pho, atoms = image
  data = (pho)
  write(str(index)+'.cube',atoms,data=data)
  lowBound = data.min() 
  upBound  = data.max()
  plot(atoms,data,[-0.007],index)

  