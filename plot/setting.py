# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 18:16:20 2016
The collection of the useful methods used in the TDAP results analysis
"""

__author__ = "Chao Lian <charleslian@126.com>"
__date__ = "Fri Jan 22 18:16:20 2016"

__version__ = "1.0"
__credits__ = "Chao Lian initial and maintain the codes"

import numpy as np
import matplotlib.pyplot as plt

A4=(5.656565,8.0)
A4_LANDSCAPE=(8.0,5.656565)
A4_LANDSCAPE_ENLARGE=(397/24.5,210/25.4)
#ALPHABET = ([chr(i) for i in range(97,123)])
ALPHABET =(["("+chr(i)+")" for i in range(97,123)])

colors=['navy','orangered','mediumvioletred','maroon','green','gold','purple','grey',
        'cyan','lime','darkorange','red','magenta','pink',
        'blue','yellowgreen','chocolate','lightcoral']
#------------------------------------------------------------------- 
def getColors(colorList,cmap='jet'):
  import matplotlib.cm
  sc = matplotlib.cm.ScalarMappable(cmap=cmap)
  colors = sc.to_rgba(np.linspace(0.0,1.0,colorList))
  #colors = sc.to_rgba(np.linspace(0.1,0.9,colorList))
  return colors
  
#------------------------------------------------------------------- 
def setProperty(ax, **kargs):
  """
  a utility function to set the property of the figure axe
  """
  ax.autoscale(enable=True, axis='both', tight=None)
  
  if('ticksize' in kargs):
    ticksize = kargs['ticksize']
  else:
    ticksize='xx-large'
    
  if('labelsize' in kargs):
    labelsize = kargs['labelsize']
  else:
    labelsize='xx-large'
    
  if('loc' in kargs):
    loc = kargs['loc']
  else:
    loc = 0
            
  #if('figurelabel' in kargs):
    #from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
    #at = AnchoredText(kargs['figurelabel'], pad=0.0, prop={'size':labelsize},
    #                  frameon=True, fancybox=True, framealpha=0.5 ,loc=loc)
    #at.zorder=0
    #at.patch.set_linewidth(0)
    #ax.add_artist(at)
  
  if('xlimits' in kargs):
    ax.set_xlim(kargs['xlimits'])
    
  if('ylimits' in kargs):
    ax.set_ylim(kargs['ylimits'])
  
  if('vline' in kargs):
    for x in kargs['vline']:
      ax.axvline(x, color='k',linestyle='-.')
    
  if('hline' in kargs):
    for y in kargs['hline']:
      ax.axhline(y, color='k',linestyle='-.')

  if('xticks' in kargs):
    ax.set_xticks(kargs['xticks'])
  else:
    pass
    #xticks=ax.get_xticks()
    #ax.set_xticks(xticks[:]) 
    
  if('yticks' in kargs):
    ax.set_yticks(kargs['yticks'])
  else:
    pass
  
  
  if('xticklabels' in kargs):
    ax.set_xticklabels(kargs['xticklabels'],fontsize=ticksize)
  elif False:
    orginlabels = []
    for index,ticks in enumerate(ax.get_xticks()):
      if ticks >= ax.get_xlim()[0] and ticks <= ax.get_xlim()[1]:
        orginlabels.append(ax.get_xticklabels()[index])

    numLabels = len(orginlabels)  
    if numLabels % 2 != 0:
      for label in orginlabels:
        if label not in [orginlabels[numLabels/2], orginlabels[0], orginlabels[-1]]:
          label.set_visible(False)
    else:
      numLabels -= 1
      for label in orginlabels:
        if label not in [orginlabels[numLabels/2],orginlabels[0],orginlabels[-2]]:
          label.set_visible(False)
      

  if('yticklabels' in kargs):
    ax.set_yticklabels(kargs['yticklabels'],fontsize=ticksize)
  elif False:
    orginlabels = []
    for index,ticks in enumerate(ax.get_yticks()):
      if ticks >= ax.get_ylim()[0] and ticks <= ax.get_ylim()[1]:
        orginlabels.append(ax.get_yticklabels()[index])

    numLabels = len(orginlabels)  
    if numLabels % 2 != 0:
      for label in orginlabels:
        if label not in [orginlabels[numLabels/2], orginlabels[0], orginlabels[-1]]:
          label.set_visible(False)
    else:
      numLabels -= 1
      for label in orginlabels:
        if label not in [orginlabels[numLabels/2],orginlabels[0],orginlabels[-2]]:
          label.set_visible(False)
      
  if('title' in kargs):
    ax.set_title(kargs['title'],fontsize=labelsize) 
  
  if kargs['grid']:
    ax.grid(linestyle='--', linewidth=1, which='major')
     
  if('xlabel' in kargs) and len(ax.get_xticklabels()) > 0 :
    if ax.get_xticklabels()[0].get_visible():  
      ax.set_xlabel(kargs['xlabel'],fontsize=labelsize) 
  if('ylabel' in kargs) and len(ax.get_yticklabels()) > 0:
    if ax.get_yticklabels()[0].get_visible():    
      ax.set_ylabel(kargs['ylabel'],fontsize=labelsize) 
  #ax.get_yaxis().get_major_formatter().set_useOffset(False)

  ax.tick_params(labelsize=ticksize)
  if kargs['minortick']:
      ax.minorticks_on()
  #print ax.get_xlim(),ax.get_ylim()
  ax.legend(fontsize='large',loc=loc,frameon=False, ncol=1, fancybox=True, framealpha=0.5)

def getPropertyFromPosition(index=None, xlabel='',ylabel='',title='', 
                            grid = False, minortick=True, legendLoc = None,
                            xticks=None, yticks=None, 
                            xticklabels=None, yticklabels=None,
                            xlimits=None, ylimits=None,
                            hline = None, vline = None,
                            ticksize = None):
  """
  a utility function to set the property of the figure axe
  """
  args={}
  if index is not None:
    args['figurelabel']=str(ALPHABET[index])
    args['title'] = str(ALPHABET[index])+' '+title
  else:
    args['title'] = title
    
  if legendLoc is not None:
    args['loc']= legendLoc
  else:
    args['loc'] = 0  
    
  args['ylabel'] = ylabel
  args['xlabel'] = xlabel
  args['grid'] = grid
  args['minortick'] = minortick

  if xticks is not None:
    args['xticks'] = xticks
  if yticks is not  None:
    args['yticks'] = yticks
  if vline is not  None:
    args['vline'] = vline  
  if hline is not  None:
    args['hline'] = hline  

  if xticklabels is not  None:
    args['xticklabels'] = xticklabels
  if yticklabels is not  None:
    args['yticklabels'] = yticklabels 
  if xlimits is not  None:
    args['xlimits'] = xlimits
  if ylimits is not  None:
    args['ylimits'] = ylimits
  if ticksize is not None:
    args['ticksize'] = ticksize    
  
  return args

if __name__== '__main__':
  fig, axs = plt.subplots(4,2,sharex=True,sharey=True)
  x=[i/100.0 for i in range(-1000,1000)]
  y=np.sin(x)
  axs = axs.flatten()
  
  for index in range(8):
    ax=axs[index]
    args=getPropertyFromPosition(index,'Time',r'$E_v$')
    args['xlimits']=(0.0,10.0)
    ax.plot(x,y,'-')
    setProperty(ax,**args)
    
  plt.tight_layout()
  