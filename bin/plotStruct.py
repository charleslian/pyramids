import numpy as np
from scipy.fftpack import fft, ifft
from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import matplotlib.pyplot as plt
import os

import pyramids.plot.PlotUtility as pu
from ase.calculators.siesta.import_functions import xv_to_atoms
from ase.visualize import view
import pyramids.io.output as tdio
from ase.io import write

#atoms = xv_to_atoms('siesta.XV')
pu.generateStructPNG(cell=True, repeat=[3,3,1])