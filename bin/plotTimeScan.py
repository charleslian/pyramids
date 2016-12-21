#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
from pyramids.plot.PlotUtility import scanFolder
import matplotlib
matplotlib.style.use('ggplot')
  
def getTime(index, folder):
#------------------------------------------------------------------------------
  time = dP.getTime()
  return index, folder,time
  
def getEnergy(index,folder):
  time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure(ave=True)
  return index, folder, E_ks
#------------------------------------------------------------------------------

fig, axs = plt.subplots(1,3,sharex=False,sharey=False,figsize=(15,6))
SaveName = __file__.split('/')[-1].split('.')[0]
data = scanFolder(getTime)

selectedProcesses = ['siesta','evolve','setup_H','PostSCF'] #,'TDbuildD'
explainations = ['Total','Propagation', 'Build H', 'Postprocess'] #,'Build DM'
image = data[-1][-1]['Prg.tot']
pieData = image[selectedProcesses[1:]]
other = image[selectedProcesses[0]] - np.sum(pieData.values)

print image.sort_values()
one = [i for i in pieData.values]
one.append(other)
ax = axs[2]
explode = np.zeros(len(selectedProcesses)) + 0.04
explode[0]  = 0.1; #explode[1]  = 0.00
patches, texts, autotexts = ax.pie(one, explode=explode, labels=explainations[1:]+['Other'], 
                                   labeldistance = 0.5, autopct='%.0f%%',pctdistance = 0.3,
                                   shadow=True, textprops={'fontsize':'x-large','color':'w'})
for text in texts:
  text.set_fontsize('x-large') 
  text.set_color('k') 

plt.axis('tight')

for key,label in zip(selectedProcesses,explainations):
  totalTimes = np.array([time['Prg.tot'][key] for index, folder, time in data])/3600.0
  situations = [int(folder) for index, folder, time in data]
  ax = axs[1]
  ax.plot(situations, totalTimes,'-o', ms=12, label = label)

kargs=ma.getPropertyFromPosition(ylabel=r'Clock Time (hour)',title='Clock Time')
ma.setProperty(ax,**kargs)

ax = axs[0]
data = scanFolder(getEnergy)
ref = np.load('ref.npy')
deltaEnergy = np.array([np.average(np.abs(energy - ref)) for index, folder, energy in data])
xticks = [int(folder) for index, folder, energy in data]
ax.semilogy(xticks, deltaEnergy,'-o', ms=12)

kargs=ma.getPropertyFromPosition(ylabel=r'$\Delta E$ (eV)', title=r'$\Delta$ Gauge')
ma.setProperty(ax,**kargs)

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)