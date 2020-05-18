# -*- coding: utf-8 -*-
import os
from fnmatch import fnmatch
import numpy as np
import datetime as dt
import json
import re
import aquarius_time as aq

def find(dirname, pattern):
	for l in os.listdir(dirname):
		if fnmatch(l, pattern):
			return os.path.join(dirname, l)
	return None

def read_tspotint(filename):
	f = open(filename, 'r')
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
	r = re.compile(r'^(?P<deg>[0-9]+)\xb0(?P<minute>[0-9\.]+)\'(?P<second>[0-9\.]+)?\"?(?P<dir>[EWNS])')
	m = r.match(s)
	x = np.nan
	if m is not None:
		g = m.groupdict()
		deg = int(g['deg'])
		minute = float(g['minute'])
		second = float(g['second']) if g['second'] != None else 0
		sign = 1 if g['dir'] in ['E', 'N'] else -1
		x = sign*(deg + minute/60. + second/60./60.)
	return x

def read_summary(filename):
	d = {}
	r = re.compile(r'^\s*\.?\s*(?P<k>.*[^\s]+) +:\s*(?P<v>.*[^\s]+)\s*$')
	with open(filename) as f:
		for l in f.readlines():
			m = r.match(l)
			if m is not None:
				g = m.groupdict()
				d[g['k']] = g['v']

	summary = {}
	attrs = {}

	if 'Station Name' in d:
		attrs['platform_name'] = d['Station Name']

	if 'WMO Number' in d and d['WMO Number'] != '/////':
		attrs['platform_id'] = d['WMO Number']

	if 'Sonde   Type' in d:
		attrs['sonde_type'] = d['Sonde   Type']

	if 'Serial Number' in d:
		attrs['sonde_serial_number'] = d['Serial Number']

	if 'Balloon             Make' in d:
		attrs['balloon_type'] = d['Balloon             Make']

	if 'Weight' in d:
		attrs['balloon_weight'] = d['Weight']

	if 'Mobile Call Sign' in d:
		attrs['call_sign'] = d['Mobile Call Sign']

	if 'Altitude (MSL)' in d:
		summary['platform_altitude'] = int(d['Altitude (MSL)'].strip('m'))

	if 'Latitude' in d:
		summary['launch_lat'] = decode_geo(d['Latitude'])

	if 'Longitude' in d:
		summary['launch_lon'] = decode_geo(d['Longitude'])

	if 'Launched' in d:
		if d['Launched'].endswith('p.m.'):
			summary['launch_time'] = aq.from_datetime(dt.datetime.strptime(d['Launched'], '%d/%m/%Y %H:%M:%S p.m.'))
			summary['launch_time'] += 0.5
		elif d['Launched'].endswith('a.m.'):
			summary['launch_time'] = aq.from_datetime(dt.datetime.strptime(d['Launched'], '%d/%m/%Y %H:%M:%S a.m.'))
		else:
			summary['launch_time'] = aq.from_datetime(dt.datetime.strptime(d['Launched'], '%d/%m/%Y %H:%M:%S'))

	if 'Launched (UTC)' in d:
		summary['launch_time'] = aq.from_datetime(dt.datetime.strptime(d['Launched (UTC)'], '%d/%m/%Y %H:%M:%S'))

	summary['.'] = {
		'.': attrs,
	}

	return summary

def read_info(filename):
	with open(filename) as f:
		d = json.load(f)
		return {
			'ts': d.get('surface_temperature', np.nan),
		}

def read(dirname):
	d = read_tspotint(find(dirname, '*_TSPOTINT.txt'))
	summary = read_summary(find(dirname, '*_SUMMARY.txt'))
	d.update(summary)
	info_filename = os.path.join(dirname, 'info.json')
	if os.path.exists(info_filename):
		info = read_info(info_filename)
		d.update(info)
	return d
