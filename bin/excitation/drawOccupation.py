#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu
import os

#------------------------------------------------------------------------------
fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(8,6))

SaveName = __file__.split('/')[-1].split('.')[0] 

kcoor, kweight = dp.readKpoints()
x = np.arange(kcoor.shape[0])

xlabel = 'Energy (eV)'
ylabel = 'Population'

import pandas as pd
dataFilename = xlabel+'vs'+ylabel+'.csv'

if os.path.exists(dataFilename):
  sortedDF = pd.DataFrame.from_csv(dataFilename)
else:
  time, exe = dp.getProjectedPartition()
  time, eigen = dp.getAdiabaticEigenvalue()
  df = pd.DataFrame({xlabel:eigen[-1].flatten(),
                     ylabel:exe[-1].flatten()})
  sortedDF = df.sort_values(by=xlabel)
  sortedDF.to_csv(xlabel+'vs'+ylabel+'.csv')

xlimits=[-5,5]
xt = sortedDF[xlabel]
yt = sortedDF[ylabel]
x = xt[xt>xlimits[0]][xt<xlimits[1]]
y = yt[xt>xlimits[0]][xt<xlimits[1]]
  
bins = 200
hist, bin_edges = np.histogram(x,bins=bins,range=xlimits)
hist_o, bin_edges_o = np.histogram(x,bins=bins,range=xlimits,weights=y*0.5)

tiny = bin_edges[bins/2 + 1]
ePart = bin_edges[:-1]
yPart = (hist_o)/(hist+1E-9)

def interp(xin,yin,xout):
  from scipy.interpolate import interp1d
  spline = interp1d(xin, yin, kind='cubic')
  return spline(xout) 

ax = axs[0]

eDosInterp = np.linspace(bin_edges[0], bin_edges[-2], 2E4)
yDosInterp = interp(bin_edges[:-1], hist, eDosInterp)

eDosPartInterp = np.linspace(bin_edges[0], bin_edges[-2], 2E4)
yDosPartInterp = interp(bin_edges[:-1], hist_o, eDosPartInterp)


ax.plot(eDosInterp, yDosInterp,'.g',lw=3)
ax.fill_between(eDosPartInterp[:1E4], (yDosInterp - yDosPartInterp)[:1E4], color='b')
ax.fill_between(eDosPartInterp[1E4:], (yDosPartInterp)[1E4:], color='r')

ma.setProperty(ax,**ma.getPropertyFromPosition(0, xlabel=xlabel, ylabel='DOS', 
                                               xlimits=xlimits,
                                               ylimits=[0,None],
                                               yticklabels=[]))


ax = axs[1]
ax.fill_between(ePart, yPart, 0.0, lw=4, color='b')

def FermiDiracDistrib(E, T):
  return 1.0/(np.exp((E)/T)+1) 
  
from scipy.optimize import curve_fit  
popt, pcov = curve_fit(FermiDiracDistrib, ePart, yPart)    
print popt
popt = [1.3]

xfit = np.linspace(ePart[0],ePart[-1],1000)

ax.plot(xfit, FermiDiracDistrib(xfit,*popt),'--',lw=3,c='k')
ma.setProperty(ax,**ma.getPropertyFromPosition(1, xlabel=xlabel, 
                                               ylabel=ylabel, 
                                               xlimits=xlimits,
                                               ylimits=[0,None]))
plt.savefig('1.pdf')


#ax.fill_between(eDosInterp, yDosInterp, 0.0, color='g')
#ax.fill_between(ePart[:bins/2], yPart[:bins/2], 1.0, lw=4, color='b')
#ax.fill_between(ePart[bins/2+1:], yPart[bins/2+1:], 0.0, lw=4, color='r')
#from scipy.interpolate import interp1d
#spline = interp1d(x1, y1, kind='cubic')
#interpX1 = np.linspace(x1[0], -0.1, 2E4)#x[x < bin_edges[-2]] 
#interpX2 = np.linspace(0.1, x1[-1], 2E4)  
#print interpX1
#interpY1 = spline(interpX1) 
#interpY2 = spline(interpX2) 
#ax.fill_between(bin_edges[:-1], hist, 0.0, color='g')
#ax.plot([xlimits[0], -tiny, tiny, xlimits[1]], [1,1,0,0],'-k',lw=2)
#def FermiDiracDistrib(E, T1, T2, Ef1, Ef2):
#  return 0.5/(np.exp((E-Ef1)/T1)+1) + 0.5/(np.exp((E-Ef2)/T2)+1) 
#ax.fill_between(interpX1, interpY1, np.linspace(1, 1, 2E4), lw=4, color='r')
#ax.fill_between(interpX2, interpY2, np.linspace(0.0, 0, 2E4), lw=4, color='b')
#ax = axs[0]
#print y.iloc[-1]
#[value + y.iloc[0] for i,value in enumerate(y)]
#ax.fill_between(bin_edges[:-1], hist)
#ax.fill_between(x[x<0],y[x<0],2.0,lw=0.1,color='b')
#ax.fill_between(x[x>0],y[x>0],0.0,lw=0.1,color='r')
#ax.plot([xlimits[0],0, 0.001, xlimits[1]], [2,2,0,0],'-k',lw=2)
#from scipy.interpolate import interp1d
#spline = interp1d(x, y, kind='linear', assume_sorted=True)
#interpX = np.linspace(x.iloc[0],x.iloc[-1],1000)     
#interpY = spline(interpX) 
#ax.plot(interpX,interpY,color='g')

#ma.setProperty(ax,**ma.getPropertyFromPosition(xlimits=xlimits,ylimits=[-0.0,2.1]))
#ax.fill_between(bin_edges[:sep], hist_o[:sep]/hist[:sep], 1.0,color='b')
#ax.fill_between(bin_edges[sep:-1], hist_o[sep:]/hist[sep:], color='r')
#fillRef  = np.linspace(1, 1, 2E4)
#fillRef += np.linspace(0.0, 0, 2E4)
#
#spline = interp1d(bin_edges[:-1], hist, kind='cubic')
#interpX = np.linspace(bin_edges[0], bin_edges[-2],2E4)#x[x < bin_edges[-2]] 
#interpY = spline(interpX) 
#attachX = x[x < bin_edges[-2]] #
#attachY = spline(attachX)   #

#ax.fill_between(interpX, interpY, color='g')
#ax.fill_between(attachX, (attachY*y[x < bin_edges[-2]]*0.5), color='r')
#ax.fill_between(x,y,lw=0.0)
#ax.plot(x,y,'-')

#ax.plot(interpX,interpY,'-')
#ax.fill_between(bin_edges[:-1], hist)
#ax.plot(interpX,interpY,'g-',lw=4,)
#ax.fill_between(interpX,interpY,color='g')
#axs.fill_between(interpX, interpY)
#                 color = colors[index], lw=3, 
#                 alpha=0.7, zorder = -index, 
#                 label=r'%5.2f $V/\AA$'%(eFieldStr))
#nRow = 3
#nCol = len(ls.selectedTimeStep)/nRow
#axs = axs.flatten()

#import localSetting as ls
#kpath = ls.kpath
#cut = ls.cut
#specialKPoints = ls.specialKPoints
#evolvingBands = range(0, homo + 7)
#homo = dP.getHomo()

#print x 
#selectedDF = sortedDF.copy()
#selectedDF = selectedDF[selectedDF[xlabel] < xlimits[1]]

#print selectedDF
#print bin_edges[bins/2]
#for i,value in enumerate(bin_edges) if value < 0:
#    sep = i
#  else:
#    break
#