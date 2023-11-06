import re
import numpy as np
import ds_format as ds

from rstoollib.headers import HEADER_PTS

re_line = re.compile(b'^(?P<h>\d+h)?(?P<m>\d+m)?(?P<s>\d+s)?(?P<ms>\d+)?: \[\#(?P<label>[A-Z]+):(?P<data>[^:\]]*)(?P<extra>:[^\]*])?\]$')
re_header = re.compile(b'^# (?P<key>[^=]+)=(?P<value>.*)$')
re_session_start = re.compile(b'^# Session start (?P<session_start>.*)$')

NA = {
	'int': -9223372036854775806,
	'float': np.nan,
	'hex': -9223372036854775806,
	'string': '', 
}

PARAMS = [
	(b'relAP', 'release altitude', 'm', 'int'),
	(b'afc', 'automatic frequency control', 'Hz', 'int'),
	(b'afc1', 'automatic frequency control 1', 'Hz', 'int'),
	(b'afc2', 'automatic frequency control 2', 'Hz', 'int'),
	(b'alt', 'GPS altitude', 'm', 'int'),
	(b'ang', 'wind direction', 'degrees', 'float'),
	(b'ang\d', 'wind direction (old)', 'degrees', 'float'),
	(b'behlan', 'behavior after landing', '1', 'int', {0: 'power-save', 1: 'beacon at once'}),
	(b'burn', 'burn string', '1', 'int', {0: 'at cut down'}),
	(b'crc', 'cyclic redundancy check (CRC)', '1', 'int'),
	(b'cutalt', 'cut dow altitude', 'm', 'int'),
	(b'extra', 'extra information', '', 'string'),
	(b'fwver', 'firmware version', '1', 'float'),
	(b'galt', 'altitude', 'm', 'int'),
	(b'gpa', 'ground pressure', 'Pa', 'int'),
	(b'h', 'hour', 'hour', 'int'),
	(b'hdop', 'GPS horizontal dilution of precision (HDOP)', '', 'float'),
	(b'hu', 'relative humidity', '%', 'float'),
	(b'hu\d', 'relative humidity (old)', '%', 'float'),
	(b'hw', 'hw', '1', 'int'),
	(b'id', 'sond ID', '1', 'int'),
	(b'label', 'label', '', 'string'), 
	(b'lat', 'latitude', 'degrees', 'float'),
	(b'latd', 'latitude', 'decimal part of minute', 'int'),
	(b'latm', 'latitude', 'minute', 'float'),
	(b'lon', 'longitude', 'degrees', 'float'),
	(b'lond', 'longitude', 'decimal part of minute', 'int'),
	(b'lonm', 'longitude', 'minute', 'float'),
	(b'lux', 'light', 'lux', 'int'),
	(b'mcnt', 'message counter', '1', 'int'),
	(b'm', 'minute', 'minute', 'int'),
	(b'md', 'mode', '1', 'int', {0: 'init', 1: 'ready for launch', 2: 'rising', 3: 'falling', 4: 'on ground silent', 5: 'on ground beeping', 6: 'on ground sometimes beeping', 7: 'cutting down'}),
	(b'ms', 'milisecond', 'ms', 'int'),
	(b'new', 'GPS validity', '1', 'int', {0: 'gps is old'}),
	(b'offset', 'time start', 'seconds since 1970-01-01T00:00', 'float'),
	(b'timezone', 'timezone', '1', 'int'),
	(b'version', 'version', '1', 'int'),
	(b'install', 'install', '', 'string'),
	(b's', 'second', 's', 'int'),
	(b'software', 'software version', '', 'string'),
	(b'node_id', 'node ID', '1', 'int'),
	(b'pa', 'air pressure', 'Pa', 'int'),
	(b'pwr', 'power', 'W', ('int', 'float')),
	(b'q0', 'quality', '1', 'hex'),
	(b'q1', 'quality', '1', 'hex'),
	(b'r', 'quality', '1', 'int'),
	(b'q', 'quality', '1', 'int'),
	(b'qu', 'quality', '%', 'float'),
	(b'rec', 'correction', '1', 'int'),
	(b'rec\d', 'correction (old)', '1', 'int'),
	(b'role', 'role', '1', 'int'),
	(b'sats', 'number of GPS satellites', '1', 'int'),
	(b'seq', 'sequence number' '1', 'int'),
	(b'session_start', 'session start', '', 'string'),
	(b'sid', 'session ID', '1', 'int'),
	(b'spd', 'wind speed', 'm s-1', 'float'),
	(b'spd\d', 'wind speed (old)', 'm s-1', 'float'),
	(b'su', 'power supply', 'V', 'float'),
	(b'syn', 'syn', '1', 'int'),
	(b'te', 'temperature', 'K', 'float'),
	(b'te\d', 'temperature (old)', 'K', 'float'),
	(b'tei', 'internal temperature', 'K', 'float'),
	(b'ucnt', 'ucnt', '1', 'int'),
]

META = {p[0]: {
	'.dims': ['seq'],
	'long_name': p[1].replace(' ', '_'),
	'units': p[2],
	'flag_values': list(p[4].keys()) if len(p) > 4 else None,
	'flag_meanings': ' '.join([x.replace(' ', '_') for x in p[4].values()]) \
		if len(p) > 4 else None,
} for p in PARAMS}

for k, v in META.items():
	if v['units'] == '':
		del v['units']
	if v['flag_values'] is None:
		del v['flag_values']
	if v['flag_meanings'] is None:
		del v['flag_meanings']	

def param(key):
	for p in PARAMS:
		if re.match(b'^' + p[0] + b'$', key):
			return p

def stage2(d):
	if b'fwver' in d:
		d[b'fwver'] /= 100.
	if b'lat' in d:
		d[b'lat'] = np.sign(d[b'lat'])*(
			np.floor(np.abs(d[b'lat'])/1e6) + \
			(np.abs(d[b'lat'])/1e6 % 1.)*1e2/60.
		)
	if b'latm' in d:
		d[b'latm'] /= 1e4
	if b'latd' in d:
		d[b'latd'] /= 1e4
	if b'lon' in d:
		d[b'lon'] = np.sign(d[b'lon'])*(
			np.floor(np.abs(d[b'lon'])/1e6) + \
			(np.abs(d[b'lon'])/1e6 % 1.)*1e2/60.
		)
	if b'lonm' in d:
		d[b'lonm'] /= 1e4
	if b'lond' in d:
		d[b'lond'] /= 1e4
	if b'pwr' in d:
		try:
			d[b'pwr'] = 1e-3*{
				0: 1.3,
				1: 1.5,
				2: 3,
				3: 6,
				4: 13,
				5: 25,
				6: 50,
				7: 100,
			}[d[b'pwr']]
		except KeyError:
			d[b'pwr'] = np.nan
	if b'q0' in d or b'q1' in d:
		q0 = d.get(b'q0', 0)
		q1 = d.get(b'q1', 0)
		d[b'q'] = max(q0, q1)	
	if b'r' in d or b'q' in d:
		rssi = (d[b'r'] if b'r' in d else d[b'q'])/256.
		if b'rec' in d:
			d[b'qu'] = max(0.01, rssi - 0.02*d[b'rec'])
		else:
			d[b'qu'] = rssi
	else:
		d[b'qu'] = 0.
	for k in d.keys():
		if k == b'te' or k == b'tei' or re.match(b'^te\d$', k):
			d[k] += 273.15
	return d

def stage1(d):
	d[b'h'] = int(d[b'h'][:-1]) if d[b'h'] is not None else 0
	d[b'm'] = int(d[b'm'][:-1]) if d[b'm'] is not None else 0
	d[b's'] = int(d[b's'][:-1]) if d[b's'] is not None else 0
	d[b'ms'] = int(d[b'ms']) if d[b'ms'] is not None else 0
	d[b'extra'] = d[b'extra'] if d[b'extra'] else ''
	pairs = d[b'data'].split(b',')
	del d[b'data']
	for pair in pairs:
		key, value = pair.split(b'=')
		d[key] = value
		p = param(key)
		if p is not None and len(p) > 3:
			type_ = p[3][0] if type(p[3]) is tuple else p[3]
			if type_ == 'int':
				d[key] = int(d[key])
			elif type_ == 'float':
				d[key] = float(d[key])
			elif type_ == 'hex':
				d[key] = int(d[key], 16)
	return stage2(d)

def stage0(line):
	m = re_session_start.match(line)
	if m is not None:
		g = m.groupdict()
		d = {}
		d[b'key'] = b'session_start'
		d[b'value'] = g['session_start']
		return d
	m = re_header.match(line)
	if m is not None:
		g = m.groupdict()
		d = {}
		d[b'key'] = g['key']
		d[b'value'] = g['value']
		return d	
	m = re_line.match(line)
	if m is None:
		return
	d = m.groupdict()
	keys = list(d.keys())
	for k in keys:
		if type(k) is not bytes:
			v = d[k]
			del d[k]
			d[k.encode('utf-8')] = v
	return stage1(d)

def postprocess(dd):
	for var in [b'lat', b'lon']:
		x = np.nan
		varm = var + b'm'
		vard = var + b'd'
		for d in dd:
			xm = (np.abs(x) % 1.)*60.
			xd = xm % 1.
			if var in d:
				x = d[var]
			elif varm in d and not np.isnan(x):
				xm2 = d[varm]
				if x < 0:
					xm2 = 60. - xm2
				x = np.sign(x)*(np.floor(np.abs(x)) + xm2/60.)
			elif vard in d and not np.isnan(x):
				xd2 = d[vard]
				if x < 0.:
					xd2 = 1. - xd2
				if xd2 - xd > 0.5:
					xd2 -= 1.
				if xd2 - xd < -0.5:
					xd2 += 1.
				x = np.sign(x)*(np.floor(np.abs(x)) + \
					(np.floor(xm) + xd2)/60.)
			if varm in d:
				del d[varm]
			if vard in d:
				del d[vard]
			d[var] = x

def read(filename):
	dd = []
	keys = set()
	header = {}
	with open(filename, 'rb') as f:
		for line in f.readlines():
			line = line.strip()
			d = stage0(line)
			if d is not None:
				if b'key' in d and b'value' in d:
					header[d[b'key']] = d[b'value']	
				else:
					dd += [d]
	postprocess(dd)
	for d in dd:
		keys |= set(d.keys())
	d0= {'.': {}}
	for k in keys:
		p = param(k)
		if p is None:
			continue
		type_ = p[3][1] if type(p[3]) is tuple else p[3]
		na = NA[type_]
		ku = k.decode('utf-8')
		if type_ == 'float':
			d0[ku] = np.array(
				[(d[k] if k in d else np.nan) for d in dd]
			)
		else:
			d0[ku] = np.ma.array(
				[(d[k] if k in d else na) for d in dd],
				mask=[(k not in d) for d in dd]
			)
		d0['.'][ku] = META[p[0]]
	for k, v in header.items():
		p = param(k)
		if p is None:
			continue
		ku = k.decode('utf-8')
		if len(p) > 3:
			type_ = p[3]
			if type_ == 'int':
				d0[ku] = int(v)
			elif type_ == 'float':
				d0[ku] = float(v)
			elif type_ == 'hex':
				d0[ku] = int(v, 16)
			elif type_ == 'string':
				d0[ku] = v.decode('utf-8')
		else:
			d0[ku] = v
		d0['.'][ku] = META[p[0]]
		d0['.'][ku]['.dims'] = []
	return d0

def pts(d):
	n = len(d['pa'])
	pts = {}
	time_start = 2440587.5 + d['offset']/(24.*60.*60.)
	time_elapsed = (
		d['h']*60.*60. +
		d['m']*60. +
		d['s'] + d['ms']*1e-3
	).filled(np.nan)
	pts['time'] = time_start + time_elapsed/(24.*60.*60.)
	pts['p'] = d['pa'].astype(np.float64).filled(np.nan)
	pts['z'] = d['alt'].astype(np.float64).filled(np.nan)
	for k1, k2 in [
		['hur', 'hu'],
		['ta', 'te']
	]:
		pts[k1] = np.full(n, np.nan, np.float64)
		for i in list(range(9, 0, -1)) + ['']:
			if (k2 + str(i)) not in d: continue
			mask = ~np.isnan(d[k2 + str(i)])
			pts[k1][mask] = d[k2 + str(i)][mask]
	pts['hur'] = d['hu']
	pts['lat'] = d['lat']
	pts['lon'] = d['lon']
	pts['.'] = HEADER_PTS
	return pts
