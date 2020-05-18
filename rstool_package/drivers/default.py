import ds_format as ds

def read(filename):
	return ds.from_netcdf(filename)
