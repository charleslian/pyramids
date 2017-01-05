#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 08:43:18 2016

@author: cl-iop
"""

import numpy as np
import qutip as qp


def excitation(args):
    H0 = args['parity']*args['vFermi']*(args['kpoint'][0]*qp.sigmax() + args['kpoint'][1]*qp.sigmay())
    H1 = qp.sigmax()
    H2 = qp.sigmay()
    Hamiltonian = [H0,[H1,HCoeff]]
    states = H0.eigenstates()  
    psi0 = states[1][0]
    psi1 = states[1][1]
    import hashlib
    label = hashlib.sha224(str(args)).hexdigest()
    import os
    if os.path.exists('Data/'+label+'.qu'):
      result = qp.qload('Data/'+label)
      print 'Loading'
    else:
      result = qp.mesolve(Hamiltonian, psi0, args['times'], [], [], args=args)
      print 'Recalculate'
      qp.qsave(result, 'Data/'+   label)
    proj0 =  np.array([(state.dag()*psi0).norm() for state in result.states])
    proj1 =  np.array([(state.dag()*psi1).norm() for state in result.states])
    return result, proj0, proj1
    
def HCoeff(t, args):
  return args['A'] * np.sin(args['omega']*t + args['phi'])*np.exp(-((t -args['t0']) / args['sigma']) ** 2)

  
if __name__ == '__main__':
  import matplotlib.pyplot as plt
  fig, axs = plt.subplots(4,1,sharex='col',sharey='row',figsize=(12,10))
  
  kpairs = [(0.0,0.5), (0.0,1.0), (0.0,2.0)] #(np.sqrt(0.5),np.sqrt(0.5))
  for omega in 1.0, 2.0, 4.0:
    E = 0.05; A = E#/omega
    args={'A': A, 't0':20.0,'sigma': 8.0, 'omega':omega, 'phi':0.0, 'parity':1, 'vFermi' : 1}
    args['times'] = np.linspace(0.0, 50.0, 500.0)
    ax = axs[-1]
    label = r'$\omega = $ %2.1f eV'% (omega)
    ax.plot(args['times'], HCoeff(args['times'],args), label = label)
    import pyramids.plot.setting as ma
    kargs=ma.getPropertyFromPosition(ylabel=r'', xlabel='Time $t$ (1/ev)',title='')
    ma.setProperty(ax,**kargs)
    
    for index, k in enumerate(kpairs):
      print k
      args['kpoint'] = k
      result, proj0, proj1 = excitation(args)
      
      ax = axs[index]
      
      title = r'k$_x$ = %2.1f, k$_y$ = %2.1f'% (k[0],k[1])
      ax.plot(result.times, proj1, '-')
      kargs = ma.getPropertyFromPosition(ylabel=r'', xlabel='Time $t$ (1/ev)',title=title)
      ma.setProperty(ax,**kargs)
  plt.tight_layout()
  SaveName = __file__.split('/')[-1].split('.')[0] 
  for save_type in ['.pdf']:
    plt.savefig(SaveName+save_type,transparent=True,dpi=600)
    