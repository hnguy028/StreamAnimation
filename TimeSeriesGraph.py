import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np
import time

class TimeSeriesGraph():
  def __init__(self):
    # setup figure
    self.fig = plt.figure()

    # add subplot
    self.ax = self.fig.add_subplot(1, 1, 1)

    # viewing frame size
    self.viewing_frame = 25

    # init viewing frame limits
    self.ax.set_xlim([0, self.viewing_frame])
    self.ax.set_ylim([0, 1])

    self.graph, = self.ax.plot([], [], color=(0, 0, 1))

    self.ani = animation.FuncAnimation(self.fig, self._update, frames=self._generator(), interval=200, blit=False)

    plt.show()

  def _generator(self):
    kwargs = {}
    kwargs["points"] = np.empty(0)
    num = 0

    while 1:
      num += 1
      kwargs['n'] = num
      # kwargs['date'] = np.arange(max(0,num - self.viewing_frame), num)
      kwargs['date'] = np.random.rand(num)
      kwargs["points"] = np.append(kwargs["points"], np.random.rand(1))
      if len(kwargs["points"]) > self.viewing_frame:
        kwargs["points"] = np.delete(kwargs["points"], 0)
      yield kwargs

  def _update(self, kwargs):
      n = kwargs['n']
      x = kwargs['date']
      points = kwargs["points"]

      self.graph.set_xdata(x)
      self.graph.set_ydata(points)

      # self.ax.set_xticklabels()

      if n > self.viewing_frame:
        self.ax.set_xlim(n - self.viewing_frame, n)
      else:
        # makes it look ok when the animation loops
        self.ax.set_xlim(0, self.viewing_frame)

      return self.graph

if __name__ == '__main__':
  ani = TimeSeriesGraph()