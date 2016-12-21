import numpy as np
import pyramids.io.result as dP
def action(index,folder):
  time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure(ave=True)
  return  E_ks
  
if __name__ == '__main__':
  ref =action(1,'')
  np.save('ref',ref)
