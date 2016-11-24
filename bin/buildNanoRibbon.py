# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 16:51:00 2016

@author: cl-iop
"""
from ase.build import graphene_nanoribbon, nanotube
from ase.visualize import view
from pyramids.io.output import writeSiesta

from ase.io.cube import read_cube_data
from ase.io import write

#graphene_nanoribbon() vacuum=0.71
atom = graphene_nanoribbon(6,1,type='armchair',saturated=True,vacuum=5)
writeSiesta('structure.fdf',atom)
view(atom)

rot = '90x,0y,00z'
kwargs = {
    'rotation'      : rot, # text string with rotation (default='' )
    'radii'         : 1.0, # float, or a list with one float per atom
    'colors'        : None,# List: one (r, g, b) tuple per atom
    'show_unit_cell': 2,   # 0, 1, or 2 to not show, show, and show all of cell
    }
kwargs.update({
    'run_povray'   : True, # Run povray or just write .pov + .ini files
    'display'      : True,# Display while rendering
    'pause'        : True, # Pause when done rendering (only if display)
    'transparent'  : True,# Transparent background
    'canvas_width' : None, # Width of canvas in pixels
    'canvas_height': 800, # Height of canvas in pixels 
    'camera_dist'  : 12000.,  # Distance from camera to front atom
    'image_plane'  : 0, # Distance from front atom to image plane
    'camera_type'  : 'perspective', # perspective, ultra_wide_angle, orthographic
    'point_lights' : [],             # [[loc1, color1], [loc2, color2],...]
    'area_light'   : [(2., 3., 40.), # location
                      'White',       # color
                      .7, .7, 3, 3], # width, height, Nlamps_x, Nlamps_y
    'background'   : 'White',        # color
    'textures'     : None, # Length of atoms list of texture names
    'celllinewidth': 0.05,  # Radius of the cylinders representing the cell
    })
    

cell = atom.cell
atom = atom*(1,1,3)
for position in atom.positions:
  position -= cell[2,:]
  
atom.cell = cell
write('struct.pov',atom, **kwargs)
