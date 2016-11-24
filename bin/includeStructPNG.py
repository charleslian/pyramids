#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu


  
#------------------------------------------------------------------------------
fig, ax = plt.subplots(1,1,sharex=True,sharey=False,figsize=(8,6))
SaveName = __file__.split('/')[-1].split('.')[0]

kargs=ma.getPropertyFromPosition(ylabel=r'Eigenvalues(eV)',
                                 title='Population')


                
ma.setProperty(ax,**kargs)

#------------------------------------------------------------------------------
plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)