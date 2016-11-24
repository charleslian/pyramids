#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu
import matplotlib

matplotlib.style.use('ggplot')



#------------------------------------------------------------------------------
time, exe = dP.getProjectedPartition()
time, eigen = dP.getAdiabaticEigenvalue()

#print eigen[:,1,:]
#homo = dP.getHomo()
#print homo
print exe.shape, eigen.shape
c = ma.getColors(exe.shape[2], cmap='brg')

norm = 50.0#/np.max(exe[:,:,:] -  exe[0,:,:])
#print norm
kpts = [0]
for kpt in kpts:
  fig, ax = plt.subplots(1,1,sharex=True,sharey=False,figsize=(8,6))
  SaveName = __file__.split('/')[-1].split('.')[0] + str(kpt)
  homo = 0
  for i, band in enumerate(eigen[0,kpt,:]):
    #print band
    if band < 0:
      homo = i
      
  evolvingBands = range(0, homo+40)
  X, Y = np.meshgrid(time,eigen[0,kpt,evolvingBands])
  Z = np.transpose(exe[0,kpt,evolvingBands] - exe[:,kpt,evolvingBands])
  #print Z.shape
  
  ct = ax.contourf(X, Y, Z, 100, cmap='coolwarm', alpha = 1.0)
  plt.colorbar(ax=ax,mappable=ct)
#  for i in evolvingBands:
#    if np.mean(eigen[:,kpt,i]) < 0.0:
#      part = abs(exe[0,kpt,i] - exe[:,kpt,i]) 
#      s = ax.fill_between(time, eigen[:,kpt,i] - norm*part, 
#                               eigen[:,kpt,i] + norm*part
#                               ,lw=0.0,color='b',alpha=0.7)
#    else:
#      part = abs(exe[0,kpt,i] - exe[:,kpt,i]) 
#      s = ax.fill_between(time, eigen[:,kpt,i] - norm*part, 
#                               eigen[:,kpt,i] + norm*part
#                               ,lw=0.0,color='r',alpha=0.7)     
  ax.plot(time,eigen[:,kpt,evolvingBands], '-',lw=0.2, c='k' ,alpha=0.8)
    
  
  #print exe[-1,kpt,:]
#  axin, imag = pu.insertStruct(ax, width="50%", height=1.5, loc=2, 
#                               rotation=[0,0,0], 
#                               camera='perspective', cell=True)
                  
  kargs=ma.getPropertyFromPosition(ylabel=r'Eigenvalues(eV)',
                                   xlabel='Time(fs)',
                                   title='Population',
                                   hline=[0.0],
                                   xlimits=[np.min(time),np.max(time)],
                                   ylimits=[np.min(eigen[:,kpt,evolvingBands]),
                                            np.max(eigen[:,kpt,evolvingBands])])             
  ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
  plt.tight_layout()
  for save_type in ['.pdf']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=400)
