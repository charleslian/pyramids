# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 08:38:58 2016

@author: cl-iop
"""

import numpy as np
from matplotlib import pyplot as plt
import pyramids.io.result as dp


fig, axs = plt.subplots(1,3,sharex=True,sharey=False,figsize=(8,6))
berry = np.array([dp.getBerry(str(step)) for step in dp.getBerrySteps()])
print berry

for direct in range(3):
  axs[direct].plot(berry[:,direct])


