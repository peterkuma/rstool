import ds_format as ds

from rstool.headers import HEADER_PTS, HEADER_PROF

# This is a template for a new rstool driver which reads native instrument
# data and outputs im- or pts-formatted data.
#
# Add the driver to DRIVERS in __init__.py to enable the driver.

HEADER_IM = {
	# Intermadiate variables header.
}

def read(filename):
	# Read data from filename and return a ds dictionary with im-formatted
	# (instrument-dependent) data.
	d = {}
	d['.'] = HEADER_IM
	return d

def pts(d):
	# Convert im-formatted data in d and return a ds dictionary with
	# pts-formatted data.
	pts = {}
	pts['.'] = HEADER_PTS
	return pts
