import os
from fnmatch import fnmatch
import numpy as np
import datetime as dt
import json
import re
import csv
import aquarius_time as aq
from rstoollib.headers import HEADER_PROF, HEADER_PTS

def find(dirname, pattern):
	for l in os.listdir(dirname):
		if fnmatch(l, pattern):
			return os.path.join(dirname, l)
	return None

def read_tspotint(filename):
	f = open(filename, 'rb')
	p = []
	ta = []
	hur = []
	wds = []
	wdd = []
	zg = []
	for i, l in enumerate(f.readlines()):
		if i < 4: continue
		x = l.split()
		p.append(float(x[1]))
		ta.append(float(x[2]))
		hur.append(float(x[3]))
		wds.append(float(x[4]))
		wdd.append(float(x[5]))
		zg.append(float(x[6]))
	return {
		'p': np.array(p, np.float64)*1e2,
		'ta': np.array(ta, np.float64) + 273.15,
		'hur': np.array(hur, np.float64),
		'wds': np.array(wds, np.float64),
		'wdd': np.array(wdd, np.float64),
		'zg': np.array(zg, np.float64),
	}

def decode_geo(s):
	r = re.compile(rb'^(?P<deg>[0-9]+)\xb0(?P<minute>[0-9\.]+)\'(?P<second>[0-9\.]+)?\"?(?P<dir>[EWNS])')
	m = r.match(s)
	x = np.nan
	if m is not None:
		g = m.groupdict()
		deg = int(g['deg'])
		minute = float(g['minute'])
		second = float(g['second']) if g['second'] != None else 0
		sign = 1 if g['dir'] in [b'E', b'N'] else -1
		x = sign*(deg + minute/60. + second/60./60.)
	return x

def read_summary(filename):
	d = {}
	r = re.compile(rb'^\s*\.?\s*(?P<k>.*[^\s]+) +:\s*(?P<v>.*[^\s]+)\s*$')
	with open(filename, 'rb') as f:
		for l in f.readlines():
			m = r.match(l)
			if m is not None:
				g = m.groupdict()
				d[g['k']] = g['v']

	summary = {}
	attrs = {}

	if b'Station Name' in d:
		attrs['platform_name'] = d[b'Station Name']

	if b'WMO Number' in d and d[b'WMO Number'] != b'/////':
		attrs['platform_id'] = d[b'WMO Number']

	if b'Sonde   Type' in d:
		attrs['sonde_type'] = d[b'Sonde   Type']

	if b'Serial Number' in d:
		attrs['sonde_serial_number'] = d[b'Serial Number']

	if b'Balloon             Make' in d:
		attrs['balloon_type'] = d[b'Balloon             Make']

	if b'Weight' in d:
		attrs['balloon_weight'] = d[b'Weight']

	if b'Mobile Call Sign' in d:
		attrs['call_sign'] = d[b'Mobile Call Sign']

	if b'Altitude (MSL)' in d:
		summary['platform_altitude'] = int(d[b'Altitude (MSL)'].strip(b'm'))

	if b'Latitude' in d:
		summary['launch_lat'] = decode_geo(d[b'Latitude'])

	if b'Longitude' in d:
		summary['launch_lon'] = decode_geo(d[b'Longitude'])

	if b'Launched' in d:
		if d[b'Launched'].endswith(b'p.m.'):
			summary['launch_time'] = aq.from_datetime(dt.datetime.strptime(d[b'Launched'].decode('utf-8'), '%d/%m/%Y %H:%M:%S p.m.'))
			summary['launch_time'] += 0.5
		elif d[b'Launched'].endswith(b'a.m.'):
			summary['launch_time'] = aq.from_datetime(dt.datetime.strptime(d[b'Launched'].decode('utf-8'), '%d/%m/%Y %H:%M:%S a.m.'))
		else:
			summary['launch_time'] = aq.from_datetime(dt.datetime.strptime(d[b'Launched'].decode('utf-8'), '%d/%m/%Y %H:%M:%S'))

	if b'Launched (UTC)' in d:
		summary['launch_time'] = aq.from_datetime(dt.datetime.strptime(d[b'Launched (UTC)'].decode('utf-8'), '%d/%m/%Y %H:%M:%S'))

	summary['.'] = {
		'.': attrs,
	}

	return summary

def read_info(filename):
	with open(filename, 'rb') as f:
		d = json.load(f)
		return {
			'ts': d.get('surface_temperature', np.nan),
		}

def read_prof(dirname):
	d = read_tspotint(find(dirname, '*_TSPOTINT.txt'))
	#summary = read_summary(find(dirname, '*_SUMMARY.txt'))
	#d.update(summary)
	info_filename = os.path.join(dirname, 'info.json')
	if os.path.exists(info_filename):
		info = read_info(info_filename)
		d.update(info)
	d['.'] = HEADER_PROF
	return d

PARAMS = [
	('sample', 'sample number', '1', 'int'),
	('date_time', 'date time', '', 'string'),
	('press', 'pressure', 'Pa', 'float'),
	('tair', 'air temperature', 'K', 'float'),
	('hum', 'relative humidity', '%', 'float'),
	('lat', 'latitude', 'degrees_north', 'float'),
	('long', 'longitude', 'degrees_east', 'float'),
	('alt', 'altitude', 'm', 'float'),
	('freq', 'frequency', 'Hz', 'float'),
	('f_offs', 'frequency offset', 'Hz', 'float'),
]

META = {p[0]: {
	'.dims': ['seq'],
	'long_name': p[1].replace(' ', '_'),
	'units': p[2],
} for p in PARAMS}

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
	}
	pts['.'] = HEADER_PTS
	return pts

def read(dirname):
	dat_filename = find(dirname, '*.dat')
	d = {}
	trans = str.maketrans({'#': '', ' ': '_', '+': '_'})
	with open(dat_filename) as f:
		reader = csv.DictReader(f)
		for r in reader:
			for k, v in r.items():
				k2 = k.lower().translate(trans)
				d[k2] = d.get(k2, []) + [v]
	d2 = {}
	for p in PARAMS:
		type_ = {
			'int': np.int64,
			'float': np.float64,
			'string': str,
		}[p[3]]
		na = {
			'int': -9223372036854775806,
			'float': np.nan,
			'string': '',
		}[p[3]]
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
		#if type_ == np.float64 or type_ == np.int64:
		#	mask = d2[p[0]] == 999999999
		#	d2[p[0]][mask] = na
		#	d2[p[0]] = np.ma.array(d2[p[0]], type_,
		#		mask=mask,
		#		fill_value=na
		#	)
	if 'tair' in d2:
		d2['tair'] += 273.15
	if 'press' in d2:
		d2['press'] *= 1e2
	d2['.'] = META
	return d2
