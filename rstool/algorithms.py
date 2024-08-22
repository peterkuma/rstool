import numpy as np
from scipy.optimize import fmin

from rstool.const import *

def calc_bvf(*, thetav, zg, p, g, res=400):
	'''
	**calc_bvf**(\*, *thetav*, *zg*, *p*, *g*, *res*=400)

	Calculate Brunt-Väisälä frequency from air temperature *ta* (K),
	geopotential height *zg* (m), air pressure *p* (Pa) and gravitational
	acceleration *g* (m.s<sup>-2</sup>). *res* is vertical resolution in
	geopotential height (m).
	'''
	zg_half = np.arange(np.nanmin(zg), np.nanmax(zg) + res, res)
	zg_full = (zg_half[1:] + zg_half[:-1])*0.5
	thetav_half = np.interp(zg_half, zg, thetav)
	thetav_full = (thetav_half[1:] + thetav_half[:-1])*0.5
	phalf = np.interp(zg_half, zg, p)
	pfull = (phalf[1:] + phalf[:-1])*0.5
	bvf2 = g*np.diff(thetav_half)/np.diff(zg_half)/thetav_full
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

	Calculate gravitational acceleration (m.s<sup>-2</sup>) from latitude *lat*
	(degree). Height dependence is ignored.
	'''
	return 9.780327*(
		1 +
		0.0053024*np.sin(lat/180*np.pi)**2 -
		0.0000058*np.sin(2*lat/180*np.pi)**2
	)

def calc_gammad(*, g):
	'''
	**calc_gammad**(\*, *g*)

	Calculate dry adiabatic air temperature lapse rate (K.m<sup>-1</sup>) at
	gravitational acceleration *g* (m.s<sup>-2</sup>).
	'''
	return g/cp

def calc_gammam(*, p, ta, gammad):
	'''
	**calc_gammam**(\*, *p*, *ta*, *gamma*)

	Calculate moist adiabatic air temperature lapse rate (K.m<sup>-1</sup>)
	from pressure *p* (Pa), temperature *ta* (K) and dry adiabatic air
	temperature lapse rate *gammad* (K.m<sup>-1</sup>).
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

def calc_lts(*, p, theta, thetas):
	'''
	**calc_lts**(\*, *p*, *theta*, *thetas*):

	Calculate lower tropospheric stability (K) from air pressure *p* (Pa), air
	potential temperature *theta* (K) and near-surface air potential
	temperature *thetas* (K).
	'''
	theta700 = np.interp(700e2, p[::-1], theta[::-1])
	return theta700 - thetas

def calc_rho(*, rhod, rhow):
	'''
	**calc_rho**(\*, *rhod*, *rhow*)

	Calculate density of air (kg.m<sup>-3</sup>) from density of dry air
	*rho_d* (kg.m<sup>-3</sup>) and density of water vapor *rho_w*
	(kg.m<sup>-3</sup>).
	'''
	return rhod + rhow

def calc_rhod(*, p, e, ta):
	'''
	**calc_rho_d**(\*, *p*, *e*, *ta*)

	Calculate density of dry air (kg.m<sup>-3</sup>) from air pressure *p*,
	water vapor partial pressure *e* (Pa), and air temperature *ta* (K).
	'''
	return (p - e)/rd/ta

def calc_rhow(*, p, e, ta):
	'''
	**calc_rhow**(\*, *p*, *e*, *ta*)

	Calculate density of water vapor (kg.m<sup>-3</sup>) from air pressure *p*,
	water vapor partial pressure *e* (Pa), and air temperature *ta* (K).
	'''
	return e/rw/ta

def calc_ta_par(*, p, ps, tas):
	'''
	**calc_ta_par**(\*, *p*, *ps*, *tas*)

	Calculate dry adiabatic air parcel temperature at air pressure *p* (Pa),
	assuming surface air pressure *ps* and near-surface air temperature *tas*
	(K).
	'''
	return tas*(p/ps)**kappa

def calc_ta_par_sat(*, p, tas, ws, g, gammad):
	'''
	**calc_ta_par_sat**(\*, *p*, *tas*, *ws*, *g*, *gammad*)

	Calculate saturation air parcel temperature at pressure *p* (Pa), assuming
	near-surface air temperature *tas* (K), near-surface humidity mixing ratio
	*ws* (1), gravitational acceleration *g* (m.s<sup>-2</sup>) and dry
	adiabatic air temperature lapse rate *gammad* (K.m<sup>-1</sup>). *p* has
	to be an array dense enough for accurate integration.
	'''
	n = len(p)
	ta_par_sat = np.full(n, np.nan, np.float64)
	ta_par_sat[0] = tas
	for i in range(1, n):
		wsat = calc_wsat(p=p[i-1], ta=ta_par_sat[i-1])
		if ws < wsat:
			gamma = gammad
		else:
			gamma = calc_gammam(p=p[i], ta=ta_par_sat[i-1], gammad=gammad)
		dta_dp = rd*ta_par_sat[i-1]/(p[i]*g)*gamma
		dp = p[i] - p[i-1]
		ta_par_sat[i] = ta_par_sat[i-1] + dta_dp*dp
	return ta_par_sat

def calc_tv(*, ta, w):
	'''
	**calc_tv**(\*, *ta*, *w*)

	Calculate virtual temperature (K) from air temperature *ta* (K) and
	humidity mixing ratio *w* (1).
	'''
	return ta*(1 + w/eps)/(1 + w)

def calc_theta(*, p, ta, p0=1e5):
	'''
	**calc_theta**(\*, *p*, *ps*, *ta*, *p0*=1e5)

	Calculate air potential temperature (K) from air pressure *p* (Pa), surface
	air pressure *ps* (Pa) and air temperature *ta* (K). Assume standard
	pressure *p0*.
	'''
	return ta*(p0/p)**kappa

@np.vectorize
def calc_td(*, e):
	'''
	**calc_td**(\*, *e*)

	Calculate dew point temperature (K) from water vapor pressure *e* (Pa).
	'''
	def f(ta):
		esat = calc_esat(ta=ta)
		return np.abs(esat - e)
	if np.isfinite(e):
		return fmin(f, n0, disp=False)[0]
	else:
		return np.nan

@np.vectorize
def calc_pc(*, ps, ws, tas):
	'''
	**calc_pc**(\*, *ps*, *ws*, *tas*)

	Calculate condensation pressure (Pa) from surface air pressure *ps* (Pa),
	near-surface humidity mixing ratio *ws* (Pa) and near-surface air
	temperature *tas* (K).
	'''
	def f(p):
		ta = calc_ta_par(p=p, ps=ps, tas=tas)
		wsat = calc_wsat(p=p, ta=ta)
		return np.abs(wsat - ws)
	if np.isfinite(ps) and np.isfinite(ws) and np.isfinite(tas):
		return fmin(f, 1e5, disp=False)[0]
	else:
		return np.nan

def calc_ua(*, wds, wdd):
	'''
	**calc_ua**(\*, *wds*, *wdd*)

	Calculate eastward wind (m.s<sup>-1</sup>) from wind speed *wds*
	(m.s<sup>-1</sup>) and wind direction *wdd* (degree).
	'''
	return -np.sin(wdd/180*np.pi)*wds

def calc_va(*, wds, wdd):
	'''
	**calc_va**(\*, *wds*, *wdd*)

	Calculate northward wind (m.s<sup>-1</sup>) from wind speed *wds*
	(m.s<sup>-1</sup>) and wind direction *wdd* (degree).
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
	    [option 3] *hur*, *wsat*\\
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

	Calculate wind direction (degree) from eastward wind *ua*
	(m.s<sup>-1</sup>) and northward wind *va* (m.s<sup>-1</sup>).
	'''
	return np.arctan2(-ua, -va)/np.pi*180 % 360

def calc_wds(*, ua, va):
	'''
	**calc_wds**(\*, *ua*, *va*)

	Calculate wind speed (m.s<sup>-1</sup>) from eastward wind *ua*
	(m.s<sup>-1</sup>) and northward wind *va* (m.s<sup>-1</sup>).
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
	gravitational acceleration *g* (m.s<sup>-2</sup>), [option 2] by
	interpolation from air pressure level *p1* (Pa), air pressure at all levels
	*p* (Pa) and altitude at all levels *z* (m).
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
	    [option 1] *z*, *g*\\
	    [option 2] *p1*, *p*, *zg*\\
	)

	Calculate geopotential height (m) from [option 1] altitude *z* (m) and
	gravitational acceleration *g* (m.s<sup>-2</sup>), [option 2] by
	interpolation from air pressure level *p1* (Pa), air pressure at all levels
	*p* (Pa) and geopotential height at all levels *zg* (m).
	'''
	if z is not None and g is not None:
		return z*g/gsl
	elif p1 is not None and p is not None and zg is not None:
		return np.interp(p1, p[::-1], zg[::-1])
	else:
		raise TypeError('invalid arguments')
