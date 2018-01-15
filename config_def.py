class PanningGraph_Config:
  def __init__(self, dimensions, left_axis_attributes, left_axis_markers, left_axis_ylim,
               right_axis_attributes, right_axis_markers, right_axis_ylim,
               time_attribute, num_xaxis_points=15, time_delta=(1, 's'), xaxis_datetime_format='%Y-%m-%d %H:%M:%S'):

    self.dimensions = dimensions
    self.left_axis_attributes = left_axis_attributes
    self.left_axis_markers = left_axis_markers
    self.left_axis_ylim = left_axis_ylim
    self.right_axis_attributes = right_axis_attributes
    self.right_axis_markers = right_axis_markers
    self.right_axis_ylim = right_axis_ylim
    self.time_attribute = time_attribute
    self.num_xaxis_points = num_xaxis_points
    self.time_delta = time_delta
    self.xaxis_datetime_format = xaxis_datetime_format
