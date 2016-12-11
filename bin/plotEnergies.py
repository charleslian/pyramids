#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
#-----------------------------------------------------------------------------
def action(index,folder):
  ax = axs[0]
  time, Efield = dP.getEField()
  directions = ['x', 'y', 'z']
  for direct in range(3):
    ax.plot(time,Efield[:,direct],
            label=directions[direct],lw=2,alpha=0.8) 
  kargs=ma.getPropertyFromPosition(ylabel=r'$\varepsilon$(a.u.)',xlabel='Time(fs)',
                                   title='Electric Field')
  ma.setProperty(ax,**kargs)
  ax.ticklabel_format(style='sci',axis='y',scilimits=[0,0])
  #------------------------------------------------------------------------------
  ax = axs[1]
  time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
  ax.plot(time[2:], E_tot[2:,] - E_tot[2],'-', lw=2, alpha=1, label=r'$E_{KS}$')
  kargs=ma.getPropertyFromPosition(ylabel=r'E(eV)',title='Excitation Energy')
  ma.setProperty(ax,**kargs)
  #------------------------------------------------------------------------------

if __name__ == '__main__':
  fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(10,6))
  SaveName = __file__.split('/')[-1].split('.')[0]
  c = ['b','r','g','y']
  plt.style.use('ggplot')
  action(1,'')
  plt.tight_layout()
  for save_type in ['.pdf','.png']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=800)