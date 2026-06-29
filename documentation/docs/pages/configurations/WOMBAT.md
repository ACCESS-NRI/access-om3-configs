# WOMBATlite Configurations

Configurations that include the WOMBATlite ocean biogeochemistry model have `+wombatlite` appended
to the branch name. WOMBATlite includes 15 tracers, two of which are optional. Key
features of the model include:

- Phytoplankton perform photo-acclimation by altering the chlorophyll to carbon ratios dynamically
according to the [@geider1997dynamic] formulation.
- Phytoplankton nutrient affinities vary as a function of mean cell size via observed allometric
relationships [@wickman2024eco].
- Light is split into blue, green and red wavelengths and attenuated at rates dependent on ambient
chlorophyll and detrital concentrations.
- Phytoplankton growth is limited by an internal quota model for iron [@droop198325], with
minimum quotas varying dynamically in response to the cellular demands for nitrate reduction,
respiration and chlorophyll content of the cell. This also allows for luxury uptake.
- The iron cycle follows a combination of [@aumont2015pisces] and [@tagliabue2023authigenic] to
reflect Fe chemistry (solubility, ligand binding), scavenging and colloidal coagulation.
- Zooplankton grazing assumes a Holling Type III functional form [@holling1959some] and active
switching between phytoplankton and particulate detrital prey types [@gentleman2003functional].
- Iron cycling through zooplankton routes Fe preferentially to egestion (i.e., faecal pellets)
following [@le2021fecal], enriching detritus in Fe.
- Calcium carbonate cycling includes dynamic production and dissolution mechanics as a function of
the ambient seawater carbonate chemistry. Production is affected by the substrate-inhibitor ratio
following [@lehmann2025global]. Dissolution occurs in both saturated (reducing particle
micro-environments) and undersaturated waters following [@kwon2024biological].
- The nitrogen cycle can be made to be open, with implicit schemes for nitrogen fixation and
denitrification switched on or off at run time.
- Sinking of particulates varies as a function of mean community cell/body size using the insights
of [@cael2021reconciling] and [@wickman2024eco], with CaCO3 concentrations also adding a ballasting
effect [@bach2016influence].
- Permanent burial of organics in sediments via [@dunne2007synthesis].
- External source of dissolved iron from aeolian deposition that includes mineral, fire and
anthropogenic sources [@hamilton2020impact].
- External sources of nitrate, DIC, alkalinity and detritus via rivers.
- Calibration and optimization of the model parameters to 8 global observational datasets
[@buchanan2025optimization].

For more information on the WOMBATlite model see the
[WOMBAT documentation](https://wombat-docs.readthedocs.io/stable/)

## Configuration parameters

ACCESS-OM3 configurations that include WOMBATlite use the default set of WOMBATlite namelist options
and parameters. A full list of options and parameters, including their default values, can be found
in the
[WOMBATlite documentation](https://wombat-docs.readthedocs.io/latest/Model_description/WOMBATlite_model_description/).

## External forcing

External forcing to WOMBATlite is provided using the `data_table` and includes:

- The concentration of CO2 in the atmosphere. This is a constant value in RYF configurations and an
annually-varying global mean in IAF configurations.
- The deposition flux of dissolved iron. This is a monthly climatology, derived from [@hamilton2020impact].
- The concentrations of nitrate, DIC, alkalinity and detritus in the river runoff. These are
currently constant values.

## Initial conditions

Initial conditions for key WOMBATlite tracers are derived from various sources:

- Nitrate: from [WOA23](https://www.ncei.noaa.gov/access/world-ocean-atlas-2023/) January data, with depths below 800m filled in from annual data
- Oxygen: from [WOA23](https://www.ncei.noaa.gov/access/world-ocean-atlas-2023/) January data, with depths below 1500m filled in from annual data
- Alkalinity: from [GLODAPv2](https://glodap.info/index.php/mapped-data-product/) mapped fields
- DIC: from [GLODAPv2](https://glodap.info/index.php/mapped-data-product/) mapped fields
- Iron: from [Huang 2022](https://zenodo.org/records/6994318)

Initial conditions for the remaining WOMBATlite tracers are global constants.