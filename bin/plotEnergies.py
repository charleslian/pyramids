#!/usr/bin/python
if __name__ == '__main__':
  import matplotlib.pyplot as plt
  plt.style.use('ggplot')
  fig, ax = plt.subplots(1,1,sharex=True,sharey=False,figsize=(10,6))
  from pyramids.plot.PlotUtility import plotTotalEnergy
  plotTotalEnergy(ax)
  SaveName = __file__.split('/')[-1].split('.')[0]
  plt.tight_layout()
  if False:
    for save_type in ['.pdf','.png']:
      filename = SaveName + save_type
      plt.savefig(filename,dpi=600)