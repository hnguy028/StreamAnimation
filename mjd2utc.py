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

import math
import time

def MJD2UTC(mjd):
	mjd_time, mjd_day = math.modf(mjd)
	tm_hour = math.floor((86400.0*mjd_time)/3600.0)
	tm_min = math.floor(math.fmod((86400.0*mjd_time),3600.0)/60.0)
	tm_sec = round(math.fmod(math.fmod((86400.0*mjd_time),3600.0),60.0),0)
	jd = mjd_day + 0.5 + 2400000.5
	F, I = math.modf(jd)
	I = int(I)
	A = math.trunc((I - 1867216.25)/36524.25)
	if I > 2299160:
		B = I + 1 + A - math.trunc(A / 4.)
	else:
		B = I
	C = B + 1524
	D = math.trunc((C - 122.1) / 365.25)
	E = math.trunc(365.25 * D)
	G = math.trunc((C - E) / 30.6001)
	tm_mday = C - E + F - math.trunc(30.6001 * G)

	if G < 13.5:
		tm_mon = G - 1
	else:
		tm_mon = G - 13

	if tm_mon > 2.5:
		tm_year = D - 4716
	else:
		tm_year = D - 4715

	return time.strftime('%d %b %Y %H:%M:%S', time.struct_time((int(tm_year), int(tm_mon), int(tm_mday), int(tm_hour), int(tm_min), int(tm_sec), 0, 0, -1)))
