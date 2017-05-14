#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 14:57:18 2017

@author: clian
"""
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
from pyramids.io.fdf import tdapOptions
from matplotlib import pyplot as plt
import numpy as np
import os

Ry = 13.6
f = os.popen('grep "Ekin + Etot (const)" result')
energy = np.array([float(line.split()[-2]) for line in f.readlines()])

fig, axs = plt.subplots(2,1,sharex=True)
axs[0].plot((energy[3:]-energy[0])*Ry)

Efield = [[float(i) for i in line.split()] for line in open('TDEFIELD')]
Efield = np.array(Efield)/1E5
axs[1].plot(Efield)