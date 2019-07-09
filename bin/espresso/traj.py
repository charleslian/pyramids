# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 14:28:56 2017

@author: cl-iop
"""


import numpy as np
from ase.atoms import Atoms, Atom
from ase import units
from ase.calculators.singlepoint import SinglePointCalculator
from ase.utils import basestring
#fileObj = open('result')
#traj = read(filename='result',index=slice(None),format='espresso-out')
def make_atoms(index, lines, key, cell):
    """Scan through lines to get the atomic positions."""
    atoms = Atoms()
    if key == 'Cartesian axes':
        for line in lines[index + 3:]:
            entries = line.split()
            if len(entries) == 0:
                break
            symbol = entries[1]
            #print entries, symbol, index
            x = float(entries[6])
            y = float(entries[7])
            z = float(entries[8])
            atoms.append(Atom(symbol, (x, y, z)))
        atoms.set_cell(cell)
    elif key == 'ATOMIC_POSITIONS':
        for line in lines[index + 1:]:
            entries = line.split()
            if len(entries) == 0 or (entries[0] == 'End'):
                break
            symbol = entries[0]
            #print entries
            x = float(entries[1])
            y = float(entries[2])
            z = float(entries[3])
            atoms.append(Atom(symbol, (x, y, z)))
        atoms.set_cell(cell, scale_atoms=False)
    # Energy is located after positions.
#    energylines = [number for number, line in enumerate(lines) if
#                   ('!' in line and 'total energy' in line)]
#    energyline = min([n for n in energylines if n > index])
#    energy = float(lines[energyline].split()[-2]) * units.Ry
#    # Forces are located after positions.
#    forces = np.zeros((len(atoms), 3))
#    forcelines = [number for number, line in enumerate(lines) if
#                  'Forces acting on atoms (Ry/au):' in line]
#    forceline = min([n for n in forcelines if n > index])
#    for line in lines[forceline + 4:]:
#        words = line.split()
#        if len(words) == 0:
#            break
#        fx = float(words[-3])
#        fy = float(words[-2])
#        fz = float(words[-1])
#        atom_number = int(words[1]) - 1
#        forces[atom_number] = (fx, fy, fz)
#    forces *= units.Ry / units.Bohr
#    calc = SinglePointCalculator(atoms, energy=energy, forces=forces)
#    atoms.set_calculator(calc)
    return atoms


def read_espresso_out(fileobj):
    """Reads quantum espresso output text files."""
    if isinstance(fileobj, basestring):
        fileobj = open(fileobj, 'rU')
    lines = fileobj.readlines()
    images = []

    # Get unit cell info.
    bl_line = [line for line in lines if 'bravais-lattice index' in line]
    if len(bl_line) != 1:
        raise NotImplementedError('Unsupported: unit cell changing.')
    bl_line = bl_line[0].strip()
    brav_latt_index = bl_line.split('=')[1].strip()
    if brav_latt_index != '0':
        raise NotImplementedError('Supported only for Bravais-lattice '
                                  'index of 0 (free).')
    lp_line = [line for line in lines if 'lattice parameter (alat)' in
               line]
    if len(lp_line) != 1:
        raise NotImplementedError('Unsupported: unit cell changing.')
    lp_line = lp_line[0].strip().split('=')[1].strip().split()[0]
    lattice_parameter = float(lp_line) * units.Bohr
    ca_line_no = [number for (number, line) in enumerate(lines) if
                  'crystal axes: (cart. coord. in units of alat)' in line]
    if len(ca_line_no) != 1:
        raise NotImplementedError('Unsupported: unit cell changing.')
    ca_line_no = int(ca_line_no[0])
    cell = np.zeros((3, 3))
    for number, line in enumerate(lines[ca_line_no + 1: ca_line_no + 4]):
        line = line.split('=')[1].strip()[1:-1]
        values = [float(value) for value in line.split()]
        cell[number, 0] = values[0]
        cell[number, 1] = values[1]
        cell[number, 2] = values[2]
    cell *= lattice_parameter
    #print cell
    
    for number, line in enumerate(lines):
      key = 'Begin final coordinates'  # these just reprint last posn.
      if key in line:
          break
      key = 'Cartesian axes'
      if key in line:
          atoms = make_atoms(number, lines, key, cell)
          images.append(atoms)
      key = 'ATOMIC_POSITIONS'
      if key in line:
          atoms = make_atoms(number, lines, key, cell)
          images.append(atoms)
          
    return images

images = read_espresso_out('result')
print images.pop(0)

from ase.visualize import view
polar = [atom.positions[1,:] - atom.positions[0,:] for atom in images]
polar = np.array(polar)

import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
import os
from matplotlib import pyplot as plt
import numpy as np

time = 1E3*np.array([float(line.split()[-2]) for line in os.popen('grep "time      = " result').readlines()])

fig, axs = plt.subplots(1,2,sharex=False,figsize=(8,6))

ax = axs[0]
ax.plot(time, polar[:,2])

args = ma.getPropertyFromPosition(xlabel=r'Time (fs)',
                                  ylabel=r'd$_{Pb-Ti}$  ($\AA$)', hline=[2.2],

)
ma.setProperty(ax,**args)


ax = axs[1]
from scipy.fftpack import fft, ifft
numStep = time.shape[0]

omega = (1.0/time)[:numStep/2]
epsilon = np.abs(fft(polar[:,2])[:numStep/2])
ax.plot(omega, epsilon)


args = ma.getPropertyFromPosition(xlabel=r'$\Omega$ (fs$^{-1}$)',
                                  ylabel=r'', xlimits=[0,0.05], 
ylimits=[0,600]
)
ma.setProperty(ax,**args)

  #, atom.symbols[1]

view(images)
