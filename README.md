#### MOM6-CICE6 025 deg JRA55-do RYF ACCESS-OM3 configuration

# *converted into an 8km regional pan-Antarctic configuration!!*

see https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc/panantarctic_instructions.md for steps used to make panan configuration

MOM_input uses this commit c33a731 https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_25km_jra_ryf/MOM_input (similar to GFDL OM5)
Added MOM_override_newparams with some choices from high res/panan

**WARNING: This configuration is still under development and should not be used for production.**

See [`main` branch
README](https://github.com/COSIMA/MOM6-CICE6/blob/main/README.md) for usage
information.

## Features

- data atmosphere (DATM) = JRA55-do v1-4, RYF 1990-1991
- data runoff (DROF) = JRA55-do v1-4, RYF 1990-1991
- tripolar grid

## Requirements

This configuration requires [Payu](https://github.com/payu-org/payu) > v1.1.3 to run.
