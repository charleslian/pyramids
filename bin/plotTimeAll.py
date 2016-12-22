#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
from pyramids.plot.PlotUtility import scanFolder

def getTime(index, folder):
#------------------------------------------------------------------------------
  time = dP.getTime()
  return index, folder,time
  
def getEnergy(index,folder):
  time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure(ave=True)
  return index, folder, E_ks
#------------------------------------------------------------------------------
def case(indexCase, folderCase):
  data = scanFolder(getTime)
  selectedProcesses = ['evolve','DHSCF','PostSCF','siesta'] #,'TDbuildD'
  explainations = ['Propagation', 'Build H', 'Postprocess','Total'] #,'Build DM'
  image = data[-1][-1]['Prg.tot']
  pieData = image[selectedProcesses[:-1]]
  other = image[selectedProcesses[-1]] - np.sum(pieData.values)
  
  ax = axsall[1][indexCase]
  explode = np.zeros(len(pieData)) + 0.04
  explode[0]  = 0.07
  patches, texts, autotexts = ax.pie(pieData.values, explode=explode, labels=explainations[:-1], 
                                     labeldistance = 0.2, autopct='%.0f%%',pctdistance = 0.7,
                                     shadow=True, textprops={'fontsize':'xx-large','color':'gold'})
  for text in texts:
    text.set_fontsize(0) 
    
  kargs=ma.getPropertyFromPosition(indexCase + 3, title='')
  ma.setProperty(ax,**kargs) 
  
  for key,label in zip(selectedProcesses,explainations):
    totalTimes = np.array([time['Prg.tot'][key] for index, folder, time in data])/3600.0
    situations = [int(folder) for index, folder, time in data]
    ax = axsall[0][indexCase]
    ax.semilogy(situations, totalTimes,'-o', ms=12, label = label)
  
  ax.grid(which='Both',axis=u'y')
  kargs=ma.getPropertyFromPosition(indexCase, ylabel=r'Clock Time (hour)',title=folderCase)
  ma.setProperty(ax,**kargs)
  
fig, axsall = plt.subplots(2,3,sharex=False,sharey='row',figsize=(15,10))
print axsall
SaveName = __file__.split('/')[-1].split('.')[0]

scanFolder(case)

plt.tight_layout()
for save_type in ['.pdf','.eps']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)