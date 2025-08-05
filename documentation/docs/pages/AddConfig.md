## Adding a new configuration to ACCESS-OM3 configs 

## Scope
Regional MOM6 configurations (ACCESS-rOM3) are under active development at ACCESS-NRI and within the communities we collaborate with. Some of these configurations have a wider intereast and it will be benificial for these configurations to be supported and maintained at ACCESS-NRI in a similar manner to the global configurations (ACCESS-OM3). Here we provide protocol and guidance on how to include a regional configuration as a supported configuration. Including regional configurations will require ongoing upkeep and regional MOM6 configurations considered as candidates for inclusion as a supported config will need to minimises the upkeep overhead whist meeting a community need.

## What benifits are there to having my configuration maintained by ACCESS-NRI?
- We will keep it updated to most recent version of MOM6;
- We may add improvements when they come to light;
- Gives more visibilty to your configuration and allows for greater community input and collaboration.


## Criteria
These criteria guidlines rather than something we will stricly adhear to. We have them as a starting point for a discussion and to give an indication on what we are looking for in a configuration. If you have a configuration that fills a community need but might be quite fit all these criteria then we invite you to still consider submitting for a managed configuration. Conversly, we may need to become more choosy, or delay taking on the management of configurations that fit the criteria if we are already managing a large number of configurations. We encourage opening an issue and having a conversation with us early on in the development of the configuration so we can plan ahead on our capacity to take on new configurations and to provide you advice on developing your configuration. If we do not accept your configuration as a supported configuration we will provide you with a reason.

### Minimising overheads
The configuration files will need to match as closly as possible to an existing ACCESS-OM3 or ACCESS-rOM3 configuration to minimise the work needed to maintain. In particular, the configuration needs to be running on the NUOPC coupler, on Gadi and be able to interface with `payu`. With the exception of the MOM_input, MOM_override and config.yaml files, the expectation is that files will only differ from an existing configuration by one or two lines. It is expected that the MOM_input will be very different in regional configurations due to the need to specify different parameter choises but the layout and order of these specifications should match layout and order of the ACCESS-OM3 configurations. The MOM_override file can be used to add configuration options that are not in the ACCESS-OM3 MOM_input file such boundary condition specifications. config.yaml will differ due to the need to specify different input files and executables but the layout of this file should closly match an ACCESS-OM3 configuration, including pointing to an ACCESS-NRI managed executable.  

### Community interest criteria
The configuration needs to be usfull for a broad section of the Australian research community and for a long period of time (min 3 years). Evidence of this could include:

   1. A previous similar domain was well utilised (i.e. a 5 km version was well used and exdpanding computing capacity means a similar 1km resolution is now feasible to run);
   2. There is a cross-institute grant or funding source (>3 years in length) that uses the configuration;
   3. There are already >5 people, across at least 2 institutions that are activly involved in the configuration (i.e. draft/published manuscripts /git commits or conference presentations);
   4. A survey of the community indicated a need;
   5. You are welcome to provide other evidence of community interest.

### Other criteria
There needs to be enough information provided so a user can run the configuration and have confidence that they know exactly what they are running. The extra information that needs to be avaliable to be considered as a supported configuration should include:

1. Documentation of the configuration
2. Input netcdf files will need metadata that inform of the file's provenance (e.g. information on the commands used to make the file, the version of the scripts used and the date the file was made.)
3. Scripts and notebooks used to create the input files need to be avaliable in a public GitHub repository (or similar)

This is not essential for inclusion as a supported configuration but community members collaborating on this configuration should consider the development of scripts for model/data assessment (Hackathons are a great way to do this) and publish a manuscript to describe the configuration.

## Support length
There is a need to retire configurations when the become less utialised to create capacity for ACCESS-NRI to take on new configurations 
Will will provide support initially for at least a 3 year period, potentially longer if there is an obvious ongoing need (e.g. it is supported by a grant that is >3 years). After this, the case for ongoing support with be revisited anually (unless a case is made for and longer revision period). Once a configuration is retired, it will still be avaliable for use by the communnity but updates will not occur so the configuration will be out of date and will eventaually become unuable. Community members are welcome to take over the management of these configurations. 

## Initial development of configuration
Configurations are not expected to initially meet the requirements for an ACCESS-NRI supported configuration. TO develop your configuration you can branch access-om3-configs into your own repository. From there you can create a branch for your configuration and make the nessasary changes to your configurations. 

## Steps
To apply to have a configuration as a supported configuration then raise an issue on ACCESS-OM3 configs and describe your configuration and how it meets the criteria.
If your configurations does not meet the criteria for an access-supported model then it is still possible to share the model configurations, with a community member taking responsibility for maintaining the repository. Space can be provided on 
@claireyung / @helenmacdonald to fill in please!

## Aditional reading:

- 
- 

## References


