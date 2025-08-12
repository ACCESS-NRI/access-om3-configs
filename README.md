## MOM6-CICE6 1/12th deg JRA55-do RYF regional pan-Antarctic ACCESS-OM3 configuration

See https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc2-sapphirerapid-Charrassin-newparams-rerun-Wright-spinup-accessom2IC-yr9/panantarctic_instructions.md for detailed steps used to make panan configuration

`MOM_input` uses this commit c33a731 from https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_25km_jra_ryf/MOM_input (similar to GFDL OM5)

Added `MOM_override_newparams` with some choices from COSIMA MOM6-SIS2 panan and high resolution GFDL regional models

**WARNING: This configuration is still under development and should not be used for production.**

See [`main` branch
README](https://github.com/COSIMA/MOM6-CICE6/blob/main/README.md) for usage
information.

## Features

- data atmosphere (DATM) = JRA55-do v1-4, RYF 1990-1991
- data runoff (DROF) = JRA55-do v1-4, RYF 1990-1991
- pan-Antarctic domain with open boundary conditions at 37.5 degrees S
## Requirements

This configuration requires [Payu](https://github.com/payu-org/payu) > v1.1.3 to run.
