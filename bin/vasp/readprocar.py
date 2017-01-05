#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

f=open('DOSCAR','r')
for i in range(5):
        print f.readline()
Ef=float(f.readline().split()[3])
print Ef
f.close()

f=open('PROCAR','r')
print f.readline()
info=f.readline().split()
nk,nb,na=int(info[3]),int(info[7]),int(info[11])
no=3
print nk*nb*na
bands=np.zeros([nk,nb])
weights=np.zeros([nk,nb,na,no])
colors=['b','r','g']
atoms=[0,1]
orbitals=[0,1]
kpoints=np.zeros([nk,3])
for i in  range(nk):
	print f.readline()
        coor=f.readline().split()
	print 'coor',coor
        for k in range(3):
                kpoints[i,k]=float(coor[k+3])   
        for j in range(nb):
        	print f.readline()
                bands[i,j]=float(f.readline().split()[-1])
		f.readline()
        	print f.readline()
		for k in range(3):
        		weight=[float(x) for x in f.readline().split()[1:-1]]
			weights[i,j,k]=weight
			print weights[i,j,k]
        	f.readline()
        f.readline()

x=range(nk)
for i in range(nk):
	for j in range(nb):
		for l in orbitals:
			markersize=0
			for k in atoms:
				markersize+=weights[i,j,k,l]
				#print markersize
			plt.plot(x[i],bands[i,j]-Ef,color=colors[l],marker='o',markersize=markersize*20)
plt.ylim(-5,5)
plt.show()
f.close()
