import numpy as np
import ds_format as ds

from rstoollib.algorithms import *

def postprocess(d):
	"""Postprocess profile (prof) dataset d by calculating derived
	variables."""
	if 'zg' not in d and 'z' in d and 'lat' in d:
		d['zg'] = calc_zg(d['z'], d['lat'])
	if 'z' not in d and 'zg' in d and 'lat' in d:
		d['z'] = calc_z(d['zg'], d['lat'])
	d['theta'] = calc_theta(d['p'], d['ta'])
	d['p2'], d['bvf'] = calc_bvf(d['theta'], d['zg'], d['p'])
	d['es'] = calc_es(d['ta'])
	d['ta_par'] = calc_ta_par(d['p'], d['ta'][0])
	if 'ts' in d:
		d['llp'] = calc_llp(d['ts'], d['p'], d['theta'])
	if 'ua' in d and 'va' in d:
		d['wds'] = calc_wds(d['ua'], d['va'])
		d['wdd'] = calc_wdd(d['ua'], d['va'])
	elif 'wds' in d and 'wdd' in d:
		d['ua'] = calc_ua(d['wds'], d['wdd'])                           
		d['va'] = calc_va(d['wds'], d['wdd'])    
	if 'hus' in d:
		ws = calc_w(d['p'], d['es'])
		qs = 1./(1./ws + 1)
		d['hur'] = 100.*d['hus']/qs
	if 'hur' in d:
		d['e'] = d['hur']/100.*d['es']
		d['p_lcl'] = calc_lclp(d['p'][0], d['e'][0], d['ta'][0])
		d['zg_lcl'] = np.interp(d['p_lcl'], d['p'][::-1], d['zg'][::-1])
		#d['clp'] = calc_clp(d['p'], d['e'], d['ta'])
		#d['cl'] = np.interp(d['clp'], d['p'][::-1], d['zg'][::-1])
		d['ta_par_s'] = calc_ta_par_s(d['p'], d['ta'][0], d['e'][0])
	if 'ts' in d:
		d['ta_surf_par'] = calc_ta_par(d['p'], d['ts'])
		d['ta_surf_par_s'] = calc_ta_par_s(d['p'], d['ts'], d['e'][0])
		#d['ta_surf_par_x'] = calc_ta_par(d['p'], d['ts'] + 0.5)
		#d['ta_surf_par_s_x'] = calc_ta_par_s(d['p'], d['ts'] + 0.5, d['e'][0])

