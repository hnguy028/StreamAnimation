from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

def draw(pydata, plot_type='table'):
  if plot_type == 'table':
    # todo : make window + figure sizing dynamic
    fig = plt.figure(figsize=(8, 8))
    fig.subplots_adjust(left=0.7, top=1, bottom=0, right=.95, wspace=0)

    # init empty
    data_list = np.zeros(len(onc_stream_def.rows))

    # table
    ax = plt.subplot2grid((1, 1), (0, 0), colspan=2, rowspan=2)
    ax.table(cellText=data_list,
             rowLabels=onc_stream_def.rows,
             loc="center")

    ax.axis("off")

    animation = FuncAnimation(fig, update, interval=2000, fargs=pydata)
    plt.show()


class onc_stream_def:
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

  def update(self, pydata):
    data_list = np.zeros(len(self.rows))
    #data_list = np.random.randint(10,90, size=(len(rows), 1))
    #scatter_x = (1, 2, 3)
    #scatter_y = (1224.53, 1231.76, 1228.70)

def update(frame_number):
  data_list = np.random.randint(10, 90, size=(len(rows), 1))
  ax.table(cellText=data_list,
           rowLabels=rows,
           loc="center")
