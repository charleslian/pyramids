#!/usr/bin/python

"""
Created on Fri Nov 20 07:13:33 2015

@author: cl-iop
"""

import os
import numpy as np


  

def splitMDCAR():
  """
  split the siesta.MD_CAR file to POSCAR file per step
  """
  #numPosFile=int(os.popen('ls POSCAR* | wc -l').readline().split()[0])
  systemLabel = 'siesta'
  #element = 'Si'
  
  NumBlocks=int(os.popen('grep -i '+systemLabel+' '+systemLabel+'.MD_CAR | wc -l').readline().split()[0])
  position_file = open('siesta'+'.MD_CAR')
  atomNumList = [int(i) for i in os.popen('head -6 siesta.MD_CAR |tail -1').readline().split()]
  
  
  #print sum(atomNumList)
  numAtomPositionLine = sum(atomNumList)
  totalNumLine = numAtomPositionLine + 7
  
  context = position_file.readlines()
  
  for index in range(NumBlocks):
    output=context[index*totalNumLine:(index+1)*totalNumLine]
    poscarFileName = "POSCAR"+str(index)
    poscarFile=open(poscarFileName,'w')
    poscarFile.writelines(output)
  

if __name__ == '__main__':
  splitMDCAR()