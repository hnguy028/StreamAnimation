#Copyright:
#
#  All contents Copyright (c)2017. Her Majesty the Queen in Right of Canada.
#  Natural Resources Canada, Canadian Geodetic Survey. All rights reserved.
#
#Warranty:
#
#  This digital application and associated files are provided on an "as is"
#  basis and Canada makes no guarantees, representations or warranties
#  respecting this application or these files, either expressed or implied,
#  arising by law or otherwise, including but not limited to: effectiveness,
#  completeness, accuracy or fitness for a particular purpose. Any use
#  whatsoever of this application and these files shall constitute acceptance
#  of all terms and conditions detailed in the associated licence.

from ctypes import *

class rt_stream_pgc(Structure):
   _fields_ = [
   ('MJD', c_double),
   ('sta_name', c_char * 8),
   ('X0', c_double),
   ('dX', c_double),
   ('sX', c_double),
   ('Y0', c_double),
   ('dY', c_double),
   ('sY', c_double),
   ('Z0', c_double),
   ('dZ', c_double),
   ('sZ', c_double),
   ('dN', c_double),
   ('sN', c_double),
   ('dE', c_double),
   ('sE', c_double),
   ('dh', c_double),
   ('sh', c_double),
   ('cNE', c_double),
   ('cNh', c_double),
   ('cEh', c_double),
   ('lat', c_double),
   ('lon', c_double),
   ('h', c_double),
   ('nbsat', c_int),
   ('spare', c_int),
   ('MJD_out', c_double),
  ]

class rt_stream_onc(Structure):
   _fields_ = [
   ('sta_name', c_char * 8, ),
   ('MJD_sys', c_double),
   ('MJD_ini', c_double),
   ('MJD_obs', c_double),
   ('lat', c_double),
   ('lon', c_double),
   ('hgt', c_double),
   ('dN', c_float),
   ('dE', c_float),
   ('dh', c_float),
   ('sN', c_float),
   ('sE', c_float),
   ('sh', c_float),
   ('cNE', c_float),
   ('cNh', c_float),
   ('cEh', c_float),
   ('sig0', c_float),
   ('pdop', c_float),
   ('cor_age', c_float),
   ('dt_ms', c_float),
   ('pmin', c_float),
   ('pmax', c_float),
   ('ar_dt_ms', c_float),
   ('nmsg_obs', c_ubyte),
   ('nmsg_eph', c_ubyte),
   ('nmsg_cor', c_ubyte),
   ('nmsg_ion', c_ubyte),
   ('nsat_trk', c_ubyte),
   ('nsat_eph', c_ubyte),
   ('nsat_cor', c_ubyte),
   ('nsat_ion', c_ubyte),
   ('nsat_use', c_ubyte),
   ('nrej_trk', c_ubyte),
   ('nrej_eph', c_ubyte),
   ('nrej_cor', c_ubyte),
   ('nrej_ion', c_ubyte),
   ('nrej_elv', c_ubyte),
   ('namb_jmp', c_ubyte),
   ('nrng_rej', c_ubyte),
   ('nphs_rej', c_ubyte),
   ('status', c_ubyte),
   ('ffix_amb', c_ubyte),
   ('pfix_amb', c_ubyte),
   ('prov_id', c_ushort),
   ('soln_id', c_ubyte),
   ('msgc_id', c_ubyte),
  ]
