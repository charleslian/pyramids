#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

f=open('EIGENVAL','r')
for i in range(5):
	f.readline()

x,nk,nb=(int(i) for i in f.readline().split())
print nk,nb
bands=np.zeros([nk,nb])
kpoints=np.zeros([nk,3])
for i in range(nk):
	f.readline()
	coor=f.readline().split()
	for k in range(3):
		kpoints[i,k]=float(coor[k])	
	for j in range(nb):
		bands[i,j]=float(f.readline().split()[1])

x=range(nk)
plt.plot(x,bands,'-k')
plt.show()		
f.close()

