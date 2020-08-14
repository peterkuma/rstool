import numpy as np
import ds_format as ds

VARS = ['tas', 'hurs', 'ps', 'wds', 'wdd', 'ts', 'lon', 'lat']

def read(filename, time):
	d = ds.read(filename, ['time'])
	i = np.argmin(np.abs(d['time'] - time))
	dt = np.abs(d['time'][i] - time)
	if dt <= 1/24.:
		return ds.read(filename, VARS, sel={'time': i})
	else:
		return None
