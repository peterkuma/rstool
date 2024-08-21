#!/usr/bin/env python3
'''rstool converts radiosonde measurement data to NetCDF intrument-dependent intermediate (im), points (pts) and profile (prof) datasets and calculates derived physical quantities.

Usage: rstool INPUT_TYPE OUTPUT_TYPE INPUT [SURFACE] OUTPUT

Arguments:

  INPUT_TYPE   See Input types below.
  OUTPUT_TYPE  See Output types below.
  INPUT        Input file or directory.
  SURFACE      Near-surface variables (NetCDF).
  OUTPUT       Output file (NetCDF).

Input types:

  imet           InterMet Systems iMet-1-ABxn. INPUT should be a directory generated by the iMetOS-II software, containing ".dat" and ".flt" files.
  prof           rstool profile ("prof") dataset (NetCDF).
  pts            rstool points ("pts") dataset (NetCDF). Collection of measurement points. The output of running rstool with the output type "pts".
  im:INSTRUMENT  Intermediate (im) instrument-dependent rstool format
  (NetCDF). INSTRUMENT is one of "imet" or "ws".
  ws             Windsond. INPUT should be a ".sounding" file generated by the Windsond software.

Output types:

  pts        Collection of measurement points (NetCDF).
  prof       Vertical profile calculated by interpolating the measurement points during the ascent of the radiosonde as a function of pressure (NetCDF).
  prof:desc  The same as "prof", but for the descending path of the radiosonde (if present in the input data).
  im         Intermediate instrument-dependent rstool format (NetCDF).

The following input/output type combinations are possible, where INSTRUMENT is "imet" or "ws":

  INSTRUMENT im            Native instrument format to instrument-dependent intermediate format (NetCDF).
  INSTRUMENT pts           Native instrument format to the points format.
  INSTRUMENT prof          Native instrument format to the profile format.
  INSTRUMENT prof:desc     Native instrument format to a descending profile format.
  im:INSTRUMENT pts        Instrument-dependent intermediate format (NetCDF) to the points format.
  im:INSTRUMENT prof       Instrument-dependent intermediate format (NetCDF) to the profile format.
  im:INSTRUMENT prof:desc  Instrument-dependent intermediate format (NetCDF) to the descending profile format.
  pts prof                 The points format to the profile format.
  pts prof:desc            The points format to the descending profile format.
  prof prof                The profile format to the profile format. This can be used to calculate derived physical quantities from a basic set of quantities.
'''

import sys
import signal
signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))

__version__ = '2.0.0-dev'

import datetime as dt
import numpy as np
import ds_format as ds
import aquarius_time as aq

import rstool
from rstool.drivers import DRIVERS
from rstool.headers import HEADER_PTS, HEADER_PROF
from rstool import postprocess, prof

def get_driver(name):
	try:
		drv = DRIVERS[name]
	except KeyError:
		raise ValueError('%s: unknown input type' % name)
	return drv

def main2(input_type, output_type, input_, output, surf=None):
	d_im = None
	d_pts = None
	d_prof = None
	d_prof_desc = None
	d_surf = None
	desc = False

	not_supported_msg = 'input or output type not supported'

	if input_type.startswith('im:'):
		name = input_type[(input_type.index(':')+1):]
		drv = get_driver(name)
		d_im = ds.read(input_)
	elif input_type == 'pts':
		d_pts = ds.read(input_)
	elif input_type == 'prof':
		d_prof = ds.read(input_)
		d_prof['.'] = HEADER_PROF
	else:
		drv = get_driver(input_type)
		if hasattr(drv, 'read'):
			d_im = drv.read(input_)

	if d_pts is None and d_im is not None and hasattr(drv, 'pts'):
		d_pts = drv.pts(d_im)

	if d_prof is None and d_pts is not None:
		d_prof = prof(d_pts)
		d_prof_desc = prof(d_pts, desc=True)

	if d_prof is not None and surf is not None:
		drv = rstool.drivers.surf
		d_surf = drv.read(surf, d_prof['time'][0])
		if d_surf is not None:
			for k, v in d_surf.items():
				if k != '.':
					d_prof[k] = d_surf[k]

	if d_prof is not None:
		postprocess(d_prof)

	if d_prof_desc is not None:
		postprocess(d_prof_desc)

	if output_type == 'prof':
		if d_prof is None:
			raise ValueError(not_supported_msg)
		d = d_prof
	elif output_type == 'prof:desc':
		if d_prof_desc is None:
			raise ValueError(not_supported_msg)
		d = d_prof_desc
	elif output_type == 'pts':
		if d_pts is None:
			raise ValueError(not_supported_msg)
		d = d_pts
	elif output_type == 'im':
		if d_im is None:
			raise ValueError(not_supported_msg)
		d = d_im
	else:
		raise ValueError(not_supported_msg)

	d['.'] = d.get('.', {})
	d['.']['.'] = d['.'].get('.', {})
	d['.']['.'].update({
		'software': 'rstool ' + __version__ + \
			' (https://github.com/peterkuma/rstool)',
		'created': aq.to_iso(aq.from_datetime(dt.datetime.utcnow())),
	})
	ds.write(output, d)

def main():
	if len(sys.argv) not in [5, 6]:
		sys.stderr.write(sys.modules[__name__].__doc__)
		sys.exit(1)

	input_type = sys.argv[1]
	output_type = sys.argv[2]
	if len(sys.argv) == 5:
		surf = None
		input_ = sys.argv[3]
		output = sys.argv[4]
	elif len(sys.argv) == 6:
		input_ = sys.argv[3]
		surf = sys.argv[4]
		output = sys.argv[5]

	np.seterr(all='ignore')

	main2(input_type, output_type, input_, output, surf=surf)

if __name__ == '__main__':
	main()
