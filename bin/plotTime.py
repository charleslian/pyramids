#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
from pyramids.plot.PlotUtility import scanFolder
import matplotlib
matplotlib.style.use('ggplot')
  
def action(index, folder):
#------------------------------------------------------------------------------
  time = dP.getTime()
  return index, folder,time

#------------------------------------------------------------------------------

fig, axs = plt.subplots(1,2,sharex=False,sharey=False,figsize=(12,6))
SaveName = __file__.split('/')[-1].split('.')[0]
data = scanFolder(action)

selectedProcesses = ['siesta','TDzevolk','TDbuildD', 'DHSCF','PostSCF']
explainations = ['Total','Solve TDKS equation','Build DM', 'Build H', 'Postprocess']
image = data[-1][-1]['Prg.tot']
pieData = image[selectedProcesses[1:]]
other = image[selectedProcesses[0]] - np.sum(pieData.values)

print image.sort_values()
one = [i for i in pieData.values]
one.append(other)
ax = axs[1]
explode = np.zeros(len(selectedProcesses))
explode[0]  = 0.05; explode[1]  = 0.16
ax.pie(one, explode=explode, labels=explainations[1:]+['Other'], 
       autopct='%.0f%%',shadow=True)

for key,label in zip(selectedProcesses,explainations):
  totalTimes = np.array([time['Prg.tot'][key] for index, folder, time in data])/3600.0
  situations = np.array([float(folder) for index, folder, time in data])
  ax = axs[0]
  ax.plot(situations, totalTimes,'-o', ms=12, label = label)

kargs=ma.getPropertyFromPosition(ylabel=r'Clock Time (hour)',title='Clock Time')
ma.setProperty(ax,**kargs)