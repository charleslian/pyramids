import numpy as np
from pyramids.plot.setting import getPropertyFromPosition, setProperty
import pyramids.io.result as dp
import pyramids.plot.PlotUtility as pu
import matplotlib.pyplot as plt


def action(index, folder):
  ax = axs[0]
  gap= axs[1]
  from ase.calculators.siesta.import_functions import xv_to_atoms
  atoms = xv_to_atoms('siesta.XV')
  import pyramids.plot.PlotUtility as pu
  
  pu.plot2DBZ(ax,atoms)
  pu.plot2DBZ(gap,atoms)
  eigSteps = dp.getEIGSteps()
  initStep, finalStep = eigSteps[0],eigSteps[-1]
  print initStep, finalStep
  energy = dp.readEigFile('siesta'+str(finalStep)+'.EIG')
  popStart = dp.readEigFile('siesta'+str(finalStep)+'q.EIG') 
  popEnd = dp.readEigFile('siesta'+str(initStep)+'q.EIG')
  part  = np.abs(popStart - popEnd)
  plotted = part[:,3]
  plotted[plotted < 0.1*np.max(plotted)] = 0.0
  norm = 100.0
  kcoor, kweight = dp.readKpoints()
  kcoorAll, klistAll = dp.recoverAllKPoints(kcoor,2*np.pi*atoms.get_reciprocal_cell(),
                                            repeat = [1,1,0], flatten = False)
  diffEnergy = energy[:,4] - energy[:,3]
  outRange = np.ones(diffEnergy.shape)*20
  outRange[diffEnergy > 4.5] = 0.0 
  
  for k in kcoorAll:
    ct1 = ax.scatter(k[:,0], k[:,1], norm*plotted, color = colors[index], marker='h',
                    alpha=1.0, lw=0.0)
    ct2 = gap.scatter(k[:,0], k[:,1], outRange, cmap=cmap, c=diffEnergy, 
                      vmin = 1.0, vmax = 5.0, marker='h', alpha=1.0, lw=0.00)
  ax.scatter([], [], 60, color = colors[index], label=folder, alpha=1.0, lw=0.0)   
  if index ==0 :
    #plt.colorbar(ct2,ax=ax,extendrect=False)
    plt.colorbar(ct2,ax=gap,extendrect=False)
    


fig, axs = plt.subplots(1,2,figsize=(10,5),sharex=True,sharey=True)
SaveName = __file__.split('/')[-1].split('.')[0]
cmap = 'gist_rainbow'
colors = 'b', 'lime', 'yellow', 'r'
pu.scanFolder(action)  
setProperty(axs[0],**getPropertyFromPosition(0, title='Excitation', xticklabels=[], yticklabels=[],
            #xlabel=r'$k_x (\AA^{-1})$', ylabel="$k_y (\AA^{-1})$",
            ))
setProperty(axs[1],**getPropertyFromPosition(1, title='Energy Difference', 
            xlimits=[-2,2], ylimits=[-2,2], xticklabels=[], yticklabels=[],
            #xlabel=r'$k_x (\AA^{-1})$', ylabel="$k_y (\AA^{-1})$",
            ))
# --------------------------------------Final----------------------------------   

plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename, orientation='portrait',dpi=600)