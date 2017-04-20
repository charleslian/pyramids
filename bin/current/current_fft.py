# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 17:33:37 2017

@author: mxguan-iop
#this is a script to calculate the fourier transformation of current and thus obtain the HHG spectrum in a periodic material.
"""

import numpy as np
from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import matplotlib.pyplot as plt
import os
SaveName = __file__.split('/')[-1].split('.')[0]
#----------------------------------------------- 
def getCurrentPython():
  options = tdapOptions()
  context = []
  for line in open('result').readlines():
      if len(line) == 1:
          continue
      if 'Current' in line.split() :
          context.append(line[:-1])
  #print context
  current = [[float(line.split()[-4]),float(line.split()[-3]),float(line.split()[-2])] for line in context]
  #print current
  data = np.array(current)
  #time = np.arange(len(current))*timestep
 # print data
  return data 
#----------------------------------------------- 
def getAField():
  if os.path.exists('TDAFIELD'):
     Afield = [[float(i) for i in line.split()] for line in open('TDAFIELD')]   
     Afield = np.array(Afield)/1E5
     options = tdapOptions()
     timestep = options.tdTimeStep[0]
     time = np.arange(len(Afield))*timestep
  else:
    time = np.zeros(2)
    Afield = np.zeros([2,3])
  return time, Afield  
#------------------------------------------------------------------- 
def getcurrentfft(direction, dumping=0.00):
  from scipy.fftpack import fft    
 
  timeArray,afield =getAField()  
  current =getCurrentPython() 
  
  option = tdapOptions()
  lengthTime = option.tdTimeStep[0]
  
  timeArray = timeArray[2:]/option.tdTimeStep[0]  
  numStep =  len(timeArray)

  current = current[:,1]       #perform FFT for current in different directions,eg:the second line is y direction      
  current *= np.exp(-dumping*timeArray) 
                         
  freqResolution =1.0/(lengthTime*numStep)
  freqArray = (timeArray-(numStep/2.0))*freqResolution
  
  energyArray = freqArray*4.1356
  energyArray = energyArray[numStep/2:]
 
  
  epsilon_current = fft(current)[:numStep/2] 
  epsilon_current = (np.real(epsilon_current),np.imag(epsilon_current))
  current_fft_mode=np.power(epsilon_current[0],2)+np.power(epsilon_current[1],2)
  import pandas as pd
  df = pd.DataFrame({'x-energy':energyArray, 
                    'y1-Im(current)':np.abs(epsilon_current[0]*energyArray/4.1356), 
                    'y2-Re(current)':np.abs(epsilon_current[1]*energyArray/4.1356)})
  #print df
  df.to_csv('current_fft.csv',sep=',')
  return  current,energyArray[10:],current_fft_mode[10:]#current,energyArray[76:],current_fft_mode[76:]#to ensure that the nth order is the maximum
  
#-------------------------------------------------------------------   
guassFieldEnergy =0.329973
fig1, axs = plt.subplots(2,1,sharey=False,sharex=False,figsize=(8,10))
colors = ['r','g','b']
for i, direct in enumerate(['x','0.00056','z']):
    if not os.path.exists(direct):
        continue
    os.chdir(direct)
    current,energyArray,current_fft_mode = getcurrentfft(i,0.001)
    print energyArray
    #energyArray=energyArray/2.5
axs[0].semilogy(energyArray/guassFieldEnergy,current_fft_mode,'-',linewidth=2.,color='black',label='y',alpha=0.5)
axs[1].plot(energyArray/guassFieldEnergy,current_fft_mode,'-',linewidth=2.,color='red',label='y')
xlimits=[0.5,25]
args1 = getPropertyFromPosition(xlimits=xlimits,ylimits=None,ylabel='log(intensity)',xlabel='Order')
args2 = getPropertyFromPosition(xlimits=xlimits,ylimits=None,ylabel='intensity',xlabel='Order')
setProperty(axs[0],**args1)
setProperty(axs[1],**args2)

plt.tight_layout()
plt.savefig('HHG-y-total-damp=0.001.pdf',dpi=600)




  
