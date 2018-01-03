import json
import GraphHandler as tms

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
         json_data = json.loads(line)
         pydata = rt_stream_onc(**json_data)
         yield pydata

################################ --------- ################################

if __name__ == '__main__':
  ani = tms.TimeSeriesGraph(stream().read())