#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu




#------------------------------------------------------------------------------
exe = dP.readEigFile(filename = 'siestapump.EIG')
eig = dP.readEigFile(filename = 'siesta.EIG')

homo = dP.getHomo()
kpath = []
cut = [0]
specialKPoints = [r'$M$',r'$\Gamma$',r'$K$',r'$\Gamma$']
for i in range(172,8,-19):
  kpath.append(i)
cut.append(len(kpath))
for i in range(18,103,17):
  kpath.append(i)
  kpath.append(i-1)
cut.append(len(kpath))
for i in range(103,163,20):
  kpath.append(i)
  kpath.append(i+1)
cut.append(len(kpath))

kpath = np.array(kpath) - 1
evolvingBands = range(0, homo + 10)
x = np.arange(kpath.shape[0])

excited = exe[kpath,:]
eigenvalue = eig[kpath,:]

fig, ax = plt.subplots(1,1,sharex=True,sharey=False,figsize=(8,6))
SaveName = __file__.split('/')[-1].split('.')[0] 
norm = 300
#print x.shape, excited.shape, eig.shape

for i in evolvingBands:
  part = excited[:,i]
  if np.mean(excited[:,i]) < 0:
    color = 'b'
  else:
    color = 'r'
    
  s = ax.fill_between(x, eig[kpath,i] - norm*part, eig[kpath,i] + norm*part,
                      lw=0.0,color=color,alpha=0.7)
  ax.plot(x, eig[kpath,i],'--',lw=1.5,c='grey')

plt.axis('tight')                
kargs=ma.getPropertyFromPosition(ylabel=r'Eigenvalues(eV)',
                                 xlabel='',xticks=cut,
                                 xticklabels=specialKPoints,
                                 xlimits=[cut[0],cut[-1]],
                                 vline=cut,
                                 title='Population',
                                 hline=[0.0],)
                               #xlimits=[np.min(time),np.max(time)],
                               #ylimits=[np.min(eigen[:,kpt,evolvingBands]),
                               #         np.max(eigen[:,kpt,evolvingBands])])             
ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=400)
