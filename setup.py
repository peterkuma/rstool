#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='rstool',
	version='1.0.0',
	py_modules=['rstool'],
	entry_points={
		'console_scripts': ['rstool=rstool:main'],
	},
	packages=find_packages(),
	description='Command-line program for converting native radiosonde data to NetCDF and calculation of derived quantities, supporting InterMet Systems (iMet) and Windsond radiosondes',
	author='Peter Kuma',
	author_email='peter@peterkuma.net',
	url='https://github.com/peterkuma/rstool',
	platforms='any',
	keywords=['radiosonde', 'netcdf', 'atmospheric-science'],
	install_requires=[
		'numpy',
		'scipy',
		'pyproj',
		'ds-format>=1.1.1',
		'aquarius-time>=0.1.0',
		'cftime>=1.5.1',
	],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Atmospheric Science',
		'Topic :: Scientific/Engineering :: Physics',
	],
)
