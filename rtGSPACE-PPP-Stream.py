#!/usr/bin/env python

__author__ = "Hieu Nguyen"
__copyright__ = "Copyright 2017, Hieu Nguyen"
__version__ = "1.0"

class rt_stream_pgc:
    def __init__(self):
        MJD = None          # Modified Julian Date
        sta_name = None     # Station 4-char ID
        X0 = None           # A priori X coordinate [m]
        dX = None           # Estimated correction to X0 [m]
        sX = None           # Standard deviation of dX [m]
        Y0 = None           # A priori Y coordinate [m]
        dY = None           # Estimated correction to Y0 [m]
        sY = None           # Standard deviation of dY [m]
        Z0 = None           # A priori Z coordinate [m]
        dZ = None           # Estimated correction to Z0 [m]
        sZ = None           # Standard deviation of dZ [m]
        dN = None           # North offset wrt a priori coordinates [m]
        sN = None           # Standard deviation of dN [m]
        dE = None           # East offset wrt a priori coordinates [m]
        sE = None           # Standard deviation of dE [m]
        dh = None           # Ellipsoidal height offset wrt a priori coordinates [m]
        sh = None           # Standard deviation of dh [m]
        cNE = None          # Covariance of dN and dE
        cNh = None          # Covariance of dN and dh
        cEh = None          # Covariance of dE and dh
        lat = None          # Estimated station latitude [deg]
        lon = None          # Estimated station longitude [deg]
        h = None            # Estimated station height [m]
        nbsat = None        # Number of satellites in solution
        spare = None        # explicit byte padding
        MJD_out = None      # Time of output (as opposed to time of epoch)
        # 200 bytes

class rt_stream_onc:
    def __init__(self):
        self.sta_name = None    # 0: Station 4-char ID
        self.MJD_sys = None     # 0: Current Epoch (system) MJD
        self.MJD_ini = None     # 0: Initial Solution Epoch (observation time) MJD
        self.MJD_obs = None     # 0: Current Observation Epoch (observation time) MJD
        self.lat = None         # 2: A-priori station latitude [deg]
        self.lon = None         # 2: A-priori station longitude [deg]
        self.hgt = None         # 2: A-priori station height [m]

        self.dN = None          # 2: Estimated north offset wrt a priori coordinates [m]
        self.dE = None          # 2: Estimated east offset wrt a priori coordinates [m]
        self.dh = None          # 2: Estimated height offset wrt a priori coordinates [m]
        self.sN = None          # 2: Standard deviation of dN [m]
        self.sE = None          # 2: Standard deviation of dE [m]
        self.sh = None          # 2: Standard deviation of dh [m]
        self.cNE = None         # 2: Covariance of dN and dE
        self.cNh = None         # 2: Covariance of dN and dh
        self.cEh = None         # 2: Covariance of dE and dh
        self.sig0 = None        # 2: A-posteriori Least-Squares standard deviation
        self.pdop = None        # 2: Position Dilution-of-Precistion (geometry only)
        self.cor_age = None     # 2: Correction Age (sec)
        self.dt_ms = None       # 2: Total Computation time (msec)
        self.pmin = None        # 3: Minimum Fixing probability
        self.pmax = None        # 3: Maximum Fixing probability
        self.ar_dt_ms = None    # 3: AR Computation Time (msec)

        self.nmsg_obs = None    # 0: Number of observation messages read
        self.nmsg_eph = None    # 0: Number of ephemeris messages read
        self.nmsg_cor = None    # 0: Number of correction messages read
        self.nmsg_ion = None    # 0: Number of ionosphere messages read
        self.nsat_trk = None    # 1: Number of satellites tracked
        self.nsat_eph = None    # 1: Number of satellites tracked with healthy ephemeris
        self.nsat_cor = None    # 1: Number of satellites tracked with global corrections
        self.nsat_ion = None    # 1: Number of satellites tracked with local (ionosphere) corrections
        self.nsat_use = None    # 1: Number of satellites used
        self.nrej_trk = None    # 1: Number of satellites rejected with bad tracking
        self.nrej_eph = None    # 1: Number of satellites rejected with bad ephemeris
        self.nrej_cor = None    # 1: Number of satellites rejected with bad global corrections
        self.nrej_ion = None    # 1: Number of satellites rejected with bad local corrections
        self.nrej_elv = None    # 1: Number of satellites rejected below elevation mask
        self.namb_jmp = None    # 1: Number of carrier-phase jumps (ambiguities reset)
        self.nrng_rej = None    # 1: Number of pseudo-ranges rejected
        self.nphs_rej = None    # 1: Number of carrier-phases rejected
        self.status = None      # 2: change on carrier-phase status (rise/set/reset/fixed)
        self.ffix_amb = None    # 3: Number of satellites fully-fixed (i.e. nl-only)
        self.pfix_amb = None    # 3: Number of satellites part-fixed (i.e. wl-only)
        self.prov_id = None     # 0: Solution Provider ID
        self.soln_id = None     # 0: Solution ID
        self.msgc_id = None     # 0: Message Configuration ID
        # 144 bytes