#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
from pyramids.io.fdf import tdapOptions 
from pyramids.plot.PlotUtility import scanFolder
from ase.calculators.siesta.import_functions import xv_to_atoms
#------------------------------------------------------------------------------
efield = 2
exElectron = 0
exEnergy = 1
start = 2

def action(index, folder):
  timeEn, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
  deltaE = E_ks[start:,] - E_ks[2]
  atoms = xv_to_atoms('siesta.XV')
  return index, folder, timeEn, deltaE, atoms
  
#------------------------------------------------------------------------------
fig, axs = plt.subplots(1,1,sharex='col',sharey='row',figsize=(8,6))
SaveName = __file__.split('/')[-1].split('.')[0]

data = scanFolder(action)
c = ma.getColors(data[-1][0]+1)


for index, folder, timeEn, deltaE, atoms in data:
  #------------------------------------------------------------------------------
  ax = axs
  numAtoms = len(atoms.get_chemical_symbols())
  ax.plot(timeEn[start:], deltaE/numAtoms,'.',alpha=1.0, c=c[index], label=folder+r'$\times$'+folder, ms=8,
          lw=2)
#---------------------------------------
kargs=ma.getPropertyFromPosition(ylabel=r'Energy $E$ (eV/atom)', xlabel='Time $t$ (fs)',
                                 title='')
ma.setProperty(ax,**kargs)

#------------------------------------------------------------------

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)