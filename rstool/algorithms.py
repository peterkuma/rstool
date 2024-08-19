import numpy as np
import scipy.constants
from rstool.const import *
from scipy.optimize import fmin
from scipy.integrate import quad

def calc_g(lat=45.):
	"""Calculate gravitational acceleration (m.s-2) from latitude lat
	(degree)."""
	return 9.780327*(
		1 +
		0.0053024*np.sin(lat/180.0*np.pi)**2 -
		0.0000058*np.sin(2*lat/180.0*np.pi)**2
	)

def calc_zg(z, lat):
	"""Calculate geopotential height (m) from height z (m) and latitude lat
	(degree)."""
	return z*calc_g(lat)/gsl

def calc_z(zg, lat):
	"""Calculate height (m) from geopotential height zg (m) and latitude lat
	(degree)."""
	return zg/calc_g(lat)*gsl

def calc_ua(wds, wdd):
	"""Calculate zonal wind speed (m.s-1) from wind speed wds (m.s-1) and
	wind direction wdd (degree)."""
	return np.sin(wdd/180.*np.pi)*wds

def calc_va(wds, wdd):
	"""Calculate meridional wind speed (m.s-1) from wind speed wds (m.s-1)
	and wind direction wdd (degree)."""
	return np.cos(wdd/180.*np.pi)*wds

def calc_wds(ua, va):
	""" Calculate wind speed (m.s-1) from meridional wind speed ua (m.s-1)
	and zoal wind speed va (m.s-1)."""
	return np.sqrt(ua**2. + va**2.)

def calc_wdd(ua, va):
	""" Calculate wind direction (degree) from meridional wind speed ua
	(m.s-1) and zoal wind speed va (m.s-1)."""
	x = np.arctan2(-ua, -va)/np.pi*180.
	return np.where(x >= 0., x, 360. + x)

def calc_theta(p, ta):
	"""Calculate potential temperature (K) from pressure p (Pa) and air
	temperature ta (K)."""
	ps = p[0]
	return ta*((ps/p)**(1.0*rd/cp))

def calc_theta_v(theta, w):
	return theta*(1 + w/eps)/(1 + w)

def calc_bvf(ta, zg, p, lat):
	"""Calculate Bunt-Vaisala fequency from air temperature ta (K),
	geopotential height zg (m) and pressure p (Pa)."""
	g = calc_g(lat)
	zgx = np.arange(0, 20000, 400)
	tax = np.interp(zgx, zg, ta)
	px = np.interp(zgx, zg, p)
	gx = np.interp(zgx, zg, g)
	bvf2 = (gx[1:] + gx[:-1])*0.5*np.diff(tax)/np.diff(zgx)/((tax[1:] + tax[:-1])*0.5 + 273.15)
	bvf = np.sqrt(np.abs(bvf2))*np.sign(bvf2)
	return (px[1:] + px[:-1])/2.0, bvf

def calc_esat(ta):
	"""Calculate saturated vapor pressure (Pa) from air temperature ta
	(K)."""
	return 6.112*np.exp((17.67*(ta - 273.15))/(ta - 273.15 + 243.5))*1e2

def calc_wsat(p, ta):
	"""Calculate saturated water vapour mixing ratio (1) from pressure p
	(Pa) and air temperature ta (K)."""
	return calc_w(p, calc_esat(ta))

def calc_gamma_s(p, ta, lat=45.):
	"""Calculate saturated adiabatic lapse rate from pressure p (Pa),
	temperature ta (K), at latitude lat (degree)."""
	gamma_d = calc_gamma_d(lat)
	wsat = calc_wsat(p, ta)
	return gamma_d*(1. + lv*wsat/(rd*ta))/(1. + lv**2.*wsat/(rd*cp*ta**2.))

def calc_gamma_d(lat=45.):
	"""Calculate dry adiabatic lapse rate at latitude lat (degree)."""
	g = calc_g(lat)
	return -(g/cp)

def calc_ta_par(p, tas):
	"""Calculate dry parcel temperature at pressures p (Pa), assuming
	near-surface air temperature tas (K).
	"""
	ps = p[0]
	return tas*(p/ps)**(rd/cp)

def calc_ta_par_s(p, tas, es):
	"""Calculate saturated parcel temperature at pressures p (Pa), assuming
	near-surface air temperature tas (K) and near-surface water vapor pressure
	es (Pa). p has to be an array dense enough for an acurrate integration."""
	g = calc_g()
	ps = p[0]
	n = len(p)
	ta_s = np.full(n, np.nan, np.float64)
	ta_s[0] = tas
	gamma_d = calc_gamma_d()
	w0 = calc_w(ps, es)
	for i in range(1, n):
		esat = calc_esat(ta_s[i-1])
		wsat = calc_w(p[i-1], esat)
		if ws < wsat:
			gamma = gamma_d
		else:
			gamma = calc_gamma_s(p[i], ta_s[i-1])
		dta_dp = -rd*ta_s[i-1]/(p[i]*g)*gamma
		dp = p[i] - p[i-1]
		ta_s[i] = ta_s[i-1] + dta_dp*dp
	return ta_s

def calc_w(p, e):
	"""Calculate water vapor mixing ratio (1) from pressure p (Pa) and water
	vapor pressure e (Pa)."""
	return eps*e/(p - e)

def calc_w_from_q(q):
	"""Calculate water vapor mixing ratio (1) from specific humidity q
	(1)."""
	return q/(1. - q)

def calc_e(w, p):
	"""Calculate vapor pressure (Pa) from water vapor mixing ratio w (1)
	and pressure p (Pa)."""
	return w*p/(eps + w)

@np.vectorize
def calc_td(e):
	"""Calculate dew point (K) from water vapor pressure e (Pa)."""
	def f(ta):
		esat = calc_esat(ta)
		return np.abs(esat - e)
	return fmin(f, 273.15, disp=False)[0]

def calc_p_lcl(ps, es, tas):
	"""Calculate lifting condensation level (LCL) pressure (Pa) from surface
	air pressure ps (Pa), near-surface water vapor mixing ratio es (Pa) and
	near-surface air temperature tas (K)."""
	ws = calc_w(ps, es)
	def f(p):
		ta = tas*((p/ps)**(rd/cp))
		esat = calc_esat(ta)
		w = calc_w(p, esat)
		return np.abs(w - ws)
	return fmin(f, 1000e2, disp=False)[0]

def calc_clp(p, e, ta):
	ws = calc_w(p[0], e[0])
	esat = calc_esat(ta)
	wsat = calc_w(p, esat)
	def f(p1):
		wsat1 = np.interp(p1, p[::-1], wsat[::-1])
		return np.abs(wsat1 - ws)
	return fmin(f, p[0], disp=False)[0]

def calc_p_ll(ts, p, theta):
	return min(p[0], np.interp(ts, theta, p))
