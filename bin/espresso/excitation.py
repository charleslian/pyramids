#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 07:43:17 2017

@author: clian
"""

import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
from pyramids.io.fdf import tdapOptions
from matplotlib import pyplot as plt
import numpy as np
import os

def readData(filename='silicon.phase.dat'):
  f = open(filename)
  text = f.readlines()
  nbnd, nkstot = [int(i) for i in text[0].split()]
  
  nstep = (len(text) - 1)/(nkstot+1)
  print nbnd, nkstot, nstep
  del text[::(nkstot+1)]
  #print text
  #data = np.zeros([nbnd,nkstot,nstep])
  #data = 
  data = np.array([[float(i) for i in line.split()] for line in text])
  data = data[:nstep*nkstot].reshape([nstep, nkstot, nbnd])
  #print data[0,0,:]
  #[ for k in range(nkstot) for step in range(nstep)]
  return data

    
phase = readData()
norm = readData('silicon.norm.dat')
plt.plot((norm[:,:,:4] - norm[0,:,:4]).sum(axis=(1,2)))
plt.plot((norm[:,:,4:]- norm[0,:,4:]).sum(axis=(1,2)))