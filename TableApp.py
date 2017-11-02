import Tkinter as tk
import argparse
import json
import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class App(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self)
    table = Table(self, 46, 2, **kwargs)
    table.pack(side="top", fill=None)
    table.update_table()

    # create a second window
    # second_window = tk.Toplevel(self)
    # table2 = Table(second_window, 46, 2, **kwargs)

class Table(tk.Frame):
  def __init__(self, parent, rows=10, columns=2, **kwargs):
    # use black background so it "peeks through" to
    # form grid lines
    tk.Frame.__init__(self, parent, background="black")
    self._widgets = []

    self.row_size = rows
    self.column_size = columns
    row_headers = kwargs["row_headers"]
    self.generator = kwargs["generator"]
    self.update_time = 1000 # ms

    # init table
    for row in range(rows):
      current_row = []
      for column in range(columns):

        if column == 0:
          label = tk.Label(self, text=row_headers[row],
                           borderwidth=0, width=60,
                           anchor="e", font=("Helvetica", 8))
        else:
          label = tk.Label(self, text="%s/%s" % (row, column),
                           borderwidth=0, width=20,
                           anchor="w", font=("Helvetica", 8))

        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
        current_row.append(label)

      self._widgets.append(current_row)

    for column in range(columns):
      self.grid_columnconfigure(column, weight=1)

  def update_cell(self, row, column, value):
    cell = self._widgets[row][column]
    cell.configure(text=value)

  def update_table(self):
    pydata = self.generator.next()

    self.update_cell(0, 1, str(pydata.sta_name))
    self.update_cell(1, 1, str(pydata.MJD_sys))
    self.update_cell(2, 1, str(pydata.MJD_ini))
    self.update_cell(3, 1, str(pydata.MJD_obs))
    self.update_cell(4, 1, str(pydata.lat))
    self.update_cell(5, 1, str(pydata.lon))
    self.update_cell(6, 1, str(pydata.hgt))
    self.update_cell(7, 1, str(pydata.dN))
    self.update_cell(8, 1, str(pydata.dE))
    self.update_cell(9, 1, str(pydata.dh))
    self.update_cell(10, 1, str(pydata.sN))
    self.update_cell(11, 1, str(pydata.sE))
    self.update_cell(12, 1, str(pydata.sh))
    self.update_cell(13, 1, str(pydata.cNE))
    self.update_cell(14, 1, str(pydata.cNh))
    self.update_cell(15, 1, str(pydata.cEh))
    self.update_cell(16, 1, str(pydata.sig0))
    self.update_cell(17, 1, str(pydata.pdop))
    self.update_cell(18, 1, str(pydata.cor_age))
    self.update_cell(19, 1, str(pydata.dt_ms))
    self.update_cell(20, 1, str(pydata.pmin))
    self.update_cell(21, 1, str(pydata.pmax))
    self.update_cell(22, 1, str(pydata.ar_dt_ms))
    self.update_cell(23, 1, str(pydata.nmsg_obs))
    self.update_cell(24, 1, str(pydata.nmsg_eph))
    self.update_cell(25, 1, str(pydata.nmsg_cor))
    self.update_cell(26, 1, str(pydata.nmsg_ion))
    self.update_cell(27, 1, str(pydata.nsat_trk))
    self.update_cell(28, 1, str(pydata.nsat_eph))
    self.update_cell(29, 1, str(pydata.nsat_cor))
    self.update_cell(30, 1, str(pydata.nsat_ion))
    self.update_cell(31, 1, str(pydata.nsat_use))
    self.update_cell(32, 1, str(pydata.nrej_trk))
    self.update_cell(33, 1, str(pydata.nrej_eph))
    self.update_cell(34, 1, str(pydata.nrej_cor))
    self.update_cell(35, 1, str(pydata.nrej_ion))
    self.update_cell(36, 1, str(pydata.nrej_elv))
    self.update_cell(37, 1, str(pydata.namb_jmp))
    self.update_cell(38, 1, str(pydata.nrng_rej))
    self.update_cell(39, 1, str(pydata.nphs_rej))
    self.update_cell(40, 1, str(pydata.status))
    self.update_cell(41, 1, str(pydata.ffix_amb))
    self.update_cell(42, 1, str(pydata.pfix_amb))
    self.update_cell(43, 1, str(pydata.prov_id))
    self.update_cell(44, 1, str(pydata.soln_id))
    self.update_cell(45, 1, str(pydata.msgc_id))

    # update every second
    self.after(self.update_time, self.update_table)

class rt_stream_onc:
  def __init__(self, **entries):
    self.__dict__.update(entries)

class stream:
  def __init__(self, filename):
    self.filename = filename

  def read(self):
    while 1:
      with open(self.filename, 'r') as f:
        for line in f:
          # convert json data into stream object
          # pydata = rtGPSPACEPPPStream.rt_stream_pgc.from_buffer_copy(line)
          json_dict = json.loads(line)
          pydata = rt_stream_onc(**json_dict)
          time.sleep(1)
          yield pydata

if __name__== "__main__":
  parser = argparse.ArgumentParser(description='Prg Description')
  parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
  parser.add_argument('-f', '--filename', type=str, nargs=1,
                      action='store', default="pydata.txt",
                      help='pseudo stream filename')

  args = parser.parse_args()

  rows = ['                                               Station 4-char ID',
          '                                      Current Epoch (system) MJD',
          '                   Initial Solution Epoch (observation time) MJD',
          '                Current Observation Epoch (observation time) MJD',
          '                                 A-priori station latitude [deg]',
          '                                A-priori station longitude [deg]',
          '                                     A-priori station height [m]',
          '             Estimated north offset wrt a priori coordinates [m]',
          '              Estimated east offset wrt a priori coordinates [m]',
          '            Estimated height offset wrt a priori coordinates [m]',
          '                                    Standard deviation of dN [m]',
          '                                    Standard deviation of dE [m]',
          '                                    Standard deviation of dh [m]',
          '                                         Covariance of dN and dE',
          '                                         Covariance of dN and dh',
          '                                         Covariance of dE and dh',
          '                   A-posteriori Least-Squares standard deviation',
          '                 Position Dilution-of-Precistion (geometry only)',
          '                                            Correction Age (sec)',
          '                                   Total Computation time (msec)',
          '                                      Minimum Fixing probability',
          '                                      Maximum Fixing probability',
          '                                      AR Computation Time (msec)',
          '                             Number of observation messages read',
          '                               Number of ephemeris messages read',
          '                              Number of correction messages read',
          '                              Number of ionosphere messages read',
          '                                    Number of satellites tracked',
          '             Number of satellites tracked with healthy ephemeris',
          '            Number of satellites tracked with global corrections',
          'Number of satellites tracked with local (ionosphere) corrections',
          '                                       Number of satellites used',
          '                 Number of satellites rejected with bad tracking',
          '                Number of satellites rejected with bad ephemeris',
          '       Number of satellites rejected with bad global corrections',
          '        Number of satellites rejected with bad local corrections',
          '              Number of satellites rejected below elevation mask',
          '               Number of carrier-phase jumps (ambiguities reset)',
          '                                Number of pseudo-ranges rejected',
          '                               Number of carrier-phases rejected',
          '           Change on carrier-phase status (rise/set/reset/fixed)',
          '                 Number of satellites fully-fixed (i.e. nl-only)',
          '                  Number of satellites part-fixed (i.e. wl-only)',
          '                                            Solution Provider ID',
          '                                                     Solution ID',
          '                                        Message Configuration ID']

  data_stream = stream(args.filename)

  generator = data_stream.read()

  fig = plt.Figure()

  x = np.arange(0, 2 * np.pi, 0.01)  # x-array


  def animate(i):
    line.set_ydata(np.sin(x + i / 10.0))  # update the data
    return line,

  root = tk.Tk()

  label = tk.Label(root, text="SHM Simulation").grid(column=0, row=0)

  canvas = FigureCanvasTkAgg(fig, master=root)
  canvas.get_tk_widget().grid(column=0, row=1)

  ax = fig.add_subplot(111)
  line, = ax.plot(x, np.sin(x))
  ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=False)

  app = App(row_headers=rows, generator=generator)
  app.mainloop()