# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 11:42:46 2017

@author: clian
"""
fileindex = 1
f = open('weight1','w')

context = open('pwscf.norm.dat').readlines()
nbnd, nk = [int(i) for i in context[0].split()]
print nbnd, nk
for line in context[2:]:
  if line[0] == '-':
    fileindex += 1
    f.close()
    f = open('weight%i'%fileindex,'w')
    f.write('%i  %i\n'%(nk, nbnd))
  else:
    f.write(line)