#/usr/bin/python
"""
Created on Fri Jul 22 09:54:42 2016
@author: Chao (Charles) Lian
@email: Charleslian@126.com
"""
import numpy as np

def readDenCharge(filename):
  import numpy as np
  Bohr = 0.529
  fileHandle =  open(filename)  
  fileContext = fileHandle.readlines()
  
  numAtom =int(fileContext[2].split()[0])
  print numAtom
  
  
  nx = int(fileContext[3].split()[0])
  ny = int(fileContext[4].split()[0])
  nz = int(fileContext[5].split()[0])
  
  dx = float(fileContext[3].split()[1]) * Bohr
  dy = float(fileContext[4].split()[2]) * Bohr
  dz = float(fileContext[5].split()[3]) * Bohr
  
  volume = dx * dy * dz 
  #print dx,dy,dz, volume
  
  headlines = ""
  for line in fileContext[:numAtom+6]: 
    headlines += line
  
  #print headlines
  
  data = []
  for line in fileContext[numAtom+6:]:
    data.extend([float(value) for value in line.split()])
  
  data = np.array(data)
  data = np.reshape(data,(nx*ny,nz))
  
  return headlines,data,volume


if __name__ == '__main__':
  import sys
  

  if len(sys.argv) != 2:
    print 'Wrong num of arguments!'
    sys.exit()
  headlines, data1,volume = readDenCharge(sys.argv[1])
  headlines, data2,volume = readDenCharge(sys.argv[2])
  
  dataDiff = data1 - data2
  
  print np.sum(np.ma.masked_where(dataDiff <= 0, dataDiff))*volume
  print np.sum(np.ma.masked_where(dataDiff >= 0, dataDiff))*volume
  
  outputFile =  open('diff.RHO.cube','w')           
  outputFile.writelines(headlines)
  
  for row in dataDiff:
    for value in row:
      outputFile.write(str(value)+' ')

    



