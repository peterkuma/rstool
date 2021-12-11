HEADER_PTS = [
	('hur', 'relative humidity', 'relative_humidity', '%', ['seq']),
	('hurs', 'near-surface relative humidity', 'relative_humidity', '%', []),
	('lat', 'latitude', 'latitude', 'degrees_north', ['seq']),
	('lon', 'longitude', 'longitude', 'degrees_east', ['seq']),
	('p', 'pressure', 'air_pressure', 'Pa', ['seq']),
	('ps', 'surface air pressure', 'surface_air_pressure', 'Pa', []),
	('station_lat', 'station latitude', 'latitude', 'degrees_north', []),
	('station_lon', 'station longitude', 'longitude', 'degrees_east', []),
	('station_z', 'station altitude', 'height_above_reference_ellipsoid', 'm', []),
	('ta', 'air temperature', 'air_temperature', 'K', ['seq']),
	('tas', 'near-surface air temperature', 'air_temperature', 'K', []),
	('time', 'time', 'time', 'days since -4713-11-24 12:00 UTC', ['seq']),
	('uas', 'eastward near-surface wind', 'eastward_wind', 'm s-1', []),
	('vas', 'northward near-surface wind', 'northward_wind', 'm s-1', []),
	('z', 'altitude', 'height_above_reference_ellipsoid', 'm', ['seq']),
]
HEADER_PTS = {
	x[0]: {'.dims': x[4], 'long_name': x[1], 'standard_name': x[2], 'units': x[3]}
	for x in HEADER_PTS
}
HEADER_PTS['time']['calendar'] = 'proleptic_gregorian'

HEADER_PROF = [
	('bvf', 'brunt vaisala frequency in air', 'brunt_vaisala_frequency_in_air', 's-1', ['p2']),
	('e', 'water vapor pressure in air', 'water_vapor_partial_pressure_in_air', 'Pa', ['p']),
	('es', 'saturation vapor pressure', 'water_vapor_partial_pressure_in_air', 'Pa', ['p']),
	('hur', 'relative humidity', 'relative_humidity', '%', ['p']),
	('hurs', 'near-surface relative humidity', 'relative_humidity', '%', []),
	('lat', 'latitude', 'latitude', 'degrees_north', ['p']),
	('llp', 'atmosphere lifting level pressure', 'air_pressure', 'Pa', []),
	('lon', 'longitude', 'longitude', 'degrees_east', ['p']),
	('p', 'pressure', 'air_pressure', 'Pa', ['p']),
	('p2', 'pressure 2', 'air_pressure', 'Pa', ['p2']),
	('p_lcl', 'atmosphere lifting condensation level pressure', 'air_pressure', 'Pa', []),
	('ps', 'surface air pressure', 'surface_air_pressure', 'Pa', []),
	('station_lat', 'station latitude', 'latitude', 'degrees_north', []),
	('station_lon', 'station longitude', 'longitude', 'degrees_east', []),
	('station_z', 'station altitude', 'height_above_reference_ellipsoid', 'm', []),
	('ta', 'air temperature', 'air_temperature', 'K', ['p']),
	('ta_par', 'dry parcel temperature', 'air_temperature', 'K', ['p']),
	('ta_par_s', 'saturated parcel temperature', 'air_temperature', 'K', ['p']),
	('ta_surf_par', 'dry surface parcel temperature', 'air_temperature', 'K', ['p']),
	('ta_surf_par_s', 'saturated surface parcel temperature', 'air_temperature', 'K', ['p']),
	('tas', 'near-surface air temperature', 'air_pressure', 'K', []),
	('theta', 'air potential temperature', 'air_potential_temperature', 'K', ['p']),
	('time', 'time', 'time', 'days since -4713-11-24 12:00 UTC', ['p']),
	('ts', 'surface temperature', 'surface_temperature', 'K', []),
	('ua', 'eastward wind', 'eastward_wind', 'm s-1', ['p']),
	('uas', 'eastward near-surface wind', 'eastward_wind', 'm s-1', []),
	('va', 'northward wind', 'northward_wind', 'm s-1', ['p']),
	('vas', 'northward near-surface wind', 'northward_wind', 'm s-1', []),
	('wdd', 'wind from direction', 'wind_from_direction', 'degrees', ['p']),
	('wdds', 'near-surface wind from direction', 'wind_from_direction', 'degrees', ['p']),
	('wds', 'wind speed', 'wind_speed', 'm s-1', ['p']),
	('wdss', 'near-surface wind speed', 'wind_speed', 'm s-1', ['p']),
	('z', 'altitude', 'height_above_reference_ellipsoid', 'm', ['p']),
	('zg', 'geopotential height', 'geopotential_height', 'm', ['p']),
	('zg_lcl', 'lifting condensation level geopotential height', 'geopotential_height', 'm', []),
	#'ta_surf_par_x': {
	#	'.dims': ['p'],
	#	'long_name': 'dry_surface_parcel_temperature',
	#	'units': 'K',
	#},
	#'ta_surf_par_s_x': {
	#	'.dims': ['p'],
	#	'long_name': 'saturated_surface_parcel_temperature',
	#	'units': 'K',
	#},
	#'clp': {
	#	'.dims': [],
	#	'long_name': 'atmosphere_condensation_level_pressure',
	#	'units': 'Pa',
	#},
	#'cl': {
	#	'.dims': [],
	#	'long_name': 'atmosphere_condensation_level',
	#	'units': 'm',
	#},
	#'platform_altitude': {
	#	'.dims': [],
	#	'long_name': 'platform_altitude',
	#	'units': 'm',
	#},
	#'launch_lon': {
	#	'.dims': [],
	#	'long_name': 'launch_lon',
	#	'units': 'degrees_east',
	#},
	#'launch_lat': {
	#	'.dims': [],
	#	'long_name': 'launch_lat',
	#	'units': 'degrees_north',
	#},
	#'launch_time': {
	#	'.dims': [],
	#	'long_name': 'launch_time',
	#	'units': 'days since -4713-01-01 12:00 UTC',
	#},
]
HEADER_PROF = {
	x[0]: {'.dims': x[4], 'long_name': x[1], 'standard_name': x[2], 'units': x[3]}
	for x in HEADER_PROF
}
