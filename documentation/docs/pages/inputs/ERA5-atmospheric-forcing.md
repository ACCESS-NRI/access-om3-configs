# ERA5 atmospheric forcing

[ERA5](https://confluence.ecmwf.int/spaces/CKB/pages/76414402/ERA5+data+documentation) is ECMWF's fifth-generation global atmospheric reanalysis. The [hourly single-level product](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview) used by ACCESS-OM3 is provided on a regular 0.25° × 0.25° latitude-longitude grid.

ACCESS-OM3 uses ERA5 through the CDEPS **DATM** component. ERA5 supplies atmospheric forcing only; runoff continues to be supplied from JRA55-do through **DROF**.

The ACCESS-OM3-ready ERA5 files are currently stored on NCI at:

```text
/g/data/av17/access-nri/OM3/era5_rechunked_1h_yearly/
```

ERA5 forcing is currently used in the [`dev-MCW_100km_era_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_era_iaf) configuration. This allows evaluation of the coupled MOM6–CICE6–WW3 model using atmospheric forcing consistent with the [Wave Hindcast for the Australian Climate Service (WHACS)](https://data.csiro.au/collection/csiro:64350), which used ERA5 hourly winds and daily sea ice.

## ERA5 forcing fields

The ERA5 DATM configuration uses the following streams:

| Stream | ERA5 variable $\rightarrow$ CDEPS field | Treatment |
| --- | --- | --- |
| `ERA5.RAINC` | `cp` $\rightarrow$ `Faxa_rainc` | preceding-hour accumulation |
| `ERA5.RAINL` | `lsp` $\rightarrow$ `Faxa_rainl` | preceding-hour accumulation |
| `ERA5.SNOWC` | `csf` $\rightarrow$ `Faxa_snowc` | preceding-hour accumulation |
| `ERA5.SNOWL` | `lsf` $\rightarrow$ `Faxa_snowl` | preceding-hour accumulation |
| `ERA5.LWDN` | `strd` $\rightarrow$ `Faxa_lwdn` | preceding-hour accumulation |
| `ERA5.SWDN` | `ssrd` $\rightarrow$ `Faxa_swdn` | preceding-hour accumulation |
| `ERA5.SWNET` | `ssr` $\rightarrow$ `Faxa_swnet` | preceding-hour accumulation |
| `ERA5.SLP_10` | `msl` $\rightarrow$ `Sa_pslv`, `Sa_pbot` | instantaneous |
| `ERA5.T_10` | `t2m` $\rightarrow$ `Sa_t2m`, `Sa_tbot` | instantaneous |
| `ERA5.TDEW` | `d2m` $\rightarrow$ `Sa_tdew` | instantaneous |
| `ERA5.U_10` | `u10` $\rightarrow$ `Sa_u`, `Sa_u10m` | instantaneous |
| `ERA5.V_10` | `v10` $\rightarrow$ `Sa_v`, `Sa_v10m` | instantaneous |

The five instantaneous ERA5 fields are:

```text
msl
t2m
d2m
u10
v10
```

The seven accumulated fields are:

```text
cp
lsp
csf
lsf
strd
ssrd
ssr
```

None of the configured streams is an hourly-mean field.

## Time handling

ERA5 accumulated fields are timestamped at the **end** of the period they represent. For example, a precipitation value stamped at 07:00 represents the accumulation from 06:00 to 07:00.

For linear temporal interpolation, the accumulated fields are therefore shifted by:

```xml
<offset>-1800</offset>
```

This places the forcing value at the midpoint of the represented one-hour interval.

Instantaneous fields are already valid at their timestamps and use:

```xml
<offset>0</offset>
```

This treatment was established in [om3-scripts PR #122](https://github.com/ACCESS-NRI/om3-scripts/pull/122).

All ERA5 DATM streams currently use:

```xml
<tintalgo>linear</tintalgo>
```

for temporal interpolation.

## Spatial remapping

DATM reads ERA5 data on its source grid and passes the fields to the CMEPS mediator, where they are remapped onto the ACCESS-OM3 grid.

Accumulated flux fields use conservative remapping:

```text
consf
```

while instantaneous atmospheric state fields use patch remapping:

```text
patch
```

The current ERA5 DATM mesh is:

```text
/g/data/vk83/prerelease/configurations/inputs/access-om3/share/meshes/share/2026.07.30/ERA5-datm-ESMFmesh.nc
```

Within `datm.streams.xml`, the staged file is referenced as:

```xml
<meshfile>./INPUT/ERA5-datm-ESMFmesh.nc</meshfile>
```

## ERA5 CDEPS processing

The [ERA5 CDEPS data mode](https://github.com/ACCESS-NRI/CDEPS/blob/6a21caa1d2b6a47a10c77e8017045fa231f5a2ad/datm/datm_datamode_era5_mod.F90#L454-L459) performs several transformations before the atmospheric fields are passed to the coupled components.

`msl` is used for both:

```text
Sa_pslv
Sa_pbot
```

and `t2m` is used for:

```text
Sa_t2m
Sa_tbot
```

The 2 m dew-point temperature is combined with temperature and pressure to derive atmospheric humidity fields including:

```text
Sa_q2m
Sa_shum
```

CDEPS calculates air density using pressure, temperature and the derived humidity.

The atmospheric reference height:

```text
Sa_z
```

is set to 10 m. The forcing therefore combines 2 m temperature and humidity with 10 m winds.

Wind speed is derived from `u10` and `v10`.

### Radiation

ERA5 radiation variables are stored as accumulated energy in J m⁻² and divided by 3,600 s to obtain W m⁻².

For shortwave radiation, CDEPS partitions:

```text
ssrd / 3600
```

into four shortwave components:

- 28% visible direct;
- 31% near-infrared direct;
- 24% visible diffuse;
- 17% near-infrared diffuse.

ERA5 variables `aluvp`, `aluvd`, `alnip` and `alnid` are albedo-like quantities rather than shortwave flux bands and are therefore not used as these four components.

### Precipitation

ERA5 precipitation and snowfall accumulations are supplied in metres of water equivalent.

CDEPS multiplies these fields by freshwater density and divides by $3600\ \mathrm{s}$ to convert them to:

$$
\mathrm{kg\,m^{-2}\,s^{-1}}.
$$

## Forcing period

The forcing period is defined in `datm.streams.xml` using:

```xml
<year_first>...</year_first>
<year_last>...</year_last>
<year_align>...</year_align>
```

For interannual forcing, `year_align` is normally set equal to `year_first`, so forcing years align directly with model years.

The current ERA5 file collection spans the available yearly forcing files beginning in 1940. Users should confirm that files exist for the requested simulation period before starting an experiment.

The stream configuration uses:

```xml
<taxmode>extend</taxmode>
```

for interannual forcing. `extend` uses the nearest available endpoint field outside the configured time axis rather than cycling through the forcing period.

This behaviour should not be used as a substitute for selecting an appropriate scientific experiment period.

## ERA5 input preparation

The original ERA5 files available at NCI are not arranged optimally for ACCESS-OM3 model access.

Source files examined in [access-om3-configs issue #1381](https://github.com/ACCESS-NRI/access-om3-configs/issues/1381) used chunks of:

```text
(time, latitude, longitude) = (93, 91, 180)
```

The ACCESS-OM3 [ERA5 yearly rechunking script](https://github.com/ACCESS-NRI/om3-scripts/blob/main/era5_rechunking/make_era5_yearly_rechunked.py) converts the source data to:

```text
(time, latitude, longitude) = (1, 721, 1440)
```

and concatenates the monthly files into one yearly file for each forcing variable.

Because individual monthly ERA5 files can use different packing, the script decodes the source values before combining them, repacks the yearly file using a common `int16` encoding, and validates the decoded output against the packing tolerance.

The resulting files are stored under:

```text
/g/data/av17/access-nri/OM3/era5_rechunked_1h_yearly/
```

## Converting a JRA55-do configuration to ERA5

This section describes how to change an existing ACCESS-OM3 **JRA55-do interannual forcing configuration** to use ERA5 atmospheric forcing.

The conversion can be seen by comparing:

- [`dev-MC_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_100km_jra_iaf)
- [`dev-MCW_100km_era_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_era_iaf)

Only atmospheric forcing changes are described here.

Differences associated with WW3, model executables, PE layouts, queue selection or computational resources are unrelated to the JRA55-do → ERA5 forcing conversion.

!!! note

    ERA5 replaces only **DATM atmospheric forcing**.

    Runoff continues to use JRA55-do through DROF. The JRA55-do `land/` and `landIce/` inputs must therefore remain in the configuration.

The conversion requires changes to:

```text
datm_in
config.yaml
fd.yaml
datm.streams.xml
```

### 1. Change the DATM data mode

In `datm_in`, change:

```fortran
datamode = "JRA55do"
```

to:

```fortran
datamode = "ERA5"
```

No other change to `datm_in` is required.

### 2. Replace the DATM mesh

In the `input:` section of `config.yaml`, remove the JRA55-do DATM mesh:

```yaml
- /g/data/vk83/configurations/inputs/access-om3/share/meshes/share/2026.01.21/JRA55do-datm-ESMFmesh.nc
```

and add the ERA5 DATM mesh:

```yaml
- /g/data/vk83/prerelease/configurations/inputs/access-om3/share/meshes/share/2026.07.30/ERA5-datm-ESMFmesh.nc
```

This stages the mesh as:

```text
./INPUT/ERA5-datm-ESMFmesh.nc
```

which is the filename referenced by the ERA5 DATM streams.

### 3. Replace the atmospheric forcing inputs

Remove the JRA55-do atmospheric forcing directory:

```yaml
- /g/data/qv56/replicas/input4MIPs/CMIP6Plus/OMIP/MRI/MRI-JRA55-do-1-6-0/atmos/
```

and add the ACCESS-OM3 ERA5 forcing directory:

```yaml
- /g/data/av17/access-nri/OM3/era5_rechunked_1h_yearly/
```

Do **not** remove the JRA55-do runoff inputs:

```yaml
- /g/data/qv56/replicas/input4MIPs/CMIP6Plus/OMIP/MRI/MRI-JRA55-do-1-6-0/land/
- /g/data/qv56/replicas/input4MIPs/CMIP6Plus/OMIP/MRI/MRI-JRA55-do-1-6-0/landIce/
```

These are required by DROF.

The relevant forcing inputs should therefore resemble:

```yaml
input:
    # ERA5 atmospheric mesh
    - /g/data/vk83/prerelease/configurations/inputs/access-om3/share/meshes/share/2026.07.30/ERA5-datm-ESMFmesh.nc

    # JRA55-do runoff
    - /g/data/qv56/replicas/input4MIPs/CMIP6Plus/OMIP/MRI/MRI-JRA55-do-1-6-0/land/
    - /g/data/qv56/replicas/input4MIPs/CMIP6Plus/OMIP/MRI/MRI-JRA55-do-1-6-0/landIce/

    # ERA5 atmospheric forcing
    - /g/data/av17/access-nri/OM3/era5_rechunked_1h_yearly/
```

Other grid, initial-condition and model-component inputs are independent of this forcing conversion.

### 4. Update the field dictionary

Compared with the [`fd.yaml` files in the 25 km](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_25km_jra_iaf/fd.yaml) and [100 km](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_iaf/fd.yaml) JRA55-do configurations, ERA5 requires three additional atmospheric fields. Add these entries to the `atm import to med` section of `fd.yaml`:

```yaml
- standard_name: Sa_q2m
  alias: inst_spec_humid_height_lowest
  canonical_units: kg kg-1
  description: atm import to med - specific humidity at 2m
#
- standard_name: Sa_t2m
  alias: inst_temp_height_lowest
  canonical_units: K
  description: atm import to med - temperature at 2m
#
- standard_name: Sa_wspd10m
  alias: inst_wind_speed_height_lowest
  canonical_units: m s-1
  description: atm import to med - wind speed at 10m
```

The [ERA5 CDEPS data mode](https://github.com/ACCESS-NRI/CDEPS/blob/6a21caa1d2b6a47a10c77e8017045fa231f5a2ad/datm/datm_datamode_era5_mod.F90) advertises and populates these three fields; no other field-dictionary additions are required.

### 5. Generate `datm.streams.xml`

The ERA5 `datm.streams.xml` should be generated rather than edited manually.

Use [`generate_xml_datm_era5.py`](https://github.com/ACCESS-NRI/om3-scripts/blob/main/data_stream_xml_generation/generate_xml_datm_era5.py) from `om3-scripts`.

The script takes:

```text
YEAR_FIRST YEAR_LAST --input-base ERA5_DIRECTORY
```

For example:

```bash
python /g/data/vk83/apps/om3-scripts/data_stream_xml_generation/generate_xml_datm_era5.py \
    1940 2026 \
    --input-base /g/data/av17/access-nri/OM3/era5_rechunked_1h_yearly
```

This writes:

```text
datm.streams.xml
```

in the current working directory.

Choose `YEAR_FIRST` and `YEAR_LAST` to match the ERA5 forcing files required by the experiment.

For an interannual experiment where:

```text
YEAR_FIRST != YEAR_LAST
```

the generator sets:

```xml
<taxmode>extend</taxmode>
```

For a repeating-year experiment where:

```text
YEAR_FIRST == YEAR_LAST
```

the generator instead sets:

```xml
<taxmode>cycle</taxmode>
```

The generator also sets:

- the ERA5 stream names;
- ERA5 source-variable to CDEPS-field mappings;
- `ERA5-datm-ESMFmesh.nc` as the source mesh;
- conservative or patch spatial remapping;
- temporal interpolation;
- accumulated-field time offsets; and
- the requested forcing period.

### 6. Check the generated stream file

After generation, check that `datm.streams.xml` points to the staged ERA5 files.

For example:

```xml
<stream_info name="ERA5.U_10">
```

should contain files similar to:

```xml
<file>./INPUT/10u/10u_era5_oper_sfc_20200101-20201231.nc</file>
```

and should use:

```xml
<meshfile>./INPUT/ERA5-datm-ESMFmesh.nc</meshfile>
```

Accumulated streams should contain:

```xml
<offset>-1800</offset>
```

while instantaneous streams should contain:

```xml
<offset>0</offset>
```

### 7. Check the simulation period

The model start date must lie within the intended ERA5 forcing period.

For example, if `datm.streams.xml` contains:

```xml
<year_first>1940</year_first>
<year_last>2026</year_last>
<year_align>1940</year_align>
```

then:

```text
start_ymd = 19580101
```

falls within the forcing period.

Although `taxmode=extend` allows DATM to extend beyond the time axis, simulations should normally remain within the scientifically intended forcing period.

### Conversion summary

Converting JRA55-do atmospheric forcing to ERA5 requires:

```text
datm_in

datamode = "JRA55do"
          ↓
datamode = "ERA5"
```

```text
config.yaml

JRA55do-datm-ESMFmesh.nc
          ↓
ERA5-datm-ESMFmesh.nc
```

```text
config.yaml

JRA55-do atmos/
          ↓
/g/data/av17/access-nri/OM3/era5_rechunked_1h_yearly/
```

```text
fd.yaml

add Sa_q2m
add Sa_t2m
add Sa_wspd10m
```

and regenerating:

```text
datm.streams.xml
```

using:

```text
generate_xml_datm_era5.py
```

The following remain unchanged as part of the atmospheric forcing conversion:

```text
JRA55-do land/
JRA55-do landIce/
drof.streams.xml
DROF configuration
MOM6 grid
CICE6 grid
ocean initial conditions
```
