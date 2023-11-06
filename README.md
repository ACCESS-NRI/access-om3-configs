# MOM6-CICE6-WW3 1 deg JRA55-do RYF ACCESS-OM3 configuration

<<<<<<< HEAD
data atmosphere (datm) = JRA v1.3 (NB: not JRA55-do), 1958-2016, no-leap calendar

data runoff (drof) = JRA v1.1 (NB: not JRA55-do), 1958-2016, no-leap calendar

Note:
- **This is an untested Payu configuration for an untested CESM configuration**. This configuration is adapted from an officially-unsupported CESM configuration (The CIME GMOM_JRA_WD "compset").
- This configuration uses a Payu driver that does not currently exist in the main Payu repo. We're working to include it, but in the meantime those wanting to play with this configuration will need to use the version of Payu in [this](https://github.com/dougiesquire/payu/tree/cesm_cmeps) branch - see instructions [here](https://github.com/COSIMA/access-om3/issues/15#issuecomment-1463219077).
- No effort has (yet) been put into optimising the PE layout of this configuration on Gadi - currently each model component simply runs sequentially and is allocated an entire node.
- The executable used by this configuration was built using CIME (see [here](https://forum.access-hive.org.au/t/cesm-configurations-on-gadi-using-cime/115) for setup details):
  ```bash
  cd cime/scripts
  ./create_newcase --case my_case --compset GMOM_JRA_WD --res T62_g16 --machine gadi --run-unsupported
  cd my_case
  ./case.setup
  ./case.build
  ```
- By default, this configuration will advance 1 month per model run
=======
**WARNING: This configuration is still under development and should not be used for production.**

See [`main` branch
README](https://github.com/COSIMA/MOM6-CICE6-WW3/blob/main/README.md) for usage
information.

## Features

- data atmosphere (DATM) = JRA55-do v1-4, RYF 1990-1991
- data runoff (DATM) = JRA55-do v1-4, RYF 1990-1991
- tripolar grid

## Requirements

This configuration requires payu v1.0.29 or greater to run correctly.
>>>>>>> 07169be5f6655852f4b8704229346fa1fd03a28e
