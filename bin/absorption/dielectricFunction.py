# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 15:50:28 2016

@author: cl-iop
"""
import numpy as np
from scipy.fftpack import fft, ifft

dipole = np.array([[float(num) for num in line.split()[-3:]] for line in open('dipole.dat')])
print dipole

y = fft(dipole[:,2])
import matplotlib.pyplot as plt
plt.plot(np.imag(y))
plt.grid()
plt.show()

yinv = ifft(y)