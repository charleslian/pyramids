#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 20:18:56 2017

@author: clian
"""

control = open('control.part').readlines()
scfkpt = open('scfkpt.part').readlines()
bandkpt = open('bandkpt.part').readlines()
struct = open('struct.part').readlines()


for i, line in enumerate(control):
    if control[i].find('&system') == 1:
        nsys = i
    if control[i].find('&control') == 1:
        ncon = i
        

control.insert(nsys+1, struct[0]) #, scfkpt, bandkpt, struct
control.extend(struct[1:])

if nsys < ncon:
    insetline = 2
else:
    insetline = 1
    
scfin = control[:]
bandin = control[:]

scfin.insert(ncon+insetline,'    calculation = "scf",\n    restart_mode = "from_scratch",\n')
scfin.extend(scfkpt)

bandin.insert(ncon+insetline,'    calculation = "bands",\n')
bandin.extend(bandkpt)


open('scf.in','w').writelines(scfin)
open('band.in','w').writelines(bandin)


#for i in scfin:
#    print i,
#
#for i in bandin:
#    print i,
    
    