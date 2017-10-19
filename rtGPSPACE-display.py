#!/usr/bin/env python

import socket
import select
#import binascii
import rtGPSPACEPPPStream
import mjd2utc

def main():
    MCAST_GRP = '224.2.10.100'
    MCAST_PORT = 30000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except AttributeError:
        print("AtrEr")
#  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
#  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

    sock.connect((MCAST_GRP, MCAST_PORT))
    #host = socket.gethostbyname(socket.gethostname())
    host = socket.gethostbyname("198.103.205.130")
    # sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
    # sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

    socket.setdefaulttimeout(5)

    while 1:
        print("Looping")
        try:
            # cdata, addr = sock.recvfrom(1024)
            cdata = sock.recvfrom(1024)
            print(cdata)

        except socket.error:
            print('Expection')
            # hexdata = binascii.hexlify(cdata)
            # print 'Data = %s' % hexdata

        pydata = rtGPSPACEPPPStream.rt_stream_onc.from_buffer_copy(cdata)
        print('\033c')
        print('                                               Station 4-char ID: %s' % pydata.sta_name)
        print('                                      Current Epoch (system) MJD: %24.15f UTC: %s' % (pydata.MJD_sys, mjd2utc.MJD2UTC(pydata.MJD_sys)))
        print('                   Initial Solution Epoch (observation time) MJD: %24.15f UTC: %s' % (pydata.MJD_ini, mjd2utc.MJD2UTC(pydata.MJD_ini)))
        print('                Current Observation Epoch (observation time) MJD: %24.15f UTC: %s' % (pydata.MJD_obs, mjd2utc.MJD2UTC(pydata.MJD_obs)))
        print('                                 A-priori station latitude [deg]: %24.15f' % pydata.lat)
        print('                                A-priori station longitude [deg]: %24.15f' % pydata.lon)
        print('                                     A-priori station height [m]: %24.15f' % pydata.hgt)
        print('             Estimated north offset wrt a priori coordinates [m]: %24.15f' % pydata.dN)
        print('              Estimated east offset wrt a priori coordinates [m]: %24.15f' % pydata.dE)
        print('            Estimated height offset wrt a priori coordinates [m]: %24.15f' % pydata.dh)
        print('                                    Standard deviation of dN [m]: %24.15f' % pydata.sN)
        print('                                    Standard deviation of dE [m]: %24.15f' % pydata.sE)
        print('                                    Standard deviation of dh [m]: %24.15f' % pydata.sh)
        print('                                         Covariance of dN and dE: %24.15f' % pydata.cNE)
        print('                                         Covariance of dN and dh: %24.15f' % pydata.cNh)
        print('                                         Covariance of dE and dh: %24.15f' % pydata.cEh)
        print('                   A-posteriori Least-Squares standard deviation: %24.15f' % pydata.sig0)
        print('                 Position Dilution-of-Precistion (geometry only): %24.15f' % pydata.pdop)
        print('                                            Correction Age (sec): %24.15f' % pydata.cor_age)
        print('                                   Total Computation time (msec): %24.15f' % pydata.dt_ms)
        print('                                      Minimum Fixing probability: %24.15f' % pydata.pmin)
        print('                                      Maximum Fixing probability: %24.15f' % pydata.pmax)
        print('                                      AR Computation Time (msec): %24.15f' % pydata.ar_dt_ms)
        print('                             Number of observation messages read: %8d' % pydata.nmsg_obs)
        print('                               Number of ephemeris messages read: %8d' % pydata.nmsg_eph)
        print('                              Number of correction messages read: %8d' % pydata.nmsg_cor)
        print('                              Number of ionosphere messages read: %8d' % pydata.nmsg_ion)
        print('                                    Number of satellites tracked: %8d' % pydata.nsat_trk)
        print('             Number of satellites tracked with healthy ephemeris: %8d' % pydata.nsat_eph)
        print('            Number of satellites tracked with global corrections: %8d' % pydata.nsat_cor)
        print('Number of satellites tracked with local (ionosphere) corrections: %8d' % pydata.nsat_ion)
        print('                                       Number of satellites used: %8d' % pydata.nsat_use)
        print('                 Number of satellites rejected with bad tracking: %8d' % pydata.nrej_trk)
        print('                Number of satellites rejected with bad ephemeris: %8d' % pydata.nrej_eph)
        print('       Number of satellites rejected with bad global corrections: %8d' % pydata.nrej_cor)
        print('        Number of satellites rejected with bad local corrections: %8d' % pydata.nrej_ion)
        print('              Number of satellites rejected below elevation mask: %8d' % pydata.nrej_elv)
        print('               Number of carrier-phase jumps (ambiguities reset): %8d' % pydata.namb_jmp)
        print('                                Number of pseudo-ranges rejected: %8d' % pydata.nrng_rej)
        print('                               Number of carrier-phases rejected: %8d' % pydata.nphs_rej)
        print('           Change on carrier-phase status (rise/set/reset/fixed): %8d' % pydata.status)
        print('                 Number of satellites fully-fixed (i.e. nl-only): %8d' % pydata.ffix_amb)
        print('                  Number of satellites part-fixed (i.e. wl-only): %8d' % pydata.pfix_amb)
        print('                                            Solution Provider ID: %8d' % pydata.prov_id)
        print('                                                     Solution ID: %8d' % pydata.soln_id)
        print('                                        Message Configuration ID: %8d' % pydata.msgc_id)



if __name__ == '__main__':
  main()
