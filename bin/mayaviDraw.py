# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 10:12:28 2016

@author: cl-iop
"""
from ase.io.cube import read_cube_data
from ase.io import write
from ase.visualize import view


from ase.calculators.siesta.import_functions import xv_to_atoms
atoms = xv_to_atoms('siesta.XV')
unitcell = atoms.cell 
superAtoms = atoms#*(2,2,1)
#view(atoms)
superAtoms.cell = unitcell
#superAtoms.positions -= 0.5*(unitcell[0,:] + unitcell[1,:] )

rot = '90x,0y,00z'  # found using ag: 'view -> rotate'

kwargs = {
    'rotation'      : rot, # text string with rotation (default='' )
    'radii'         : 1.0, # float, or a list with one float per atom
    'colors'        : None,# List: one (r, g, b) tuple per atom
    'show_unit_cell': 0,   # 0, 1, or 2 to not show, show, and show all of cell
    }
    
kwargs.update({
    'run_povray'   : True, # Run povray or just write .pov + .ini files
    'display'      : True,# Display while rendering
    'pause'        : True, # Pause when done rendering (only if display)
    'transparent'  : True,# Transparent background
    'canvas_width' : None, # Width of canvas in pixels
    'canvas_height': 800, # Height of canvas in pixels 
    'camera_dist'  : 120.,  # Distance from camera to front atom
    'image_plane'  : 0, # Distance from front atom to image plane
    'camera_type'  : 'perspective', # perspective, ultra_wide_angle, orthographic
    'point_lights' : [],             # [[loc1, color1], [loc2, color2],...]
    'area_light'   : [(2., 3., 40.), # location
                      'White',       # color
                      .7, .7, 3, 3], # width, height, Nlamps_x, Nlamps_y
    'background'   : 'White',        # color
    'textures'     : None, # Length of atoms list of texture names
    'celllinewidth': 0.1,  # Radius of the cylinders representing the cell
    })
write('struct.pov',superAtoms*(1,1,1), **kwargs)

