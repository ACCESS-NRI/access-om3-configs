# Ocean diagnostics

Ocean diagnostics in MOM6 are configured via the `diag_table` file, which controls all runtime diagnostic output. Full details of the `diag_table` format and semantics are available in the [MOM6 docs](https://mom6.readthedocs.io/en/main/api/generated/pages/Diagnostics.html). This documentation focuses specifically on the diagnostic filename conventions used by ACCESS-OM3 configurations.

## `diag_table` Structure
The `diag_table` consists of three sections: `<title>`, `<file>`, and `<field>`.

- The title section is mandatory. It appears at the top of the file and consists of a title string and a reference date specified by 6 integers.
- The file section defines diagnostic output files and their output frequency. Each file entry may contain one or more diagnostic fields.
- The field section defines individual diagnostic fields. Because MOM6 is a general-coordinate model, diagnostics may be written either in the native model coordinate system, or in user-defined (remapped) coordinates.

## ACCESS file name naming schemes
The diagnostic filename conventions used by ACCESS-OM3 configurations are summarised [here](https://github.com/ACCESS-NRI/access-om3-configs/issues/374#issuecomment-2750096126). At a high level, diagnostic files follow the pattern:
```
<file_prefix>.<model>.<dimension_or_mode>.<field_or_mode>[.<vertical_coordinate>][.<d2>].<frequency>.<time_cell_method>.<datestamp>.nc
```

!!! tip Although several components are shown as optional, not all combinations are valid. In practice, filenames fall into a small number of well-defined cases, described below.

### Common components
- `<file_prefix>`: Always `access-om3`,
- `<model>`: Always `mom6` for the ocean model,
- `<dimension_or_mode>`: 
    - One of `2d` or `3d` for spatial diagnostics,
    - `static` for static 2D grid data,
    - `scalar` for (`0d`) scalar diagnostics,

### Field name or mode token
- `<field_or_mode>`
    - For standard `2d` / `3d` diagnostics, this is the diagnostic field name.
    - For special cases:
        - `static` files do not include a field name,
        - `scalar` files do not include a field name and instead contain multiple scalar diagnostics in a single file.

!!! tip The ACCESS-OM3 convention is to write one physical field per file, except in the two special cases above.

### Temporal components
- `frequency`: The output interval between records, specified using MOM/FMS frequency strings, such as "1day", "3hour", "1month" etc
- `<time_cell_method>`: Specifies how values are accumulated within each output interval, such as "mean", "max", "min", "snap" etc.
- `<datestamp>`: Uses FMS time-string formatting, such as "%4yr" (4-digit year), other options can be "%dy" (day), "%mo" (month), "%hr" (hour), "%mn" (minute), "%sc" ("second") etc.

### Optional spatial components
- `<vertical_coordinate>`: Is included only for non-native vertical coordinates, such as `z`, `rho2` etc
- `<d2>`: Indicates half-resolution (downsampling) diagnostics. This is only supported for standard `2d` / `3d` spatial diagnostics and requires:
    - `NIGLOBAL` / `Layout_X` divisible by 2
    - `NJGLOBAL` / `Layout_Y` divisible by 2

    where `NIGLOBAL` and `NJGLOBAL` are the global horizontal grid sizes, and `Layout_X`, `Layout_Y` are the processor layouts. Related issue was discussed [here](https://github.com/ACCESS-NRI/access-om3-configs/issues/539).

### Practical filename cases
In practice, ACCESS-OM3 uses three distinct filename classes.

#### 1. Standard 2D / 3D diagnostics (most common)
```
access-om3.mom6.<2d|3d>.<field_name>
[.<vertical_coordinate>][.d2].<frequency>.<time_cell_method>.<datestamp>.nc
```

Example:
```
access-om3.mom6.3d.thkcello.rho2.d2.1mon.mean.1990.nc
```
Charateristics:

- One `2d` or `3d` diagnostic field per file,
- Applies to spatial diagnostics on the native model grid (`2d`, `3d`),
- `<vertical_coordinate>` is included only for non-native vertical coordinates (e.g. `z`, `rho2`),
- `d2` indicates half-resolution output and is supported only for standard `2d` / `3d` diagnostics.
- Not valid for `static` or `scalar` outputs.

#### 2. Static grid diagnostics
Static grid variables are written once per run and grouped into a single file.
```
access-om3.mom6.static.nc
```
Characteristics:

- No field name,
- No frequency, time method, or datestamp,
- No `d2` support
- Contains multiple static grid variables

#### 3. Scalar (global integral) diagnostics
Global scalar diagnostics are grouped into a single file.
```
access-om3.mom6.scalar.<frequency>.<time_cell_method>.<datestamp>.nc
```

Example:

```
access-om3.mom6.scalar.1day.snap.1990.nc
```

Characteristics:

- No field name
- No `d2` support
- Contains multiple scalar diagnostics (e.g. `masso`, `soga`, `thetaoga`, `tosga`)
