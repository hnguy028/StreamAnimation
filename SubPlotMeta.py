class SubPlot:
  def __init__(self, dimensions, plot_type):
    self.dimensions = dimensions
    self.type = plot_type

  def update(self):
    raise NotImplementedError

  def plot(self):
    raise NotImplementedError
