{% set run_access_om3 = "https://docs.access-hive.org.au/models/run-a-model/run-access-om3/" %}

# Home

Welcome to the documentation for the [ACCESS-OM3 ocean-seaice model configurations](https://github.com/ACCESS-NRI/access-om3-configs)! 

ACCESS-OM3 is the third generation of the ACCESS global ocean - sea ice model. It uses up-to-date releases of the [MOM6](https://github.com/ACCESS-NRI) ocean model and [CICE6](https://github.com/ACCESS-NRI/CICE) sea ice model. It is the first ACCESS model that couples model components using CMEPS ([Community Mediator for Earth Prediction Systems](https://escomp.github.io/CMEPS/versions/master/html/index.html)), built on top of NUOPC ([National Unified Operational Prediction Capability](https://earthsystemmodeling.org/nuopc/)) infrastructure.

## ACCESS-OM3 Quickstart 
If you would like to simply run the model, see the [How to Run ACCESS OM3 documentation](https://docs.access-hive.org.au/models/run-a-model/run-access-om3/). 

<div class="text-card-group" markdown>
[![Hive](assets/ACCESS_icon_HIVE.png){: class="icon-before-text"} Run ACCESS-OM3]({{run_access_om3}}){: class="text-card" target="_blank" rel="noopener"}
</div>

## ACCESS-OM3 Documentation Overview

See the navigation links on the left. Some reading tips, see:

 - [Contributing](/contributing) if you'd like to get involved / provide feedback on ACCESS-OM3;
 - [Inputs](/inputs/Forcing-data-models) if you would like to understand how the input files are generated;
 - [Configuration choices/Configurations](/configurations/Overview/) for information/background about specific configurations. The remaining sub-sections in `Configuration choices` provide background on key files and background on how ACCESS-OM3 configurations work/can be customised. **These parts are likely of most interest to users.**
 - [Infrastructure](/infrastructure/Architecture/) is likely of more interest to ACCESS-NRI staff and developers. Having said this, some users, might find pages such as `Architecture` useful background.

## ACCESS-OM3-Configs Overview
ACCESS-OM3 configurations are provided via branches in the [access-om3-configs](https://github.com/ACCESS-NRI/access-om3-configs) GitHub repository. The [access-om3-configs](https://github.com/ACCESS-NRI/access-om3-configs) repository contains several configurations using the following components:

- [MOM6](https://mom6.readthedocs.io/) ocean model
- [CICE](https://cice-consortium-cice.readthedocs.io/en/) sea ice model
- [WW3](https://github.com/NOAA-EMC/WW3/wiki/About-WW3) wave model
- [DATM](https://escomp.github.io/CDEPS/versions/master/html/datm.html) atmosphere data model
- [DROF](https://escomp.github.io/CDEPS/versions/master/html/drof.html) runoff data model

All the configurations use the [Payu](https://payu.readthedocs.io/en/latest/) workflow management tool, and pre-built executables available on [NCI](https://nci.org.au/).

### Repository structure

The [`main`](https://github.com/ACCESS-NRI/access-om3-configs/tree/main) branch does not store any model configurations, only documentation.

Each configuration in [github.com/ACCESS-NRI/access-om3-configs](https://github.com/ACCESS-NRI/access-om3-configs) repository is stored as a git branch. Most of the branches are named
according to the following naming scheme:

`{dev|release}-{MODEL_COMPONENTS}_{nominal_resolution}km_{forcing_data}_{forcing_method}[+{modifier}]`

where `{MODEL_COMPONENTS}` is an acronym specifying the active model components in the following order:

- `M`: MOM6
- `C`: CICE6
- `W`: WW3
- `r` : a regional configuration
  
and the nominal resolution is given in kilometers, corresponding to the nominal resolution in degrees as follows:

- `100km`: 1°
- `25km`: 0.25°
- `10km`: 0.1°
- `8km`: 1/12°

For regional configurations, a short word describing the location of the domain is included after the nominal resolution. For example:

- `tas5km`:    5km resolution around Tasmainia
- `superoz4km` 4km resolution around Australia
   
Additional configuration information, like if the configuration includes biogeochemistry, is appended to the name as a modifier, e.g.

- `+wombatlite` if the configuration uses WOMBATlite

Currently the following released configurations are available:

- [`release-MC_100km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/release-MC_25km_jra_ryf)

Currently the following development configurations are available:

**MOM6-CICE6-DATM-DROF configurations**

- [`dev-MC_100km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_100km_jra_ryf)
- [`dev-MC_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_100km_jra_iaf)
- [`dev-MC_100km_jra_ryf+wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_100km_jra_ryf+wombatlite)
- [`dev-MC_25km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_25km_jra_ryf)
- [`dev-MC_25km_jra_ryf+wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_25km_jra_ryf+wombatlite)

**MOM6-CICE6-WW3-DATM-DROF configurations**

- [`dev-MCW_100km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_jra_ryf)
- [`dev-MCW_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_jra_iaf)

!!! warning
    These `dev_*` configurations are still under development and should **not** be used for production runs.

### Comparison table
The following links can be used to easily compare different configuration branches

**MC → MC**

- [`release-MC_25km_jra_ryf`⬅️`dev-MC_25km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/release-MC_25km_jra_ryf..dev-MC_25km_jra_ryf)
- [`dev-MC_100km_jra_ryf`⬅️`dev-MC_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf..dev-MC_100km_jra_iaf)
- [`dev-MC_100km_jra_ryf`⬅️`dev-MC_100km_jra_ryf+wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf..dev-MC_100km_jra_ryf+wombatlite)
- [`dev-MC_100km_jra_ryf`⬅️`dev-MC_25km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf..dev-MC_25km_jra_ryf)
- [`dev-MC_100km_jra_ryf+wombatlite`⬅️`dev-MC_25km_jra_ryf+wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf+wombatlite..dev-MC_25km_jra_ryf+wombatlite)
- [`dev-MC_25km_jra_ryf`⬅️`dev-MC_25km_jra_ryf+wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_25km_jra_ryf..dev-MC_25km_jra_ryf+wombatlite)

**MCW → MCW**

- [`dev-MCW_100km_jra_ryf`⬅️`dev-MCW_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MCW_100km_jra_ryf..dev-MCW_100km_jra_iaf)

**MC → MCW**

- [`dev-MC_100km_jra_ryf`⬅️`dev-MCW_100km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf..dev-MCW_100km_jra_ryf)
- [`dev-MC_100km_jra_iaf`⬅️`dev-MCW_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_iaf..dev-MCW_100km_jra_iaf)

