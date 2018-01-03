import SubPlot
import matplotlib.dates as mdates
import datetime as dt

class Panning_SubPlot(SubPlot):
  def __init__(self, dimensions, fig, time_attr, time_fmt, time_delta=(1, 's'), axis=(1,0),
               laxis_attr=[], raxis_attr=[],
               laxis_marker=[], raxis_marker=[],
               laxis_lim=(-1, 1), raxis_lim=(-1, 1),
               num_points=15):

    SubPlot.__init__(self, dimensions, 'panning')
    self.fig = fig
    self.time_attr = time_attr
    self.time_format = time_fmt,
    self.time_delta = time_delta
    self.axis = axis
    self.left_axis_attr = laxis_attr
    self.right_axis_attr = raxis_attr
    self.left_axis_lim = laxis_lim
    self.right_axis_lim = raxis_lim
    self.num_points = num_points

    self.ax = fig.add_subplot(self.dimensions)

    if self.axis[1] == 1:
      self.ax2 = self.ax.twinx()

    self.ax.set_ylim([self.left_axis_lim[0], self.left_axis_lim[1]])
    self.ax.xaxis.set_major_formatter(mdates.DateFormatter(self.time_format))

    if isinstance(laxis_marker, list):
      if len(laxis_marker) == 1:
        self.left_axis_markers = dict(zip(self.left_axis_attr, [laxis_marker[0]] * len(self.left_axis_attr)))
      elif len(laxis_marker) == len(self.left_axis_attr):
        self.left_axis_markers = dict(zip(self.left_axis_attr, laxis_marker))
      else:
        self.usage()
    else:
      self.usage()

  def plot(self, x, y, marker, label):
    #return self.ax.plot(times, range(len(times)), color=(0, 0, 1))
    pass
