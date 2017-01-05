#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
#-----------------------------------------------------------------------------
def getEnergy(index,folder):
  time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure(ave=True)
  return index, folder, E_ks

from pyramids.plot.PlotUtility import scanFolder
data = scanFolder(getEnergy)
ref = np.load('ref.npy')
deltaEnergy = np.array([np.average(np.abs(energy - ref)) for index, folder, energy in data])
xticks = [float(folder) for index, folder, energy in data]

import pandas as pd
data = pd.DataFrame(data={'x':xticks, 'y':deltaEnergy})
SaveName = __file__.split('/')[-1].split('.')[0]
data.to_csv(SaveName+'.csv')
