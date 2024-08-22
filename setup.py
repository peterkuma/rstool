#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='rstool',
	version='2.0.0',
	py_modules=['rstool'],
	entry_points={
		'console_scripts': ['rstool=rstool.main:main'],
	},
	packages=find_packages(),
	description='Command-line program for converting radiosonde measurement data to NetCDF and calculation of derived physical quantities, supporting InterMet Systems (iMet) and Windsond radiosondes, as well as calculating derived quantities from model profiles.',
	author='Peter Kuma',
	author_email='peter@peterkuma.net',
	url='https://github.com/peterkuma/rstool',
	platforms='any',
	keywords=[
		'atmospheric-science'
		'climate',
		'climate-model',
		'climate-science',
		'imet',
		'intermet',
		'netcdf',
		'nwp',
		'radiosonde',
		'weather',
		'weather-model',
		'weather-balloon',
		'windsond',
	],
	install_requires=[
		'numpy',
		'scipy',
		'pyproj',
		'ds-format>=4.1.0',
		'aquarius-time>=0.3.0',
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
