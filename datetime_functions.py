import datetime as dt
import pandas as pd
from dateutil.relativedelta import *

# return a list of datetime objects from ending in the given datetime
def _get_date_axis(_datetime, _datetime_format, _periods, _freq):
  return _timestamp2datetime(pd.date_range(end=_datetime, periods=_periods + 1, freq=_freq), _datetime_format)

# converts list of timestamp() objects to datetime() objects
def _timestamp2datetime(timestamp_list, datetime_format):
  return [dt.datetime.strptime(str(timestamp), datetime_format) for timestamp in timestamp_list]

  # increment datetime objects by specified times
def _increment_datetime(datetime, auto=False, _seconds=0, _minutes=0, _hours=0, _days=0, _weeks=0, _months=0, _years=0):
  # to be handled by the TimeSeriesGraph class variables
  if auto:
    return datetime + relativedelta(seconds=0)
  else:
    # increment as specified in the function call
    if _months == 0 and _years == 0:
      # self.frame_date = datetime + dt.timedelta(seconds=_seconds, minutes=_minutes, hours=_hours)
      return datetime + dt.timedelta(seconds=_seconds, minutes=_minutes, hours=_hours)
    else:
      # self.frame_date = datetime + relativedelta(seconds=_seconds, minutes=_minutes, hours=_hours, days=_days, weeks=_weeks, _months=_months, years=_years)
      return datetime + relativedelta(seconds=_seconds, minutes=_minutes, hours=_hours, days=_days, weeks=_weeks,_months=_months, years=_years)