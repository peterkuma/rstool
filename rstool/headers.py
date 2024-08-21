def header(x):
	out = {}
	for i, h in enumerate(['long_name', 'standard_name', 'units', '.dims']):
		if x[i+1] is not None:
			out[h] = x[i+1]
	if len(x) == 6:
		out.update(x[5])
	return out

HEADER_PTS = [
	('hur', 'relative humidity', 'relative_humidity', '%', ['seq']),
	('hurs', 'near-surface relative humidity', 'relative_humidity', '%', []),
	('lat', 'latitude', 'latitude', 'degree_north', ['seq']),
	('lon', 'longitude', 'longitude', 'degree_east', ['seq']),
	('p', 'air pressure', 'air_pressure', 'Pa', ['seq']),
	('ps', 'surface air pressure', 'surface_air_pressure', 'Pa', []),
	('station_lat', 'station latitude', 'latitude', 'degree_north', []),
	('station_lon', 'station longitude', 'longitude', 'degree_east', []),
	('station_z', 'station altitude', 'height_above_reference_ellipsoid', 'm',
		[]),
	('station_time', 'station time', 'time', 'days since -4713-11-24 12:00 UTC',
		[], {'calendar': 'proleptic_gregorian'}),
	('ta', 'air temperature', 'air_temperature', 'K', ['seq']),
	('time', 'time', 'time', 'days since -4713-11-24 12:00 UTC', ['seq'],
		{'calendar': 'proleptic_gregorian'}),
	('uas', 'eastward near-surface wind', 'eastward_wind', 'm s-1', []),
	('vas', 'northward near-surface wind', 'northward_wind', 'm s-1', []),
	('z', 'altitude', 'height_above_reference_ellipsoid', 'm', ['seq']),
]
HEADER_PTS = {x[0]: header(x) for x in HEADER_PTS}

HEADER_PROF = [
	('bvf', 'brunt vaisala frequency in air', 'brunt_vaisala_frequency_in_air',
		's-1', ['p_bvf']),
	('e', 'water vapor partial pressure in air',
		'water_vapor_partial_pressure_in_air', 'Pa', ['p']),
	('es', 'near-surface water vapor partial pressure in air',
		'water_vapor_partial_pressure_in_air', 'Pa', []),
	('esat', 'saturation water vapor partial pressure in air',
		'water_vapor_partial_pressure_in_air', 'Pa', ['p']),
	('esats', 'near-surface saturation water vapor partial pressure in air',
		'water_vapor_partial_pressure_in_air', 'Pa', []),
	('g', 'gravitational acceleration', None, 'm s-2', [],
		{'comment': 'at mean sea level, ignoring height dependence'}),
	('gamma', 'air temperature lapse rate', 'air_temperature_lapse_rate',
		'K m-1', [], {
			'comment': 'assuming dry adiabatic process',
			'units_metadata': 'temperature: difference'
		}),
	('gamma_sat', 'air temperature saturation lapse rate',
		'air_temperature_lapse_rate', 'K m-1', ['p'], {
			'comment': 'assuming moist adiabatic process',
			'units_metadata': 'temperature: difference'
		}),
	('hur', 'relative humidity', 'relative_humidity', '%', ['p']),
	('hurs', 'near-surface relative humidity', 'relative_humidity', '%', []),
	('hus', 'specific humidity', 'specific_humidity', '1', ['p']),
	('lat', 'latitude', 'latitude', 'degree_north', ['p']),
	('lon', 'longitude', 'longitude', 'degree_east', ['p']),
	('p', 'pressure', 'air_pressure', 'Pa', ['p']),
	('p_bvf', 'pressure of bvf', 'air_pressure', 'Pa', ['p_bvf']),
	('pc', 'condensation pressure', 'air_pressure', 'Pa', []),
	('ps', 'surface air pressure', 'surface_air_pressure', 'Pa', []),
	('rho', 'air density', 'air_density', 'Pa', ['p']),
	('rhod', 'dry air density', 'air_density', 'Pa', ['p']),
	('rhods', 'near-surface dry air density', 'air_density', 'Pa', []),
	('rhos', 'near-surface air density', 'air_density', 'Pa', []),
	('rhow', 'water vapor density', 'air_density', 'Pa', ['p']),
	('rhows', 'near-surface water vapor density', 'air_density', 'Pa', []),
	('station_lat', 'station latitude', 'latitude', 'degree_north', []),
	('station_lon', 'station longitude', 'longitude', 'degree_east', []),
	('station_time', 'station time', 'time', 'days since -4713-11-24 12:00 UTC',
		[], {'calendar': 'proleptic_gregorian'}),
	('station_z', 'station altitude', 'height_above_reference_ellipsoid', 'm',
		[]),
	('ta', 'air temperature', 'air_temperature', 'K', ['p']),
	('td', 'dew point temperature', 'dew_point_temperature', 'K', ['p']),
	('tds', 'near-surface dew point temperature', 'dew_point_temperature', 'K', []),
	('tv', 'virtual temperature', 'virtual_temperature', 'K', ['p']),
	('tvs', 'near-surface virtual temperature', 'virtual_temperature', 'K', []),
	('ta_par', 'dry adiabatic air parcel temperature', 'air_temperature', 'K', ['p']),
	('ta_par_sat', 'saturation air parcel temperature', 'air_temperature', 'K',
		['p']),
	('ta_surf_par', 'dry adiabatic surface air parcel temperature', 'air_temperature', 'K',
		['p']),
	('ta_surf_par_sat', 'saturation surface air parcel temperature',
		'air_temperature', 'K', ['p']),
	('tas', 'near-surface air temperature', 'air_temperature', 'K', []),
	('td', 'dew point temperature', 'dew_point_temperature', 'K', ['p']),
	('tds', 'near-surface dew point temperature', 'dew_point_temperature', 'K',
		[]),
	('theta', 'air potential temperature', 'air_potential_temperature', 'K',
		['p'], {'comment': 'assumed standard pressure 1000 hPa'}),
	('theta_v', 'virtual potential temperature', 'virtual_temperature', 'K',
		['p'], {'comment': 'assumed standard pressure 1000 hPa'}),
	('time', 'time', 'time', 'days since -4713-11-24 12:00 UTC', ['p'],
		{'calendar': 'proleptic_gregorian'}),
	('ts', 'surface temperature', 'surface_temperature', 'K', []),
	('ua', 'eastward wind', 'eastward_wind', 'm s-1', ['p']),
	('uas', 'eastward near-surface wind', 'eastward_wind', 'm s-1', []),
	('va', 'northward wind', 'northward_wind', 'm s-1', ['p']),
	('vas', 'northward near-surface wind', 'northward_wind', 'm s-1', []),
	('w', 'humidity mixing ratio', None, '1', ['p']),
	('wdd', 'wind from direction', 'wind_from_direction', 'degree', ['p']),
	('wdds', 'near-surface wind from direction', 'wind_from_direction',
		'degree', []),
	('wds', 'wind speed', 'wind_speed', 'm s-1', ['p']),
	('wdss', 'near-surface wind speed', 'wind_speed', 'm s-1', []),
	('ws', 'near-surface humidity mixing ratio', None, '1', []),
	('wsat', 'saturation humidity mixing ratio', None, '1', ['p']),
	('wsats', 'near-surface saturation humidity mixing ratio', None,
		'1', []),
	('z', 'altitude', 'height_above_reference_ellipsoid', 'm', ['p']),
	('zg', 'geopotential height', 'geopotential_height', 'm', ['p']),
	('zg_bvf', 'geopotential height of bvf', 'geopotential_height', 'm', ['p_bvf']),
	('lcl', 'lifting condensation level', 'geopotential_height', 'm', [], {
		'comment': 'calculated from the measured pressure and geopotential height profile'
	}),
]
HEADER_PROF = {x[0]: header(x) for x in HEADER_PROF}
