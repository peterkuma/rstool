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
	"""
	Calculate profile (prof) from points (pts).
	
	d - Points (pts) dataset (dict).
	pres - Pressure resolution (float).
	desc - Descending profile (bool).
	"""
	pmin, pmax = d['p'].min(), d['p'].max()	
	phalf_min = pmin - (pmin % pres)
	phalf_max = pmax + pres - (pmax % pres)
	phalf = np.arange(phalf_min, phalf_max + pres, pres)[::-1]
	pfull = 0.5*(phalf[1:] + phalf[:-1])
	n = len(phalf) - 1
	prof = {
		'p': pfull,
		'wdd': np.full(n, np.nan, np.float64),
		'wds': np.full(n, np.nan, np.float64),
	}
	for var in VARS:
		prof[var] = np.full(n, np.nan, np.float64)

	if desc:
		mask1 = np.array(list(~(np.diff(d['p']) < 0.)) + [True], np.bool)
	else:
		mask1 = np.array(list(~(np.diff(d['p']) > 0.)) + [True], np.bool)
	for i in range(n):
		p1 = phalf[i]
		p2 = phalf[i + 1]
		for var in VARS:
			mask2 = (d['p'] > p2) & (d['p'] <= p1)
			prof[var][i] = d[var][mask1 & mask2].mean()

	geod = Geod(ellps='WGS84')
	for i in range(1, n - 1):
		az, _, dst = geod.inv(
			prof['lon'][i - 1],
			prof['lat'][i - 1],
			prof['lon'][i],
			prof['lat'][i],
		)
		prof['wdd'][i] = az if az >= 0. else 360. + az
		dt = prof['time'][i] - prof['time'][i - 1]
		prof['wds'][i] = dst/dt

	prof['.'] = HEADER_PROF
	return prof
