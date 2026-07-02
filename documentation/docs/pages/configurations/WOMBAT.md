# WOMBATlite Configurations

Configurations that include the WOMBATlite ocean biogeochemistry model have `+wombatlite` appended
to the branch name. WOMBATlite includes 15 tracers, two of which are optional. Key
features of WOMBATlite and detailed documentation can be found in the
[WOMBAT documentation](https://wombat-docs.readthedocs.io/2026.05.001/Model_description/WOMBATlite_model_description/).

## Configuration parameters

ACCESS-OM3 configurations that include WOMBATlite use the default set of WOMBATlite namelist options
and parameters. A full list of options and parameters, including their default values, can be found
in the
[WOMBATlite documentation](https://wombat-docs.readthedocs.io/2026.05.001/Model_description/WOMBATlite_model_description/#parameter-set-and-default-values).

## External forcing

External forcing to WOMBATlite is provided using the `data_table` and includes:

- The concentration of CO2 in the atmosphere. This is a constant value in RYF configurations and an
annually-varying global mean in IAF configurations.
- The deposition flux of dissolved iron. This is a monthly climatology, derived from [@hamilton2020impact].
- The concentrations of nitrate, DIC, alkalinity and detritus in the river runoff. These are
currently constant values.

## Initial conditions

Initial conditions for key WOMBATlite tracers are derived from various sources:

- Nitrate: from [WOA23](https://www.ncei.noaa.gov/access/world-ocean-atlas-2023/) January data, with depths below 800m filled in from annual data.
- Oxygen: from [WOA23](https://www.ncei.noaa.gov/access/world-ocean-atlas-2023/) January data, with depths below 1500m filled in from annual data.
- Alkalinity: from [GLODAPv2](https://glodap.info/index.php/mapped-data-product/) mapped fields.
- DIC: from [GLODAPv2](https://glodap.info/index.php/mapped-data-product/) mapped fields.
- Iron: from [Huang et al. (2022)](https://zenodo.org/records/6994318).

Initial conditions for the remaining WOMBATlite tracers are global constants. See the
[generation script](https://github.com/ACCESS-NRI/om3-scripts/blob/main/wombat_ic_generation/generate_wombat_ic.py)
for full details of how the initial conditions are defined.
