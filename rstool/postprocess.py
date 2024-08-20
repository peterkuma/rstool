from rstool.algorithms import *

DEPS = [
	[['p2', 'bvf'], ['theta_v', 'zg', 'p', 'g'], calc_bvf],
	['e', ['w', 'p'], calc_e],
	['es', ['ws', 'ps'], calc_e, ['w', 'p']],
	['esat', 'ta', calc_esat],
	['esats', 'tas', calc_esat, 'ta'],
	['g', 'station_lat', calc_g, 'lat'],
	['gamma', 'g', calc_gamma],
	['gamma_sat', ['p', 'ta', 'gamma'], calc_gamma_sat],
	['hur', ['w', 'wsat'], calc_hur],
	['hurs', ['ws', 'wsats'], calc_hur, ['w', 'wsat']],
	['hus', 'w', calc_hus],
	['huss', 'ws', calc_hus, 'w'],
	['p_lcl', ['ps', 'ws', 'tas'], calc_p_lcl],
	['p_ll', ['ts', 'p', 'theta'], calc_p_ll],
	['ta_par', ['p', 'ps', 'tas'], calc_ta_par],
	['ta_par_sat', ['p', 'tas', 'ws', 'g', 'gamma'], calc_ta_par_sat],
	['ta_surf_par', ['p', 'ps', 'ts'], calc_ta_par, ['p', 'ps', 'tas']],
	['ta_surf_par_sat', ['p', 'ts', 'ws', 'g', 'gamma'], calc_ta_par_sat,
		['p', 'tas', 'ws', 'g', 'gamma']],
	['td', ['e', 'hur', 'ta'], calc_td],
	['tds', ['es', 'hurs', 'tas'], calc_td, ['e', 'hur', 'ta']],
	['tv', ['ta', 'w'], calc_tv],
	['tvs', ['tas', 'ws'], calc_tv, ['ta', 'w']],
	['theta', ['p', 'ps', 'ta'], calc_theta],
	['theta_v', ['theta', 'w'], calc_tv, ['ta', 'w']],
	['ua', ['wds', 'wdd'], calc_ua],
	['uas', ['wdss', 'wdds'], calc_ua, ['wds', 'wdd']],
	['va', ['wds', 'wdd'], calc_va],
	['vas', ['wdss', 'wdds'], calc_va, ['wds', 'wdd']],
	['w', 'hus', calc_w],
	['w', ['hur', 'wsat'], calc_w],
	['wdd', ['ua', 'va'], calc_wdd],
	['wdds', ['uas', 'vas'], calc_wdd, ['ua', 'va']],
	['wds', ['ua', 'va'], calc_wds],
	['wdss', ['uas', 'vas'], calc_wds, ['ua', 'va']],
	['ws', 'huss', calc_w, ['hus']],
	['ws', ['hurs', 'wsats'], calc_w, ['hur', 'wsat']],
	['wsat', ['p', 'esat'], calc_w, ['p', 'e']],
	['wsats', ['ps', 'esats'], calc_w, ['p', 'e']],
	['z', ['zg', 'g'], calc_z],
	['zg', ['z', 'g'], calc_zg],
	['zg_lcl', ['p_lcl', 'p', 'zg'], calc_z, ['p1', 'p', 'z']],
	['zg_ll', ['p_ll', 'p', 'zg'], calc_z, ['p1', 'p', 'z']],
]

def postprocess_target(d, target, chain=[]):
	for rec in DEPS:
		if len(rec) == 4:
			target1, source, func, map_ = rec
			if not isinstance(map_, list):
				map_ = [map_]
		else:
			target1, source, func = rec
			map_ = None
		if target == target1 or isinstance(target1, list) and target in target1:
			if not isinstance(source, list):
				source = [source]
			if not isinstance(target1, list):
				target1 = [target1]
			#print('target1: %s, source: %s' % (target1, source))
			for s in source:
				if s not in d:
					if s in chain:
						#print('in chain')
						break
					#print('-> %s' % s)
					if not postprocess_target(d, s, chain + [target]):
						break
			else:
				if map_ is not None:
					res = func(**{m: d[s] for m, s in zip(map_, source)})
				else:
					res = func(**{s: d[s] for s in source})
				if not isinstance(res, tuple):
					res = (res,)
				for t, x in zip(target1, res):
					#print('setting %s to %s' % (t, x))
					d[t] = x
				return True
	#print('not found')
	return False

def postprocess(d):
	'''Postprocess profile (prof) dataset d by calculating derived
	variables.'''
	tmp_station_lat = 'station_lat' not in d
	if tmp_station_lat:
		# Use a temporary latitude of 45 degrees for g calculation, but remove
		# the variable when done.
		d['station_lat'] = 45
	for rec in DEPS:
		target, source, func = rec[:3]
		if not isinstance(target, list):
			target = [target]
		for t in target:
			postprocess_target(d, t)
	if tmp_station_lat:
		del d['station_lat']
