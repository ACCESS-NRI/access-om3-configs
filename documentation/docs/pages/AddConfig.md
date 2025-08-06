## Adding a new configuration to ACCESS-OM3 configs 

### Scope
Regional MOM6 configurations (ACCESS-rOM3) are under active development at ACCESS-NRI and within the communities we collaborate with. Some of these configurations have a wider interest and it will be beneficial for these configurations to be supported and maintained at ACCESS-NRI in a similar manner to the global configurations (ACCESS-OM3). Here we provide protocol and guidance on how apply to have your regional configuration supported by ACCESS-NRI. 

### What are the benifits?
When a configuration is supported by ACCESS-NRI then it is kept up to date with the latest version of MOM6, including applying bug fixes, adding new features and upgrades. It will also give more visibility to your configuration and allows for greater community input and collaboration.

### Criteria
Including regional configurations will require ongoing upkeep and we cannot support all regional configurations. Supported Regional MOM6 configurations will need to minimise the upkeep overhead whist meeting a community need. The following criteria will be considered when deciding which configurations to support. There can be some flexibility in these criteria for the right configuration so if your configuration doesn't fit all criteria then we encourage you to discuss this with us. Conversely, we may need decline configurations that fit the criteria if we are already managing many configurations. We encourage starting a conversation with us early in the development of the configuration so we can plan and assist in meeting the criteria. 

#### Minimising overheads
The configuration files will need to closely match an existing ACCESS-OM3 or ACCESS-rOM3 configuration to minimise maintanance costs. In particular, the configuration needs to be running on the NUOPC coupler, on Gadi and be able to interface with `payu`. Except for the MOM_input, MOM_override and config.yaml files, the expectation is that files will only differ from an existing configuration by one or two lines. The MOM_input can be very different in regional configurations due to the need to specify different parameter choices but the layout and order of these specifications should match layout and order of the ACCESS-OM3 configurations. The MOM_override file can be used to add further configuration options such boundary condition specifications. The config.yaml file will differ due to the need to specify different input files and executables but the layout of this file should closely match an ACCESS-OM3 configuration, including pointing to an ACCESS-NRI managed executable.    

#### Community interest
The configuration needs to be useful for a broad section of the Australian research community and for a long period of time (min 3 years). Evidence of this could include:

   1. A previous similar domain was well utilised (i.e. a 5 km version was popular, and you now want support for a 1km version);
   2. There is a cross-institute grant or funding source (>3 years in length) that uses the configuration;
   3. There are already >5 people, across at least 2 institutions that are actively involved in the configuration;
   4. A survey of the community indicates a need;
   5. You are welcome to suggest other evidence of community interest.

#### Other criteria
There needs to be enough information provided so a user can run the configuration and have confidence that they know exactly what they are running. The extra information that needs to be available for us to support a configuration is:

1. Documentation of the configuration
2. Input netcdf files will need to be shared and include metadata that inform of date and commands used to create the file.
3. Scripts and notebooks used to create the input files need to be avaliable in a public GitHub repository.
4. The branch name will need to follow the access-om3-configs [naming convention](https://github.com/ACCESS-NRI/access-om3-configs?tab=readme-ov-file#repository-structure)

### Support length
There is a need to retire configurations when they become less utilised to create capacity for ACCESS-NRI to take on new configurations. 
We will provide support initially for at least a 3 year period and potentially longer if there is an obvious ongoing need (e.g. it is supported by a grant that is >3 years). After this, the case for ongoing support with be revisited annually (unless a case is made for a longer revision period). Once a configuration is retired, it will still be available for use by the communnity but updates will not occur. Community members are welcome to take over the management of these configurations. 

### Initial development of configuration
Configurations are not expected to initially meet the requirements for an ACCESS-NRI supported configuration. To develop your configuration, you can fork access-om3-configs into your own repository. From there you can create a branch for your configuration and make the necessary changes to your configurations. You can then create a draft pull request back to the access-om3-configs repository. ACCESS-NRI team members can assist with this process

### Applying for a supported configuration
To apply to have a configuration as a supported configuration, [raise an issue on ACCESS-OM3 configs](https://github.com/ACCESS-NRI/access-om3-configs/issues/new/choose) (pick "blank template") and describe your configuration and how it meets (or will meet) the criteria.
If your configuration does not meet the criteria for an access-supported model then it is still possible to share the model configurations, with a community member taking responsibility for maintaining the repository. Space for configuration files can be provided upon request on the [ACCESS-NRI community repository](https://github.com/ACCESS-Community-Hub). These configuration can still use ACCESS-NRI supported executable and `payu`.

