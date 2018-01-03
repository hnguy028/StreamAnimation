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
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd
from dateutil.relativedelta import *

import mjd2utc
import constants as constants
import config

'''

'''


class TimeSeriesGraph():
  def __init__(self, data_stream,
               ax1_attributes=['dN', 'dE', 'dh'], ax1_color=['blue', 'green', 'brown'],
               ax2_attributes=['sN', 'sE', 'sh'], ax2_color=['red', 'orange', 'black'],
               time_attribute='MJD_sys',
               _points_per_frame=15, _frame_size=(15, 10), _step_size=(1, 's'),
               _steam_datetime_format='%d %b %Y %H:%M:%S', _output_datetime_format='%Y-%m-%d %H:%M:%S',
               y_lim=(-0.07, 0.05), y_lim2=(0.00, 0.02)):

    # setup figure
    self.fig = plt.figure(figsize=_frame_size)

    # subplot orientation and config
    self.subplots = {}
    self._plot_config()

    self.stream_point_attributes = ['sta_name', 'MJD_sys', 'MJD_ini', 'MJD_obs', 'lat', 'lon', 'hgt', 'dN', 'dE', 'dh', 'sN', 'sE', 'sh',
                  'cNE', 'cNh', 'cEh', 'sig0', 'pdop', 'cor_age', 'dt_ms', 'pmin', 'pmax',
                  'ar_dt_ms', 'nmsg_obs', 'nmsg_eph', 'nmsg_cor', 'nmsg_ion', 'nsat_trk',
                  'nsat_eph', 'nsat_cor', 'nsat_ion', 'nsat_use', 'nrej_trk', 'nrej_eph',
                  'nrej_cor', 'nrej_ion', 'nrej_elv', 'namb_jmp', 'nrng_rej', 'nphs_rej',
                  'status', 'ffix_amb', 'pfix_amb', 'prov_id', 'soln_id', 'msgc_id']

    self.data_stream = data_stream
    self.time_attribute = time_attribute
    self.viewing_frame = _points_per_frame

    # default datetime and formats
    self.datetime_format = _output_datetime_format
    self.stream_datetime_format = _steam_datetime_format

    self.default_datetime = dt.datetime.strptime('2016-01-01 00:00:00', self.datetime_format)
    self.current_datetime = dt.datetime.strptime('2016-01-01 00:00:00', self.datetime_format)

    self.frame_date = dt.datetime.strptime(str(self.default_datetime), self.datetime_format)

    self.x_axis_frequency = str(_step_size[0]) + _step_size[1]
    self.frame_step = _step_size[0]
    self.frame_step_measure = _step_size[1]

    # init viewing frame limits

    # set axis limit
    self.ax.set_ylim([y_lim[0], y_lim[1]])
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
    self.ax.xaxis.set_major_formatter(mdates.DateFormatter(self.datetime_format))
    self.ax2.xaxis.set_major_formatter(mdates.DateFormatter(self.datetime_format))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(self.datetime_format))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    # plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter(_datetime_format))
    # plt.gca().xaxis.set_minor_locator(mdates.SecondLocator())

    # set label rotation and output format to datetimes
    plt.gcf().autofmt_xdate()

    times = self._get_date_axis(str(self.frame_date))

    self.graph, = self.ax.plot(times, range(len(times)), color=(0, 0, 1))
    self.graph2, = self.ax2.plot(times, range(len(times)), color=(0, 0, 1))

    self.ani = animation.FuncAnimation(self.fig, self._update, frames=self._generator, interval=200, blit=False)

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
          pass

        self._load_kwargs(kwargs, pydata)
      except Exception as e:
        print(e)

      frame_counter += 1

      # clean up points not within viewing frame
      # todo : handle case where axis may have different sizes -> error
      if len(kwargs[self.ax1_attr[0]]) > self.viewing_frame + 1:
        self._deque_kwargs(kwargs)

      # generate corresponding x axis data
      kwargs['datetime'] = self._get_date_axis(self.current_datetime)[-len(kwargs[self.ax1_attr[0]]):]
      
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

  # return a list of datetime objects from ending in the given datetime
  def _get_date_axis(self, _datetime, _periods=None, _freq=None):
    return self._timestamp2datetime(
      pd.date_range(end=_datetime, periods=self.viewing_frame + 1, freq=self.x_axis_frequency))

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
        return datetime + relativedelta(seconds=_seconds, minutes=_minutes, hours=_hours, days=_days, weeks=_weeks,
                                        _months=_months, years=_years)

  # update function called every iteration of the FuncAnimation implementation
  def _update(self, kwargs):
    n, x = kwargs['frame_number'], kwargs['datetime']

    # legend information
    marker_labels = []
    markers = []

    # set axis data and store marker definitions
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
      self.ax2.set_xlim([self.current_datetime - relativedelta(seconds=self.viewing_frame * self.frame_step), self.current_datetime])
    else:
      # initial case when there fewer points than self.viewing_frame
      self.ax.set_xlim([max(self.default_datetime,
                            self.current_datetime - dt.timedelta(seconds=self.frame_step * self.viewing_frame)),
                        self.current_datetime])

      self.ax2.set_xlim([max(self.default_datetime,
                            self.current_datetime - dt.timedelta(seconds=self.frame_step * self.viewing_frame)),
                        self.current_datetime])

    self.ax3.legend(markers, marker_labels, loc='center', mode='expand')

    self.ax4.legend(handles=kwargs['mrp'], loc='center', mode='expand', ncol=3)

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

    self.ax = self.fig.add_subplot(2, 2, 1)
    # self.ax_2 = self.ax.twinx()

    self.ax2 = self.fig.add_subplot(2, 2, 2)
    # self.ax2_2 = self.ax.twinx()

    self.subplots[constants.plot_type_1].append(self.ax)
    self.subplots[constants.plot_type_1].append(self.ax2)

    self.ax3 = self.fig.add_subplot(2, 2, 3)
    self.ax3.axis('off')

    self.subplots[constants.plot_type_2].append(self.ax3)

    self.ax4 = self.fig.add_subplot(2, 2, 4)
    self.ax4.axis('off')

    self.subplots[constants.plot_type_3].append(self.ax4)