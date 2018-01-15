#!/usr/bin/env python
'''
    TimeSeriesGraph.py : Creates an graphical interface for data streams

    2017Nov09 : Generates a live time series graph, running from a pseudo data stream
'''

__author__ = "Hieu Nguyen"
__created__ = "2017-11-02"
__version__ = "0.1"
__status__ = "Development"

import matplotlib.animation as animation
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np

import mjd2utc
import datetime_functions
import constants as constants
import config
import Sub_Plots

'''

'''
class GraphHandler():
  def __init__(self, data_stream):
    Graph_2x2_PPLL(data_stream, _frame_size=config.application_window)

'''
  [ Panning , Panning ]
  [ Legend  , Legend  ]
'''
class Graph_2x2_PPLL():
  def __init__(self, data_stream,
               time_attribute='MJD_sys',
               _points_per_frame=15, _frame_size=(15, 10), _tick_delta=(1, 's'),
               _stream_datetime_format=config.stream_datetime_format, _output_datetime_format=config.output_datetime_format):

    # setup figure
    self.fig = plt.figure(figsize=_frame_size)

    # subplot orientation and config
    self.subplots = {}

    self.stream_point_attributes = config.stream_point_attributes

    self.data_stream = data_stream
    self.time_attribute = time_attribute
    self.viewing_frame = _points_per_frame

    # default datetime and formats
    self.datetime_format = _output_datetime_format
    self.stream_datetime_format = _stream_datetime_format

    self.current_datetime = dt.datetime.strptime(constants.default_datetime, self.datetime_format)

    self.tick_delta = _tick_delta
    self.x_axis_frequency = str(_tick_delta[0]) + _tick_delta[1]

    self.ax1_attr = config.plot_01.left_axis_attributes
    self.ax2_attr = config.plot_02.left_axis_attributes

    self._plot_config()

    plt.gcf().autofmt_xdate()

    self.graph = self.ax.plot_init()
    self.ax2.plot_init()

    self.ani = animation.FuncAnimation(self.fig, self._update, frames=self._generator, interval=10, blit=False)

    plt.show()

  def usage(self, error_code=1, msg=None):
    print("Usage - Called")
    exit(0)

  def _generator(self):
    # init
    kwargs = {}
    self._init_kwargs(kwargs)

    # init generator counter
    frame_counter = 0

    while 1:

      # read from stream
      try:
        pydata = self.data_stream.next()

        # null check
        if pydata == None:
          frame_counter += 1
          continue

        self._load_kwargs(kwargs, pydata)
      except Exception as e:
        print(e)

      frame_counter += 1

      # todo : handle case where axis may have different sizes -> error, we are assuming all axis attributes are of the same length as ax1_attr[0]
      num_points_per_attr = len(kwargs[self.ax1_attr[0]])

      # clean up points not within viewing frame
      if  num_points_per_attr > self.viewing_frame + 1:
        self._deque_kwargs(kwargs)

      # generate corresponding x axis data
      kwargs['datetime'] = datetime_functions._get_date_axis(self.current_datetime, self.datetime_format, self.viewing_frame, self.x_axis_frequency)[-num_points_per_attr:]
      
      # pass along current frame number
      kwargs['frame_number'] = frame_counter

      yield kwargs

  # helper method to init null arrays for axis data
  def _init_kwargs(self, kwargs):
    for attr in self.ax1_attr + self.ax2_attr:
      kwargs[attr] = np.empty(0)

    kwargs['mrp'] = []

  # helper method for cleaning up the viewing frame
  def _deque_kwargs(self, kwargs):
    for attr in self.ax1_attr + self.ax2_attr:
      kwargs[attr] = np.delete(kwargs[attr], 0)

  # helper method for generator : given a list of attributes, the function loads the values from the object into the given dictionary
  def _load_kwargs(self, kwargs, obj):
    for attr in self.ax1_attr + self.ax2_attr:
      try:
        kwargs[attr] = np.append(kwargs[attr], getattr(obj, attr))
      except AttributeError as e:
        print(e)

    # extract respective datetime of the obj
    try:
      self.current_datetime = dt.datetime.strptime(mjd2utc.MJD2UTC(float(getattr(obj, self.time_attribute))), self.stream_datetime_format)
    except AttributeError as e:
      print(e)

    legend_entries = []
    for attrib in self.stream_point_attributes:
      try:
        _label = str(attrib) + "  :  " + str(getattr(obj, attrib))
        legend_entries.append(mpatches.Patch(color='white', label=_label))
      except AttributeError as e:
        # remove attrib from attributes to avoid error
        self.stream_point_attributes.remove(attrib)
        print e, ', attribute removed from future reads'

    kwargs['mrp'] = legend_entries

  # update function called every iteration of the FuncAnimation implementation
  def _update(self, kwargs):
    n, x = kwargs['frame_number'], kwargs['datetime']

    # legend information
    marker_labels = []

    symb = self.ax.plot(x, kwargs)
    markers = symb[0]
    for xx,yy in zip(symb[1], symb[2]):
      marker_labels.append(yy + " - " + xx)

    symb = self.ax2.plot(x, kwargs)
    markers += symb[0]
    for xx,yy in zip(symb[1], symb[2]):
      marker_labels.append(yy + " - " + xx)

    self.ax.set_xlim(self.current_datetime)
    self.ax2.set_xlim(self.current_datetime)

    self.ax3.plot(markers=markers, marker_labels=marker_labels)
    self.ax4.plot(handles=kwargs['mrp'])

    # todo : make padding more dynamic (and possible to add subplots).

    plt.tight_layout()

    self.ax.set_xticks(x)
    self.ax2.set_xticks(x)

    plt.setp(self.ax.get_xticklabels(), visible=True, rotation=80)
    plt.setp(self.ax2.get_xticklabels(), visible=True, rotation=80)

    plt.tight_layout()

    return self.graph

  # inits types of plot and orientation
  def _plot_config(self):
    for types in constants.plot_types:
      self.subplots[types] = []

    # Note : for the time_attribute we should use the one defined in the constructor for consistency
    self.ax = Sub_Plots.Panning_SubPlot(config.plot_01.dimensions, self.fig, self.time_attribute, config.plot_01.xaxis_datetime_format, self.tick_delta,
                                        laxis_attr=config.plot_01.left_axis_attributes,
                                        laxis_color=config.plot_01.left_axis_markers, laxis_lim=config.plot_01.left_axis_ylim,
                                        num_points=config.plot_01.num_xaxis_points)
    self.ax2 = Sub_Plots.Panning_SubPlot(config.plot_02.dimensions, self.fig, self.time_attribute, config.plot_02.xaxis_datetime_format, self.tick_delta,
                                        laxis_attr=config.plot_02.left_axis_attributes,
                                        laxis_color=config.plot_02.left_axis_markers, laxis_lim=config.plot_02.left_axis_ylim,
                                        num_points=config.plot_02.num_xaxis_points)

    self.subplots[constants.plot_type_1].append(self.ax)
    self.subplots[constants.plot_type_1].append(self.ax2)

    self.ax3 = Sub_Plots.Legend_SubPlot(223, self.fig)
    self.ax4 = Sub_Plots.Legend_SubPlot(224, self.fig)

    self.subplots[constants.plot_type_2].append(self.ax3)
    self.subplots[constants.plot_type_2].append(self.ax4)