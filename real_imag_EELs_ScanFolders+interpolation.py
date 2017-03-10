# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 15:36:43 2016

@author: moomin
"""
import numpy as np
from scipy.fftpack import fft, ifft
import pyramids.plot.PlotUtility as pu 
from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp1d
fig, ax = plt.subplots(1,1,sharey=True,sharex=True,figsize=(7,15)) 
colors = getColors(7)
dumping = 0.01
width = 186.0
fieldE = 0.01
xlimits = [0,30] 
ylimits = None
def huskyOnTheFly(index,folder):
    count = 0
    for i, direct in enumerate(['x','y','z']):
        #print os.listdir('.')
        if not os.path.exists(direct):
            continue
        
        os.chdir(direct)
        timeArray, efield = dp.getEField()  
        
        option = tdapOptions()
        lengthTime = option.tdTimeStep[0]
        numStep =  option.tdFinalStep - 2
        
        timeArray = timeArray[2:]/option.tdTimeStep[0]
        time, dipole = dp.getDipolePython()
          
        dipole = dipole[2:,i]
        
        
        dipole *= np.exp(-dumping*timeArray)
                                  
        freqResolution = 1.0/(lengthTime*numStep)
        freqArray = (timeArray-(numStep/2.0))*freqResolution
        
        energyArray0 = freqArray*4.1356
        energyArray = energyArray0[numStep/2:]
#        energyArray1 = list(energyArray0[numStep/2:])
#        energyArray2 = list(energyArray0[:numStep/2])
        
#        energyArray1 +=energyArray2
        
#        energyArray = np.array(energyArray1)
        
        epsilon = fft(dipole)[:numStep/2]
        epsilon = (np.real(epsilon),np.imag(epsilon))
        
#        print (energyArray)
        
        absorbanceimag = (epsilon[0]*energyArray*0.0367/6.28)/(width*float(folder)*fieldE)
        absorbancereal = (epsilon[1]*energyArray*0.0367/6.28)/(width*float(folder)*fieldE)
#        absorbanceimag = 3.334*(epsilon[0]*energyArray/4.1356)/0.25
#        absorbancereal = 3.334*(epsilon[1]*energyArray/4.1356)/0.25
        if count == 0:
           count += 1           
           absorbanceSumimag = absorbanceimag
           absorbanceSumreal = 0.25/np.pi+absorbancereal
        else:
           absorbanceSumimag += absorbanceimag
           absorbanceSumreal += absorbancereal
        eels =  absorbanceSumimag / (absorbanceSumimag**2 + absorbanceSumreal**2)
        os.chdir('..')
    peaks = []   
#    for j in range(1,len(absorbanceSum)-1):
#        if energyArray[j] > xlimits[0] and energyArray[j] < xlimits[1]:    
#            if absorbanceSum[j] >= absorbanceSum[j-1] and absorbanceSum[j] >= absorbanceSum[j+1]:
#                if absorbanceSum[j] > 0.03 and energyArray[j] > 5 and energyArray[j] < 8: # energyArray[j] < 22.0 and  
#                    peaks.append(energyArray[j])     
#    print peaks     
          
          
          
        
    return energyArray, absorbanceSumimag, folder, absorbanceSumreal, eels, peaks
    




collection = pu.scanFolder(huskyOnTheFly)
print collection[0][0]
print collection[0][1]

for i,data in enumerate(collection):
#    for peak in data[3]:
#        ax.text(peak,0.14,'%3.2f' % peak,fontsize='large',rotation=90)  
  
#    plt.semilogy(data[0],data[1],linewidth=2.0,color=colors[i+1],alpha=0.6,label=data[2])
#    plt.plot(data[0],np.log10(data[1]),linewidth=4.0,color=colors[i+1],alpha=0.6,label=data[2])
#    xDownIndex = 0  
#    xUpIndex = 100
#    interpXimge = np.linspace(data[0][xDownIndex], data[0][xUpIndex-1], 2000)
#    splinesimge = interp1d(data[0][xDownIndex:xUpIndex], data[1][xDownIndex:xUpIndex],kind='cubic')    
#    overEimge = splinesimge(interpXimge)
#    
#    interpXreal = np.linspace(data[0][xDownIndex], data[0][xUpIndex-1], 2000)
#    splinesreal = interp1d(data[0][xDownIndex:xUpIndex], data[3][xDownIndex:xUpIndex],kind='cubic')    
#    overEreal = splinesreal(interpXreal)
#    
#    interpXeels = np.linspace(data[0][xDownIndex], data[0][xUpIndex-1], 2000)
#    splineseels = interp1d(data[0][xDownIndex:xUpIndex], data[4][xDownIndex:xUpIndex],kind='cubic')    
#    overEeels = splineseels(interpXeels)
    
#    plt.plot(interpX,splines(interpX)/np.max(splines(interpX)),'-o',markersize=5.0,linewidth=4.0,color=colors[i],alpha=0.6,label=data[2])
    plt.plot(data[0],i*3+data[1]/np.max(data[1]),'--',markersize=10.0,linewidth=3.0,color=colors[i+1],alpha=0.65) 
    plt.plot(data[0],i*3+data[3]/np.max(data[3]),'-',markersize=10.0,linewidth=3.0,color=colors[i+1],alpha=0.65)
#    plt.plot(interpXreal,i*3+interpXreal-interpXreal,'-',markersize=10.0,linewidth=6.0,color=colors[i+1],alpha=0.65)
    plt.fill_between(data[0],i*3+(data[4])/np.max(data[4]),i*3,linewidth=3.0,color=colors[i+1],alpha=0.5,)
#    plt.plot(interpX,splines(interpX),'-o',markersize=5.0,linewidth=4.0,color=colors[i],alpha=0.6,label=data[2])
#    plt.plot(data[0],data[1]/np.max(data[1]),'-o',linewidth=4.0,color=colors[i+1],alpha=0.6,label=data[2])
#    plt.plot(data[0],data[1]/float(data[2]),'-o',linewidth=4.0,color=colors[i+1],alpha=0.6,label=data[2])
    args = getPropertyFromPosition(xlimits=xlimits,ylimits=ylimits,
                                   ylabel='EELs',xlabel='Energy(eV)')#,vline=data[3])
    setProperty(ax,**args)
    

#plt.show()
plt.tight_layout()
#plt.savefig('dielectriFunctionVariable(without over E or maxabsorbance).pdf',dpi=600)
plt.savefig('EEls.eps',i=800)
plt.savefig('EEls.png',i=800)
#plt.savefig('dielectriFunctionVariable1-1.jpg',dpi=600)