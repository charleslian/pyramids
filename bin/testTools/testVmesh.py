# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 16:28:29 2016

@author: cl-iop
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from pyramids.plot.setting import getPropertyFromPosition, setProperty

import pyramids.io.result as dp

def read(filename='siesta.Vmesh'):
  return np.array([float(line.split()[-1]) for line in open(filename)])


fig = plt.figure(figsize=(6,8))
ax = fig.add_subplot(1,1,1)
line, = ax.plot(read('siesta0.Vmesh'))  


def update_quiver(num):
    """updates the horizontal and vertical vector components by a
    fixed increment on each frame
    """
    num = num%50
    line.set_ydata(read('siesta'+str(num)+'.Vmesh'))

# you need to set blit=False, or the first set of arrows never gets
# cleared on subsequent frames
anim = animation.FuncAnimation(fig, update_quiver,
                               interval=10, blit=False)