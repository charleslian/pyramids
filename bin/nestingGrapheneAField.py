import numpy as np
from pyramids.plot.setting import getPropertyFromPosition, setProperty
import pyramids.io.result as dp
import pyramids.plot.PlotUtility as pu
import matplotlib.pyplot as plt


fig, ax = plt.subplots(1,1,figsize=(8,8))
SaveName = __file__.split('/')[-1].split('.')[0]
cmaps = 'hsv', 'hsv', 'hsv'
colors = 'b', 'g', 'r'

def action(index, folder):
  from ase.calculators.siesta.import_functions import xv_to_atoms
  atoms = xv_to_atoms('siesta.XV')
  import pyramids.plot.PlotUtility as pu
  pu.plot2DBZ(ax,atoms)
  eigSteps = dp.getEIGSteps()
  initStep, finalStep = eigSteps[0],eigSteps[-1]
  energy = dp.readEigFile('siesta'+str(finalStep)+'.EIG')
  popStart = dp.readEigFile('siesta'+str(finalStep)+'q.EIG') 
  popEnd = dp.readEigFile('siesta'+str(initStep)+'q.EIG')
  part  = np.abs(popStart - popEnd)
  #plotted = np.array([value for value in part[:,3] if value > 0.00001])
  plotted = part[:,3]
  #print plotted
  norm = 100.0#/np.max(plotted)
  kcoor, kweight = dp.readKpoints()
  kcoorAll, klistAll = dp.recoverAllKPoints(kcoor,2*np.pi*atoms.get_reciprocal_cell(),
                                            repeat = [1,1,0], flatten = False)
#  kcoorAll = kcoorAll.reshape([kcoor.shape[0], kcoorAll.shape[0]/kcoor.shape[0], 3])
#  print kcoorAll
  diffEnergy = energy[:,4] - energy[:,3]
  for k in kcoorAll:
    ct = ax.scatter(k[:,0], k[:,1], norm*plotted, cmap=cmaps[index], 
               c=diffEnergy, vmin = 0, vmax = 6.0,  alpha=1.0, lw=0.00)
    
  if index ==0 :
    plt.colorbar(ct,ax=ax)
  

  

pu.scanFolder(action) 

setProperty(ax,**getPropertyFromPosition())
# --------------------------------------Final----------------------------------   
plt.axis('equal')
plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  #plt.savefig(filename,orientation='portrait',dpi=600)