import numpy as np
from scipy.optimize import fmin

from rstool.const import *

def calc_bvf(*, theta_v, zg, p, g, res=400):
	'''
	**calc_bvf**(\*, *theta_v*, *zg*, *p*, *g*, *res*=400)

	Calculate Brunt-Väisälä fequency from air temperature *ta* (K),
	geopotential height *zg* (m), air pressure *p* (Pa) and gravitational
	acceleration *g* (m.s-2). *res* is vertical resolution in geopotential
	height (m).
	'''
	zg_half = np.arange(np.nanmin(zg), np.nanmax(zg) + res, res)
	zg_full = (zg_half[1:] + zg_half[:-1])*0.5
	theta_v_half = np.interp(zg_half, zg, theta_v)
	theta_v_full = (theta_v_half[1:] + theta_v_half[:-1])*0.5
	phalf = np.interp(zg_half, zg, p)
	pfull = (phalf[1:] + phalf[:-1])*0.5
	bvf2 = g*np.diff(theta_v_half)/np.diff(zg_half)/theta_v_full
	bvf = np.sqrt(np.abs(bvf2))*np.sign(bvf2)
	return pfull, zg_full, bvf

def calc_e(*, p, w):
	'''
	**calc_e**(\*, *p*, *w*)

	Calculate water vapor partial pressure in air (Pa) from humidity
	mixing ratio *w* (1) and air pressure *p* (Pa).
	'''
	return w*p/(eps + w)

def calc_esat(*, ta):
	'''
	**calc_esat**(\*, *ta*)

	Calculate saturation water vapor partial pressure (Pa) from air
	temperature *ta* (K).
	'''
	return 6.112*np.exp((17.67*(ta - n0))/(ta - n0 + 243.5))*1e2

def calc_g(*, lat=45):
	'''
	**calc_g**(\*, *lat*=45)

	Calculate gravitational acceleration (m.s-2) from latitude *lat*
	(degree). Height dependence is ignored.
	'''
	return 9.780327*(
		1 +
		0.0053024*np.sin(lat/180*np.pi)**2 -
		0.0000058*np.sin(2*lat/180*np.pi)**2
	)

def calc_gamma(*, g):
	'''
	**calc_gamma**(\*, *g*)

	Calculate air temperature lapse rate (K.m-1) at gravitational
	acceleration *g* (m.s-2).
	'''
	return g/cp

def calc_gamma_sat(*, p, ta, gamma):
	'''
	**calc_gamma_sat**(\*, *p*, *ta*, *gamma*)

	Calculate saturation air temperature lapse rate (K.m-1) from pressure
	*p* (Pa), temperature *ta* (K) and air temperature lapse rate *gamma*
	(K.m-1).
	'''
	wsat = calc_wsat(p=p, ta=ta)
	return gamma*(1 + lv*wsat/(rd*ta))/(1 + lv**2*wsat*eps/(rd*cp*ta**2))

def calc_hur(*, w, wsat):
	'''
	**calc_hur**(\*, *w*, *wsat*)

	Calculate relative humidity (%) from humidity mixing ratio *w* (1) and
	saturation water vapor mixing ratio in air *wsat* (1).
	'''
	return 100*w/wsat

def calc_hus(*, w):
	'''
	**calc_hus**(\*, *w*)

	Calculate specific humidity (1) from humidity mixing ratio *w* (1).
	'''
	return w/(1 + w)

def calc_ta_par(*, p, ps, tas):
	'''
	**calc_ta_par**(\*, *p*, *ps*, *tas*)

	Calculate dry adiabatic air parcel temperature at air pressure *p* (Pa),
	assuming surface air pressure *ps* and near-surface air temperature *tas*
	(K).
	'''
	return tas*(p/ps)**kappa

def calc_ta_par_sat(*, p, tas, ws, g, gamma):
	'''
	**calc_ta_par_sat**(\*, *p*, *tas*, *ws*, *g*, *gamma*)

	Calculate saturation air parcel temperature at pressure *p* (Pa),
	assuming near-surface air temperature *tas* (K), near-surface humidity
	mixing ratio *ws* (1), gravitational acceleration *g* (m.s-2) and air
	temperature lapse rate *gamma* (K.m-1). *p* has to be an array dense enough
	for acurrate integration.
	'''
	n = len(p)
	ta_par_sat = np.full(n, np.nan, np.float64)
	ta_par_sat[0] = tas
	for i in range(1, n):
		wsat = calc_wsat(p=p[i-1], ta=ta_par_sat[i-1])
		if ws < wsat:
			gamma1 = gamma
		else:
			gamma1 = calc_gamma_sat(p=p[i], ta=ta_par_sat[i-1], gamma=gamma)
		dta_dp = rd*ta_par_sat[i-1]/(p[i]*g)*gamma1
		dp = p[i] - p[i-1]
		ta_par_sat[i] = ta_par_sat[i-1] + dta_dp*dp
	return ta_par_sat

def calc_tv(*, ta, w):
	'''
	**calc_tv**(\*, *ta*, *w*)

	Calculate virtual temperature (K) from air temperature *ta* (K) and
	humidity mixing ration *w* (1).
	'''
	return ta*(1 + w/eps)/(1 + w)

def calc_theta(*, p, ps, ta):
	'''
	**calc_theta**(\*, *p*, *ps*, *ta*)

	Calculate air potential temperature (K) from air pressure *p* (Pa),
	surface air pressure *ps* (Pa) and air temperature *ta* (K).
	'''
	return ta*(ps/p)**kappa

@np.vectorize
def calc_td(*, e):
	'''
	**calc_td**(\*, *e*, *hur*, *ta*)

	Calculate dew point temperature (K) from water vapor pressure *e* (Pa).
	'''
	def f(ta):
		esat = calc_esat(ta=ta)
		return np.abs(esat - e)
	return fmin(f, n0, disp=False)[0]

@np.vectorize
def calc_p_lcl(*, ps, ws, tas):
	'''
	**calc_p_lcl**(\*, *ps*, *ws*, *tas*)

	Calculate lifting condensation level pressure (Pa) from surface air
	pressure *ps* (Pa), near-surface humidity mixing ratio *ws* (Pa) and
	near-surface air temperature *tas* (K).
	'''
	def f(p):
		ta = calc_ta_par(p=p, ps=ps, tas=tas)
		wsat = calc_wsat(p=p, ta=ta)
		return np.abs(wsat - ws)
	return fmin(f, 1e5, disp=False)[0]

def calc_p_ll(*, ps, ts, p, theta):
	return min(ps, np.interp(ts, theta, p))

def calc_ua(*, wds, wdd):
	'''
	**calc_ua**(\*, *wds*, *wdd*)

	Calculate eastward wind (m.s-1) from wind speed *wds* (m.s-1) and wind
	direction *wdd* (degree).
	'''
	return -np.sin(wdd/180*np.pi)*wds

def calc_va(*, wds, wdd):
	'''
	**calc_va**(\*, *wds*, *wdd*)

	Calculate northward wind (m.s-1) from wind speed *wds* (m.s-1) and wind
	direction *wdd* (degree).
	'''
	return -np.cos(wdd/180*np.pi)*wds

def calc_w(*,
	p=None, e=None, # option 1
	hus=None, # option 2
	hur=None, wsat=None, # option 3
):
	'''
	**calc_w**(\*,\\
	    [option 1] *p*, *e*\\
	    [option 2] *hus*\\
	    [option 3] *hur*, *wsat*`\\
	)

	Calculate humidity mixing ratio from [option 1] pressure *p* (Pa) and
	water vapor partial pressure *e* (Pa), [option 2] specific humidity *hus*
	(1), or [option 3] relative humidity *hur* (%) and saturation humidity
	mixing ratio *wsat* (1).
	'''
	if p is not None and e is not None:
		return eps*e/(p - e)
	elif hus is not None:
		return hus/(1 - hus)
	elif hur is not None and wsat is not None:
		return hur/100*wsat
	else:
		raise TypeError('invalid arguments')

def calc_wdd(*, ua, va):
	'''
	**calc_wdd**(\*, *ua*, *va*)

	Calculate wind direction (degree) from eastward wind *ua* (m.s-1) and
	northward wind *va* (m.s-1).
	'''
	return np.arctan2(-ua, -va)/np.pi*180 % 360

def calc_wds(*, ua, va):
	'''
	**calc_wds**(\*, *ua*, *va*)

	Calculate wind speed (m.s-1) from eastward wind *ua* (m.s-1) and
	northward wind *va* (m.s-1).
	'''
	return np.sqrt(ua**2 + va**2)

def calc_wsat(*, p, ta):
	'''
	**calc_wsat**(\*, *p*, *ta*)

	Calculate saturation humidity mixing ratio (1) from air pressure *p*
	(Pa) and air temperature *ta* (K).
	'''
	esat = calc_esat(ta=ta)
	return calc_w(p=p, e=esat)

def calc_z(*,
	zg=None, g=None, # option 1
	p1=None, p=None, z=None, # option 2
):
	'''
	**calc_z**(\*,\\
	    [option 1] *zg*, *g*\\
	    [option 2] *p1*, *p*, *z*\\
	)

	Calculate altitude (m) from [option 1] geopotential height *zg* (m) and
	grativational acceleration *g* (m.s-2), [option 2] by interpolation from
	air pressure level *p1* (Pa), air pressure at all levels *p* (Pa) and
	altitude at all levels *z* (m).
	'''
	if zg is not None and g is not None:
		return zg/g*gsl
	elif p1 is not None and p is not None and z is not None:
		return np.interp(p1, p[::-1], z[::-1])
	else:
		raise TypeError('invalid arguments')

def calc_zg(*,
	z=None, g=None, # option 1
	p1=None, p=None, zg=None, # option 2
):
	'''
	**calc_zg**(\*,\\
	    [option 1] *z*, *g*`\\
	    [option 2] *p1*, *p*, *zg*\\
	)

	Calculate geopotential height (m) from [option 1] altitude *z* (m) and
	gravitational acceleration *g* (m.s-2), [option 2] by interpolation from
	air pressure level *p1* (Pa), air pressure at all levels *p* (Pa) and
	geopotential height at all levels *zg* (m).
	'''
	if z is not None and g is not None:
		return z*g/gsl
	elif p1 is not None and p is not None and zg is not None:
		return np.interp(p1, p[::-1], zg[::-1])
	else:
		raise TypeError('invalid arguments')
