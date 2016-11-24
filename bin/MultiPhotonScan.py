#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
from pyramids.io.fdf import tdapOptions 
from pyramids.plot.PlotUtility import scanFolder
#------------------------------------------------------------------------------
efield = 2
exElectron = 0
exEnergy = 1

def action(index, folder):
  timeEf, eField = dP.getEField()
  timeEl, exe = dP.getExcitedElectrons()
  exe  -= exe[0]
  timeEn, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
  deltaE =  (E_ks[2:,] - E_ks[2])
  return [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)]
#------------------------------------------------------------------------------

fig, axs = plt.subplots(3,2,sharex=False,sharey=True,figsize=(6,12))
SaveName = __file__.split('/')[-1].split('.')[0]

data = scanFolder(action)
c = ma.getColors(data[-1][0][0]+1)

x = []; y = []


option = tdapOptions()
freq, pulseTime, pulseWidth = option.laserParam[0][:3]

start = int((pulseTime + 1.5*pulseWidth)/option.tdTimeStep[0])
photonEnergy = freq*4.1356

ave = 2

for [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)] in data:
  mpOrder = (deltaE[start:]/exe[start:])/photonEnergy #
  for imp, mp in enumerate(mpOrder): 
    if mp > 60.0 or mp < 0.0:
      mpOrder[imp] = mpOrder[imp - 1]
    #if np.abs(mpOrder[imp] - meanValue) > 1:
      #mpOrder[imp] = meanValue
  x1 = float(folder)*13.6/0.529
  x.append(x1)
  y1 = np.mean(mpOrder[-1])
  y.append(y1)
    
  axs[ave,0].plot(timeEl[start:], mpOrder,'o', alpha=1.0,
           c=c[index], ms = 4, mew = 0.0)
          
  axs[ave,1].plot(x1, y1,'o',
              alpha = 0.9, ms = 15, c = c[index],
              #label=folder
              )   
     
  bbox_args = dict(boxstyle="round", fc="0.8")
  arrow_args = dict(color=c[index],shrink=0.03,width=1,headwidth=4)
  axs[ave,1].annotate('', xy=(x1, y1), 
                  xycoords=axs[ave,1].transData,
                  xytext=(timeEl[-1], y1), 
                  textcoords=axs[ave,0].transData,
                  ha="right", va="bottom",
                  bbox=bbox_args,
                  arrowprops=arrow_args
                  )    


x = np.array(x)  
y = np.array(y) 

def func(x, a, b):
  return a*x**2.0 + b #*x**4.0 + c
from scipy.optimize import curve_fit
popt, pcov = curve_fit(func, x, y)    
print popt, pcov

xfit = np.linspace(0.0,np.max(x),100)
axs[ave,1].plot(xfit,func(xfit,*popt),'--',lw=3,c='k',
                zorder=0, 
                label= r'$K = %3.4f \varepsilon^2 + %3.4f $' % tuple(popt)
                )


kargs=ma.getPropertyFromPosition(0, ylabel=r'Multi-photon Order $K$',
                                 ylimits=[0.8,1.6],
                                 xlimits=[timeEl[start],timeEl[-1]],
                                 xlabel='Time (fs)',
                                 )         
ma.setProperty(axs[ave,0],**kargs)
kargs=ma.getPropertyFromPosition(1,
                                 xlabel=r'$\varepsilon$ (V/$\AA$)',
                                 legendLoc = 4,
                                 #ylimits=[np.min(y),np.max(y)]
                                 )         
ma.setProperty(axs[ave,1],**kargs)



plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)