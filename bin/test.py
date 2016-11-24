# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 11:34:59 2016

@author: cl-iop
"""
import matplotlib.pyplot as plt
import numpy as np
from numpy import linspace, meshgrid
from matplotlib import animation


Lx = 2
Ly = 2
Nx = 10
Ny = 10
Nt = 10

x = linspace(0, Lx, Nx)
y = linspace(0, Ly, Ny)
x,y = meshgrid(x,y)

fig = plt.figure()
ax = plt.axes(xlim=(0, Lx), ylim=(0, Ly))  
plt.xlabel(r'x')
plt.ylabel(r'y')

# animation function
def animate(i): 
  print x.size
  z = np.random.random(size=x.size)
  z = z.reshape(x.shape)
  cont = plt.contourf(x, y, z, 25)

  return cont  

anim = animation.FuncAnimation(fig, animate, frames=Nt)

anim.save('animation.mp4')