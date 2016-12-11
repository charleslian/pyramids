#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma
#-----------------------------------------------------------------------------
def action(index,folder):
  ls = ['-','-','-','-']
  ax = axs[0][0]
  time, Efield = dp.getEField()
  #directions = ['x', 'y', 'z']
  for direct in range(3):
    if max(Efield[:,direct]) > 1E-10:
      ax.plot(time,Efield[:,direct],ls=ls[index],
              label=folder,lw=2,alpha=0.5) 
  kargs=ma.getPropertyFromPosition(ylabel=r'$\varepsilon$(a.u.)',xlabel='Time(fs)',
                                   title='Electric Field')
  ma.setProperty(ax,**kargs)
  ax.ticklabel_format(style='sci',axis='y',scilimits=[0,0])
  #------------------------------------------------------------------------------
  ax = axs[1][0]
  time, T, E_ks, E_tot, Vol, P  = dp.getEnergyTemperaturePressure()
#  for i in range(2,E_ks.shape[0]-1):
#    if abs(E_ks[i] - E_ks[i-1]) > 1.0:
#      E_ks[i] = E_ks[i-1]
  ax.plot(time, E_tot - E_tot[0],'-', lw=2, alpha=0.5, label=folder)
  kargs=ma.getPropertyFromPosition(ylabel=r'E(eV)',title='Excitation Energy')
  ma.setProperty(ax,**kargs)
  #------------------------------------------------------------------------------
  ax = axs[0][1]
  dp.getTrajactory()
  import pyramids.process.struct as pps
  time, distance = pps.calculateRMSD()
  ax.plot(time, distance, lw=3)
  kargs=ma.getPropertyFromPosition(xlabel='Time (fs)', ylabel=r'$\langle u \rangle^\frac{1}{2}$ ($\AA$)', 
                                   title='RMSD')
  ma.setProperty(ax,**kargs)
  #------------------------------------------------------------------------------
  ax = axs[1][1]
  time, T, E_ks, E_tot, Vol, P  = dp.getEnergyTemperaturePressure()
  ax.plot(time, T, lw=3, label=folder)
  kargs=ma.getPropertyFromPosition(xlabel='Time (fs)', ylabel=r'T (K)', 
                                   title='Temperature')
  ma.setProperty(ax,**kargs)
  
if __name__ == '__main__':
  fig, axs = plt.subplots(2,2,sharex=True,sharey=False,figsize=(10,6))
  #axs = axs.flatten()
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