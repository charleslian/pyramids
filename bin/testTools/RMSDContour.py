import numpy as np
from matplotlib import pyplot as plt
import pyramids.io.result as dp
from pyramids.plot.PlotUtility import scanFolder
import pyramids.plot.setting as ma
import pyramids.process.struct as pps

def plotContourByMatrix(x,y,z,ax):
  X, Y = np.meshgrid(x, y)
  Z = np.array(z) 
  cts = [f(X, Y, Z, nContour, cmap=cmap, alpha = 1.0, ) for f in ax.contour, ax.contourf]
  plt.colorbar(cts[1],ax=ax)
#--------------------------------------------------------------------------------------------
def action(index,folder):
  dataCurFolder = []
  dataCurFolder.append([index, folder])
  dp.getTrajactory()
  dataCurFolder.append(pps.calculateRMSD())
  dataCurFolder.append(dp.getEnergyTemperaturePressure())
  return dataCurFolder
  
#--------------------------------------------------------------------------------------------
fig, axs = plt.subplots(1,2,sharex=True,sharey=True,figsize=(10,6))#
data = scanFolder(action)
c = ma.getColors(len(data))


x = []
y = []
z = []
T = []
for line in data:
  index, folder = line[0]
  x = line[1][0]
  y.append(float(folder))
  z.append(line[1][1])
  T.append(line[2][1])

nContour = 300
cmap = 'jet'
xlabel=r'Time (fs)'
ylabel=r'$\varepsilon$ (Ry/Bohr/e)'

x = np.array(x)
y = np.array(y)
z = np.array(z)

ax = axs[0]
plotContourByMatrix(x,y,z,ax)
args = ma.getPropertyFromPosition(xlabel=xlabel, ylabel=ylabel)
ma.setProperty(ax,**args)
 
ax = axs[1] 
plotContourByMatrix(x,y,T,ax)
args = ma.getPropertyFromPosition(xlabel=xlabel, ylabel=ylabel)
ma.setProperty(ax,**args)



plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]
if True:
  for save_type in ['.pdf','.png']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=600)