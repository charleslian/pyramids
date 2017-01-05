import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import pyramids.io.result as dp


fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111)

kcoor, kweight = dp.readKpoints()
Berry = dp.getBerry(str(3))

quiverLine = ax.quiver(kcoor[:,0], kcoor[:,1], Berry[:,0],Berry[:,1],
        units='x',lw=0.5, edgecolors=('k'), headaxislength=5,
        color='b',zorder=10,pivot='middle',alpha = 0.5)

#for step in dp.getBerrySteps():
  #Berry = dp.getBerry(str(step))
#print dp.getBerrySteps()

def update_quiver(num, quiverLine):
    """updates the horizontal and vertical vector components by a
    fixed increment on each frame
    """
    
    if num not in dp.getBerrySteps():
      return
    Berry = dp.getBerry(str(num))

    quiverLine.set_UVC(Berry[:,0],Berry[:,1])

    return quiverLine,

# you need to set blit=False, or the first set of arrows never gets
# cleared on subsequent frames
anim = animation.FuncAnimation(fig, update_quiver, fargs=(quiverLine,),
                               interval=10, blit=False)
plt.show()