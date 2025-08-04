## Adding a new configuration to ACCESS-OM3 configs 

### Scope
Regional MOM6 configurations (ACCESS-rOM3) are under active development at ACCESS-NRI and within the communities we collaborate with. Some of these configurations have a wider intereast and it will be benificial for these configurations to be supported and maintained at ACCESS-NRI in a similar manner to the global configurations (ACCESS-OM3). Here we provide protocol and guidance on how to include a regional configuration as a supported configuration. Including regional configurations will require ongoing upkeep and regiona MOM6 configurations considered as candidates for inclusion as a supported config will need to minimises the upkeep overhead whist meeting a community need.

### What benifits are there to having my configuration maintained by ACCESS-NRI?
- we will keep it updated to most recent version of MOM6
- We may add improvements when they come to light
- Gives more visibilty to your configuration and allows for greater community input and collaboration
- 


## Criteria
### Minimising overheads
The configuration files will need to match as closly as possible to an existing ACCESS-OM3 or ACCESS-rOM3 configuration. With the exception of the MOM_input, MOM_override and config.yaml files, the expectation is that files will only differ by one or two lines. It is expected that the MOM_input will be very different in regional configurations due to the need to specify different parameter choises but the layout and order of these specifications should match layout and order of the ACCESS-OM3 configurations. The MOM_override file can be used to add configuration options that are not in the ACCESS-OM3 MOM_input file such boundary condition specifications.

config.yaml will differ due to the need to specify different input files and executables but the layout of this file should closly match an ACCESS-OM3 configurations.

### Community interest criteria
 - there needs to be evidence that there is a large long-term (>3 years) community need for the configuration.  
 - Evidence could include
   1) A previous similar domains well utilised (i.e. a 5 km version of this configuration was popular but you are upgrading to 1km resolution)
   2) There is a cross-institute
   3) There are already >5 people, across at least 2 institutions that are activly involved in this (i.e. draft/published manuscripts or conference presentations) 
 - Ease of support (where possible needs to be aligned with existing X configuration or support is limited). 

### other
- doc description of what they are providing (stubby system)
- input files with provenance (e.g. metadata that help you make the file)

## Support
- will will provide support initially for at lease a 3 year period and then the case for ongoing support with be revisited at regular intervales (annually or longer) 
 - Length of time we provide support / updates for


## OSIT thoughts
 - If they have submitted data to intake/shared data?
 - an ACCESS-NRI executable
 - input files with provenance (e.g. metadata that help you make the file)
 - community interest/engagement in the application
 - doc description of what they are providing (stubby system)

## initial development of configuration
Configurations are not expected to initially meet the requirements

## Steps
To apply to have a configuration as a supported configuration then raise an issue on ACCESS-OM3 configs and describe your configuration and how it meets the criteria .
If your configurations does not meet the criteria for an access-supported model then it is still possible to share the model configurations, with a community member taking responsibility for maintaining the repository. A regional MOM configuration that is based on an access-om3 or access-rom3 conf 
@claireyung / @helenmacdonald to fill in please!

## Aditional reading:

- 
- 

## References


