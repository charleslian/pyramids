#!/usr/bin/python
"""
Created on Mon Aug 24 16:59:10 2015

@author: cl-iop
"""

import numpy as np
import matplotlib_assist as ma

def read_data(filename):
  f=open(filename,'r')
  data=[]
  for i,line in enumerate(f.readlines()):
    if i>1:  
      (x0,y0,z0)=(float(x) for x in line.split())
      if z0 >5E-4:
        data.append((x0,y0,z0))
        
  data=np.array(data)
  #plt.subplot(1,2,index+1)
  #
  return (data[:,0],data[:,1],data[:,2])
  

filename='unfolded_EBS_not-symmetry_averaged.dat'

fig=plt.figure(figsize=ma.A4) #figsize=(6.27,6.27)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0)


X,Y,Z=read_data(filename)
middle=(np.max(X)-np.min(X))/2
X=X-middle
scale=5E4
index_tuple=(1,1,1)
ax=plt.subplot(*index_tuple)
ax.scatter(X,Y,Z*Z*scale,c=-abs(X),marker='o',linewidths=0.000, alpha=0.8)
kargs=ma.get_property_from_position(index_tuple,'Energy/eV','Momentum(1/$\AA$)')
ax.set_xlim(X.min(),X.max())
kargs['xticks']=[-0.5,0.0,0.5]

ax.set_ylim(-1.3,0.2)
    
  
  
ma.set_property(ax,**kargs)
