import numpy as np
import ds_format as ds

from rstoollib.algorithms import *

def remove_descending(d):
	n = len(d['p'])
	mask = np.zeros(n, dtype=np.bool)
	p0 = None
	for i in range(n):
		if p0 is None or d['p'][i] < p0:
			mask[i] = True
			p0 = d['p'][i]
	ds.select(d, {'p': mask})

def calc_vars(d):
	d['theta'] = calc_theta(d['p'], d['ta'])
	d['p2'], d['bvf'] = calc_bvf(d['theta'], d['zg'], d['p'])
	d['es'] = calc_es(d['ta'])
	d['ta_par'] = calc_ta_par(d['p'], d['ta'][0])
	if 'ts' in d:
		d['llp'] = calc_llp(d['ts'], d['p'], d['theta'])
	if 'wds' in d and 'wdd' in d:
		d['ua'] = calc_ua(d['wds'], d['wdd'])
		d['va'] = calc_va(d['wds'], d['wdd'])
	if 'hus' in d:
		ws = calc_w(d['p'], d['es'])
		qs = 1./(1./ws + 1)
		d['hur'] = 100.*d['hus']/qs
	if 'hur' in d:
		d['e'] = d['hur']/100.*d['es']
		d['lclp'] = calc_lclp(d['p'][0], d['e'][0], d['ta'][0])
		d['lcl'] = np.interp(d['lclp'], d['p'][::-1], d['zg'][::-1])
		d['clp'] = calc_clp(d['p'], d['e'], d['ta'])
		d['cl'] = np.interp(d['clp'], d['p'][::-1], d['zg'][::-1])
		d['ta_par_s'] = calc_ta_par_s(d['p'], d['ta'][0], d['e'][0])
	if 'ts' in d:
		d['ta_surf_par'] = calc_ta_par(d['p'], d['ts'])
		d['ta_surf_par_s'] = calc_ta_par_s(d['p'], d['ts'], d['e'][0])
		d['ta_surf_par_x'] = calc_ta_par(d['p'], d['ts'] + 0.5)
		d['ta_surf_par_s_x'] = calc_ta_par_s(d['p'], d['ts'] + 0.5, d['e'][0])

def postprocess(d):
	remove_descending(d)
	calc_vars(d)