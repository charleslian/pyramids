import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from pyramids.plot.setting import getPropertyFromPosition, setProperty
import pyramids.io.result as dp

#fig,axs = plt.subplots(3,1,sharey=True)
fig = plt.figure(figsize=(6,8))


omega = 0.5
L = 10.0
k = (1/L)*2*np.pi
x = np.linspace(0,L,100)
t0 = 100

def gaussian(t, t0):
 return np.exp(-(t-t0)**2/(t0*0.66)**2)

ax0 = fig.add_subplot(3,1,1)
light = np.sin(omega*0.0 + k*x)
line, = ax0.plot(x,light)
comp, = ax0.plot([0,L],[0,0],'--')
kargs=getPropertyFromPosition(xlabel=r'distance',ylabel=r'EField')
setProperty(ax0,**kargs)

ax1 = fig.add_subplot(3,1,2,sharex=ax0)
light2 = np.sin(omega*0.0 + k*x)
line2, = ax1.plot(x,light2)
kargs=getPropertyFromPosition(xlabel=r'distance',ylabel=r'EField')
setProperty(ax1,**kargs)


ax2 = fig.add_subplot(3,1,3)
interval = np.linspace(0,2*t0,500)
ax2.plot(interval,np.sin(omega*interval)*gaussian(interval,t0))
scatter, = ax2.plot(0,np.sin(omega*0),'o')
kargs=getPropertyFromPosition(xlabel=r'Time',ylabel=r'EField')
setProperty(ax2,**kargs)

def update_quiver(num):
    """updates the horizontal and vertical vector components by a
    fixed increment on each frame
    """
    rate = 0.5
    cycle = int(2*t0/rate)
    
    num = num%cycle
    t = num*rate
    #if num not in dp.getBerrySteps():
    #  return
    line.set_data(x,np.sin(omega*t+k*x)*gaussian(t,t0))
    line2.set_data(x,np.sin(omega*t)*gaussian(t,t0))
    comp.set_data([0,L],[np.sin(omega*t)*gaussian(t,t0),np.sin(k*L+omega*t)*gaussian(t,t0)])
    scatter.set_data(t,np.sin(omega*t)*gaussian(t,t0))

# you need to set blit=False, or the first set of arrows never gets
# cleared on subsequent frames
anim = animation.FuncAnimation(fig, update_quiver,
                               interval=10, blit=False)
                               
                               
plt.tight_layout()                        
plt.show()