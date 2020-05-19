rstool
======

**Development status:** beta

rstool is an open source command-line program for converting native radiosonde
data to NetCDF and calculation of derived physical quantities.

Supported instruments:

- [InterMet Systems](https://www.intermetsystems.com) (iMet) radiosondes such as iMet-1-ABxn
- [Windsond](http://windsond.com/)

Support for other instruments can be added by writing a Python module
in `rstoollib/drivers`
to read the data files produced by the radiosonde (see the template
in `template.py`).

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

- `imet` - InterMet Systems iMet-1-ABxn. Expected `input`: directory generated
    by the iMetOS-II software.
- `ws` - Windsond. Expected `input`: `.sounding` file generated by the Windsond
    software.
- `raw:<instrument>` - "Raw" instrument-dependent format (NetCDF). `instrument`
    is one of `imet`, `ws`.
- `pts` - Collection of measurement points (NetCDF). The output of running
    rstool with the output type `pts`.

Output types:

- `raw` - "Raw" instrument-dependent format (NetCDF).
- `pts` - Collection of measurement points (NetCDF).
- `prof` - Vertical profile calculated by interpolating the measurement points
    as a function of height (NetCDF).

Currently supported input and output type combinations (other combinations are
in development):

- `rstool ws raw <input> <output>`
- `rstool imet prof <input> <output>`

Installation
------------

Recommended operating system to run rstool is Linux with Python 3.
Install with:

```sh
pip3 install https://github.com/peterkuma/ds-python/archive/master.zip \
    https://github.com/peterkuma/aquarius-time/archive/master.zip
python3 setup.py install
```

or

```sh
pip3 install --user https://github.com/peterkuma/ds-python/archive/master.zip \
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

### Points (pts)

| Parameter | Description | Units | Type |
| --- | --- | --- | --- |

### Profile (prof)

The naming of variables follows CMIP5 standard names.

| Parameter | Description | Units | Type |
| --- | --- | --- | --- |
| bvf | brunt vaisala frequency in air | s<sup>-1</sup> | float64 |
| e | water vapor pressure | Pa | float64 |
| es | saturation vapor pressure | Pa | float64 |
| hur | relative humidity | % | float64 |
| hurs | near-surface relative humidity | % | float64 |
| lat | latitude | degrees north | float64 |
| lon | longitude | degrees east | float64 |
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
| zg_lcl | lifting condensation level geopotential height | m | float64 |
| zg | geopotential height | m | float64 |

### Windsond raw (raw:ws)

List of native parameters in the `.sounding` and `.csv` files
and their description:

| Parameter | Description | Units | Type | Coding |
| --- | --- | --- | --- | --- |
| relAP | release altitude | m | |
| afc0 | automatic frequency control | Hz | int | |
| afc1 | automatic frequency control | Hz | int | |
| alt | GPS altitude | m | int | |
| ang | wind direction | degree | float | |
| ang\<n\> | wind direction (old #\<n\>) | degree | float | |
| behlan | behavior after landing | 1 | int | 0: power-save, 1: beacon at once |
| burn | burn string | 1 | int | 0: at cut down
| clk | | | | |
| crc | cyclic redundancy check (CRC) | 1 | int | |
| cutalt | cut dow altitude | m | int |
| cutpr2 | | | | |
| datetime | seconds since file-start
| fwver | firmware version | 1 | int | fwver/100.0 |
| galt | altitude | m | int | |
| gpa | ground pressure | Pa | int | |
| hdop | GPS horizontal dilution of precision (HDOP) |  | float | |
| hu | relative humidity | % | float | |
| hu\<n\> | relative humidity (old #\<n\>) | % | float | |
| hw |  | 1 | int | |
| id | sond ID | 1 | int | |
| lat | latitude | degree | int | sign(lat)*(floor(abs(lat)/1e6) + (abs(lat)/1e6 % 1.)*1e2/60.) |
| latd | latitude | decimal part of minute | int | latd/1e4 |
| latm | latitude | minute | int | latm/1e4 |
| lon | longitude | degree | int | sign(lon)*(floor(abs(lon)/1e6) + (abs(lon)/1e6 % 1.)*1e2/60.) |
| lond | longitude | decimal part of minute | int | lond/1e4 |
| lonm | longitude | minute | int | lonm/1e4 |
| lux | light | lux | int | |
| mcnt | message counter | 1 | int | |
| md | mode | 1 | int | 0: init, 1: ready for launch, 2: rising, 3: falling, 4: on ground, silent, 5: on ground, beeping, 6: on ground, sometimes beeping, 7: cutting down |
| new | GPS validity | 1 | int | 0: GPS is old |
| pa | air pressure | Pa | int | |
| pwr | power | mW | int | 0: 1.3, 1: 1.5, 2: 3, 3: 6, 4: 13, 5: 25, 6: 50, 7: 100 |
| q0 | quality | % | hex | max(0.01, max(q0, q1)/256.0 - 0.02*rec) if rec else max(q0, q1)/256.0 |
| q1 | quality | % | hex | |
| r | quality | % | int | quality = max(0.01, r/256.0 - 0.02*rec) if rec else r/256.0 |
| rec | correction | 1 | int | |
| rec0 | correction | 1 | int | |
| rec1 | correction | 1 | int | |
| role | | 1 | int | |
| sats | number of GPS satellites | 1 | int | |
| seq | sequence number | 1 | int | |
| sid | session ID | 1 | int | |
| spd | wind speed | m.s<sup>-1</sup> | float | |
| spd\<n\> | wind speed (old #\<n\>) | m.s<sup>-1</sup> | float | |
| su | power supply | V | float | |
| syn | | 1 | int | |
| te | temperature | ℃ | float | |
| te\<n\> | temperature (old #\<n\>) | ℃ | float | |
| tei | internal temperature | ℃ | float | |
| ucnt | | 1 | int | |

## License

MIT license (see [LICENSE.md](LICENSE.md))
