class SubPlot:
  def __init__(self, dimensions, plot_type):
    self.dimensions = dimensions
    self.type = plot_type

  def plot(self):
    raise NotImplementedError
