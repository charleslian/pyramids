#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
#-----------------------------------------------------------------------------
def action(index,folder):
  ls = ['-','-','-','-']
  ax = axs[0]
  time, Efield = dP.getEField()
  #directions = ['x', 'y', 'z']
  for direct in range(3):
    if max(Efield[:,direct]) > 1E-10:
      ax.plot(time,Efield[:,direct],
              label=folder,lw=2,alpha=0.5) 
  kargs=ma.getPropertyFromPosition(ylabel=r'$\varepsilon$(a.u.)',xlabel='Time(fs)',
                                   title='Electric Field')
  ma.setProperty(ax,**kargs)
  ax.ticklabel_format(style='sci',axis='y',scilimits=[0,0])
  #------------------------------------------------------------------------------
  ax = axs[1]
  time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure(ave=True)
#  for i in range(2,E_ks.shape[0]-1):
#    if E_ks[i+1] - (E_ks[i] + E_ks[i-1])*0.5 > 2.0:
#      E_ks[i+1] = (E_ks[i] + E_ks[i-1])*0.5
  ax.plot(time[2:], E_ks[2:] - E_ks[2],'.', lw=2, alpha=0.5, label=folder)
  kargs=ma.getPropertyFromPosition(ylabel=r'E(eV)',title='Excitation Energy')
  ma.setProperty(ax,**kargs)
  #------------------------------------------------------------------------------

if __name__ == '__main__':
  fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(10,6))
  SaveName = __file__.split('/')[-1].split('.')[0]
  c = ['b','r','g','y']
  plt.style.use('ggplot')
  #action(1,'')
  from pyramids.plot.PlotUtility import scanFolder
  scanFolder(action)
  plt.tight_layout()
  for save_type in ['.pdf','.png']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=800)