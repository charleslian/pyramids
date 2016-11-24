#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

f=open('DOSCAR','r')
for i in range(5):
  f.readline()

emax,emin,ne,ef,weight=(float(i) for i in f.readline().split())

ne=int(ne)
print ne#,dos
energy=[]
dos=[]
for i in range(ne):
  data_line=f.readline().split()
  energy.append(float(data_line[0]))
  dos.append([float(i) for i in data_line[1:]])
  
x=np.array(energy)
y=np.array(dos)
y=y[:,:y.shape[1]/2]


plt.plot(x,y)
plt.xlim([-2,2])
plt.ylim([0,10])
plt.show()		
f.close()

