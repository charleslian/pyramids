#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
#-----------------------------------------------------------------------------
def action(index,folder):
  time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure(ave=True)
  return folder, E_ks

if __name__ == '__main__':
  fig, ax = plt.subplots(1,1,sharex=True,sharey=False,figsize=(10,6))
  SaveName = __file__.split('/')[-1].split('.')[0]
  c = ['b','r','g','y']
  plt.style.use('ggplot')
  #action(1,'')
  from pyramids.plot.PlotUtility import scanFolder
  
  data = scanFolder(action)
  ref = np.load('ref.npy')
  deltaEnergy = np.array([np.average(np.abs(energy - ref)) for folder, energy in data])
  ax.semilogy(deltaEnergy,'-o',lw=3)
  xticks = [folder for folder, energy in data]
  
  kargs=ma.getPropertyFromPosition(ylabel=r'E(eV)',title=r'$\Delta$ Gauge', xticklabels = xticks)
  ma.setProperty(ax,**kargs)
  
  plt.tight_layout()
  for save_type in ['.pdf','.png']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=800)