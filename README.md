rstool
======

**Development status:** beta

rstool is an open source command-line program for reading and converting
native radiosonde data to NetCDF and calculation of derived physical quantities.

Supported instruments:

- [InterMet Systems](https://www.intermetsystems.com) (iMet) radiosondes such as
    iMet-1-ABxn, data files produced by the iMetOS-II software (`.dat`).
- [Windsond](http://windsond.com/), data files produced by the Windsond software
  (`.sounding`).

Support for other instruments can be added by writing a Python module
in `rstoollib/drivers`
to read the data files produced by the radiosonde (see the template
in `rstoollib/drivers/template.py`).

Usage
-----

```sh
rstool <input_type> <output_type> <input> <output>
```

Arguments:

- `input_type` - See Input types below.
- `output_type` - See Output types below.
- `input` - Input file or directory.
- `output` - Output file (NetCDF).

Input types:

- `imet` - InterMet Systems iMet-1-ABxn. `input` should be the 
    directory generated by the iMetOS-II software.
- `ws` - Windsond. `input` should be the `.sounding` file generated by the
    Windsond software.
- `raw:<instrument>` - "Raw" instrument-dependent format (NetCDF). `instrument`
    is one of `imet`, `ws`.
- `pts` - Collection of measurement points (NetCDF). The output of running
    rstool with the output type `pts`.

Output types:

- `raw` - "Raw" instrument-dependent format (NetCDF).
- `pts` - Collection of measurement points (NetCDF).
- `prof` - Vertical profile calculated by interpolating the measurement points
    during the ascent of the radiosonde as a function of height (NetCDF).
- `prof:desc` - The same as `prof`, but for the descent.

The following input/output type combinations are supported:

- `<instrument> raw`
- `<instrument> pts`
- `<instrument> prof`
- `<instrument> prof:desc`
- `raw:<instrument> pts`
- `raw:<instrument> prof`
- `pts prof`
- `raw prof:desc`
- `pts prof:desc`

where `instrument` is one of: `imet`, `ws`.

Installation
------------

Recommended operating system to run rstool is Linux with Python 3.
Install with:

```sh
pip3 install numpy pyproj
    https://github.com/peterkuma/ds-python/archive/master.zip \
    https://github.com/peterkuma/aquarius-time/archive/master.zip
python3 setup.py install
```

or

```sh
pip3 install --user numpy pyproj \
    https://github.com/peterkuma/ds-python/archive/master.zip \
    https://github.com/peterkuma/aquarius-time/archive/master.zip
python3 setup.py install --user
```

to install in user's home directory (make sure the directory `~/.local/bin`
is in the environmental variable `PATH`). Run with:

`rstool`

on the command line.

## Format description

Below is a description of the output NetCDF formats. Whenever possible,
CF Conventions and CMIP5 standard names are loosely followed by "duck typing".
Time is expressed as Julian days
(fractional number of days since -4712-01-01T12:00:00 UTC).

The formats can be converted in the order raw (raw:\<instrument\>) → points
(pts) → profile (prof).

### Points (pts)

pts is an instrument-independent format containing a sequence of radiosonde
measurements
as received by the base station ordered by time, converted to a standard set
of variables.

| Variable | Description | Units | Type |
| --- | --- | --- | --- |
| hur | relative humidity | % | float64 |
| lat | latitude | degrees North | float64 |
| lon | longitude | degrees East | float64 |
| ta | air temperature | K | float64 |
| p | pressure | Pa | float64 |
| time | time | days since -4712-01-01T12:00:00 UTC | float64 |
| z | height above reference ellipsoid | m | float64 |

### Profile (prof)

prof is an instrument-independent format containing standard variables
interpolated as a function of height.

| Variable | Description | Units | Type |
| --- | --- | --- | --- |
| bvf | Brunt–Väisälä frequency in air | s<sup>-1</sup> | float64 |
| e | water vapor pressure | Pa | float64 |
| es | saturation vapor pressure | Pa | float64 |
| hur | relative humidity | % | float64 |
| hurs | near-surface relative humidity | % | float64 |
| lat | latitude | degrees North | float64 |
| lon | longitude | degrees East | float64 |
| p | pressure | Pa | float64 |
| p2 | pressure | Pa | float64 |
| p_lcl | lifting condensation level pressure | Pa | float64 |
| ps | near-surface pressure | Pa | float64 |
| ta | air temperature | K | float64 |
| ta_par | dry parcel temperature | K | float64 |
| ta_par_s | saturated parcel temperature | K | float64 |
| ta_surf_par | dry surface parcel temperature | K | float64 |
| ta_surf_par_s | saturated surface parcel temperature | K | float64 |
| tas | near-surface air temperature | K | float64 |
| theta | air potential temperature | K | float64 |
| time | time | days since -4712-01-01T12:00:00 UTC | float64 |
| ts | surface temperature | K | float64 |
| ua | x wind | m.s<sup>-1</sup> | float64 |
| va | y wind | m.s<sup>-1</sup> | float64 |
| wdd | wind from direction | degrees | float64 |
| wdds | near-surface wind from direction | degrees | float64 |
| wds | wind speed | m.s<sup>-1</sup> | float64 |
| wdss | near-surface wind speed | m.s<sup>-1</sup> | float64 |
| z | height above reference ellipsoid | m | float64 |
| zg | geopotential height | m | float64 |
| zg_lcl | lifting condensation level geopotential height | m | float64 |

### iMet raw (raw:imet)

raw:imet is a raw instrument format of the InterMet radiosonde converted to
NetCDF by reading the `.dat` file.

| Variable | Description | Units | Type |
| --- | --- | --- | --- |
sample | sample number | 1 | int64 |
date_time | date time | year/month/day hour:minute:second | string |
press | pressure | Pa | float64 |
tair | air temperature | K | float64 |
hum | relative humidity | % | float64 |
lat | latitude | degrees North | float64 |
long | longitude | degrees East | float64 |
alt | altitude | m | float64 |
freq | frequency | Hz | float64 |
f_offs | frequency offset | Hz | float64 |

### Windsond raw (raw:ws)

raw:ws is a raw instrument format of the Windsond radiosonde converted to
NetCDF by reading the `.sounding` file.

| Variable | Description | Units | Type | Comment |
| --- | --- | --- | --- | --- |
| afc | automatic frequency control | Hz | int64 |
| afc1 | automatic frequency control 1 | Hz | int64 |
| afc2 | automatic frequency control 2 | Hz | int64 |
| alt | GPS altitude | m | int64 |
| ang | wind direction | degrees | float64 |
| ang\<n\> | wind direction (old) | degrees | float64 |
| behlan | behavior after landing | 1 | int64 | 0: power-save, 1: beacon at once |
| burn | burn string | 1 | int64 | 0: at cut down
| crc | cyclic redundancy check (CRC) | 1 | int64 |
| cutalt | cut dow altitude | m | int64 |
| extra | extra information | | string |
| fwver | firmware version | 1 | float64 |
| galt | altitude | m | int64 | |
| gpa | ground pressure | Pa | int |
| hdop | GPS horizontal dilution of precision (HDOP) |  | float64 |
| hu | relative humidity | % | float64 |
| hu\<n\> | relative humidity (old) | % | float64 |
| hw | hw | 1 | int64 |
| id | sond ID | 1 | int64 |
| install | install | | string |
| label | label | | string |
| lat | latitude | degrees North | float64 |
| lon | longitude | degrees East | float64 |
| lux | light | lux | int64 |
| mcnt | message counter | 1 | int64 |
| md | mode | 1 | int64 | 0: init, 1: ready for launch, 2: rising, 3: falling, 4: on ground, silent, 5: on ground, beeping, 6: on ground, sometimes beeping, 7: cutting down |
| new | GPS validity | 1 | int64 | 0: GPS is old |
| node_id | node ID | 1 | int64 |
| offset | time start | seconds since 1970-01-01T00:00 | float64 |
| pa | air pressure | Pa | int64 |
| pwr | power | W | float64 |
| q | quality | 1 | int64 |
| q0 | quality | 1 | int64 |
| q1 | quality | 1 | int64 |
| qu | quality | % | float64 |
| r | quality | 1 | int64 |
| rec | correction | 1 | int64 |
| rec<n> | correction (old) | 1 | int64 |
| relAP | release altitude | m | int64 |
| role | role | 1 | int64 |
| sats | number of GPS satellites | 1 | int64 |
| seq | sequence number | 1 | int64 |
| sid | session ID | 1 | int64 |
| software | software version | | string |
| spd | wind speed | m.s<sup>-1</sup> | float64 |
| spd\<n\> | wind speed (old) | m.s<sup>-1</sup> | float64 |
| su | power supply | V | float64 |
| syn | | 1 | int64 |
| te | temperature | K | float64 |
| te\<n\> | temperature (old) | K | float64 |
| tei | internal temperature | K | float64 |
| timezone | timezone | 1 | int64 |
| ucnt | ucnt | 1 | int64 |
| version | version | 1 | int64 |

### Attributes

rstool writes the following attributes in the raw (raw:\<instrument\>),
points (pts) and profile (prof) NetCDF files.

| Attribute | Description | Comment |
| --- | --- | --- |
| created | date created | year-month-dayThour:minute:second
| software | software identification | rstool x.y.z (https://github.com/peterkuma/rstool)

## License

This software can be used, modified and distributed freely under
the terms of an MIT license (see [LICENSE.md](LICENSE.md)).
