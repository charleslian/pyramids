#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 21:52:52 2017

@author: clian
"""
import numpy as np

#Use Period T as center quality

fs2s = 1E-15
c = 3E8
THz2eV =  4.1356675E-3

# T in fs
def fromPeriod(t):
  #print "The period T is", T, 'fs, which is'
  T = t, 'fs'
  f = 1.0E3/t, 'THz'
  E = f[0]*THz2eV, 'eV'
  wavelenth = 3E5/f[0], 'nm' 
  for x in T, f, E, wavelenth:
    print "%11.5f \t %s"%(x)
  print 
  #omega = T/(2*np.pi)

#F in fs-1
def fromFrequency(f): 
  T = 1.0/f
  fromPeriod(T)
    
#E in eV
def fromEnergy(E):
  f = E/THz2eV * 1E-3
  T = 1.0/f 
  fromPeriod(T)

#wavelenth in nm
def fromWavelength(wavelenth):
  f = 3E2/(wavelenth)
  T = 1.0/f 
  fromPeriod(T)

if __name__ == '__main__':
  import argparse
  
  class options(argparse.ArgumentParser):
    def __init__(self):
      super(options, self).__init__()
      
      self.add_argument('-f', '--frequency', type=float, nargs='?',
                        help='Frequency as input, unit in /fs')
      self.add_argument('-l', '--wavelength', type=float, nargs='?',
                        help='Wavelength as input, unit in nm')
      self.add_argument('-t', '--period', type=float, nargs='?',
                        help='Period as input, unit in fs')                   
      self.add_argument('-e', '--energy', type=float, nargs='?',
                        help='Energy as input, unit in eV')                        
      self.args = self.parse_args() 
    
  options = options()
  args = options.args
  if args.energy is not None:
    print "input energy %5.4f eV"%args.energy
    fromEnergy(args.energy)
  if args.period is not None:
    print "input period %5.4f fs"%args.period
    fromPeriod(args.period)
  if args.wavelength is not None:
    print "input wavelength %5.4f nm"%args.wavelength
    fromWavelength(args.wavelength)
  if args.frequency is not None:
    print "input frequency %5.4f /fs"%args.frequency
    fromFrequency(args.frequency)
      
      
  
#  fromPeriod(250.0)
#  fromFrequency(4E-3)
#  fromEnergy(0.01654267)
#  fromWavelength(75000)
#  
#  fromPeriod(2.0)
#  fromFrequency(0.5)
#  fromEnergy(2.06783375)
#  fromWavelength(600)
  
  

#fromFrequency(0.032/(2*np.pi))