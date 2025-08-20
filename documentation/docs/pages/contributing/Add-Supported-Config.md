## Adding a new configuration to ACCESS-OM3 configs 

### Scope
There are ACCESS-OM3 global and regional configurations (ACCESS-OM3 and ACCESS-rOM3) that are under active development at ACCESS-NRI and within the communities we collaborate with. Some of the configurations developed outside of ACCESS-NRI have a wider interest and it will be beneficial for these configurations to be supported and maintained at ACCESS-NRI. Here we provide protocol and guidance on how to apply to have your configuration supported by ACCESS-NRI. 

### What are the benefits?
When a configuration is supported by ACCESS-NRI then it can be kept up to date with the latest versions of ACCESS-OM3's components, including applying bug fixes, adding new features and upgrades. It will also give more visibility to your configuration, allow others to readily run the configuration and allows for greater community input and collaboration. In some cases, a supported configuration can also benefit from being an official "release" meaning there can be additional documentation and provenance of how the configuration was created and run.

### Criteria
Including community developed configurations will require ongoing upkeep and we cannot support all configurations. Supported configurations will need to minimise the upkeep overhead whilst meeting a community need. The following criteria will be considered when deciding which configurations to support. There can be some flexibility in these criteria for the right configuration so if your configuration doesn't fit all criteria then we encourage you to discuss this with us. Conversely, we may decline configurations that fit the criteria if we are already managing many configurations. We encourage starting a conversation with us early in the development of the configuration so we can plan and assist in meeting the criteria. 

#### Minimising overheads
The configuration files will need to closely match an existing ACCESS-OM3 or ACCESS-rOM3 configuration to minimise maintenance burden. In particular, the configuration needs to be:

 - running on the NUOPC coupler; 
 - on Gadi;
 - runs using `payu`; 
 - Except for the `MOM_input`, `MOM_override` and `config.yaml` files, the expectation is that files will only differ from an existing configuration by one or two lines. 
 
The `MOM_input` can be very different in  configurations due to the need to specify different parameter choices but the layout and order of these specifications should match layout and order of the ACCESS-OM3 configurations. The `MOM_override` file can be used to add further configuration options such boundary condition specifications. The `config.yaml` file will differ due to the need to specify different input files and executables but the layout of this file should closely match an ACCESS-OM3 configuration, including pointing to an ACCESS-NRI managed executable. This may sound challenging but the development team is here to help contributors understand and meet these criteria upon review.

#### Community interest
The configuration needs to be useful for a large part of the Australian research community and for a long period of time (min 3 years). Evidence of this could include:

   1. A previous similar domain was well utilised (i.e. a 5 km version was popular, and you now want support for a 1km version);
   2. There is a cross-institute grant or funding source (>3 years in length) that uses the configuration;
   3. There are already >5 people, across at least 2 institutions that are actively involved in the configuration;
   4. A survey of the community indicates a need;
   5. You are welcome to suggest other evidence of community interest.

#### Other criteria
There needs to be enough documentation provided such that a user can run the configuration and have confidence that they know exactly what they are running. We have a checklist below of the information and steps needed to be available for a configuration to be supported.

### Support length
There is a need to have a timeline for when supported configurations will move to having reduced support, reduced support may mean no updates. This allows new science to be addressed by newer configurations by creating capacity for ACCESS-NRI to take on new configurations. 

We will provide support initially for at least a 1 year period and potentially longer if there is an obvious ongoing need (e.g. it is supported by a grant that is >3 years). After this, the case for ongoing support will be revisited annually (unless a case is made for a longer revision period). Once a configuration is retired, it will still be available for use by the community but updates will not occur. Community members are welcome to take over the management of these configurations. 

### Initial development of configuration
Configurations are not expected to initially meet the requirements for an ACCESS-NRI supported configuration. To develop your configuration, you can fork `access-om3-configs` into your own repository. From there you can create a branch for your configuration and make the necessary changes to your configuration. You can then create a draft pull request back to the `ACCESS-NRI/access-om3-configs` repository. `ACCESS-NRI` staff members can assist with this process.

### Applying for a supported configuration
To apply to have a configuration as a supported configuration, [raise an issue on ACCESS-OM3 configs](https://github.com/ACCESS-NRI/access-om3-configs/issues/new/choose) (pick "blank template") and describe your configuration and how it meets (or will meet) the criteria.

If your configuration does not meet the criteria for being an ACCESS-supported model, then it is still possible to share the model configuration. In this instance, a community member can take responsibility for maintaining the repository. Space for configuration files can be provided upon request on the [ACCESS-NRI community repository](https://github.com/ACCESS-Community-Hub). These kinds of configurations can still use ACCESS-NRI supported executable and `payu`.

#### Checklist for developing a supported configurations
Use this checklist whilst developing your configuration to make sure you include relevant information needed and are following the ACCESS-OM3 conventions. 

1. Create documentation of the configuration (see [here](https://access-om3-configs.access-hive.org.au/configurations/dev-MC_25km_jra_ryf/)) for an example.
2. The configuration is running on the NUOPC coupler.
3. The configuration is running stably on an ACCESS-NRI supported ACCESS-OM3 executable.
4. The configuration closely matches the _most up-to-date branch_ of an existing ACCESS-OM3 or ACCESS-rOM3 supported configuration.
5. There isn't a similar ACCESS-OM3 or ACCESS-rOM3 supported configuration that supercedes the configuration.
6. Input netcdf files will need to be shared and include metadata that inform of date and commands used to create the file.
7. Scripts and notebooks used to create the input files need to be available in a public GitHub repository.
8. Your configuration is shared on GitHub on a branch located within a fork of `access-om3-configs` and has a shared git history with another `access-om3-configs` configuration.
9. Check that your branch name follows the `access-om3-configs` [branch naming convention](https://access-om3-configs.access-hive.org.au/#access-om3-configs-overview) (see under the `repository-structure` heading. For regional models this should start with `dev-rM` and when specifying the resolution also add a 3-5 letter description of the location. For example: 'dev-rM-tas5km`. 
10. Get in touch with the @ACCESS-NRI/ocean team and ask us to create a branch for you on `access-om3-configs` of the same name and origin such that a pull request can be created.
