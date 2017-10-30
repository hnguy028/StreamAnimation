from matplotlib.animation import FuncAnimation
import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import time
import random
import rtGPSPACEPPPStream, mjd2utc

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

def main(filename):
    data_stream = stream(filename)

    generator = data_stream.read()
    #for pydata in generator:
    #  draw(pydata, 'table')
    draw1(generator)

      # add a slight pause

#def draw(pydata):
#  pass

#def draw(pydata, plot_type='table'):
def draw1(generator, plot_type='table'):
  if plot_type == 'table':
    # todo : make window + figure sizing dynamic
    fig = plt.figure(figsize=(8, 8))
    fig.subplots_adjust(left=0.7, top=1, bottom=0, right=.95, wspace=0)

    # init empty
    data_list = np.asarray([' ' for  _ in range(len(onc_stream_def.rows))])
    #data_list = np.zeros((len(onc_stream_def.rows),1))

    # table
    ax = plt.subplot2grid((1, 1), (0, 0), colspan=0, rowspan=2)
    ax.table(cellText=data_list,
             colLabels=('null'),
             rowLabels=np.asarray(onc_stream_def.rows),
             loc="center")

    ax.axis("off")

    def update(pydata):
      data_list = np.asarray(['test' for _ in range(46)])
      data_list1 = np.asarray([str(pydata.sta_name),
                   str(pydata.MJD_sys),
                   str(pydata.MJD_ini),
                   str(pydata.MJD_obs),
                   str(pydata.lat),
                   str(pydata.lon),
                   str(pydata.hgt),
                   str(pydata.dN),
                   str(pydata.dE),
                   str(pydata.dh),
                   str(pydata.sN),
                   str(pydata.sE),
                   str(pydata.sh),
                   str(pydata.cNE),
                   str(pydata.cNh),
                   str(pydata.cEh),
                   str(pydata.sig0),
                   str(pydata.pdop),
                   str(pydata.cor_age),
                   str(pydata.dt_ms),
                   str(pydata.pmin),
                   str(pydata.pmax),
                   str(pydata.ar_dt_ms),
                   str(pydata.nmsg_obs),
                   str(pydata.nmsg_eph),
                   str(pydata.nmsg_cor),
                   str(pydata.nmsg_ion),
                   str(pydata.nsat_trk),
                   str(pydata.nsat_eph),
                   str(pydata.nsat_cor),
                   str(pydata.nsat_ion),
                   str(pydata.nsat_use),
                   str(pydata.nrej_trk),
                   str(pydata.nrej_eph),
                   str(pydata.nrej_cor),
                   str(pydata.nrej_ion),
                   str(pydata.nrej_elv),
                   str(pydata.namb_jmp),
                   str(pydata.nrng_rej),
                   str(pydata.nphs_rej),
                   str(pydata.status),
                   str(pydata.ffix_amb),
                   str(pydata.pfix_amb),
                   str(pydata.prov_id),
                   str(pydata.soln_id),
                   str(pydata.msgc_id)])

      ax.table(cellText=data_list,
               colLabels=("null"),
               rowLabels=np.asarray(onc_stream_def.rows),
               loc="center")

    ani = FuncAnimation(fig, update, generator)
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

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Prg Description')
  parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
  parser.add_argument('-f', '--filename', type=str, nargs=1,
                      action='store', default="pydata.txt",
                      help='pseudo stream filename')

  args = parser.parse_args()
  main(args.filename)