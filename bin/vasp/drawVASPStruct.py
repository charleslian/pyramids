#/usr/bin/python
from ase.calculators.siesta.import_functions import xv_to_atoms
from ase.visualize import view
import pyramids.io.output as tdio
from ase.io import write,read

atoms = read('POSCAR')
#view(atoms)

rotation = [-0,0,-30]
repeat = [3,3,1]
cell = True
rot = str(rotation[0])+'x,'+str(rotation[1])+'y,'+str(rotation[2])+'z'

if cell:
  showcell = 1
else:
  showcell = 0
  
  
kwargs = {
    'rotation'      : rot, # text string with rotation (default='' )
    'radii'         : 1.0, # float, or a list with one float per atom
    'colors'        : None,# List: one (r, g, b) tuple per atom
    'show_unit_cell': showcell,   # 0, 1, or 2 to not show, show, and show all of cell
    }
kwargs.update({
  'run_povray'   : True, # Run povray or just write .pov + .ini files
  'display'      : False,# Display while rendering
  'pause'        : True, # Pause when done rendering (only if display)
  'transparent'  : True,# Transparent background
  'canvas_width' : None, # Width of canvas in pixels
  'canvas_height': 800, # Height of canvas in pixels 
  'camera_dist'  : 2000.,  # Distance from camera to front atom
  'image_plane'  : 0, # Distance from front atom to image plane
  'camera_type'  : 'orthographic', # perspective, ultra_wide_angle, orthographic
  'point_lights' : [],             # [[loc1, color1], [loc2, color2],...]
  'area_light'   : [(2., 3., 40.), # location
                    'White',       # color
                    .7, .7, 3, 3], # width, height, Nlamps_x, Nlamps_y
  'background'   : 'White',        # color
  'textures'     : None, # Length of atoms list of texture names
  'celllinewidth': 0.1,  # Radius of the cylinders representing the cell
  })
  
cell = atoms.cell
atoms.center()
atoms = atoms*repeat
for position in atoms.positions: 
  position -= repeat[0]/2*cell[0,:]
  position -= repeat[1]/2*cell[1,:]
  position -= repeat[2]/2*cell[2,:]
atoms.cell = cell
write('struct.pov',atoms, **kwargs)