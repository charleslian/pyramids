"""
This module include the tdapOption class, 
which is initializied by reading the input.fdf file,
to get the useful setups, such as the system label, 
time step of electronic and ionic motions, spin status,
for the following data process. 
"""

__author__ = "Chao Lian <charleslian@126.com>"
__date__ = "Fri July 22 18:16:20 2016"

__version__ = "2.0"
__credits__ = "Chao Lian initial and maintain the codes"

import numpy as np
import os
class Options(object):
  def __init__(self,inputFile='input.fdf'):
    if(os.path.exists('input.fdf')):
        self.inputFile  = inputFile
        self.options    = self.readFdf(self.inputFile)
        self.label      = self.__getString('systemlabel','siesta')
        self.mdTimeStep = self.__getFloatWithUnit('mdlengthtimestep',(0.0,'fs'))
        self.tdTimeStep = self.__getFloatWithUnit('tdlengthtimestep',(0.025,'fs'))
        self.mdFinalStep = self.__getInteger('mdfinaltimestep',1)
        self.tdFinalStep = self.__getInteger('tdfinaltimestep',self.mdFinalStep)
        self.spinPolarized = self.__getLogical('spinpolarized',False)
        self.eigStartStep = 3
        self.eigLengthStep = self.__getInteger('tdwriteeigpairstep',self.mdFinalStep)
        self.laserParam = self.__getArray('tdlightenvelope',np.zeros(5))
    elif(os.path.exists('input.in')):
        self.inputFile  = 'input.in'
        #self.options    = #self.readFdf(self.inputFile)
        self.label      = 'silicon'#self.__getString('systemlabel','siesta')
        self.mdTimeStep = (1, 'fs')#self.__getFloatWithUnit('mdlengthtimestep',(0.0,'fs'))
        self.tdTimeStep = (1, 'fs')#self.__getFloatWithUnit('tdlengthtimestep',(0.025,'fs'))
        self.mdFinalStep = 200#self.__getInteger('mdfinaltimestep',1)
        self.tdFinalStep = 200#self.__getInteger('tdfinaltimestep',self.mdFinalStep)
        self.spinPolarized = False#self.__getLogical('spinpolarized',False)
        self.eigStartStep = 2#3
        self.eigLengthStep = 1#self.__getInteger('tdwriteeigpairstep',self.mdFinalStep)
        #self.laserParam = #self.__getArray('tdlightenvelope',np.zeros(5))
    
  def output(self):
    """
    Print the obtained values for check and test
    """
    print "The system label is ",self.label    
    print "The lenght of MD time step ",self.mdTimeStep[0],self.mdTimeStep[1]
    print "The lenght of TD time step ",self.tdTimeStep[0],self.tdTimeStep[1]
    
    print "The final MD time step ", self.mdFinalStep
    print "The final TD time step ", self.tdFinalStep
    
    print "The system is spin",
    if self.spinPolarized:
      print "polarized"
    else:
      print "unpolarized"
    
  def readFdf(self,inputFile='input.fdf'):
    """
    Read the fdf file input.fdf.
    The tags, including both one-line tags and block tags, 
    are parsed by a dictonary, of which the keys are the tags 
    and the values are a string of the input value.  
    """
    fdfFile = open(inputFile)
    inBlock = False
    options = {}
    
    for line in fdfFile.readlines():
      # skip blank lines, containing only the '\n'      
      if len(line) == 1:
        continue
      if line[0] == '#':
        continue
      line = line.lower().replace('_','')
      line = line.split('#')[0]
      lineList = line.split()
      
      # Read the Blocks
      if lineList[0] == '%block':
        inBlock = True
        blockName = lineList[1].replace('.','')
        blockValues = []
        continue
      elif lineList[0] == '%endblock':
        inBlock = False
        options[blockName] = blockValues
        continue
      if inBlock:
        blockValues.append(lineList)
        
      # Read the line mode parameters 
      else:
        tag = lineList[0].replace('.','')
        if len(lineList) == 1:
          options[tag] = 'True'
        elif len(lineList) == 2:
          options[tag] = lineList[1]
        elif len(lineList) == 3:
          options[tag] = (lineList[1],lineList[2])
    return options
  
  def __getLogical(self,label,default):
    if label in self.options.keys():
      value = self.options[label]
      if 't' in value.lower():
        return True
      else:
        return False
    else:
      return default
 
  def __getString(self,label,default):
    if label in self.options.keys():
      return self.options[label]
    else:
      return default
      
  def __getInteger(self,label,default):
    if label in self.options.keys():
      return int(self.options[label])
    else:
      return default

  def __getFloat(self,label,default):
    if label in self.options.keys():
      return float(self.options[label].replace('f','e'))
    else:
      return default
      
  def __getFloatWithUnit(self,label,default):
    if label in self.options.keys():
      return float(self.options[label][0].replace('f','e')), self.options[label][1]
    else:
      return default
      
  def __getArray(self,label,default):
    if label in self.options.keys():
      value = np.array([[float(i) for i in line] for line in self.options[label]])
      return value
    else:
      return default

#-------------------------------------------------------------------
if __name__== '__main__':
  options = tdapOptions()
  options.output()
