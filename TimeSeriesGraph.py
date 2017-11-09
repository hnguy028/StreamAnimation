#!/usr/bin/env python
'''
    TimeSeriesGraph.py : Creates an graphical interface for data streams

    2017Nov09 : Generates line graph panning along with randomly generated data (date vs. rgn point data)
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
  def __init__(self, data_stream, _window_size=25, _step_size=(1, 's'), _datetime_format='%Y-%m-%d %H:%M:%S'):
    # setup figure
    self.fig = plt.figure()

    # add subplot
    self.ax = self.fig.add_subplot(1, 1, 1)
    self.ax2 = self.ax.twinx()

    self.data_stream = data_stream

    # viewing frame size
    self.viewing_frame = _window_size

    # default datetime and formats
    self.datetime_format = '%Y-%m-%d %H:%M:%S'

    self.default_datetime = dt.datetime.strptime('2016-01-01 00:00:00', self.datetime_format)
    self.current_datetime = dt.datetime.strptime('2016-01-01 00:00:00', self.datetime_format)

    self.frame_date = dt.datetime.strptime(str(self.default_datetime), self.datetime_format)

    self.x_axis_frequency = str(_step_size[0]) + _step_size[1]
    self.frame_step = _step_size[0]
    self.frame_step_measure = _step_size[1]

    # init viewing frame limits
    start = self.current_datetime - dt.timedelta(minutes=self.frame_step*self.viewing_frame)

    self.ax.set_xlim([start, self.current_datetime])
    self.ax.set_ylim([0, 1])

    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(_datetime_format))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()

    times = self._get_date_axis(str(self.frame_date))

    self.graph, = self.ax.plot(times, range(len(times)), color=(0, 0, 1))

    self.ani = animation.FuncAnimation(self.fig, self._update, frames=self._generator(), interval=400, blit=False)

    plt.show()

  def usage(self):
    pass

  def _generator(self):
    # init
    kwargs = {}
    kwargs["points"] = np.empty(0)

    # init generator counter
    frame_counter = 0
    json_data = None
    while 1:
      try:
        json_data = self.data_stream.next()
        pydata = rt_stream_onc(**json_data)
        print(pydata.sta_name)
      except:
        pass

      # increment the x-axis frame
      frame_counter += 1
      self.current_datetime = self._increment_datetime(self.current_datetime, auto=True)

      # generate y axis data
      kwargs["points"] = np.append(kwargs["points"], np.random.rand(1))

      # clean up points not within viewing frame
      if len(kwargs["points"]) > self.viewing_frame + 1:
        kwargs["points"] = np.delete(kwargs["points"], 0)

      # generate corresponding x axis data
      kwargs['datetime'] = self._get_date_axis(self.current_datetime)[-len(kwargs["points"]):]

      # pass along current frame number
      kwargs['frame_number'] = frame_counter

      yield kwargs

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
    n, x, y = kwargs['frame_number'], kwargs['datetime'], kwargs["points"]

    # set axis data
    # line graph
    self.ax.plot(x, y)

    # self.ax.plot(x, y2, 'r+')

    # scatter plot
    # self.ax.plot_date(x,y)

    # set x axis label for each point
    self.ax.set_xticks(x)

    if n > self.viewing_frame:
      # usual case when we continuously plot new points
      self.ax.set_xlim([self.current_datetime - relativedelta(seconds=self.viewing_frame * self.frame_step), self.current_datetime])
    else:
      # initial case when there fewer points than self.viewing_frame
      self.ax.set_xlim([max(self.default_datetime,
                            self.current_datetime - dt.timedelta(seconds=self.frame_step*self.viewing_frame)),
                        self.current_datetime])

    return self.graph

################################ Debugging ################################

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
  data_stream = stream()
  ani = TimeSeriesGraph(data_stream.read())