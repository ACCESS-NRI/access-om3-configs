## Adding a new configuration to ACCESS-OM3 configs 

### Scope
Regional MOM6 configurations (ACCESS-rOM3) are under active development at ACCESS-NRI and within the communities we collaborate with. Some of these configurations have a wider intereast and it will be benificial for these configurations to be supported and maintained at ACCESS-NRI in a similar manner to the global configurations (ACCESS-OM3). Here we provide protocol and guidance on how to include a regional configuration as a supported configuration. Including regional configurations will require ongoing upkeep and regional MOM6 configurations considered as candidates for inclusion as a supported config will need to minimises the upkeep overhead whist meeting a community need.

### What are the benifits?
WHen a configuration is supported by ACCESS-NRI then it is kept uptodate with the latest version of MOM6, including applying bug fixes, adding new features and upgrades. It will also give more visibilty to your configuration and allows for greater community input and collaboration.

### Criteria
We cannot support all regional MOM6 configurations as we do not have the capacity. The following criteria will be consider when desciding which configurations to support. There can be some flexibility in these criteria for the right configuration so if don't fit all criteria then we encourage you to discuss this with us. Conversly, we may need decline configurations that fit the criteria if we are already managing a large number of configurations. We encourage starting a conversation with us early on in the development of the configuration so we can plan ahead and assist in meeting the criteria.

#### Minimising overheads
The configuration files will need to match closly match an existing ACCESS-OM3 or ACCESS-rOM3 configuration to minimise the work needed to maintain. In particular, the configuration needs to be running on the NUOPC coupler, on Gadi and be able to interface with `payu`. With the exception of the MOM_input, MOM_override and config.yaml files, the expectation is that files will only differ from an existing configuration by one or two lines. The MOM_input can be very different in regional configurations due to the need to specify different parameter choises but the layout and order of these specifications should match layout and order of the ACCESS-OM3 configurations. The MOM_override file can be used to add further configuration options such boundary condition specifications. The config.yaml file will differ due to the need to specify different input files and executables but the layout of this file should closly match an ACCESS-OM3 configuration, including pointing to an ACCESS-NRI managed executable.  

#### Community interest
The configuration needs to be usfull for a broad section of the Australian research community and for a long period of time (min 3 years). Evidence of this could include:

   1. A previous similar domain was well utilised (i.e. a 5 km version was popular and you now want support for a 1km verson);
   2. There is a cross-institute grant or funding source (>3 years in length) that uses the configuration;
   3. There are already >5 people, across at least 2 institutions that are activly involved in the configuration;
   4. A survey of the community indicates a need;
   5. You are welcome to suggest other evidence of community interest.

#### Other criteria
There needs to be enough information provided so a user can run the configuration and have confidence that they know exactly what they are running. The extra information that needs to be avaliable for us to support a configuration is:

1. Documentation of the configuration
2. Input netcdf files will need metadata that inform of date and commands used to create the file.
3. Scripts and notebooks used to create the input files need to be avaliable in a public GitHub repository (or similar).
4. The branch name will need to follow the access-om3-configs [naming convention](https://github.com/ACCESS-NRI/access-om3-configs?tab=readme-ov-file#repository-structure)

Community members collaborating on a supported configuration should consider the development of scripts for model/data assessment (Hackathons are a great way to do this) and a plan to publish a manuscript to describe the configuration.

### Support length
There is a need to retire configurations when the become less utialised to create capacity for ACCESS-NRI to take on new configurations. 
Will will provide support initially for at least a 3 year period and potentially longer if there is an obvious ongoing need (e.g. it is supported by a grant that is >3 years). After this, the case for ongoing support with be revisited anually (unless a case is made for a longer revision period). Once a configuration is retired, it will still be avaliable for use by the communnity but updates will not occur. Community members are welcome to take over the management of these configurations. 

### Initial development of configuration
Configurations are not expected to initially meet the requirements for an ACCESS-NRI supported configuration. To develop your configuration you can fork access-om3-configs into your own repository. From there you can create a branch for your configuration and make the nessasary changes to your configurations. You can then create a draft pull request back to the access-om3-configs repository.

## Steps
To apply to have a configuration as a supported configuration then raise an issue on ACCESS-OM3 configs and describe your configuration and how it meets the criteria.
If your configurations does not meet the criteria for an access-supported model then it is still possible to share the model configurations, with a community member taking responsibility for maintaining the repository. Space for configuration files can be provided upon request on the [ACCESS-NRI community repository](https://github.com/ACCESS-Community-Hub). These configuration can still use ACCESS-NRI supported executable and `payu`.

