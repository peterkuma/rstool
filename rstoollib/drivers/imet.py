import os
from fnmatch import fnmatch
import numpy as np
import datetime as dt
import json
import re
import csv
import configparser
import aquarius_time as aq
from rstoollib.algorithms import *
from rstoollib.headers import HEADER_PROF, HEADER_PTS

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
	('tas', 'near-surface air temperature', 'K', 'float', []),
	('ps', 'surface air pressure', 'Pa', 'float', []),
	('hurs', 'near-surface relative humidity', '%', 'float', []),
	('uas', 'eastward near-surface wind speed', 'm s-1', 'float', []),
	('vas', 'northward near-surface wind speed', 'm s-1', 'float', []),
	('station_lon', 'station longitude', 'degrees_east', 'float', []),
	('station_lat', 'station latitude', 'degrees_north', 'float', []),
	('station_z', 'station altitude', 'm', 'float', []),
]

META = {p[0]: {
	'.dims': p[4] if len(p) > 4 else ['seq'],
	'long_name': p[1].replace(' ', '_'),
	'units': p[2],
} for p in PARAMS}

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
	try: d['tas'] = float(c['Weather']['Temperature']) + 273.15
	except: pass 
	try: d['hurs'] = float(c['Weather']['Humidity'])
	except: pass 
	try: d['ps'] = float(c['Weather']['Pressure'])
	except: pass 
	try: d['wdds'] = float(c['Weather']['Wind Direction'])
	except: pass
	try: d['wdss'] = float(c['Weather']['Wind Speed'])
	except: pass
	if 'wdss' in d and 'wdds' in d:
		d['uas'] = calc_ua(d['wdss'], d['wdds'])
		d['vas'] = calc_va(d['wdss'], d['wdds'])
	if 'wdss' in d: del d['wdss']
	if 'wdds' in d: del d['wdds']
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
	return d

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
	return d2

def read(dirname):
	filename_dat = find(dirname, '*.dat')
	filename_flt = find(dirname, '*.flt')
	d = read_flt(filename_flt)
	d2 = read_dat(filename_dat)
	d.update(d2)
	d['.'].update(META)
	return d
