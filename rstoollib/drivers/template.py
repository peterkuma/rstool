import ds_format as ds

from rstoollib.headers import HEADER_PTS, HEADER_PROF

# This is a template for a new rstool driver which reads native instrument
# data and outputs raw- or pts-formatted data.
#
# Add the driver to DRIVERS in __init__.py to enable the driver.

HEADER_RAW = {
	# Raw variables header.
}

def read(filename):
	# Read data from filename and return a ds dictionary with raw-formatted
	# (instrument-dependent) data.
	d = {}
	d['.'] = HEADER_RAW
	return d

def pts(d):
	# Convert raw-formatted data in d and return a ds dictionary with
	# pts-formatted data.
	pts = {}
	pts['.'] = HEADER_PTS
	return pts

# Optional (alternative to implementing read and pts):

def read_prof(filename):
	# Read data from filename and return a ds dictionary with prof-formatted
	# (instrument-dependent) data.
	prof = {}
	prof['.'] = HEADER_PROF
	return prof

