#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu
#-----------------------------------------------------------------------------
def action(index,folder):
  ls = ['-','--','-.','-:']
  pu.plotExcitation(axs[0])
  pu.plotTotalEnergy(axs[1])
  #------------------------------------------------------------------------------
  
if __name__ == '__main__':
  fig, axs = plt.subplots(1,2,sharex=True,sharey=False,figsize=(10,6))
  #axs = axs.flatten()
  SaveName = __file__.split('/')[-1].split('.')[0]
  c = ['b','r','g','y']
  plt.style.use('ggplot')
  #action(1,'')
  from pyramids.plot.PlotUtility import scanFolder
  scanFolder(action)
  plt.tight_layout()
  if False:
    for save_type in ['.pdf','.png']:
      filename = SaveName + save_type
      plt.savefig(filename,dpi=600)