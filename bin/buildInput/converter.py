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
def fromPeriod(T):
  print "The period T is", T, 'fs, which is'
  T = T*fs2s
  f = 1.0/T * 1E-12, 'THz'
  E = f[0]*THz2eV, 'eV'
  wavelenth = c/(f[0]*1E3), 'nm' 
  for x in f, E, wavelenth:
    print "%5.8f \t %s"%(x)
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
  f = c/(wavelenth) * 1E-6
  T = 1.0/f 
  fromPeriod(T)

if __name__ == '__main__':
  import argparse
  
  class options(argparse.ArgumentParser):
    def __init__(self):
      super(options, self).__init__()
      
      self.add_argument('input', metavar='x', type=int, nargs='?',  
                        help='input value.')
      self.add_argument('-f', '--frequency', nargs=None,  
                        help='frequency as input, unit in 1/fs')
      self.add_argument('-l', '--wavelength', nargs=None,  
                        help='wavelength as input, unit in nm')
      self.add_argument('-t', '--period', nargs=None,  
                        help='period as input, unit in fs')                   
      self.add_argument('-e', '--energy', nargs=None,  
                        help='energy as input, unit in eV')                        
      self.args = self.parse_args() 
    
  options = options()
  args = options.args
  if args.energy is not None:
    fromEnergy(args.energy)
  if args.period is not None:
    fromPeriod(args.period)
  if args.wavelength is not None:
    fromWavelength(args.wavelength)
  if args.frequency is not None:
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