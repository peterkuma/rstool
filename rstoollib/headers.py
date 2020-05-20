HEADER_PROF = {
	'zg': {
		'.dims': ['p'],
		'long_name': 'geopotential_height',
		'units': 'm',
	},
	'z': {
		'.dims': ['p'],
		'long_name': 'height_above_reference_ellipsoid',
		'units': 'm',
	},
	'p': {
		'.dims': ['p'],
		'long_name': 'pressure',
		'units': 'Pa',
	},
	'p2': {
		'.dims': ['p2'],
		'long_name': 'pressure_2',
		'units': 'Pa',
	},
	'ta': {
		'.dims': ['p'],
		'long_name': 'air_temperature',
		'units': 'K',
	},
	'hur': {
		'.dims': ['p'],
		'long_name': 'relative_humidity',
		'units': '%',
	},
	'wds': {
		'.dims': ['p'],
		'long_name': 'wind_speed',
		'units': 'm s-1',
	},
	'wdd': {
		'.dims': ['p'],
		'long_name': 'wind_from_direction',
		'units': 'degrees',
	},
	'ua': {
		'.dims': ['p'],
		'long_name': 'x_wind',
		'units': 'm s-1',
	},
	'va': {
		'.dims': ['p'],
		'long_name': 'y_wind',
		'units': 'm s-1',
	},
	'theta': {
		'.dims': ['p'],
		'long_name': 'air_potential_temperature',
		'units': 'K',
	},
	'bvf': {
		'.dims': ['p2'],
		'long_name': 'brunt_vaisala_frequency_in_air',
		'units': 's-1',
	},
	'es': {
		'.dims': ['p'],
		'long_name': 'saturation_vapor_pressure',
		'units': 'Pa',
	},
	'e': {
		'.dims': ['p'],
		'long_name': 'water_vapor_pressure',
		'units': 'Pa',
	},
	'ta_par': {
		'.dims': ['p'],
		'long_name': 'dry_parcel_temperature',
		'units': 'K',
	},	
	'ta_par_s': {
		'.dims': ['p'],
		'long_name': 'saturated_parcel_temperature',
		'units': 'K',
	},
	'ta_surf_par': {
		'.dims': ['p'],
		'long_name': 'dry_surface_parcel_temperature',
		'units': 'K',
	},
	'ta_surf_par_s': {
		'.dims': ['p'],
		'long_name': 'saturated_surface_parcel_temperature',
		'units': 'K',
	},
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
	'p_lcl': {
		'.dims': [],
		'long_name': 'lifting_condensation_level_pressure',
		'units': 'Pa',
	},
	'ts': {
		'.dims': [],
		'long_name': 'surface_temperature',
		'units': 'K',
	},
	'llp': {
		'.dims': [],
		'long_name': 'atmosphere_lifting_level_pressure',
		'units': 'Pa',
	},
	'zg_lcl': {
		'.dims': [],
		'long_name': 'lifting_condensation_level_geopotential_height',
		'units': 'm',
	},
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
	'time': {
		'.dims': ['p'],
		'long_name': 'time',
		'units': 'days since -4712-01-01 12:00:00',
	},
	'lon': {
		'.dims': ['p'],
		'long_name': 'longitude',
		'units': 'degrees_east',
	},
	'lat': {
		'.dims': ['p'],
		'long_name': 'latitude',
		'units': 'degrees_north',
	},
	'tas': {
		'.dims': [],
		'long_name': 'air_temperature',
		'units': 'K',
	},
	'ps': {
		'.dims': [],
		'long_name': 'pressure',
		'units': 'Pa',
	},
	'hurs': {
		'.dims': [],
		'long_name': 'relative_humidity',
		'units': '%',
	},
	'wdss': {
		'.dims': [],
		'long_name': 'wind_speed',
		'units': 'm s-1',
	},
	'wdds': {
		'.dims': [],
		'long_name': 'wind_from_direction',
		'units': 'degrees',
	},
}

HEADER_PTS = {
	'p': {
		'.dims': ['seq'],
		'long_name': 'pressure',
		'units': 'Pa',
	},
	'lon': {
		'.dims': ['seq'],
		'long_name': 'longitude',
		'units': 'degrees_east',
	},
	'lat': {
		'.dims': ['seq'],
		'long_name': 'latitude',
		'units': 'degrees_north',
	},
	'e': {
		'.dims': ['seq'],
		'long_name': 'water_vapor_pressure',
		'units': 'Pa',
	},
	'ta': {
		'.dims': ['seq'],
		'long_name': 'air_temperature',
		'units': 'K',
	},
	'hur': {
		'.dims': ['seq'],
		'long_name': 'relative_humidity',
		'units': '%',
	},
	'wds': {
		'.dims': ['seq'],
		'long_name': 'wind_speed',
		'units': 'm s-1',
	},
	'wdd': {
		'.dims': ['seq'],
		'long_name': 'wind_from_direction',
		'units': 'degrees',
	},
	'ua': {
		'.dims': ['seq'],
		'long_name': 'x_wind',
		'units': 'm s-1',
	},
	'va': {
		'.dims': ['seq'],
		'long_name': 'y_wind',
		'units': 'm s-1',
	},
	'z': {
		'.dims': ['seq'],
		'long_name': 'height_above_reference_ellipsoid',
		'units': 'm',
	},
}
