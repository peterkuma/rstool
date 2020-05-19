from setuptools import setup, find_packages

setup(
    name='rstool',
    version='0.1.0',
    packages=find_packages(),
    scripts=['bin/rstool'],
    author='Peter Kuma',
    author_email='peter@peterkuma.net',
    classifiers=[
        'Development Status :: 4 - Beta',
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
