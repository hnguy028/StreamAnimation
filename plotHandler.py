#!/usr/bin/env python

class Table:
  def __init__(self, _dimensions=(1,1)):
    self.dimensions = _dimensions
    self.table = None

  def update(self, pydata):
    if pydata != None:
      #
      data = self.format_pydata(pydata)

      # update information to table

  def format_pydata(self, pydata):
    # re format pydata to be used with matplotlib table creation
    data = pydata
    return data