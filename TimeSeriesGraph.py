# import matplotlib.pylab as plb
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np
import pandas as pd
from dateutil.relativedelta import *
# import time

class TimeSeriesGraph():
  def __init__(self):
    # setup figure
    self.fig = plt.figure()
    self.fig.autofmt_xdate()

    # add subplot
    self.ax = self.fig.add_subplot(1, 1, 1)

    # viewing frame size
    self.viewing_frame = 25

    # default datetime and formats
    self.datetime_format = '%Y-%m-%d %H:%M:%S'

    self.default_datetime = dt.datetime.strptime('2016-01-01 00:00:00', self.datetime_format)
    self.current_datetime = dt.datetime.strptime('2016-01-01 00:00:00', self.datetime_format)

    self.frame_date = dt.datetime.strptime(str(self.default_datetime), self.datetime_format)

    self.frame_step = 10
    self.frame_step_measure = 'min'
    self.x_axis_frequency = str(self.frame_step) + self.frame_step_measure

    # init viewing frame limits
    start = self.current_datetime - dt.timedelta(minutes=self.frame_step)
    self.ax.set_xlim([start, self.current_datetime])
    self.ax.set_ylim([0, 1])

    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(self.datetime_format))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    times = self._get_date_axis(str(self.frame_date))

    self.graph, = self.ax.plot(times, range(len(times)), color=(0, 0, 1))

    self.ani = animation.FuncAnimation(self.fig, self._update, frames=self._generator(), interval=400, blit=False)

    plt.gcf().autofmt_xdate()
    plt.show()

  def _generator(self):
    # init
    kwargs = {}
    kwargs["points"] = np.empty(0)

    frame_counter = 1

    while 1:
      # increment the x-axis
      frame_counter += 1
      self.current_datetime = self._increment_datetime(self.current_datetime, auto=True)

      kwargs['n'] = frame_counter

      kwargs['date'] = np.arange(max(0,frame_counter - self.viewing_frame), frame_counter)
      # kwargs['date'] = np.arange(max(self.default_datetime,self.current_datetime), num)
      kwargs['datetime'] = self._get_date_axis(self.current_datetime)
      # kwargs['date'] = np.random.rand(num)

      kwargs["points"] = np.append(kwargs["points"], np.random.rand(1))
      if len(kwargs["points"]) > self.viewing_frame:
        kwargs["points"] = np.delete(kwargs["points"], 0)
      yield kwargs

  def _get_date_axis(self, datetime):
    return self.timestamp2datetime(pd.date_range(end=datetime, periods=self.viewing_frame, freq=self.x_axis_frequency))

  def timestamp2datetime(self, timestamp_list):
    return [dt.datetime.strptime(str(timestamp), self.datetime_format) for timestamp in timestamp_list]

  def _increment_datetime(self, datetime, auto=False, _seconds=0, _minutes=0, _hours=0, _days=0, _weeks=0, _months=0, _years=0):
    # to be handled by class variables
    if auto:
      return datetime + relativedelta(minutes=self.frame_step)
    else:
      if _months == 0 and _years == 0:
        # self.frame_date = datetime + dt.timedelta(seconds=_seconds, minutes=_minutes, hours=_hours)
        return datetime + dt.timedelta(seconds=_seconds, minutes=_minutes, hours=_hours)
      else:
        # self.frame_date = datetime + relativedelta(seconds=_seconds, minutes=_minutes, hours=_hours, days=_days, weeks=_weeks, _months=_months, years=_years)
        return datetime + relativedelta(seconds=_seconds, minutes=_minutes, hours=_hours, days=_days, weeks=_weeks, _months=_months, years=_years)

  def _update(self, kwargs):
      n = kwargs['n']
      xx = kwargs['date']
      x = kwargs['datetime']
      y = kwargs["points"]

      self.graph.set_xdata(x)
      self.graph.set_ydata(y)

      self.ax.set_xticklabels(x)

      if n > self.viewing_frame:
        # usual case when we continuously plot new points
        # self.ax.set_xlim(n - self.viewing_frame, n)
        self.ax.set_xlim([self.current_datetime - relativedelta(minutes=self.viewing_frame * self.frame_step), self.current_datetime])
      else:
        # when there arent enough points (less than viewing frame)
        # self.ax.set_xlim(0, self.viewing_frame)
        self.ax.set_xlim([max(self.default_datetime,
                              self.current_datetime - dt.timedelta(minutes=self.frame_step*self.viewing_frame)),
                          self.current_datetime])
        # self.ax.set_xlim([self.default_datetime, self.default_datetime + relativedelta(minutes=self.viewing_frame * self.frame_step)])

      return self.graph

if __name__ == '__main__':
  ani = TimeSeriesGraph()