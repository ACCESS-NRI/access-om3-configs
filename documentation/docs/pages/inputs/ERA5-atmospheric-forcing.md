# ERA5 atmospheric forcing

[ERA5](https://confluence.ecmwf.int/spaces/CKB/pages/76414402/ERA5+data+documentation) is ECMWF's fifth-generation global atmospheric reanalysis. The [hourly single-level product](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview) used by ACCESS-OM3 is provided on a regular 0.25° × 0.25° latitude-longitude grid.

ACCESS-OM3 uses ERA5 through the CDEPS **DATM** component. ERA5 supplies atmospheric forcing only; runoff continues to be supplied from JRA55-do through **DROF**. See [Forcing data models](Forcing-data-models.md) for the coupling and runoff background, and [JRA55-do → ERA5 conversion](ERA5-conversion.md) for configuration changes.

The ACCESS-OM3-ready ERA5 files are currently stored on NCI at:

```text
/g/data/av17/access-nri/OM3/era5_rechunked_1h_yearly/
```

ERA5 forcing is currently used in the [`dev-MCW_100km_era_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_era_iaf) configuration. This allows evaluation of the coupled MOM6–CICE6–WW3 model using atmospheric forcing consistent with the [Wave Hindcast for the Australian Climate Service (WHACS)](https://data.csiro.au/collection/csiro:64350), which used ERA5 hourly winds and daily sea ice.

## ERA5 forcing fields

Each stream reads one ERA5 variable from its own subdirectory of `/g/data/av17/access-nri/OM3/era5_rechunked_1h_yearly/`.

| Stream | Directory | ERA5 variable | CDEPS field(s) | Description (`long_name`) | Treatment |
| --- | --- | --- | --- | --- | --- |
| `ERA5.RAINC` | `cp/` | `cp` | `Faxa_rainc` | Convective precipitation | preceding-hour accumulation |
| `ERA5.RAINL` | `lsp/` | `lsp` | `Faxa_rainl` | Large-scale precipitation | preceding-hour accumulation |
| `ERA5.SNOWC` | `csf/` | `csf` | `Faxa_snowc` | Convective snowfall | preceding-hour accumulation |
| `ERA5.SNOWL` | `lsf/` | `lsf` | `Faxa_snowl` | Large-scale snowfall | preceding-hour accumulation |
| `ERA5.LWDN` | `strd/` | `strd` | `Faxa_lwdn` | Surface long-wave (thermal) radiation downwards | preceding-hour accumulation |
| `ERA5.SWDN` | `ssrd/` | `ssrd` | `Faxa_swdn` | Surface short-wave (solar) radiation downwards | preceding-hour accumulation |
| `ERA5.SWNET` | `ssr/` | `ssr` | `Faxa_swnet` | Surface net short-wave (solar) radiation | preceding-hour accumulation |
| `ERA5.SLP_10` | `msl/` | `msl` | `Sa_pslv`, `Sa_pbot` | Mean sea level pressure | instantaneous |
| `ERA5.T_10` | `2t/` | `t2m` | `Sa_t2m`, `Sa_tbot` | 2 metre temperature | instantaneous |
| `ERA5.TDEW` | `2d/` | `d2m` | `Sa_tdew` | 2 metre dewpoint temperature | instantaneous |
| `ERA5.U_10` | `10u/` | `u10` | `Sa_u`, `Sa_u10m` | 10 metre U wind component | instantaneous |
| `ERA5.V_10` | `10v/` | `v10` | `Sa_v`, `Sa_v10m` | 10 metre V wind component | instantaneous |

None of the streams are hourly means.

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

The same temperature is also copied directly to potential temperature (`Sa_ptem`).

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

For shortwave radiation, CDEPS partitions `ssrd / 3600` into four components: 28% visible direct, 31% near-infrared direct, 24% visible diffuse and 17% near-infrared diffuse.

ERA5 variables `aluvp`, `aluvd`, `alnip` and `alnid` are albedo-like quantities rather than shortwave flux bands and are therefore not used as these four components.

### Precipitation

ERA5 precipitation and snowfall accumulations are supplied in metres of water equivalent.

CDEPS multiplies these fields by freshwater density and divides by 3,600 s to convert them to kg m⁻² s⁻¹.

## Forcing period

The configured file list spans 1940–2025. The forcing period is defined in `datm.streams.xml` using:

```xml
<year_first>1940</year_first>
<year_last>2025</year_last>
<year_align>1940</year_align>
```

For interannual forcing, `year_align` is normally set equal to `year_first`, so forcing years align directly with model years.

Users should confirm that files exist for the requested simulation period before starting an experiment.

The stream configuration uses:

```xml
<taxmode>extend</taxmode>
```

for interannual forcing. `extend` uses the nearest available endpoint field outside the configured time axis rather than cycling through the forcing period.

This behaviour should not be used as a substitute for selecting an appropriate scientific experiment period.

## ERA5 input preparation

The original ERA5 files replicated under NCI project `rt52` are not arranged optimally for ACCESS-OM3 model access.

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
