import numpy as np
from pyramids.plot.setting import getPropertyFromPosition, setProperty
import pyramids.io.result as dp
import pyramids.plot.PlotUtility as pu
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(10,5))
axs = [plt.subplot2grid((1,15), (0, 0), rowspan=1, colspan=7), 
       plt.subplot2grid((1,15), (0, 7), rowspan=1, colspan=7),
       plt.subplot2grid((1,15), (0, 14), rowspan=1, colspan=1)]#

def action(index, folder):

  ax, gap, cb = axs    
  from ase.calculators.siesta.import_functions import xv_to_atoms
  atoms = xv_to_atoms('siesta.XV')
  import pyramids.plot.PlotUtility as pu
  
  pu.plot2DBZ(ax,atoms)
  pu.plot2DBZ(gap,atoms)
  eigSteps = dp.getEIGSteps()
  initStep, finalStep = eigSteps[0],eigSteps[-1]
  #print initStep, finalStep
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
  ax.scatter([], [], 60, color = colors[index], label=folder, alpha=1.0, lw=0.0)   
  for k in kcoorAll:
    ct1 = ax.scatter(k[:,0], k[:,1], norm*plotted, color = colors[index], marker='h',
                    alpha=1.0, lw=0.0)
    pass
  if index == 0:               
    for k in kcoorAll:              
      ct2 = gap.scatter(k[:,0], k[:,1], outRange, cmap=cmap, c=diffEnergy, 
                        vmin = 1.0, vmax = 5.0, marker='h', alpha=1.0, lw=0.00)
      pass                      
    plt.colorbar(ct2,ax=gap,cax=cb, extendrect=False,format='%3.1f eV')
  ax.annotate('M\'',xy=(1.55,0),fontsize='xx-large')
  ax.plot([1.48,1.48], [0,0], 'ok')
  
  ax.annotate('M\'',xy=(-1.75,0),fontsize='xx-large')
  ax.plot([-1.48,-1.48], [0,0], 'ok')
  
#fig, axs = plt.subplots(1,2,figsize=(8,4),sharex=True,sharey=True)
SaveName = __file__.split('/')[-1].split('.')[0]
cmap = 'gist_rainbow'
colors = 'r', 'yellow',  'lime',  'b',
pu.scanFolder(action)  
setProperty(axs[0],**getPropertyFromPosition(0, legendLoc=10, title='Excitation', 
            xlimits=[-2,2], ylimits=[-2,2], #xticklabels=[], #yticklabels=[],
            #xlabel=r'$k_x (\AA^{-1})$', ylabel="$k_y (\AA^{-1})$",
            ))
setProperty(axs[1],**getPropertyFromPosition(1,title='Energy Difference', 
            xlimits=[-2,2], ylimits=[-2,2],  yticklabels=[], #xticklabels=[],
            #xlabel=r'$k_x (\AA^{-1})$', ylabel="$k_y (\AA^{-1})$",
            ))
# --------------------------------------Final----------------------------------   

plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename, orientation='portrait',dpi=600)