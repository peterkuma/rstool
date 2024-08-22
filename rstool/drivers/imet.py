import os
from fnmatch import fnmatch
import numpy as np
import datetime as dt
import json
import re
import csv
import configparser
import aquarius_time as aq

from rstool.algorithms import *
from rstool.const import n0
from rstool.headers import HEADER_PROF, HEADER_PTS

PARAMS = [
	('alt', 'altitude', 'height_above_reference_ellipsoid', 'm', 'float'),
	('date_time', 'date time', None, '', 'string'),
	('f_offs', 'frequency offset', None, 'Hz', 'float'),
	('freq', 'frequency', None, 'Hz', 'float'),
	('hum', 'relative humidity', 'relative_humidity', '%', 'float'),
	('hurs', 'near-surface relative humidity', 'relative_humidity', '%',
		'float', []),
	('lat', 'latitude', 'latitude', 'degrees_north', 'float'),
	('long', 'longitude', 'longitude', 'degrees_east', 'float'),
	('press', 'air pressure', 'air_pressure', 'Pa', 'float'),
	('ps', 'surface air pressure', 'surface_air_pressure', 'Pa', 'float', []),
	('sample', 'sample number', None, '1', 'int'),
	('station_lat', 'station latitude', 'latitude', 'degrees_north', 'float',
		[]),
	('station_lon', 'station longitude', 'longitude', 'degrees_east', 'float',
		[]),
	('station_time', 'station time', 'time', 'days since -4713-11-24 12:00 UTC',
		'float', [], {'calendar': 'proleptic_gregorian'}),
	('station_z', 'station altitude', 'height_above_reference_ellipsoid', 'm',
		'float', []),
	('tair', 'air temperature', 'air_temperature', 'K', 'float'),
	('tas', 'near-surface air temperature', 'air_temperature', 'K', 'float',
		[]),
	('uas', 'eastward near-surface wind speed', 'eastward_wind', 'm s-1',
		'float', []),
	('vas', 'northward near-surface wind speed', 'northward_wind', 'm s-1',
		'float', []),
]

def header(x):
	out = {}
	for i, h in enumerate(['long_name', 'standard_name', 'units']):
		if x[i+1] is not None:
			out[h] = x[i+1]
	out['.dims'] = x[5] if len(x) > 5 else ['seq']
	if len(x) > 6:
		out.update(x[6])
	return out

META = {x[0]: header(x) for x in PARAMS}

def find(dirname, pattern):
	for l in os.listdir(dirname):
		if fnmatch(l, pattern):
			return os.path.join(dirname, l)
	return None

def parse_geo(s):
	r = re.compile(rb'^(?P<deg>[0-9]+)\xb0(?P<minute>[0-9\.]+)\'(?P<second>[0-9\.]+)?\"?(?P<dir>[EWNS])')
	m = r.match(s)
	if m is not None:
		g = m.groupdict()
		deg = int(g['deg'])
		minute = float(g['minute'])
		second = float(g['second']) if g['second'] != None else 0
		sign = 1 if g['dir'] in [b'E', b'N'] else -1
		return sign*(deg + minute/60. + second/60./60.)
	return np.nan

def parse_time(s):
	r = re.compile(r'^(\d+)(\d\d)(\d\d)T(\d\d)(\d\d)(\d\d)(?:\.(\d*))')
	m = r.match(s)
	if m is not None:
		g = list(m.groups())
		frac = 0
		if len(g) == 7:
			frac = g[6]
			del g[6]
			n = len(frac)
			frac = int(frac)/10**n
		g = [int(x) for x in g]
		return aq.from_date([1] + g + [frac])
	return np.nan

def read_flt(filename):
	d = {
		'tas': np.nan,
		'hurs': np.nan,
		'ps': np.nan,
		'uas': np.nan,
		'vas': np.nan,
		'.': {'.': {}},
	}
	c = configparser.ConfigParser()
	try: c.read(filename, encoding='utf-8-sig')
	except: return d
	try: d['tas'] = float(c['Weather']['Temperature']) + n0
	except: pass
	try: d['hurs'] = float(c['Weather']['Humidity'])
	except: pass
	try: d['ps'] = float(c['Weather']['Pressure'])*1e2
	except: pass
	try: d['wdds'] = float(c['Weather']['Wind Direction'])
	except: pass
	try: d['wdss'] = float(c['Weather']['Wind Speed'])
	except: pass
	try: d['.']['.']['operator'] = c['Flight Station']['OperatorName']
	except: pass
	try: d['.']['.']['station'] = c['Flight Station']['Name']
	except: pass
	try: d['.']['.']['balloon'] = c['Flight Balloon']['Name']
	except: pass
	try: d['.']['.']['balloon'] += ' %sg' % c['Flight Balloon']['Filling Weight']
	except: pass
	try: d['.']['.']['sonde'] = c['Flight Sonde']['ID']
	except: pass
	try: d['.']['.']['sonde'] += ' S/N: %s' % c['Flight Sonde']['Sonde SN']
	except: pass
	try: d['station_lon'] = float(c['Flight Station']['Longitude'])
	except: pass
	try: d['station_lat'] =  float(c['Flight Station']['Latitude'])
	except: pass
	try: d['station_z'] =  float(c['Flight Station']['Altitude'])
	except: pass
	try: d['station_time'] = parse_time(c['Weather']['Date/Time'])
	except: pass
	return d

def pts(d):
	time_trans = str.maketrans({'/': '-', ' ': 'T'})
	time = np.array([
		aq.from_iso(x.translate(time_trans))
		for x in d['date_time']
	], np.float64)
	pts = {
		'time': time,
		'ta': d['tair'],
		'p': d['press'],
		'hur': d['hum'],
		'lat': d['lat'],
		'lon': d['long'],
		'z': d['alt'],
		'ps': d['ps'],
		'tas': d['tas'],
		'hurs': d['hurs'],
		'uas': d['uas'],
		'vas': d['vas'],
		'station_lon': d['station_lon'],
		'station_lat': d['station_lat'],
		'station_time': d['station_time'],
		'station_z': d['station_z'],
	}
	pts['.'] = HEADER_PTS
	pts['.']['.'] = d['.'].get('.', {})
	return pts

def read_dat(filename):
	d = {}
	trans = str.maketrans({'#': '', ' ': '_', '+': '_'})
	with open(filename) as f:
		reader = csv.DictReader(f)
		for r in reader:
			for k, v in r.items():
				k2 = k.lower().translate(trans)
				d[k2] = d.get(k2, []) + [v]
	d2 = {}
	for p in PARAMS:
		if p[0] not in d:
			continue
		type_ = {
			'int': np.int64,
			'float': np.float64,
			'string': str,
		}[p[4]]
		na = {
			'int': -9223372036854775806,
			'float': np.nan,
			'string': '',
		}[p[4]]
		n = len(d[p[0]])
		d2[p[0]] = np.array(d[p[0]], type_)
		if type_ == np.float64:
			mask = d2[p[0]] == 999999999.
			d2[p[0]][mask] = np.nan
		elif type_ == np.int64:
			mask = d2[p[0]] == 999999999
			d2[p[0]][mask] = na
			d2[p[0]] = np.ma.array(d2[p[0]], type_,
				mask=mask,
				fill_value=na
			)
	if 'tair' in d2:
		d2['tair'] += n0
	if 'press' in d2:
		d2['press'] *= 1e2
	return d2

def read(dirname):
	filename_dat = find(dirname, '*.dat')
	filename_flt = find(dirname, '*.flt')
	d = read_flt(filename_flt)
	d2 = read_dat(filename_dat)
	d.update(d2)
	d['.'].update(META)
	return d
