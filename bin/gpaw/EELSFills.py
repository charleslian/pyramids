import pyramids.io.result as dp
import pyramids.plot.setting as ma
import os
SaveName = __file__.split('/')[-1].split('.')[0]
dirName = os.path.abspath('.').split('/')[-1]
label = dirName.replace('&&','\\').replace('&',' ')

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np

#
#ax = fig.add_subplot(111, projection='3d')

from ase.io import write, read
atoms = read('structure.vasp',format='vasp')
reciprocal_vectors = 2*np.pi*atoms.get_reciprocal_cell()
print reciprocal_vectors

fig, ax = plt.subplots(1,1,figsize=(10,8))

Q, E, Z, X, Y, contour = dp.getEELS()

selectIndex = np.where(E<10)
c = ma.getColors(Q.shape[0])

for i, q in enumerate(Q):
  percent = np.max(Z)*0.02
  if i == 0:
    shift = q*percent
  else:
    shift += q*percent
  
  ax.fill_between(E[selectIndex], Z[i][selectIndex]-shift, -shift, 
                  facecolor=c[i], alpha=1.0, lw=2, zorder=i)
  
#plt.colorbar(ct,ax=ax) 'darkgrey'

from matplotlib.cm import ScalarMappable
cm = ScalarMappable(cmap='jet')
cm.set_array(Q)
plt.colorbar(cm,ax=ax, extend='neither', format='%2.1f $\AA^{-1}$')

args = ma.getPropertyFromPosition(#yticklabels=[],#ylimits=[None,0.2], xlimits=[None,5], 
                                  grid = False,
                                  title='EELS spectra: $%s$' % label,
                                  ylabel=r'q ($\AA^{-1}$)',
                                  xlabel='Energy (eV)')
ma.setProperty(ax,**args)

plt.tight_layout()
for save_type in ['.png','.pdf','.eps']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)