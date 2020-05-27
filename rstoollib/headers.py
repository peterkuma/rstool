HEADER_PTS = [
	('hur', 'relative_humidity', '%', ['seq']),
	('hurs', 'near_surface_relative_humidity', '%', []),
	('lat', 'latitude', 'degrees_north', ['seq']),
	('lon', 'longitude', 'degrees_east', ['seq']),
	('p', 'pressure', 'Pa', ['seq']),
	('ps', 'surface_air_pressure', 'Pa', []),
	('station_lat', 'station latitude', 'degrees_north', []),
	('station_lon', 'station longitude', 'degrees_east', []),
	('station_z', 'station altitude', 'm', []),
	('ta', 'air_temperature', 'K', ['seq']),
	('tas', 'near_surface_air_temperature', 'K', []),
	('time', 'time', 'days since -4712-01-01 12:00:00', ['seq']),
	('uas', 'eastward_near-surface_wind_speed', 'm s-1', []),
	('vas', 'northward_near-surface_wind_speed', 'm s-1', []),
	('z', 'height_above_reference_ellipsoid', 'm', ['seq']),
]
HEADER_PTS = {
	x[0]: {'.dims': x[3], 'long_name': x[1], 'units': x[2]}
	for x in HEADER_PTS
}

HEADER_PROF = [
	('bvf', 'brunt_vaisala_frequency_in_air', 's-1', ['p2']),
	('e', 'water_vapor_pressure', 'Pa', ['p']),
	('es', 'saturation_vapor_pressure', 'Pa', ['p']),
	('hur', 'relative_humidity', '%', ['p']),
	('hurs', 'near_surface_relative_humidity', '%', []),
	('lat', 'latitude', 'degrees_north', ['p']),
	('llp', 'atmosphere_lifting_level_pressure', 'Pa', []),
	('lon', 'longitude', 'degrees_east', ['p']),
	('p', 'pressure', 'Pa', ['p']),
	('p2', 'pressure_2', 'Pa', ['p2']),
	('p_lcl', 'lifting_condensation_level_pressure', 'Pa', []),
	('ps', 'surface_air_pressure', 'Pa', []),
	('station_lat', 'station latitude', 'degrees_north', []),
	('station_lon', 'station longitude', 'degrees_east', []),
	('station_z', 'station altitude', 'm', []),
	('ta', 'air_temperature', 'K', ['p']),
	('ta_par', 'dry_parcel_temperature', 'K', ['p']),
	('ta_par_s', 'saturated_parcel_temperature', 'K', ['p']),
	('ta_surf_par', 'dry_surface_parcel_temperature', 'K', ['p']),
	('ta_surf_par_s', 'saturated_surface_parcel_temperature', 'K', ['p']),
	('tas', 'near_surface_air_temperature', 'K', []),
	('theta', 'air_potential_temperature', 'K', ['p']),
	('time', 'time', 'days since -4712-01-01 12:00:00', ['p']),
	('ts', 'surface_temperature', 'K', []),
	('ua', 'eastward_wind', 'm s-1', ['p']),
	('uas', 'eastward_near-surface_wind_speed', 'm s-1', []),
	('va', 'northward_wind', 'm s-1', ['p']),
	('vas', 'northward_near-surface_wind_speed', 'm s-1', []),
	('wdd', 'wind_from_direction', 'degrees', ['p']),
	('wdds', 'near_surface_wind_from_direction', 'degrees', ['p']),
	('wds', 'wind_speed', 'm s-1', ['p']),
	('wdss', 'near_surface_wind_speed', 'm s-1', ['p']),
	('z', 'height_above_reference_ellipsoid', 'm', ['p']),
	('zg', 'geopotential_height', 'm', ['p']),
	('zg_lcl', 'lifting_condensation_level_geopotential_height', 'm', []),
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
	#	'units': 'days since -4712-01-01 12:00:00',
	#},
]
HEADER_PROF = {
	x[0]: {'.dims': x[3], 'long_name': x[1], 'units': x[2]}
	for x in HEADER_PROF
}
