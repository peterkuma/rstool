import numpy as np
import scipy.constants
from rstoollib.const import *
from scipy.optimize import fmin
from scipy.integrate import quad

def calc_g(lat=45.):
	"""Calculate gravity from latitude (degrees)."""
	return 9.780327*(
		1 +
		0.0053024*np.sin(lat/180.0*np.pi)**2 -
		0.0000058*np.sin(2*lat/180.0*np.pi)**2
	)

def calc_zg(z, lat):
	return z*calc_g(lat)/g0

def calc_z(zg, lat):
	return zg/calc_g(lat)*g0

def calc_ua(wds, wdd):
	"""Calculate zonal wind speed (m.s-1) from wind speed wds (m.s-1) and
	wind direction wdd (degrees)."""
	return np.sin(wdd/180.*np.pi)*wds

def calc_va(wds, wdd):
	"""Calculate meridional wind speed (m.s-1) from wind speed wds (m.s-1)
	and wind direction wdd (degrees)."""
	return np.cos(wdd/180.*np.pi)*wds

def calc_wds(ua, va):
	""" Calculate wind speed (m.s-1) from meridional wind speed ua (m.s-1)
	and zoal wind speed va (m.s-1)."""
	return np.sqrt(ua**2. + va**2.)

def calc_wdd(ua, va):
	""" Calculate wind direction (degrees) from meridional wind speed ua
	(m.s-1) and zoal wind speed va (m.s-1)."""
	x = np.arctan2(-ua, -va)/np.pi*180.
	return np.where(x >= 0., x, 360. + x)

def calc_theta(p, ta):
	"""Calculate potential temperature (K) from pressure p (Pa) and air
	temperature ta (K)."""
	p0 = p[0]
	return ta*((p0/p)**(1.0*R_d/c_p))

def calc_bvf(ta, zg, p):
	"""Calculate Bunt-Vaisala fequency from air temperature ta (K),
	geopotential height zg (m) and pressure p (Pa)."""
	zgx = np.arange(0, 20000, 400)
	tax = np.interp(zgx, zg, ta)
	px = np.interp(zgx, zg, p)
	bvf2 = 1.*scipy.constants.g*np.diff(tax)/np.diff(zgx)/((tax[1:] + tax[:-1])/2. + 273.15)
	bvf = np.sqrt(np.abs(bvf2))*np.sign(bvf2)
	return (px[1:] + px[:-1])/2.0, bvf

def calc_es(ta):
	"""Calculate saturated vapor pressure (Pa) from air temperature ta
	(K)."""
	return 6.112*np.exp((17.67*(ta - 273.15))/(ta - 273.15 + 243.5))*1e2

def calc_ws(p, ta):
	"""Calculate saturated water vapour mixing ratio (1) from pressure p
	(Pa) and air temperature ta (K)."""
	return calc_w(p, calc_es(ta))

def calc_gamma_s(p, ta, lat=45.):
	"""Calculate saturated adiabatic lapse rate from pressure p (Pa),
	temperature ta (K), at latitude lat (degrees)."""
	gamma_d = calc_gamma_d(lat)
	ws = calc_ws(p, ta)
	return gamma_d*(1. + l_v*ws/(R_d*ta))/(1. + l_v**2.*ws/(R_d*c_p*ta**2.))

def calc_gamma_d(lat=45.):
	"""Calculate dry adiabatic lapse rate at latitude lat (degrees)."""
	g = calc_g(lat)
	return -(g/c_p)

def calc_ta_par(p, ta0):
	"""Calculate dry parcel temperature at pressures p (Pa), assuming
	surface air temperature ta0 (K).
	"""
	p0 = p[0]
	return ta0*(p/p0)**(R_d/c_p)

def calc_ta_par_s(p, ta0, e0):
	"""Calculate saturated parcel temperature at pressures p (Pa), assuming
	surface air temperature ta0 (K) and surface water vapor pressure e0
	(Pa). p has to be an array dense enough for an acurrate integration."""
	g = calc_g()
	p0 = p[0]
	n = len(p)
	ta_s = np.full(n, np.nan, np.float64)
	ta_s[0] = ta0
	gamma_d = calc_gamma_d()
	w0 = calc_w(p0, e0)
	for i in range(1, n):
		es = calc_es(ta_s[i-1])
		ws = calc_w(p[i-1], es)
		if w0 < ws:
			gamma = gamma_d
		else:
			gamma = calc_gamma_s(p[i], ta_s[i-1])
		dta_dp = -R_d*ta_s[i-1]/(p[i]*g)*gamma
		dp = p[i] - p[i-1]
		ta_s[i] = ta_s[i-1] + dta_dp*dp
	return ta_s

def calc_w(p, e):
	"""Calculate water vapor mixing ratio (1) from pressure p (Pa) and water
	vapor pressure e (Pa)."""
	return epsilon*e/(p - e)

def calc_w_from_q(q):
	"""Calculate water vapor mixing ratio (1) from specific humidity q
	(1)."""
	return q/(1. - q)

def calc_e(w, p):
	"""Calculate specific humidity (1) from water vapor mixing ratio w (1)
	and pressure p (Pa)."""
	return w*p/(epsilon + w)

@np.vectorize
def calc_td(e):
	"""Calculate dew point (K) from water vapor pressure e (Pa)."""
	def f(ta):
		es = calc_es(ta)
		return np.abs(es - e)
	return fmin(f, 273.15, disp=False)[0]

def calc_lclp(p0, e0, ta0):
	"""Calculate lifting condensation level (LCL) pressure (Pa) from surface
	pressure p0 (Pa), surface water vapor mixing ratio e0 (Pa) and surface
	air temperature ta0 (K)."""
	w0 = calc_w(p0, e0)
	def f(p):
		ta = ta0*((p/p0)**(1.0*R_d/c_p))
		es = calc_es(ta)
		w = calc_w(p, es)
		return np.abs(w - w0)
	return fmin(f, 1000e2, disp=False)[0]

def calc_clp(p, e, ta):
	w0 = calc_w(p[0], e[0])
	es = calc_es(ta)
	ws = calc_w(p, es)
	def f(p1):
		ws1 = np.interp(p1, p[::-1], ws[::-1])
		return np.abs(ws1 - w0)
	return fmin(f, p[0], disp=False)[0]

def calc_llp(ts, p, theta):
	p0 = p[0]
	p1 = min(p0, np.interp(ts, theta, p))
	return p1
