# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:46:05 2017

@author: mxguan-iop
#this is a script to calculate the  current FFT with laser direction rotate 
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
def getcurrentfft_angle(angle, dumping=0.00):
  from scipy.fftpack import fft    
 
  timeArray,afield =getAField()  
  current =getCurrentPython() 
  
  option = tdapOptions()
  lengthTime = option.tdTimeStep[0]
  
  timeArray = timeArray[2:]/option.tdTimeStep[0]  
  numStep =  len(timeArray)
  
  freqResolution =1.0/(lengthTime*numStep)
  freqArray = (timeArray-(numStep/2.0))*freqResolution
  
  energyArray = freqArray*4.1356
  energyArray = energyArray[numStep/2:]
 
  
  angle =angle*np.pi/180.0
 # print  current[:,0] , current[:,1] 
  current_x = current[:,0]       #perform FFT for current in different directions,eg:the second line is y direction  
  current_y = current[:,1]   
  current_x *= np.exp(-dumping*timeArray)
  current_y *= np.exp(-dumping*timeArray)
  current_par=np.cos(angle)*current_y+np.sin(angle)*current_x
  current_per=np.sin(angle)*current_y+np.cos(angle)*current_x
                         
  
  epsilon_currentpar = fft(current_par)[:numStep/2] 
  epsilon_currentpar = (np.real(epsilon_currentpar),np.imag(epsilon_currentpar))
  currentpar_fft_mode=np.power(epsilon_currentpar[0],2)+np.power(epsilon_currentpar[1],2)
  
  epsilon_currentper= fft(current_per)[:numStep/2] 
  epsilon_currentper = (np.real(epsilon_currentper),np.imag(epsilon_currentper))
  currentper_fft_mode=np.power(epsilon_currentper[0],2)+np.power(epsilon_currentper[1],2)
  
  return  energyArray[20:],currentpar_fft_mode[20:],currentper_fft_mode[20:]#to ensure that the nth order is the maximum
  
#-------------------------------------------------------------------   

guassFieldEnergy = 1.979838

energyArray,currentpar_fft_mode,currentper_fft_mode = getcurrentfft_angle(60,0.000)
data=getcurrentfft_angle(60,0.000)
data=np.transpose(np.array(data))[:,1:3]

#print data
fig1, axs = plt.subplots(2,1,sharey=False,sharex=False,figsize=(8,10))
for i in range(2):
  axs[0].semilogy(energyArray/guassFieldEnergy,data[:,i],label=['Parallel','Perpendicular'][i],lw=2, alpha=1.0)
  axs[1].plot(energyArray/guassFieldEnergy,data[:,i],label=['Parallel','Perpendicular'][i],lw=2, alpha=1.0)
  xlimits = [1.5, 10]
  args1 = getPropertyFromPosition(xlimits=xlimits,ylimits=None,ylabel='log(intensity)',xlabel='Order')
  args2 = getPropertyFromPosition(xlimits=xlimits,ylimits=None,ylabel='intensity',xlabel='Order')
  setProperty(axs[0],**args1)
  setProperty(axs[1],**args2)
plt.tight_layout()
plt.savefig('par_per.pdf',dpi=600)

maxPeak_par = energyArray[np.argmax(currentpar_fft_mode)], np.max(currentpar_fft_mode)/1000000
maxPeak_per = energyArray[np.argmax(currentper_fft_mode)], np.max(currentper_fft_mode)/1000000
print maxPeak_par ,maxPeak_per


  
