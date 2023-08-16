# Payu configuration for 1 deg MOM6-CICE6-WW3-datm-drof configuration using CMEPS with the CESM driver

**WARNING: This configuration is to be used for testing purposes only.**

This configuration is adapted from an officially-unsupported CESM configuration
(The CIME GMOM_JRA_WD "compset"). It was generated using a fork of
[CESM](https://github.com/COSIMA/CESM) with following commands:
```bash
git clone https://github.com/COSIMA/CESM
cd CESM/cime/scripts
./create_newcase --case my_case --compset GMOM_JRA_WD --res T62_g16 --machine gadi --run-unsupported
cd my_case
./case.setup
```
The configuration was then adapted to run with ACCESS-OM3 using payu.
