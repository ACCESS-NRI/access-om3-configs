# JRA55-do → ERA5 conversion

This page describes how to change an existing ACCESS-OM3 **JRA55-do interannual forcing configuration** to use [ERA5 atmospheric forcing](ERA5-atmospheric-forcing.md). See [Forcing data models](Forcing-data-models.md) for the existing JRA55-do atmosphere and runoff treatment.

The conversion can be seen by comparing:

- [`dev-MC_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_100km_jra_iaf)
- [`dev-MCW_100km_era_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_era_iaf)

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

## 1. Change the DATM data mode

In `datm_in`, change:

```fortran
datamode = "JRA55do"
```

to:

```fortran
datamode = "ERA5"
```

No other change to `datm_in` is required.

## 2. Replace the DATM mesh

In the existing `input:` list in `config.yaml`, replace only the JRA55-do **DATM atmospheric** mesh:

```yaml
- /g/data/vk83/configurations/inputs/access-om3/share/meshes/share/2026.01.21/JRA55do-datm-ESMFmesh.nc
```

with the ERA5 DATM mesh:

```yaml
- /g/data/vk83/prerelease/configurations/inputs/access-om3/share/meshes/share/2026.07.30/ERA5-datm-ESMFmesh.nc
```

Retain the existing **DROF runoff** mesh, `JRA55do-drof-ESMFmesh.nc`, unchanged. The [ERA5 configuration](https://github.com/ACCESS-NRI/access-om3-configs/blob/d84b1acaf4b509052fdffd2718af57bc9b8b6161/config.yaml#L38-L39) stages both the ERA5 DATM mesh and the JRA55-do DROF mesh.

This stages the mesh as:

```text
./INPUT/ERA5-datm-ESMFmesh.nc
```

which is the filename referenced by the ERA5 DATM streams.

## 3. Replace the atmospheric forcing inputs

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

Apply these replacements to the existing `input:` list; the snippets above show individual entries, not a complete replacement list. Retain all other inputs, including the DROF mesh, runoff data, grids and initial conditions.

## 4. Update the field dictionary

Compared with the [`fd.yaml` files in the 25 km](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_25km_jra_iaf/fd.yaml) and [100 km](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_iaf/fd.yaml) JRA55-do configurations, the [ERA5 CDEPS data mode](https://github.com/ACCESS-NRI/CDEPS/blob/6a21caa1d2b6a47a10c77e8017045fa231f5a2ad/datm/datm_datamode_era5_mod.F90#L105-L120) requires three additional atmospheric fields. Add these entries to the `atm import to med` section of `fd.yaml`:

```yaml
- standard_name: Sa_q2m
  alias: inst_spec_humid_height_lowest
  canonical_units: kg kg-1
  description: atm import to med - specific humidity at 2 m
#
- standard_name: Sa_t2m
  alias: inst_temp_height_lowest
  canonical_units: K
  description: atm import to med - temperature at 2 m
#
- standard_name: Sa_wspd10m
  alias: inst_wind_speed_height_lowest
  canonical_units: m s-1
  description: atm import to med - wind speed at 10 m
```

The current ERA5 configuration's `fd.yaml` also contains [`Sa_shum_wiso`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MCW_100km_era_iaf/fd.yaml#L393-L396), but this is not required for the standard ERA5 conversion. The pinned ERA5 CDEPS data mode does not advertise or populate that field, and the configuration sets [`flds_wiso = .false.`](https://github.com/ACCESS-NRI/access-om3-configs/blob/d84b1acaf4b509052fdffd2718af57bc9b8b6161/nuopc.runconfig#L95). `Sa_shum_wiso` is only relevant when water-isotope coupling is enabled; with it disabled, no other field-dictionary additions are required.

## 5. Generate `datm.streams.xml`

The ERA5 `datm.streams.xml` should be generated rather than edited manually.

Use [`generate_xml_datm_era5.py`](https://github.com/ACCESS-NRI/om3-scripts/blob/main/data_stream_xml_generation/generate_xml_datm_era5.py) from `om3-scripts`.

The script takes:

```text
YEAR_FIRST YEAR_LAST --input-base ERA5_DIRECTORY
```

For example:

```bash
python /g/data/vk83/apps/om3-scripts/data_stream_xml_generation/generate_xml_datm_era5.py \
    1940 2025 \
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

## 6. Check the generated stream file

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

## 7. Check the simulation period

The model start date must lie within the intended ERA5 forcing period.

For example, if `datm.streams.xml` contains:

```xml
<year_first>1940</year_first>
<year_last>2025</year_last>
<year_align>1940</year_align>
```

then:

```text
start_ymd = 19580101
```

falls within the forcing period.

Although `taxmode=extend` allows DATM to extend beyond the time axis, simulations should normally remain within the scientifically intended forcing period.
