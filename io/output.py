# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 00:10:57 2016

@author: clian
"""
def writeGPAWdipole(filename,efield,time,dipole):
  import numpy as np
  f = open(filename,'w')
  f.write('# Kick = '+str(efield)+'\n')
  f.write('#            time            norm                    dmx                    dmy                    dmz \n')
  for t ,dm in zip(time,dipole):
    norm = np.linalg.norm(dm)
    line = ('%20.8lf %20.8le %22.12le %22.12le %22.12le \n'
                    % (t, norm, dm[0], dm[1], dm[2]))
    f.write(line)
    
  # Kick = [    0.000000000000e+00,     1.000000000000e-05,     0.000000000000e+00]

def writeKLines(filename, points):
  lines = '%block BandLines \n'
  N = 50
  for index, kpt in enumerate(points):
    #print kpt
    out = (N*index+1, kpt[0][0], kpt[0][1], kpt[0][2], kpt[1])
    lines += '%i %3.2f %3.2f %3.2f %s \n'% out
  lines += '%endblock BandLines \n'  
  fdf = open(filename,'w')
  fdf.writelines(lines)
    
  
def writeSiesta(filename,atoms):
  NumberOfAtoms=atoms.get_number_of_atoms()
  elements=set(zip(atoms.get_chemical_symbols(), atoms.get_atomic_numbers()))
  #print list(elements).sort(key=) 
  NumberOfSpecies=len(elements)
  
  cell=atoms.get_cell()
  
  f=open(filename,'w')
  f.write("AtomicCoordinatesFormat  Ang\n")
  f.write("LatticeConstant  1.0  Ang\n\n")
  
  f.write("NumberOfAtoms    " + str(NumberOfAtoms)   + "\n")
  f.write("NumberOfSpecies  " + str(NumberOfSpecies) + "\n\n")
  
  f.write("%block LatticeVectors\n")
  lines= '' 
  for a in cell:
    lines += "  %21.16f %21.16f %21.16f\n" % tuple(a)
  f.write(lines)
  f.write("%endblock LatticeVectors\n\n")
  
  
  f.write("%block ChemicalSpeciesLabel\n")
  lines= ''
  
  element_index=dict()
  for i,element in enumerate(elements):
    element_index[element[0]]=i+1
    lines+= "%4d %5d %5s\n" % (i+1, element[1], element[0])
  
  #print element_index
  f.write(lines)
  f.write("%endblock ChemicalSpeciesLabel\n\n")
  
  f.write("%block AtomicCoordinatesAndAtomicSpecies\n")
  lines= ''
  for a in zip(atoms.get_positions(),atoms.get_chemical_symbols()):
    lines += " %21.16f %21.16f %21.16f " % tuple(a[0])
    lines += "%2d\n" % element_index[a[1]]
    
  f.write(lines)
  f.write("%endblock AtomicCoordinatesAndAtomicSpecies\n\n")
  
def splitMDCAR():
  """
  split the siesta.MD_CAR file to POSCAR file per step
  """
  import os
  systemLabel = 'siesta'
  NumBlocks=int(os.popen('grep -i '+systemLabel+' '+systemLabel+'.MD_CAR | wc -l').readline().split()[0])
  position_file = open('siesta'+'.MD_CAR')
  atomNumList = [int(i) for i in os.popen('head -6 siesta.MD_CAR |tail -1').readline().split()]
  numAtomPositionLine = sum(atomNumList)
  totalNumLine = numAtomPositionLine + 7
  context = position_file.readlines()
  for index in range(NumBlocks):
    output=context[index*totalNumLine:(index+1)*totalNumLine]
    poscarFileName = "POSCAR"+str(index)
    poscarFile=open(poscarFileName,'w')
    poscarFile.writelines(output)
    
def writeQE(filename,atoms):
  NumberOfAtoms=atoms.get_number_of_atoms()
  elements=set(zip(atoms.get_chemical_symbols(), 
                   atoms.get_atomic_numbers(), atoms.get_masses()))
  #print list(elements).sort(key=) 
  NumberOfSpecies=len(elements)
  
  cell=atoms.get_cell()
  print atoms.get_masses()
  
  f=open(filename,'w')

  f.write("&system\n")
  f.write('  ibrav = 0,\n')
  f.write('  nat = ' + str(NumberOfAtoms) + ",\n")
  f.write('  ntyp = ' + str(NumberOfSpecies) + ",\n")
  f.write('  ecutwfc = 20.0 \n')
  f.write("/\n")
  
  f.write("CELL_PARAMETERS angstrom\n")
  lines= '' 
  for a in cell:
    lines += "  %21.16f %21.16f %21.16f\n" % tuple(a)
  f.write(lines)
  
  #f.write("%block ChemicalSpeciesLabel\n")
  lines= 'ATOMIC_SPECIES\n'
  
  for i,element in enumerate(elements):
    lines+= "%5s %21.16f %5s.pbe-mt_fhi.UPF\n" % (element[0], element[2], element[0])
  
  #print element_index
  f.write(lines)
  #f.write("%endblock ChemicalSpeciesLabel\n\n")
  
  f.write("ATOMIC_POSITIONS angstrom\n")
  lines= ''
  for a in zip(atoms.get_positions(),atoms.get_chemical_symbols()):
    lines +=  a[1]
    lines += " %21.16f %21.16f %21.16f \n" % tuple(a[0])
    
  f.write(lines)
  f.write("\n\n")  
  