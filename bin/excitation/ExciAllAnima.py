import numpy as np
from pyramids.plot.setting import getPropertyFromPosition, setProperty
import pyramids.io.result as dp
import pyramids.plot.PlotUtility as pu
import matplotlib.pyplot as plt


fig, ax = plt.subplots(1,1,figsize=(8,8))
SaveName = __file__.split('/')[-1].split('.')[0]
color = 'b', 'r', 'g'
def action(index, folder):
  from ase.calculators.siesta.import_functions import xv_to_atoms
  atoms = xv_to_atoms('siesta.XV')
  import pyramids.plot.PlotUtility as pu
  pu.plot2DBZ(ax,atoms)
  eigSteps = dp.getEIGSteps()
  initStep, finalStep = eigSteps[0],eigSteps[-1]
  #eigenvalue = dp.readEigFile('siesta'+str(finalStep)+'.EIG')
  part  = np.abs(dp.readEigFile('siesta'+str(finalStep)+'q.EIG') - dp.readEigFile('siesta'+str(initStep)+'q.EIG'))
  norm = 100.0/max(part[:,3])
  kcoor, kweight = dp.readKpoints()
  kcoorAll, klistAll = dp.recoverAllKPoints(kcoor,2*np.pi*atoms.get_reciprocal_cell(),repeat = [1,1,0])
  #evolvingBands = range(3,5)
  ax.scatter(kcoorAll[:,0], kcoorAll[:,1], s=norm*np.abs(part[:,3]),lw=0.0, color= color[index], label=folder)


pu.scanFolder(action) 
setProperty(ax,**getPropertyFromPosition())
# --------------------------------------Final----------------------------------   
plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  #plt.savefig(filename,orientation='portrait',dpi=600)