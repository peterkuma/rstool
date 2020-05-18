rstool
======

**Development status:** alpha

rstool is an open source command-line program for converting native radiosonde
data to NetCDF and calculation of derived physical quantities.

Supported instruments:

- [InterMet Systems](https://www.intermetsystems.com) (iMet) radiosondes such as iMet-1-ABxn
- [Windsond](http://windsond.com/) [in development]

Support for other instruments can be added by writing a Python module
in `rstool_package/drivers`
to read the data files produced by the radiosonde.

Usage
-----

```sh
rstool <type> <input> <output>
```

Arguments:

- `type` - See Types below.
- `input` - Input file or directory with native radiosonde data.
- `output` - Output file (NetCDF).

Types:

- `imet` - InterMet Systems iMet-1-ABxn. Expected `input`: directory generated
    by the iMetOS-II software.

Installation
------------

Recommended operating system to run rstool is Linux with Python 2.7.
Install with:

```sh
python setup.py install
```

or

```sh
python setup.py install --user
```

to install in user's home directory (make sure the directory `~/.local/bin`
is in the environmental variable `PATH`). Run with:

`rstool`

on the command line.

## Native format description

### Windsond (in development)

A developement implementation of Windsond data to NetCDF conversion is in
`ws.py`.

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
| behlan | behavior after landing | 1 | int | 0: Power-save, 1: Beacon at once |
| burn | burn string | 1 | int | 0: at cut down
| clk | | | | |
| crc | cyclic redundancy check (CRC) | 1 | int | |
| cutalt | cut dow altitude | m | int |
| cutpr2 | | | | |
| datetime | seconds since file-start
| fwver | firmware version | 1 | int | fwver/100.0 |
| galt | altitude (spotty) | m | int | |
| gpa | ground pressure | Pa | int | |
| hdop | GPS horizontal dilution of precision (HDOP) |  | float | |
| hu | relative humidity | % | float | |
| hu\<n\> | relative humidity (old #\<n\>) | % | float | |
| hw |  | 1 | int | |
| id | sond ID | 1 | int | |
| lat | latitude | degree | lat/1e6 |
| latd | latitude | decimal part of minute | int | |
| latm | latitude | minute | int | latm/1e4 |
| lon | longitude | degree | int | lon/1e6 |
| lond | longitude | decimal part of minute | int |  |
| lonm | longitude | minute | int | lonm/1e4 |
| lux | light | lux | int | |
| mcnt | message counter | 1 | int | |
| md | mode | 1 | int | 0: Init, 1: Ready for launch, 2: Rising, 3: Falling, 4: On ground, silent, 5: On ground, beeping, 6: On ground, sometimes beeping, 7: Cutting down |
| new | GPS validity | 1 | int | 0: GPS is old |
| pa | air Pressure | Pa | int | |
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
| tei | internal Temperature | ℃ | float | |
| ucnt | | 1 | int | |

## License

MIT license (see [LICENSE.md](LICENSE.md))
