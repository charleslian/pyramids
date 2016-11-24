# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 18:16:20 2016
The collection of the useful methods used in the TDAP results analysis
"""

__author__ = "Chao Lian <charleslian@126.com>"
__date__ = "Fri Jan 22 18:16:20 2016"

__version__ = "1.0"
__credits__ = "Chao Lian initial and maintain the codes"

import matplotlib
matplotlib.use('agg')

import os
import numpy as np
import pyramids.process.struct as tdp
import pyramids.plot.setting as tps
def confStructrueFigure(ax):
  ax.axis('equal')
  colors = ['r','g','b']
  ax.annotate(s='',xy=(0.4,0),xytext=(0,0),xycoords='axes fraction',
                arrowprops=dict(width=2.0,color=colors[0])) 
  ax.text(0.45,-0.02,'x',fontsize='xx-large',transform=ax.transAxes)
  ax.text(0,0.45,'y',fontsize='xx-large',transform=ax.transAxes)
  ax.text(0.22,0.22,'z',fontsize='xx-large',transform=ax.transAxes)
  ax.annotate(s='',xy=(0,0.4),xytext=(0,0),xycoords='axes fraction',
                arrowprops=dict(width=2.0,color=colors[1]))  
  ax.annotate(s='',xy=(0.2,0.2),xytext=(0,0),xycoords='axes fraction',
                arrowprops=dict(width=2.0,color=colors[2])) 
#-------------------------------------------------------------------
def generateStructPNG(atoms=None, rotation=[0,0,0],camera='perspective',repeat = [1,1,1], cell=False,**args):
  from ase.calculators.siesta.import_functions import xv_to_atoms
  from ase.io import write
  if atoms is None:
    atoms = xv_to_atoms('siesta.XV')
  
  rot = str(rotation[0])+'x,'+str(rotation[1])+'y,'+str(rotation[2])+'z'
  
  if cell:
    showcell = 2
  else:
    showcell = 0
  kwargs = {
      'rotation'      : rot, # text string with rotation (default='' )
      'radii'         : 1.0, # float, or a list with one float per atom
      'colors'        : None,# List: one (r, g, b) tuple per atom
      'show_unit_cell': showcell,   # 0, 1, or 2 to not show, show, and show all of cell
      }
  kwargs.update({
    'run_povray'   : True, # Run povray or just write .pov + .ini files
    'display'      : False,# Display while rendering
    'pause'        : True, # Pause when done rendering (only if display)
    'transparent'  : True,# Transparent background
    'canvas_width' : None, # Width of canvas in pixels
    'canvas_height': 800, # Height of canvas in pixels 
    'camera_dist'  : 12000.,  # Distance from camera to front atom
    'image_plane'  : 0, # Distance from front atom to image plane
    'camera_type'  : camera, # perspective, ultra_wide_angle, orthographic
    'point_lights' : [],             # [[loc1, color1], [loc2, color2],...]
    'area_light'   : [(2., 3., 40.), # location
                      'White',       # color
                      .7, .7, 3, 3], # width, height, Nlamps_x, Nlamps_y
    'background'   : 'White',        # color
    'textures'     : None, # Length of atoms list of texture names
    'celllinewidth': 0.1,  # Radius of the cylinders representing the cell
    })
    
  cell = atoms.cell
  atoms.center()
  atoms = atoms*repeat
  for position in atoms.positions: 
    position -= repeat[0]/2*cell[0,:]
    position -= repeat[1]/2*cell[1,:]
    position -= repeat[2]/2*cell[2,:]
  atoms.cell = cell
  write('struct.pov',atoms, **kwargs)

  
def insertImag(ax,filename='struct.png'):
  import matplotlib.pyplot as plt
  image = plt.imread(filename) 
  im = ax.imshow(image)
  ax.axis('off')
    
#-------------------------------------------------------------------
def insertStruct(ax,**args):
  import matplotlib.pyplot as plt
  colors = ['r','g','b']
  #if not os.path.exists('struct.png'):
  generateStructPNG(**args)
  image = plt.imread('struct.png') 
  
  from mpl_toolkits.axes_grid1.inset_locator import inset_axes
  axin = inset_axes(ax,
                     width=args['width'],  # width = 30% of parent_bbox
                     height=args['height'],  # height : 1 inch
                     loc=args['loc'])
  im = axin.imshow(image)
  axin.axis('off')  
  #axins.axis('equal')  
  #axins.axis('tight')
  #axins.set_xticks([])
  #axins.set_yticks([])
  
  axin.annotate(s='',xy=(0.4,0),xytext=(0,0),xycoords='axes fraction',
                arrowprops=dict(width=2.0,color=colors[0])) 
                
  axin.text(0.45,-0.02,'x',fontsize='xx-large',transform=axin.transAxes)
  axin.text(0,0.45,'y',fontsize='xx-large',transform=axin.transAxes)
  axin.text(0.22,0.22,'z',fontsize='xx-large',transform=axin.transAxes)
   
  axin.annotate(s='',xy=(0,0.4),xytext=(0,0),xycoords='axes fraction',
                arrowprops=dict(width=2.0,color=colors[1]))  
  axin.annotate(s='',xy=(0.2,0.2),xytext=(0,0),xycoords='axes fraction',
          arrowprops=dict(width=2.0,color=colors[2])) 
  return axin, im  
  
#-------------------------------------------------------------------
def scanFolder(action,folders=None):
  if folders is None:
    folders = [folder for folder in os.listdir('.')
                if os.path.isdir(folder)]                

  folders.sort()   
  collection = []   
  for index,folder in enumerate(folders):
    print "running in ",folder    
    os.chdir(folder)
    collection.append(action(index,folder))
    os.chdir('..')
  return collection

#-------------------------------------------------------------------
def drawEnergy(ax, relative = False, divided = 1.0, popFirstStep = True, label = ''):
  """
  Draw the KS Energy and Total Energy in the ax
  """
  X, temp, E_KS, Etot, volume, pressure  =  tdp.getEnergyTemperaturePressure()
  
  refEnergy=E_KS[0]
  if relative:
    E_KS = E_KS - refEnergy
    Etot = Etot - refEnergy
  
  if popFirstStep:
    ax.plot(X[1:],E_KS[1:]/divided,'-',linewidth=3.0,label = 'KS'+ label)#,color=tps.colors[0]
    ax.plot(X[1:],Etot[1:]/divided,'--',linewidth=3.0,label = 'Total'+ label)#,color=tps.colors[2]
  else:
    ax.plot(X,E_KS/divided,'-',linewidth=3.0,label = 'KS' + label)#,color=tps.colors[0]
    ax.plot(X,Etot/divided,'--',linewidth=3.0,label = 'Total' + label)#,color=tps.colors[2]
  
  kargs = tps.getPropertyFromPosition(index=None, 
                                         xlabel=r'Time(fs)',ylabel=r'Energy(eV)',title='', 
                                         xticks=None, yticks=None, 
                                         xticklabels=None, yticklabels=None,
                                         xlimits=None, ylimits=None)
                                 
  tps.setProperty(ax, **kargs)
  
    
#-------------------------------------------------------------------
def drawTemperature(ax, label = ''):
  """
  Draw the KS Energy and Total Energy in the ax
  """
  X, temp, E_KS, Etot, volume, pressure  =  tdp.getEnergyTemperaturePressure()
  ax.plot(X,temp/1E3,'-',linewidth=3.0,label = 'T'+ label)#,color=tps.colors[0]

  kargs = tps.getPropertyFromPosition(index=None, 
                                         xlabel=r'Time(fs)',ylabel=r'T($10^3$K)',title='', 
                                         xticks=None, yticks=None, 
                                         xticklabels=None, yticklabels=None,
                                         xlimits=None, ylimits=None)               
  tps.setProperty(ax, **kargs)                  
  
#-------------------------------------------------------------------  
def drawPressure(ax, label = ''):
  """
  Draw the KS Energy and Total Energy in the ax
  """
  X, temp, E_KS, Etot, volume, pressure  =  tdp.getEnergyTemperaturePressure()
  ax.plot(X,pressure,'-',linewidth=3.0,label = 'Pressure '+ label)#,color=tps.colors[0]

  kargs = tps.getPropertyFromPosition(index=None, 
                                         xlabel=r'Time(fs)',ylabel=r'Pressure(KBar)',title='', 
                                         xticks=None, yticks=None, 
                                         xticklabels=None, yticklabels=None,
                                         xlimits=None, ylimits=None)               
  tps.setProperty(ax, **kargs)

#-------------------------------------------------------------------
def drawEigenvalue(ax, label = ''):
  """
  Draw the KS Energy and Total Energy in the ax
  """
  X,eo  =  tdp.getEigenvalues()
  X,qo  =  tdp.getPartition()

  countEleState = 0 
  countHolState = 0 
  countNormalState = 0
  for i in range(eo.shape[1]):
    if eo[0,i] > 0.03 and qo[0,i] > 0.2:
      if countEleState == 0:    
        ax.plot(X,eo[:,i],'-',linewidth=3.0,color=tps.colors[0],label='Electron'+ label)
      else:
        ax.plot(X,eo[:,i],'-',linewidth=3.0,color=tps.colors[0])
      countEleState += 1
    elif eo[0,i] < -0.03 and qo[0,i] < 1.8:
      if countHolState == 0:    
        ax.plot(X,eo[:,i],'-',linewidth=3.0,color=tps.colors[1],label='Hole'+ label)
      else:
        ax.plot(X,eo[:,i],'-',linewidth=3.0,color=tps.colors[1])
      countHolState +=1
    else:
      if countNormalState == 0:    
        ax.plot(X,eo[:,i],'--',linewidth=3.0,color='grey',alpha=0.7,label='Normal'+ label)
      else:
        ax.plot(X,eo[:,i],'--',linewidth=3.0,color='grey',alpha=0.7)
      countNormalState +=1

  #ax.plot(X,eo,'-',linewidth=qo,label = 'Eigenvalues')#,color=tps.colors[0]
  kargs = tps.getPropertyFromPosition(index=None, 
                                         xlabel=r'Time(fs)',ylabel=r'Eigenvalues(eV)',title='', 
                                         xticks=None, yticks=None, 
                                         xticklabels=None, yticklabels=None,
                                         xlimits=None, ylimits=None)               
  tps.setProperty(ax, **kargs)
  
#-------------------------------------------------------------------  
def drawPartition(ax, label = ''):
  """
  Draw the KS Energy and Total Energy in the ax
  """
  X,qo  =  tdp.getPartition()
  ax.plot(X,qo,'-',linewidth=3.0,label = 'Partitions '+ label)#,color=tps.colors[0]
  kargs = tps.getPropertyFromPosition(index=None, 
                                         xlabel=r'Time(fs)',ylabel=r'Partition',title='', 
                                         xticks=None, yticks=None, 
                                         xticklabels=None, yticklabels=None,
                                         xlimits=None, ylimits=None)               
  tps.setProperty(ax, **kargs) 
  
#-------------------------------------------------------------------  
def drawRMSD(ax,selected=None, label = '', init = 0):
  """
  Draw the KS Energy and Total Energy in the ax
  """
  systemLabel,timestep = tdp.getSystemLabelTimpstep()
  if selected == None:
    selected = range(0,tdp.getNumStep(),int(1.0/timestep))
    
  tdp.splitMDCAR()
  time,distance,velocity = tdp.calculateRMSD(selected, init=init)
  
  #os.remove('POSCAR')
  ax.plot(time,distance,linewidth=3.0,label='RMSD'+ label)#,color=tps.colors[0])
  kargs = tps.getPropertyFromPosition(index=None, 
                                         xlabel=r'Time(fs)',ylabel=r'RMSD($\AA$)',title='', 
                                         xticks=None, yticks=None, 
                                         xticklabels=None, yticklabels=None,
                                         xlimits=None, ylimits=None)           
  tps.setProperty(ax, **kargs) 
  
#-------------------------------------------------------------------  
def drawRDF(ax,step=None, label = ''):
  """
  Draw the KS Energy and Total Energy in the ax
  """
  if step == None:
    step = tdp.getNumStep()
  
  systemLabel,timestep = tdp.getSystemLabelTimpstep()
  tdp.splitMDCAR()
  hist,bin_edges = tdp.calculateRDF(step-1)
  ax.plot(bin_edges[:-1],hist,linewidth=3.0,label='RDF '+str((step)*timestep)+' fs'+ label) #,color=tps.colors[0]
  kargs = tps.getPropertyFromPosition(index=None, 
                                         xlabel=r'Radius($\AA$)',ylabel=r'RDF(a.u.)',title='', 
                                         xticks=None, yticks=None, 
                                         xticklabels=None, yticklabels=None,
                                         xlimits=None, ylimits=None)           
  tps.setProperty(ax, **kargs) 
  
#-------------------------------------------------------------------  
def drawBands(ax,bandType='e', label = ''):
  """
  Draw the KS Energy and Total Energy in the ax
  """
  X, Ek, xticks, xticklabels = tdp.getBands()
  if bandType == 'e':
   eFermi = tdp.getFermiEnergy()
   Ek = Ek - eFermi
   ylabel = 'Energy(eV)'
  else:
   ylabel = r'$\omega$(cm$^{-1}$)'
 
  alpha = 1.0
  color = 'b'
  for ispin in range(Ek.shape[2]):
    for iband in range(1,Ek.shape[1]):
      ax[0].plot(X,Ek[:,iband,ispin],lw=3.0,ls='-',color=color,alpha=alpha,label=label)
  
  kargs = tps.getPropertyFromPosition(index=None, 
                                         xlabel=r'',ylabel=ylabel,title='', 
                                         xticks=xticks, yticks=None, 
                                         xticklabels=xticklabels, yticklabels=None,
                                         xlimits=None, ylimits=None)           
  tps.setProperty(ax, **kargs) 


if __name__ == '__main__':
  import matplotlib.pyplot as plt
  saveTypes=['pdf','png','eps']
  fig=plt.figure(figsize=tps.A4_LANDSCAPE)#_LANDSCAPE
  plt.subplots_adjust(left=0.1, bottom=0.10, right=0.95, top=0.95, wspace=0.3, hspace=0.05)
  print "-----------------------------draw Energy------------------------------------"
  drawEnergy(plt.subplot(111))
  for save_type in saveTypes:
    plt.savefig('Energy.'+save_type,transparent=True,dpi=600)
  
  print "-----------------------------draw Temperature--------------------------------"
  fig=plt.figure(figsize=tps.A4_LANDSCAPE)
  drawTemperature(plt.subplot(111))
  for save_type in saveTypes:
    plt.savefig('Temperature.'+save_type,transparent=True,dpi=600)
    
  print "-----------------------------draw Pressure----------------------------------"
  fig=plt.figure(figsize=tps.A4_LANDSCAPE)
  drawPressure(plt.subplot(111))
  for save_type in saveTypes:
    plt.savefig('Pressure.'+save_type,transparent=True,dpi=600)    
    
  print "-----------------------------draw Eigenvalues----------------------------------"
  fig=plt.figure(figsize=tps.A4_LANDSCAPE)
  drawEigenvalue(plt.subplot(111))
  for save_type in saveTypes:
    plt.savefig('Eigenvalues.'+save_type,transparent=True,dpi=600)
    
  print "-----------------------------draw RMSD----------------------------------"
  fig=plt.figure(figsize=tps.A4_LANDSCAPE)
  drawRMSD(plt.subplot(111))
  for save_type in saveTypes:
    plt.savefig('RMSD.'+save_type,transparent=True,dpi=600)       

  print "-----------------------------draw RDF----------------------------------"
  fig=plt.figure(figsize=tps.A4_LANDSCAPE)
  drawRDF(plt.subplot(111),step=1)
  drawRDF(plt.subplot(111))
  for save_type in saveTypes:
    plt.savefig('RDF.'+save_type,transparent=True,dpi=600)           
