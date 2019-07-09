# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 21:59:26 2017

@author: clian
"""
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
from pyramids.io.fdf import tdapOptions
from matplotlib import pyplot as plt
import numpy as np
import os
from pyramids.io.result import readData
dt = dp.getElectronStepLength()

nocc = int(float(os.popen('grep "starting charge" result').readline().split()[-1])/2.0)
print nocc
#fig, axs = plt.subplots(1,2,sharex=True,figsize=(8,5))

#ax = axs[0]
norm, kweight = readData('pwscf.norm.dat')

