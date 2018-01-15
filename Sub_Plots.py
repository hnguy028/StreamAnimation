from SubPlotMeta import SubPlot
import matplotlib.pyplot as plt
from dateutil.relativedelta import *

import matplotlib.dates as mdates
import datetime as dt

class Panning_SubPlot(SubPlot):
  def __init__(self, dimensions, fig, time_attr, time_fmt, time_delta=(1, 's'), axis=(1, 0),
               laxis_attr=[], raxis_attr=[],
               laxis_color=None, raxis_color=None,
               laxis_marker=None, raxis_marker=None,
               laxis_lim=(0, 1), raxis_lim=(0, 1),
               num_points=15):
    SubPlot.__init__(self, dimensions, 'panning')
    self.fig = fig
    self.time_attr = time_attr
    self.time_format = time_fmt
    self.time_delta = time_delta
    self.axis = axis

    self.left_axis_attr = laxis_attr
    self.right_axis_attr = raxis_attr
    self.left_axis_lim = laxis_lim
    self.right_axis_lim = raxis_lim

    self.num_points = num_points

    # add subplot
    self.ax = self.fig.add_subplot(self.dimensions)

    # set xaxis format to the time format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(self.time_format))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    # set y axis limits
    self.ax.set_ylim([self.left_axis_lim[0], self.left_axis_lim[1]])

    # if second axis dimension is set then add to plot
    if self.axis[1] == 1:
      self.ax2 = self.ax.twinx()
      self.ax2.set_ylim([self.right_axis_lim[0], self.right_axis_lim[1]])

      plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(self.time_format))
      plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    # load plot markers / colors
    self._load_markers(laxis_color, laxis_marker, raxis_color, raxis_marker)

  def usage(self):
    pass

  def _load_markers(self, lc, lm, rc, rm):

    if lc == lm == rc == rm == None:
      raise ValueError('Null values for all axes marker')

    self.markers = [{}, {}]

    if lm is not None:
      left_markers = lm
    else:
      left_markers = lc

    if rm is not None:
      right_markers = rm
    else:
      right_markers = rc

    if left_markers is not None:
      if isinstance(left_markers, list):
        if len(left_markers) == 1:
          self.markers[0] = dict(zip(self.left_axis_attr, [left_markers[0]] * len(self.left_axis_attr)))
        elif len(left_markers) == len(left_markers):
          self.markers[0] = dict(zip(self.left_axis_attr, left_markers))
        else:
          if len(left_markers) < len(self.left_axis_attr):
            self.markers[0] = dict(zip(self.left_axis_attr, left_markers + ['black'] * (len(self.left_axis_attr) - len(left_markers))))
          else:
            self.markers[0] = dict(zip(self.left_axis_attr, left_markers[:len(self.left_axis_attr)]))
      else:
        self.markers[0] = dict(zip(self.left_axis_attr, [left_markers] * len(self.left_axis_attr)))

    if right_markers is not None:
      if isinstance(right_markers, list):
        if len(right_markers) == 1:
          self.markers[1] = dict(zip(self.right_axis_attr, [right_markers[0]] * len(self.right_axis_attr)))
        elif len(right_markers) == len(right_markers):
          self.markers[1] = dict(zip(self.right_axis_attr, right_markers))
        else:
          if len(right_markers) < len(self.right_axis_attr):
            self.markers[1] = dict(zip(self.right_axis_attr, right_markers + ['black'] * (len(self.right_axis_attr) - len(right_markers))))
          else:
            self.markers[1] = dict(zip(self.right_axis_attr, right_markers[:len(self.right_axis_attr)]))
      else:
        self.markers[1] = dict(zip(self.right_axis_attr, [right_markers] * len(self.right_axis_attr)))

  # init plot (before update loops)
  def plot_init(self):
    return self.ax.plot()

  '''
    xs : linear array of datetimes
    ys : dictionary of points for each attribute
  '''
  def plot(self, xs, ys):
    lsymb = []
    lmrp = []

    rsymb = []
    rmrp = []

    if self.axis[0] == 1:
      for i in range(len(self.left_axis_attr)):
        s, v = self.plot_list(xs, ys[self.left_axis_attr[i]], self.left_axis_attr[i], 0)
        lsymb.append(s)
        lmrp.append(v)

      if self.axis[1] == 0:
        return lsymb, lmrp, self.left_axis_attr

    if self.axis[1] == 1:
      for i in range(len(self.right_axis_attr)):
        s, v = self.plot_list(xs, ys[self.right_axis_attr[i]], self.right_axis_attr[i], 1)
        rsymb.append(s)
        rmrp.append(v)

      if self.axis[0] == 0:
        return rsymb, rmrp, self.right_axis_attr

    return [lsymb, rsymb], [lmrp, rmrp], [self.left_axis_attr, self.right_axis_attr]

  '''
      axis = [0:left | 1:right | 2:both]
      return the symbol representation if y values on the plot, and most recent point plotted from y
  '''
  def plot_list(self, x, y, label, axis):
    if axis == 0:
      return self.ax.plot(x, y, self.markers[0][label])[0], str(y[-1:])
    elif axis == 1:
      return self.ax2.plot(x, y, self.markers[1][label])[0], str(y[-1:])
    else:
      raise IndexError('No axes have been set to plot')

  '''
      Sets the x axis labels given the upper bound of the datetime (right most label for the x axis), interval between 
      ticks is determined by time_delta defined in construction of the subplot
      
      TODO : implement a lower bound for left panning plots
  '''
  def set_xlim(self, datetime_upper):

    default_datetime = dt.datetime.strptime('1970-01-01 0:0:0', '%Y-%m-%d  %H:%M:%S')

    if self.time_delta[1] in ['s', 'secs', 'seconds']:
      self.ax.set_xlim([max(datetime_upper - relativedelta(seconds=self.num_points * self.time_delta[0]), default_datetime),
                        datetime_upper])
    elif self.time_delta[1] in ['m', 'mins', 'minutes']:
      self.ax.set_xlim([max(datetime_upper - relativedelta(minutes=self.num_points * self.time_delta[0]), default_datetime),
                        datetime_upper])
    elif self.time_delta[1] in ['h', 'hour', 'hours']:
      self.ax.set_xlim([max(datetime_upper - relativedelta(hours=self.num_points * self.time_delta[0]), default_datetime),
                        datetime_upper])


  def set_xticks(self, x):
    self.ax.set_xticks(x)

  def get_xticklabels(self):
    return self.ax.get_xticklabels()

class Legend_SubPlot(SubPlot):
  def __init__(self, dimensions, fig):
    SubPlot.__init__(self, dimensions, 'legend')
    self.fig = fig
    self.ax = self.fig.add_subplot(self.dimensions)
    self.ax.axis('off')

  '''
      Legend requires (the markers with the marker labels) or (a list of handles) to plot
  '''
  def plot(self, loc='center', mode='expand', markers=None, marker_labels=None, handles=None, handle_ncol=3):
    if markers is not None and marker_labels is not None:
      self.ax.legend(markers, marker_labels, loc=loc, mode=mode)
    elif handles is not None:
      self.ax.legend(handles=handles, loc='center', mode='expand', ncol=handle_ncol)