from rstool.algorithms import *

DEPS = [
	[['p_bvf', 'zg_bvf', 'bvf'], ['thetav', 'zg', 'p', 'g'], calc_bvf],
	['e', ['p', 'w'], calc_e],
	['e', 'td', calc_esat, 'ta'],
	['es', ['ps', 'ws'], calc_e, ['p', 'w']],
	['es', 'tds', calc_esat, 'ta'],
	['esat', 'ta', calc_esat],
	['esats', 'tas', calc_esat, 'ta'],
	['g', 'station_lat', calc_g, 'lat'],
	['gammad', 'g', calc_gammad],
	['gammam', ['p', 'ta', 'gammad'], calc_gammam],
	['hur', ['w', 'wsat'], calc_hur],
	['hurs', ['ws', 'wsats'], calc_hur, ['w', 'wsat']],
	['hus', 'w', calc_hus],
	['huss', 'ws', calc_hus, 'w'],
	['lcl', ['pc', 'p', 'zg'], calc_zg, ['p1', 'p', 'zg']],
	['lcls', ['pcs', 'p', 'zg'], calc_zg, ['p1', 'p', 'zg']],
	['lts', ['p', 'theta', 'thetas'], calc_lts],
	['pc', ['ps', 'ws', 'tas'], calc_pc],
	['pcs', ['ps', 'ws', 'ts'], calc_pc, ['ps', 'ws', 'tas']],
	['rho', ['rhod', 'rhow'], calc_rho],
	['rhod', ['p', 'e', 'ta'], calc_rhod],
	['rhods', ['ps', 'es', 'tas'], calc_rhod, ['p', 'e', 'ta']],
	['rhos', ['rhods', 'rhows'], calc_rho, ['rhod', 'rhow']],
	['rhow', ['p', 'e', 'ta'], calc_rhow],
	['rhows', ['ps', 'es', 'tas'], calc_rhow, ['p', 'e', 'ta']],
	['td', 'e', calc_td],
	['tds', 'es', calc_td, 'e'],
	['tv', ['ta', 'w'], calc_tv],
	['tvs', ['tas', 'ws'], calc_tv, ['ta', 'w']],
	['theta', ['p', 'ta'], calc_theta],
	['thetas', ['ps', 'tas'], calc_theta, ['p', 'ta']],
	['thetav', ['theta', 'w'], calc_tv, ['ta', 'w']],
	['thetavs', ['thetas', 'ws'], calc_tv, ['ta', 'w']],
	['ua', ['wds', 'wdd'], calc_ua],
	['uas', ['wdss', 'wdds'], calc_ua, ['wds', 'wdd']],
	['va', ['wds', 'wdd'], calc_va],
	['vas', ['wdss', 'wdds'], calc_va, ['wds', 'wdd']],
	['w', 'hus', calc_w],
	['w', ['hur', 'wsat'], calc_w],
	['w', ['p', 'e'], calc_w],
	['wdd', ['ua', 'va'], calc_wdd],
	['wdds', ['uas', 'vas'], calc_wdd, ['ua', 'va']],
	['wds', ['ua', 'va'], calc_wds],
	['wdss', ['uas', 'vas'], calc_wds, ['ua', 'va']],
	['ws', 'huss', calc_w, ['hus']],
	['ws', ['hurs', 'wsats'], calc_w, ['hur', 'wsat']],
	['ws', ['ps', 'es'], calc_w, ['p', 'e']],
	['wsat', ['p', 'esat'], calc_w, ['p', 'e']],
	['wsats', ['ps', 'esats'], calc_w, ['p', 'e']],
	['z', ['zg', 'g'], calc_z],
	['zg', ['z', 'g'], calc_zg],
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
	rm_station_lat = 'station_lat' not in d
	tmp_station_lat = 'station_lat' not in d or np.isnan(d['station_lat'])
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
	if rm_station_lat:
		del d['station_lat']
	elif tmp_station_lat:
		d['station_lat'] = np.nan
