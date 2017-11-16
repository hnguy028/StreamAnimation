import json
import datetime as dt

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

stream = stream().read()
old_data = None
new_data = None

stream_datetime_format = '%d %b %Y %H:%M:%S'

line_num = 0

while 1:
  try:
    json_data = stream.next()
    old_data = new_data
    new_data = rt_stream_onc(**json_data)

    time1 = dt.datetime.strptime(old_data.MJD_utc_sys, stream_datetime_format)
    time2 = dt.datetime.strptime(new_data.MJD_utc_sys, stream_datetime_format)

    deltaT = (time2 - time1).seconds

    if deltaT == 0:
      print(line_num, ": ", time2, " --- ", time1)
  except:
    pass

  line_num += 1
