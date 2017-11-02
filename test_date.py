u = u"""2016-07-11-095303.810,1,79
2016-07-11-095303.900,1,77
2016-07-11-095303.990,1,59
2016-07-11-095304.080,1,48
2016-07-11-095304.170,1,48
2016-07-11-095304.260,1,77
2016-07-11-095304.350,1,81
2016-07-11-095304.440,1,63
2016-07-11-095304.530,1,54
2016-07-11-095304.620,1,29"""

import io
import numpy
import matplotlib.pyplot as plt
from matplotlib import animation
import datetime
from numpy import genfromtxt


cv = numpy.genfromtxt (io.StringIO(u), delimiter=",")
second = cv[:,0]
third = cv[:,2]
FMT = '%Y-%m-%d-%H%M%S.%f'
data = numpy.genfromtxt(io.StringIO(u), delimiter=',', skip_header=2,
                        names=['t', 'in', 'x', 'y','z'],
                        dtype=['object', 'int8', 'float'])
d = [datetime.datetime.strptime(i.decode('ascii'), FMT) for i in data['t']]


x = d
y = data["x"]
fig, ax = plt.subplots()
line, = ax.plot_date([], [], 'b-')
ax.margins(0.05)

def init():
    line.set_data(x[:2],y[:2])
    return line,

def animate(i):
    imin = 0 #min(max(0, i - win), x.size - win)
    xdata = x[imin:i+2]
    ydata = y[imin:i+2]
    line.set_data(xdata, ydata)

    ax.relim()
    ax.autoscale()
    return line,

anim = animation.FuncAnimation(fig, animate, frames=7,init_func=init, interval=150)

plt.show()