# Experimental Payu configuration for 1 deg MOM6-CICE6-WW3-datm-drof configuration using CMEPS with the CESM driver

data atmosphere (datm) = JRA v1.3 (NB: not JRA55-do), 1958-2016, no-leap calendar

data runoff (drof) = JRA v1.1 (NB: not JRA55-do), 1958-2016, no-leap calendar

Note:
- **This is an untested Payu configuration for an untested CESM configuration**. This configuration is adapted from an officially-unsupported CESM configuration (The CIME GMOM_JRA_WD "compset").
- This configuration uses a Payu driver that does not currently exist in the main Payu repo. We're working to include it, but in the meantime those wanting to play with this configuration will need to use the version of Payu in [this](https://github.com/dougiesquire/payu/tree/cesm_cmeps) branch.
- No effort has (yet) been put into optimising the PE layout of this configuration on Gadi - currently each model component simply runs sequentially and is allocated an entire node.
- The execuatable used by this configuration was built using CIME (see [here](https://forum.access-hive.org.au/t/cesm-configurations-on-gadi-using-cime/115) for setup details):
  ```bash
  cd cime/scripts
  ./create_newcase --case my_case --compset GMOM_JRA_WD --res T62_g16 --machine gadi --run-unsupported
  cd my_case
  ./case.setup
  ./case.build
  ```
- By default, this configuration will advance 1 month per model run
