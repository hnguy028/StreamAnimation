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
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd
from dateutil.relativedelta import *

import json

'''
  
'''
class TimeSeriesGraph():
  def __init__(self, data_stream,
               ax1_attributes=['dN', 'dE', 'dh'], ax1_color=['blue', 'green', 'yellow'],
               ax2_attributes=['sN', 'sE', 'sh'], ax2_color=['red', 'orange', 'black'],
               _window_size=15, _step_size=(1, 's'), _datetime_format='%Y-%m-%d %H:%M:%S',
               y_lim=(-0.07, 0.05), y_lim2=(0.00, 0.02)):

    # setup figure
    self.fig = plt.figure(figsize=(15, 15))

    # add subplot
    self.subplots = []

    self.ax = self.fig.add_subplot(2, 1, 2)
    self.ax2 = self.ax.twinx()
    self.ax3 = self.fig.add_subplot(2, 1, 1)

    self.subplots.append(self.ax)
    self.subplots.append(self.ax2)
    self.subplots.append(self.fig.add_subplot(3, 1, 1))

    self.data_stream = data_stream

    # viewing frame size
    self.viewing_frame = _window_size

    # default datetime and formats
    self.datetime_format = '%Y-%m-%d %H:%M:%S'
    self.stream_datetime_format = '%d %b %Y %H:%M:%S'

    self.default_datetime = dt.datetime.strptime('2016-01-01 00:00:00', self.datetime_format)
    self.current_datetime = dt.datetime.strptime('2016-01-01 00:00:00', self.datetime_format)

    self.frame_date = dt.datetime.strptime(str(self.default_datetime), self.datetime_format)

    self.x_axis_frequency = str(_step_size[0]) + _step_size[1]
    self.frame_step = _step_size[0]
    self.frame_step_measure = _step_size[1]

    # init viewing frame limits
    start = self.current_datetime - dt.timedelta(minutes=self.frame_step * self.viewing_frame)

    # set axis limit
    self.ax.set_xlim([start, self.current_datetime])
    self.ax.set_ylim([y_lim[0], y_lim[1]])

    self.ax2.set_xlim([start, self.current_datetime])
    self.ax2.set_ylim([y_lim2[0], y_lim2[1]])

    # todo : to be defined by user (note: limit number of total attributes)
    self.ax1_attr = ax1_attributes
    self.ax2_attr = ax2_attributes

    # if axix colors only has one value - set that color for all attributes on this axis
    if isinstance(ax1_color, list):
      if len(ax1_color) == 1:
        self.ax1_colors = dict(zip(self.ax1_attr, [ax1_color[0]] * len(self.ax1_attr)))
      elif len(ax1_color) == len(self.ax1_attr):
        self.ax1_colors = dict(zip(self.ax1_attr, ax1_color))
      else:
        self.usage()
    else:
      self.usage()

    if isinstance(ax2_color, list):
      if len(ax2_color) == 1:
        self.ax2_colors = dict(zip(self.ax2_attr, [ax2_color[0]] * len(self.ax2_attr)))
      elif len(ax2_color) == len(self.ax2_attr):
        self.ax2_colors = dict(zip(self.ax2_attr, ax2_color))
      else:
        self.usage()
    else:
      self.usage()

    # set specific x axis label formats
    self.ax.xaxis.set_major_formatter(mdates.DateFormatter(_datetime_format))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(_datetime_format))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    # plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter(_datetime_format))
    # plt.gca().xaxis.set_minor_locator(mdates.SecondLocator())

    # set label rotation and output format to datetimes
    plt.gcf().autofmt_xdate()

    times = self._get_date_axis(str(self.frame_date))

    self.graph, = self.ax.plot(times, range(len(times)), color=(0, 0, 1))

    self.ani = animation.FuncAnimation(self.fig, self._update, frames=self._generator, interval=400, blit=False)

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

    json_data = None

    while 1:

      # read from stream
      try:
        json_data = self.data_stream.next()
        pydata = rt_stream_onc(**json_data)

        self._load_kwargs(kwargs, pydata)
      except:
        pass

      frame_counter += 1

      # clean up points not within viewing frame
      # todo : handle case where axis may have different sizes -> error
      if len(kwargs[self.ax1_attr[0]]) > self.viewing_frame + 1:
        self._clean_kwargs(kwargs)

      # generate corresponding x axis data
      kwargs['datetime'] = self._get_date_axis(self.current_datetime)[-len(kwargs[self.ax1_attr[0]]):]

      # pass along current frame number
      kwargs['frame_number'] = frame_counter

      yield kwargs

  # helper method to init null arrays for axis data
  def _init_kwargs(self, kwargs):
    for attr in self.ax1_attr:
      kwargs[attr] = np.empty(0)

    for attr in self.ax2_attr:
      kwargs[attr] = np.empty(0)

  # helper method for cleaning up the viewing frame
  def _clean_kwargs(self, kwargs):
    for attr in self.ax1_attr:
      kwargs[attr] = np.delete(kwargs[attr], 0)

    for attr in self.ax2_attr:
      kwargs[attr] = np.delete(kwargs[attr], 0)

  # helper method for generator : given a list of attributes, the function loads the values from the object into the given dictionary
  def _load_kwargs(self, kwargs, obj):
    for attr in self.ax1_attr:
      kwargs[attr] = np.append(kwargs[attr], getattr(obj, attr))

    for attr in self.ax2_attr:
      kwargs[attr] = np.append(kwargs[attr], getattr(obj, attr))

    # extract respective datetime of the obj
    self.current_datetime = dt.datetime.strptime(getattr(obj, 'MJD_utc_sys'), self.stream_datetime_format)

  # return a list of datetime objects from ending in the given datetime
  def _get_date_axis(self, _datetime, _periods=None, _freq=None):
    return self._timestamp2datetime(pd.date_range(end=_datetime, periods=self.viewing_frame + 1, freq=self.x_axis_frequency))

  # converts list of timestamp() objects to datetime() objects
  def _timestamp2datetime(self, timestamp_list):
    return [dt.datetime.strptime(str(timestamp), self.datetime_format) for timestamp in timestamp_list]

  # increment datetime objects by specified times
  def _increment_datetime(self, datetime, auto=False, _seconds=0, _minutes=0, _hours=0, _days=0, _weeks=0, _months=0, _years=0):
    # to be handled by the TimeSeriesGraph class variables
    if auto:
      return datetime + relativedelta(seconds=self.frame_step)
    else:
    # increment as specified in the function call
      if _months == 0 and _years == 0:
        # self.frame_date = datetime + dt.timedelta(seconds=_seconds, minutes=_minutes, hours=_hours)
        return datetime + dt.timedelta(seconds=_seconds, minutes=_minutes, hours=_hours)
      else:
        # self.frame_date = datetime + relativedelta(seconds=_seconds, minutes=_minutes, hours=_hours, days=_days, weeks=_weeks, _months=_months, years=_years)
        return datetime + relativedelta(seconds=_seconds, minutes=_minutes, hours=_hours, days=_days, weeks=_weeks, _months=_months, years=_years)

  # update function called every iteration of the FuncAnimation implementation
  def _update(self, kwargs):
    n, x = kwargs['frame_number'], kwargs['datetime']

    # legend information
    marker_labels = []
    markers = []

    # set axis data
    # line graph
    for v in self.ax1_attr:
      symb, = self.ax.plot(x, kwargs[v], self.ax1_colors[v], label=v)

      markers.append(symb)
      marker_labels.append(v + " - " + str(kwargs[v][-1:]))

    for v in self.ax2_attr:
      symb, = self.ax2.plot(x, kwargs[v], self.ax2_colors[v], label=v)

      markers.append(symb)
      marker_labels.append(v + " - " + str(kwargs[v][-1:]))

    # scatter plot
    # self.ax.plot_date(x,y)

    if n > self.viewing_frame:
      # usual case when we continuously plot new points
      self.ax.set_xlim([self.current_datetime - relativedelta(seconds=self.viewing_frame * self.frame_step), self.current_datetime])
    else:
      # initial case when there fewer points than self.viewing_frame
      self.ax.set_xlim([max(self.default_datetime,
                            self.current_datetime - dt.timedelta(seconds=self.frame_step * self.viewing_frame)),
                        self.current_datetime])

    self.ax.legend(markers, marker_labels, ncol=2, bbox_to_anchor=(0., 1., 1., .102), loc=3, mode='expand', borderaxespad=0.)
    # todo : make padding more dynamic (and possible to add subplots)
    #plt.tight_layout(rect=[0, 0, 1, 0.9])

    self.ax.set_xticks(x)
    #plt.setp(self.ax.get_xticklabels(), visible=True, rotation=70)

    return self.graph

################################ Debugging ################################

# Classes used to mimic a live data stream

class rt_stream_onc:
  def __init__(self, **entries):
    self.__dict__.update(entries)

class stream:
 def __init__(self, filename="pydata.txt"):
   self.filename = filename

 def read(self):
   while 1:
     with open(self.filename, 'r') as f:
       for line in f:
         yield json.loads(line)

################################ --------- ################################
if __name__ == '__main__':
  ani = TimeSeriesGraph(stream().read())
