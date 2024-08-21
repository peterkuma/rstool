# rstool

rstool is an open source command-line program for converting radiosonde
measurement data to NetCDF and calculation of derived physical quantities. It
can also be used for the calculation of derived quantities from source
quantities, such as exporting variables along a vertical profile from a model
and letting rstool calculate the derived quantities (`rstool prof prof` *input*
*output*).

Supported instruments:

- [InterMet Systems](https://www.intermetsystems.com) (iMet) radiosondes, such
  as iMet-1-ABxn, data files produced by the iMetOS-II software (a directory
  containing `.dat` and `.flt` files).
- [Windsond](http://windsond.com/), data files produced by the Windsond
  software (`.sounding`).

Support for other instruments can be added by writing a Python module in
`rstool/drivers` to read the data files produced by the radiosonde (see the
template in `rstool/drivers/template.py`).

## Usage

rstool converts radiosonde measurement data to NetCDF intrument-dependent
intermediate (`im`), points (`pts`), and profile (`prof`) datasets and
calculates derived physical quantities.

Usage: **rstool** *input_type* *output_type* *input* [*surface*] *output*

Arguments:

- *input_type*: See Input types below.
- *output_type*: See Output types below.
- *input*: Input file or directory.
- *surface*: Near-surface variables (NetCDF).
- *output*: Output file (NetCDF).

Input types:

- `imet`: InterMet Systems iMet-1-ABxn sounding. `input` should be a directory
  generated by the iMetOS-II software, containing `.dat` and `.flt` files.
- `prof`: rstool profile (`prof`) format (NetCDF).
- `pts`: rstool points (`pts`) format (NetCDF). Collection of measurement
  points, not interpolated to any vertical coordinates. The output of running
  rstool with the output type `pts`.
- `im:`*instrument*: Instrument-dependent intermediate (`im`) rstool format
  (NetCDF). *instrument* is one of `imet` or `ws`.
- `ws`: Windsond sounding. `input` should be a `.sounding` file generated by the
  Windsond software.

Output types:

- `pts`: Collection of measurement points (NetCDF).
- `prof`: Vertical profile calculated by interpolating the measurement points
  during the ascent of the radiosonde as a function of pressure (NetCDF).
- `prof:desc`: The same as `prof`, but for the descending path of the
  radiosonde (if present in the input data).
- `im`: Instrument-dependent intermediate rstool format (NetCDF).

The following input/output type combinations are possible, where *instrument*
is `imet` or `ws`:

- *instrument* `im`: Native instrument format to instrument-dependent
  intermediate format (NetCDF).
- *instrument* `pts`: Native instrument format to the points format.
- *instrument* `prof`: Native instrument format to the profile format.
- *instrument* `prof:desc`: Native instrument format to a descending profile
  format.
- `im:`*instrument* `pts`: Instrument-dependent intermediate format (NetCDF) to
  the points format.
- `im:`*instrument* `prof`: Instrument-dependent intermediate format (NetCDF)
  to the profile format.
- `im:`*instrument* `prof:desc`: Instrument-dependent intermediate format
  (NetCDF) to the descending profile format.
- `pts prof`: The points format to the profile format.
- `pts prof:desc`: The points format to the descending profile format.
- `prof prof`: The profile format to the profile format. This can be used to
  calculate derived physical quantities from a set source quantities.

## Examples

Convert a Windsond sounding `2000-01-01T0000.sounding` to the profile format:

```sh
rstool ws prof 2000-01-01T0000.sounding 2000-01-01T0000_prof.nc
```

Convert an iMet sounding in a directory `2000-01-01T0000` to the profile format:

```sh
rstool imet prof 2000-01-01T0000 2000-01-01T0000_prof.nc
```

Convert a Windond sounding `2000-01T01_0000.sounding` to the Windsond
intermediate format:

```sh
rstool ws im 2000-01-01T0000.sounding 2000-01-01T0000_im.nc
```

Convert an iMet sounding in a directory `2000-01-01T0000` to the points format:

```sh
rstool imet pts 2000-01-01T0000 2000-01-01T0000_pts.nc
```

Convert the Windsond intermediate format to the points format:

```sh
rstool im:ws pts 2000-01-01T0000_im.nc 2000-01-01T0000_pts.nc
```

Convert the points format to the profile format:

```sh
rstool pts prof 2000-01-01T0000_pts.nc 2000-01-01T0000_prof.nc
```

Calculate derived physical quantities from source physical quantities in the
input (profile format):

```sh
rstool prof prof input.nc output.nc
```

## Installation

It is recommended to run rstool on Linux.

### Linux

On Debian-derived distributions (Ubuntu, Devuan, ...), install the required
system packages with:

```sh
sudo apt install python3 python3-pip pipx
```

On Fedora, install the required system packages with:

```sh
sudo yum install python3 pipx
```

Install rstool:

```sh
pipx install rstool
```

Make sure that `$HOME/.local/bin` is included in the `PATH` environment
variable if not already. This can be done with `pipx ensurepath`.

You should now be able to run `rstool`.

To uninstall:

```sh
pipx uninstall rstool
```

### macOS

Open the Terminal. Install rstool with:

```sh
python3 -m pip install rstool
```

Make sure that `/Users/<user>/Library/Python/<version>/bin` is included in the
`PATH` environment variable if not already, where `<user>` is your system
user name and `<version>` is the Python version. This path should be printed
by the above command. This can be done by adding this line to the file
`.zprofile` in your home directory and restarting the Terminal:

```sh
PATH="$PATH:/Users/<user>/Library/Python/<version>/bin"
```

You should now be able to run `rstool`.

To uninstall:

```sh
python3 -m pip uninstall rstool
```

### Windows

Install [Python 3](https://www.python.org). In the installer, tick `Add
python.exe to PATH`.

Open Command Prompt from the Start menu. Install rstool with:

```sh
pip install rstool
```

You should now be able to run `rstool`.

To uninstall:

```sh
pip uninstall rstool
```

## Calculation of derived physical quantities

rstool calculates a number of physical quantities from a set of source physical
quantities, such as different humidity quantities (water vapor partial
pressure, mixing ratio, specific humidity, relative humidity, and dew point
temperature), potential temperature, lifting condensation level, and eastward
and northward wind. This is done when converting from a native instrument
format, the instrument-dependent intermediate (`im`) format, the points (`pts`)
format, or the profile (`prof`) format to the profile (`prof`) format.
Conversion of quantities is performed recursively from source to derived
quantities through any number of steps required. Supported elementary quantity
conversions are the following (*source quantities* 🠢 *derived quantities*):

thetav, zg, p, g 🠢 p_bvf, zg_bvf, bvf\
p, w 🠢 e\
td 🠢 e\
ps, ws 🠢 es\
tds 🠢 es\
ta 🠢 esat\
tas 🠢 esats\
station_lat 🠢 g\
g 🠢 gamma\
p, ta, gamma 🠢 gamma_sat\
w, wsat 🠢 hur\
ws, wsats 🠢 hurs\
w 🠢 hus\
ws 🠢 huss\
p, theta, thetas 🠢 lts\
ps, ws, tas 🠢 pc\
ps, ts, p, theta 🠢 p_ll\
rhod, rhow 🠢 rho\
p, e, ta 🠢 rhod\
ps, es, tas 🠢 rhods\
rhods, rhows 🠢 rhos\
p, e, ta 🠢-rhow\
ps, es, tas 🠢 rhows\
p, ps, tas 🠢 ta_par\
p, tas, ws, g, gamma 🠢 ta_par_sat\
p, ps, ts 🠢 ta_surf_par\
p, ts, ws, g, gamma 🠢 ta_surf_par_sat\
e 🠢 td\
es 🠢 tds\
ta, w 🠢 tv\
tas, ws 🠢 tvs\
p, ta 🠢 theta\
ps, tas 🠢 thetas\
theta, w 🠢 thetav\
thetas, ws 🠢 thetavs\
wds, wdd 🠢 ua\
wdss, wdds 🠢 uas\
wds, wdd 🠢 va\
wdss, wdds 🠢 vas\
hus 🠢 w\
hur, wsat 🠢 w\
p, e 🠢 w\
ua, va 🠢 wdd\
uas, vas 🠢 wdds\
ua, va 🠢 wds\
uas, vas 🠢 wdss\
huss 🠢 ws\
hurs, wsats 🠢 ws\
ps, es 🠢 ws\
p, esat 🠢 wsat\
ps, esats 🠢 wsats\
zg, g 🠢 z\
z, g 🠢 zg\
pc, p, zg 🠢 lcl\
p_ll, p, zg 🠢 zg_ll

## Format description

Below is a description of the output NetCDF formats. Time is expressed as
Julian date (fractional number of days since -4712-01-01 12:00 UTC, or
-4713-11-24 12:00 UTC in the proleptic Gregorian calendar). This can be
converted to UNIX time (number of non-leap seconds since 1 January 1970 00:00
UTC) with the forumula `(time - 2440587.5)*86400`.

The formats can be converted in the order from intrument-depedent intermediate
(`im:`*instrument*) to points (`pts`) to profile (`prof`).

All variables are stored either as 64-bit floating point (float64) or 64-bit
integer (int64). Missing values are stored as NaN in float64 and
-9223372036854775806 in int64.

### Points (pts)

pts is an instrument-independent format containing a sequence of radiosonde
measurements as received by the base station ordered by time, converted to a
standard set of variables.

| Variable | Long name | Standard name | Units |
| --- | --- | --- | --- |
| hur | relative humidity | relative_humidity | % |
| hurs | near-surface relative humidity | relative_humidity | % |
| lat | latitude | latitude | degree north |
| lon | longitude | longitude | degree east |
| p | air pressure | air_pressure | Pa |
| ps | surface air pressure | surface_air_pressure | Pa |
| ta | air temperature | air_temperature | K |
| tas | near-surface air temperature | air_temperature | K |
| time | time | time | days since -4713-11-24 12:00 UTC (`proleptic_gregorian` calendar) |
| station_lat | station latitude | latitude | degree north |
| station_lon | station longitude | longitude | degree east |
| station_z | station altitude | height_above_reference_ellipsoid | m |
| station_time | station time | time | days since -4713-11-24 12:00 UTC |
| uas | eastward near-surface wind | eastward_wind | m.s<sup>-1</sup> |
| vas | northward near-surface wind | northward_wind | m.s<sup>-1</sup> |
| z | altitude | height_above_reference_ellipsoid | m |

### Profile (prof)

prof is an instrument-independent format containing standard variables
interpolated as a function of height. Profiles are calculated by averaging
points (`pts`) on a regular vertical pressure grid. For calculation of an
ascending profile (default), only strictly increasing subsets of points are
considered. For a descending profile (`prof:desc`), only strictly decreasing
subsets of points are considered. Vertical intervals with no points are filled
with missing values. It is therefore possible to identify vertical intervals
where no radiosonde data were received, and optionally interpolate (linearly or
in some other way) across these intervals when plotting.

| Variable | Long name | Standard name | Units |
| --- | --- | --- | --- |
| bvf | Brunt–Väisälä frequency in air | brunt_vaisala_frequency_in_air | s<sup>-1</sup> |
| e | water vapor pressure in air | water_vapor_partial_pressure_in_air | Pa |
| es | near-surface water vapor partial pressure in air | water_vapor_partial_pressure_in_air | Pa |
| esat | saturation vapor pressure | water_vapor_partial_pressure_in_air | Pa |
| esats | near-surface saturation vapor pressure | water_vapor_partial_pressure_in_air | Pa |
| g | gravitational acceleration | | m.s<sup>-2</sup> |
| gamma | air temperature lapse rate | air_temperature_lapse_rate | K.m<sup>-1</sup> |
| gamma_sat | air temperature saturation lapse rate | air_temperature_lapse_rate | K.m</sup>-1</sup> |
| hur | relative humidity | relative_humiidty | % |
| hurs | near-surface relative humidity | relative_humidity | % |
| lat | latitude | latitude | degree north |
| lon | longitude | longitude | degree east |
| lts | lower tropospheric stability | | K |
| p | air pressure | air_pressure | Pa |
| p_bvf | air pressure of bvf | air_pressure | Pa |
| pc | condensation pressure | air_pressure | Pa |
| ps | surface air pressure | surface_air_presssure | Pa |
| rho | air density | air_density | kg.m<sup>-3</sup> |
| rhod | dry air density | air_density | kg.m<sup>-3</sup> |
| rhods | near-surface dry air density | air_density | kg.m<sup>-3</sup> |
| rhos | near-surface air density | air_density | kg.m<sup>-3</sup> |
| rhow | water vapor density | air_density | kg.m<sup>-3</sup> |
| rhows | near-surface water vapor density | air_density | kg.m<sup>-3</sup> |
| station_lat | station latitude | latitude | degree north |
| station_lon | station longitude | longitude | degree east |
| station_time | station time | time | days since -4713-11-24 12:00 UTC |
| station_z | station altitude | height_above_reference_ellipsoid | m |
| ta | air temperature | air_temperature | K |
| td | dew point temperature | dew_point_temperature | K |
| tds | near-surface dew point temperature | dew_point_temperature | K |
| tv | virtual temperature | virtual_temperature | K |
| tvs | near-surface virtual temperature | virtual_temperature | K |
| ta_par | dry air parcel temperature | air_temperature | K |
| ta_par_sat | saturation air parcel temperature | air_temperature | K |
| ta_surf_par | dry surface-temperature air parcel temperature | air_temperature | K |
| ta_surf_par_sat | saturation surface-temperature air parcel temperature | air_temperature | K |
| tas | near-surface air temperature | air_temperature | K |
| theta | air potential temperature | air_potential_temperature | K |
| thetas | near-surface air potential temperature | air_potential_temperature | K |
| thetav | virtual potential temperature | virtual_temperature | K |
| thetavs | near-surface virtual potential temperature | virtual_temperature | K |
| time | time | time | days since -4713-11-24 12:00 UTC (`proleptic_gregorian` calendar) |
| ts | surface temperature | surface_temperature | K |
| ua | eastward wind | eastward_wind | m.s<sup>-1</sup> |
| uas | eastward near-surface wind | eastward_wind | m.s<sup>-1</sup> |
| va | northward wind | northward_wind | m.s<sup>-1</sup> |
| vas | northward near-surface wind | northward_wind | m.s<sup>-1</sup> |
| w | humidity mixing ratio | humidity_mixing_ratio | 1 |
| wdd | wind from direction | wind_from_direction | degree |
| wdds | near-surface wind from direction | wind_from_direction | degree |
| wds | wind speed | wind_speed | m.s<sup>-1</sup> |
| wdss | near-surface wind speed | wind_speed | m.s<sup>-1</sup> |
| ws | near-surface humidity mixing ratio | humidity_mixing_ratio | 1 |
| wsat | saturation humidity mixing ratio | humidity_mixing_ratio | 1 |
| wsats | near-surface saturation humidity mixing ratio | humidity_mixing_ratio | 1 |
| z | altitude | height_above_reference_ellipsoid | m |
| zg | geopotential height | geopotential_height | m |
| zg_bvf | geopotential height of bvf | geopotential_height | m |
| lcl | lifting condensation level | geopotential_height | m |

### Surface (surf)

surf dataset specifies near-surface variables, which can be used as an optional
input to rstool. These can come from a co-located automatic weather station
(AWS). Some native radiosonde data can already contain the same of these
variables (iMet). Near-surface variables are needed to calculate some derived
profile variables, such as the lifting condensation level. All variables must
have a single dimension of `time`. The point nearest to the radiosonde launch
time is picked. If no points are within 1 hour of the radiosonde launch, the
surface input is ignored.  Either (`uas`, `vas`) or (`wdds`, `wdss`) can be
defined.  Either `hurs` or (`ps`, `tas`, `tds`) can be defined.

| Variable | Long name | Standard name | Units |
| --- | --- | --- | --- |
| time | time | time | days since -4713-11-24 12:00 UTC (`proleptic_gregorian` calendar) |
| hurs | near-surface relative humidity | relative_humidity | % |
| ps | surface air pressure | surface_air_pressure | Pa |
| tas | near-surface air temperature | air_temperature | K |
| tds | near-surface dew point temperature | dew_point_temperature | K |
| ts | surface temperature | surface_temperature | K |
| uas | eastward near-surface wind speed | eastward_wind_speed | m.s<sup>-1</sup> |
| vas | northward near-surface wind speed | northward_wind_speed | m.s<sup>-1</sup> |
| wdds | near-surface wind from direction | wind_from_direction | degree |
| wdss | near-surface wind speed | wind_speed | m.s<sup>-1</sup> |

### iMet intermediate (im:imet)

`im:imet` is an intermediate instrument format of the InterMet radiosonde
converted to NetCDF by reading input `.dat` and `.flt` files.

| Variable | Long name | Standard name | Units |
| --- | --- | --- | --- |
| alt | altitude | height_above_reference_ellipsoid | m |
| date_time | date time | | year/month/day hour:minute:second |
| f_offs | frequency offset | | Hz |
| freq | frequency | | Hz |
| hum | relative humidity | relative_humidity | % |
| hurs | near-surface relative humidity | relative_humidity | % |
| lat | latitude | latitude | degree north |
| long | longitude | longitude | degree east |
| press | air pressure | air_pressure | Pa |
| ps | surface air pressure | surface_air_pressure | Pa |
| sample | sample number | | 1 |
| station_lat | station latitude | station_latitude | degree north |
| station_lon | station longitude | station longitude | degree east |
| station_z | station altitude | height_above_reference_ellipsoid | m |
| tair | air temperature | air_temperature | K |
| tas | near-surface air temperature | air_temperature | K |
| uas | eastward near-surface wind speed | eastward_wind | m.s<sup>-1</sup> |
| vas | northward near-surface wind speed | northward_wind | m.s<sup>-1</sup> |

### Windsond intermediate (im:ws)

`im:ws` is an intermediate instrument format of the Windsond radiosonde
converted to NetCDF by reading an input `.sounding` file.

| Variable | Long name | Standard name | Units | Comment |
| --- | --- | --- | --- | --- |
| afc | automatic frequency control | | Hz |
| afc1 | automatic frequency control 1 | | Hz |
| afc2 | automatic frequency control 2 | | Hz |
| alt | GPS altitude | height_above_reference_ellipsoid | m |
| ang | wind direction | wind_from_direction | degree |
| ang\<n\> | wind direction (old) | wind_from_direction | degree |
| behlan | behavior after landing | | 1 | 0: power-save, 1: beacon at once |
| burn | burn string | | 1 | 0: at cut down
| crc | cyclic redundancy check (CRC) | | 1 |
| cutalt | cut dow altitude | height_above_reference_ellipsoid | m |
| extra | extra information | | |
| fwver | firmware version | | 1 |
| galt | altitude | height_above_reference_ellipsoid | m | |
| gpa | ground pressure | surface_air_pressure | Pa |
| hdop | GPS horizontal dilution of precision (HDOP) | | |
| hu | relative humidity | relative_humidity | % |
| hu\<n\> | relative humidity (old) | relative_humidity | % |
| hw | hw | | 1 |
| id | sond ID | | 1 |
| install | install | | |
| label | label | | |
| lat | latitude | latitude | degree north |
| lon | longitude | longitude | degree east |
| lux | light | | lux |
| mcnt | message counter | | 1 |
| md | mode | | 1 | 0: init, 1: ready for launch, 2: rising, 3: falling, 4: on ground, silent, 5: on ground, beeping, 6: on ground, sometimes beeping, 7: cutting down |
| new | GPS validity | | 1 | 0: GPS is old |
| node_id | node ID | | 1 |
| offset | time start | time | seconds since 1970-01-01T00:00 |
| pa | air pressure | air_pressure | Pa |
| pwr | power | |  W |
| q | quality | | 1 |
| q0 | quality | | 1 |
| q1 | quality | | 1 |
| qu | quality | | % |
| r | quality | | 1 |
| rec | correction | | 1 |
| rec<n> | correction (old) | | 1 |
| relAP | release altitude | height_above_reference_ellipsoid | m |
| role | role | | 1 |
| sats | number of GPS satellites | | 1 |
| seq | sequence number | | 1 |
| sid | session ID | | 1 |
| software | software version | | |
| spd | wind speed | wind_speed | m.s<sup>-1</sup> |
| spd\<n\> | wind speed (old) | wind_speed | m.s<sup>-1</sup> |
| su | power supply | | V |
| syn | | | 1 |
| te | air temperature | air_temperature | K |
| te\<n\> | temperature (old) | air_temperature | K |
| tei | internal temperature | | K |
| timezone | timezone | | 1 |
| ucnt | ucnt | | 1 |
| version | version | | 1 |

### Attributes

rstool writes the following attributes in the intrument-dependent intermediate
(`im:`*instrument*), points (`pts`), and profile (`prof`) NetCDF files.

| Attribute | Description | Comment |
| --- | --- | --- |
| created | date created | year-month-dayThour:minute:second
| software | software identification | rstool x.y.z (https://github.com/peterkuma/rstool)

In addition, the following attributes may be available in instrument-depedent
intermediate, pts, and prof datasets depending on the instrument:

| Attribute | Description |
| --- | --- |
| station | station information |
| balloon | balloon information |
| sonde | sonde information |
| operator | operator name |

## Python API

rstool provides functions implementing algorithms for calculating various
physical quantities. The functions are available in the Python module
`rstool.algorithms`.

**All of the functions below use keyword-only arguments, which means that they
have to be called with explicitly specified keyword arguments. They cannot be
called with positional arguments. This is to prevent accidental mistakes in
specifying the arguments.**


**calc_bvf**(\*, *thetav*, *zg*, *p*, *g*, *res*=400)

Calculate Brunt-Väisälä frequency from air temperature *ta* (K),
geopotential height *zg* (m), air pressure *p* (Pa) and gravitational
acceleration *g* (m.s<sup>-2</sup>). *res* is vertical resolution in
geopotential height (m).

**calc_e**(\*, *p*, *w*)

Calculate water vapor partial pressure in air (Pa) from humidity
mixing ratio *w* (1) and air pressure *p* (Pa).

**calc_esat**(\*, *ta*)

Calculate saturation water vapor partial pressure (Pa) from air
temperature *ta* (K).

**calc_g**(\*, *lat*=45)

Calculate gravitational acceleration (m.s<sup>-2</sup>) from latitude *lat*
(degree). Height dependence is ignored.

**calc_gamma**(\*, *g*)

Calculate air temperature lapse rate (K.m<sup>-1</sup>) at gravitational
acceleration *g* (m.s<sup>-2</sup>).

**calc_gamma_sat**(\*, *p*, *ta*, *gamma*)

Calculate saturation air temperature lapse rate (K.m<sup>-1</sup>) from
pressure *p* (Pa), temperature *ta* (K) and air temperature lapse rate
*gamma* (K.m<sup>-1</sup>).

**calc_hur**(\*, *w*, *wsat*)

Calculate relative humidity (%) from humidity mixing ratio *w* (1) and
saturation water vapor mixing ratio in air *wsat* (1).

**calc_hus**(\*, *w*)

Calculate specific humidity (1) from humidity mixing ratio *w* (1).

**calc_lts**(\*, *p*, *theta*, *thetas*):

Calculate lower tropospheric stability (K) from air pressure *p* (Pa), air
potential temperature *theta* (K) and near-surface air potential
temperature *thetas* (K).

**calc_rho**(\*, *rhod*, *rhow*)

Calculate density of air (kg.m<sup>-3</sup>) from density of dry air
*rho_d* (kg.m<sup>-3</sup>) and density of water vapor *rho_w*
(kg.m<sup>-3</sup>).

**calc_rho_d**(\*, *p*, *e*, *ta*)

Calculate density of dry air (kg.m<sup>-3</sup>) from air pressure *p*,
water vapor partial pressure *e* (Pa), and air temperature *ta* (K).

**calc_rhow**(\*, *p*, *e*, *ta*)

Calculate density of water vapor (kg.m<sup>-3</sup>) from air pressure *p*,
water vapor partial pressure *e* (Pa), and air temperature *ta* (K).

**calc_ta_par**(\*, *p*, *ps*, *tas*)

Calculate dry adiabatic air parcel temperature at air pressure *p* (Pa),
assuming surface air pressure *ps* and near-surface air temperature *tas*
(K).

**calc_ta_par_sat**(\*, *p*, *tas*, *ws*, *g*, *gamma*)

Calculate saturation air parcel temperature at pressure *p* (Pa), assuming
near-surface air temperature *tas* (K), near-surface humidity mixing ratio
*ws* (1), gravitational acceleration *g* (m.s<sup>-2</sup>) and air
temperature lapse rate *gamma* (K.m<sup>-1</sup>). *p* has to be an array
dense enough for accurate integration.

**calc_tv**(\*, *ta*, *w*)

Calculate virtual temperature (K) from air temperature *ta* (K) and
humidity mixing ratio *w* (1).

**calc_theta**(\*, *p*, *ps*, *ta*, *p0*=1e5)

Calculate air potential temperature (K) from air pressure *p* (Pa), surface
air pressure *ps* (Pa) and air temperature *ta* (K). Assume standard
pressure *p0*.

**calc_td**(\*, *e*)

Calculate dew point temperature (K) from water vapor pressure *e* (Pa).

**calc_pc**(\*, *ps*, *ws*, *tas*)

Calculate condensation pressure (Pa) from surface air pressure *ps* (Pa),
near-surface humidity mixing ratio *ws* (Pa) and near-surface air
temperature *tas* (K).

**calc_ua**(\*, *wds*, *wdd*)

Calculate eastward wind (m.s<sup>-1</sup>) from wind speed *wds*
(m.s<sup>-1</sup>) and wind direction *wdd* (degree).

**calc_va**(\*, *wds*, *wdd*)

Calculate northward wind (m.s<sup>-1</sup>) from wind speed *wds*
(m.s<sup>-1</sup>) and wind direction *wdd* (degree).

**calc_w**(\*,\
    [option 1] *p*, *e*\
    [option 2] *hus*\
    [option 3] *hur*, *wsat*\
)

Calculate humidity mixing ratio from [option 1] pressure *p* (Pa) and
water vapor partial pressure *e* (Pa), [option 2] specific humidity *hus*
(1), or [option 3] relative humidity *hur* (%) and saturation humidity
mixing ratio *wsat* (1).

**calc_wdd**(\*, *ua*, *va*)

Calculate wind direction (degree) from eastward wind *ua*
(m.s<sup>-1</sup>) and northward wind *va* (m.s<sup>-1</sup>).

**calc_wds**(\*, *ua*, *va*)

Calculate wind speed (m.s<sup>-1</sup>) from eastward wind *ua*
(m.s<sup>-1</sup>) and northward wind *va* (m.s<sup>-1</sup>).

**calc_wsat**(\*, *p*, *ta*)

Calculate saturation humidity mixing ratio (1) from air pressure *p*
(Pa) and air temperature *ta* (K).

**calc_z**(\*,\
    [option 1] *zg*, *g*\
    [option 2] *p1*, *p*, *z*\
)

Calculate altitude (m) from [option 1] geopotential height *zg* (m) and
gravitational acceleration *g* (m.s<sup>-2</sup>), [option 2] by
interpolation from air pressure level *p1* (Pa), air pressure at all levels
*p* (Pa) and altitude at all levels *z* (m).

**calc_zg**(\*,\
    [option 1] *z*, *g*\
    [option 2] *p1*, *p*, *zg*\
)

Calculate geopotential height (m) from [option 1] altitude *z* (m) and
gravitational acceleration *g* (m.s<sup>-2</sup>), [option 2] by
interpolation from air pressure level *p1* (Pa), air pressure at all levels
*p* (Pa) and geopotential height at all levels *zg* (m).


## License

This software can be used, modified, and distributed freely under the terms of
the MIT license (see [LICENSE.md](LICENSE.md)).

## Releases

### 1.1.0 (2023-11-17)

- Fixed a bool type error due to a removal of the type from the numpy package.
- Improvements in the processing of surface variables.
- Latitude-dependent gravitational acceleration calculation.
- Destination variables are now only set if they do not already exist in prof
  to prof conversion.
- More accurate calculation of relative humidity from specific humidity.
- Fixed missing calendar attribute in the time variable of prof output.
- Fixes and improvements in the documentation.

### 1.0.0 (2021-12-11)

- Changed calendar to proleptic Gregorian.
- Added standard\_name attributes.

### 0.1.1 (2020-08-14)

- Fixed missing surf module.
- Installation of the script via setuptools entry points.

### 0.1.0 (2020-08-12)

- Initial beta release.

## See also

[ALCF](https://alcf-lidar.github.io),
[ccplot](https://ccplot.org),
[cl2nc](https://github.com/peterkuma/cl2nc),
[mpl2nc](https://github.com/peterkuma/mpl2nc),
[mrr2c](https://github.com/peterkuma/mrr2c)
