# MOM6-CICE6-WW3 1 deg JRA CESM configuration

**WARNING: This configuration is to be used for testing purposes only.**

This configuration is adapted from an officially-unsupported CESM configuration
(The CIME GMOM_JRA_WD "compset"). It was generated using a fork of
[CESM](https://github.com/COSIMA/CESM) with the following commands:

```bash
git clone https://github.com/COSIMA/CESM
cd CESM/cime/scripts
./create_newcase --case my_case --compset GMOM_JRA_WD --res T62_g16 --machine gadi --run-unsupported
cd my_case
./case.setup
```
The configuration was then adapted to run with ACCESS-OM3 using payu.

See [`main` branch
README](https://github.com/COSIMA/MOM6-CICE6-WW3/blob/main/README.md) for usage
information.

## Features

- data atmosphere (DATM) = JRA v1.3 (NB: not JRA55-do), 1958-2016, no-leap calendar
- data runoff (DROF) = JRA v1.1 (NB: not JRA55-do), 1958-2016, no-leap calendar
- displaced pole grid

## Requirements

This configuration requires payu v1.0.29 or greater to run correctly.
