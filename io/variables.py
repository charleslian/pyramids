"""
This module include the tdapOption class, 
which is initializied by reading the input.fdf file,
to get the useful setups, such as the system label, 
time step of electronic and ionic motions, spin status,
for the following data process. 
"""

__author__ = "Chao Lian <charleslian@126.com>"
__date__ = "Dec 5 2017"

__version__ = "3.0"
__credits__ = "Chao Lian initial and maintain the codes"

import numpy as np
from ase.io.trajectory import Trajectory
#import os

class variables(object):
  def __init__(self):
    self.label  = ''
    
    self.numAtom = 1
    self.numElect = 1
    self.numKpt = 1
    self.numBnd = 1
    
    self.mdTimeStep = 0.0, 'fs'
    self.tdTimeStep = 0.0, 'fs'
    self.mdFinalStep = 1
    self.tdFinalStep = 1
    
    self.eigStartStep = 1
    self.eigSkipStep = self.mdFinalStep
    
    self.spinPol = False 
    self.curStep = 1   # run to this step
    self.eField = np.zeros([1,3])
    self.aField = np.zeros([1,3])
    self.traj = None #np.zeros([self.numAtom,3,self.mdFinalStep])      # ionic trajectory
    self.carrier = None   # excited electron and hole
    self.energy = None    # energies
    
  def output(self):
    """
    Print the obtained values for check and test
    """
    print "The system label is ",self.label    
    print "The lenght of MD time step ",self.mdTimeStep[0],self.mdTimeStep[1]
    print "The lenght of TD time step ",self.tdTimeStep[0],self.tdTimeStep[1]
    print "The final MD time step ", self.mdFinalStep
    print "The final TD time step ", self.tdFinalStep
    print "The system is spin polarized ", self.spinPol 
    print "The current step %i, %f fs"%(self.curStep, self.curStep*self.tdTimeStep[0]) 
    

#-------------------------------------------------------------------
if __name__== '__main__':
  options = variables()
  options.output()
