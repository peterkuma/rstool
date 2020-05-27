import numpy as np
from numpy import ma
from pyproj import Geod
from rstoollib.headers import HEADER_PROF

VARS = [
	'z',
	'ta',
	'hur',
	'lat',
	'lon',
	'time',
]

def prof(d, pres=5e2, desc=False):
	"""Calculate profile (prof) from points (pts).

	d - Points (pts) dataset (dict).
	pres - Pressure resolution (float).
	desc - Descending profile (bool).
	"""
	pmin, pmax = np.nanmin(d['p']), np.nanmax(d['p'])
	phalf_min = pmin - (pmin % pres)
	phalf_max = pmax + pres - (pmax % pres)
	phalf = np.arange(phalf_min, phalf_max + pres, pres)[::-1]
	pfull = 0.5*(phalf[1:] + phalf[:-1])
	n = len(phalf) - 1
	prof = {}
	for var in VARS:
		prof[var] = np.full(n, np.nan, np.float64)

	if desc:
		mask1 = np.array(
			list(~(np.diff(d['p']) < 0.)) + [True],
			np.bool
		)
	else:
		mask1 = np.array(
			list(~(np.diff(d['p']) > 0.)) + [True],
			np.bool
		)
	for i in range(n - 1):
		p1 = phalf[i]
		p2 = phalf[i + 1]
		for var in VARS:
			mask2 = (d['p'] > p2) & (d['p'] <= p1)
			mask = mask1 & mask2
			if np.sum(mask) > 0 and np.any(~np.isnan(d[var][mask])):
				prof[var][i] = np.nanmean(d[var][mask])

	prof['p'] = pfull
	prof['ua'] = np.full(n, np.nan, np.float64)
	prof['va'] = np.full(n, np.nan, np.float64)
	geod = Geod(ellps='WGS84')
	for i in range(1, n):
		az, _, dst = geod.inv(
			prof['lon'][i - 1],
			prof['lat'][i - 1],
			prof['lon'][i],
			prof['lat'][i],
		)
		dt = (prof['time'][i] - prof['time'][i - 1])*24.*60.*60.
		if dt > 0.:
			prof['ua'][i] = dst/dt*np.sin(az/180.*np.pi)
			prof['va'][i] = dst/dt*np.cos(az/180.*np.pi)
	for var in [
		'tas',
		'hurs',
		'ps',
		'uas',
		'vas',
		'station_lat',
		'station_lon',
		'station_z'
	]:
		prof[var] = d[var] if var in d else np.nan
	prof['.'] = HEADER_PROF
	prof['.']['.'] = d['.'].get('.', {})
	return prof
