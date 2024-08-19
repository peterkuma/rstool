import numpy as np
import ds_format as ds

from rstool.algorithms import *

def postprocess(d):
	"""Postprocess profile (prof) dataset d by calculating derived
	variables."""
	if 'z' in d and 'lat' in d and 'zg' not in d:
		d['zg'] = calc_zg(d['z'], d['lat'])
	if 'zg' in d and 'lat' in d and 'z' not in d:
		d['z'] = calc_z(d['zg'], d['lat'])
	if 'p' in d and 'ta' in d and 'theta' not in d:
		d['theta'] = calc_theta(d['p'], d['ta'])
	if 'theta' in d and 'zg' in d and 'p' in d and 'lat' in d and \
		'p2' not in d and 'bvf' not in d:
		d['p2'], d['bvf'] = calc_bvf(d['theta'], d['zg'], d['p'], d['lat'])
	if 'ta' in d and 'es' not in d:
		d['es'] = calc_es(d['ta'])
	if 'p' in d and 'ta' in d and 'ta_par' not in d:
		d['ta_par'] = calc_ta_par(d['p'], d['ta'][0])
	if 'ts' in d and 'p' in d and 'theta' in d and 'p_ll' not in d:
		d['p_ll'] = calc_p_ll(d['ts'], d['p'], d['theta'])
	if 'ua' in d and 'va' in d and 'wds' not in d and 'wdd' not in d:
		d['wds'] = calc_wds(d['ua'], d['va'])
		d['wdd'] = calc_wdd(d['ua'], d['va'])
	elif 'wds' in d and 'wdd' in d and 'ua' not in d and 'va' not in d:
		d['ua'] = calc_ua(d['wds'], d['wdd'])
		d['va'] = calc_va(d['wds'], d['wdd'])
	if 'p' in d and 'es' in d and 'hus' in d and 'hur' not in d:
		ws = calc_w(d['p'], d['es'])
		w = calc_w_from_q(d['hus'])
		d['hur'] = 100*w/ws
	if 'p' in d and 'es' in d and 'hur' in d and 'e' not in d:
		ws = calc_w(d['p'], d['es'])
		w = d['hur']/100*ws
		d['e'] = calc_e(w, d['p'])
	if 'theta' in d and 'p' in d and 'es' in d and 'hur' in d and \
		'theta_v' not in d:
		ws = calc_w(d['p'], d['es'])
		w = d['hur']/100*ws
		d['theta_v'] = calc_theta_v(d['theta'], w)
	if 'p' in d and 'e' in d and 'ta' in d and 'p_lcl' not in d:
		d['p_lcl'] = calc_p_lcl(d['p'][0], d['e'][0], d['ta'][0])
	if 'p_lcl' in d and 'p' in d and 'zg' in d and 'zg_lcl' not in d:
		d['zg_lcl'] = np.interp(d['p_lcl'], d['p'][::-1], d['zg'][::-1])
		#d['clp'] = calc_clp(d['p'], d['e'], d['ta'])
		#d['cl'] = np.interp(d['clp'], d['p'][::-1], d['zg'][::-1])
	if 'p_ll' in d and 'p' in d and 'zg' in d and 'zg_ll' not in d:
		d['zg_ll'] = np.interp(d['p_ll'], d['p'][::-1], d['zg'][::-1])
	if 'p' in d and 'ta' in d and 'e' in d and 'ta_par_s' not in d:
		d['ta_par_s'] = calc_ta_par_s(d['p'], d['ta'][0], d['e'][0])
	if 'p' in d and 'ts' in d and 'ta_surf_par' not in d:
		d['ta_surf_par'] = calc_ta_par(d['p'], d['ts'])
	if 'p' in d and 'ts' in d and 'e' in d and 'ta_surf_par_s' not in d:
		d['ta_surf_par_s'] = calc_ta_par_s(d['p'], d['ts'], d['e'][0])
		#d['ta_surf_par_x'] = calc_ta_par(d['p'], d['ts'] + 0.5)
		#d['ta_surf_par_s_x'] = calc_ta_par_s(d['p'], d['ts'] + 0.5, d['e'][0])
	if 'wdss' in d and 'wdds' in d and 'uav' not in d and 'vas' not in d:
		d['uas'] = calc_ua(d['wdss'], d['wdds'])
		d['vas'] = calc_va(d['wdss'], d['wdds'])
	if 'tds' in d and 'ps' in d and 'tas' in d and 'hurs' not in d:
		e = calc_es(d['tds'])
		w = calc_w(d['ps'], e)
		es = calc_es(d['tas'])
		ws = calc_w(d['ps'], es)
		d['hurs'] = 100*w/ws
