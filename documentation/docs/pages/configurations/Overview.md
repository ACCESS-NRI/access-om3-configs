## What the configuration files are for
The configurations have much in common. Here we provide a quick overview of the common features, using examples from the [`dev-MC_100km_jra_ryf` branch](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_100km_jra_ryf). This is a MOM6-CICE6 coupled configuration without waves or biogeochemistry, at a nominal 100 km (1°) horizontal resolution, under repeat-year forcing. 

 - [`config.yaml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/config.yaml): used by [`payu`](https://payu.readthedocs.io/en/latest/) for model setup and run ([YAML](https://yaml.org/spec/1.2.2/#chapter-2-language-overview) format)
 - [`datm_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/datm_in): sets [stream-independent](https://escomp.github.io/CDEPS/versions/master/html/introduction.html#design) data atmosphere [parameters](https://escomp.github.io/CDEPS/versions/master/html/datm.html) (in [Fortran namelist](https://jules-lsm.github.io/vn4.2/namelists/intro.html) format)
 - [`datm.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/datm.streams.xml): sets input files and other [stream-dependent input data](https://escomp.github.io/CDEPS/versions/master/html/introduction.html#design) for data atmosphere in [this XML format](https://escomp.github.io/CDEPS/versions/master/html/streams.html#data-model-stream-input)
 - [`diag_table`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/diag_table): MOM6 diagnostics in [this format](https://mom6.readthedocs.io/en/main/api/generated/pages/Diagnostics.html); may be generated from a `diag_table_source.yaml` [YAML](https://yaml.org/spec/1.2.2/#chapter-2-language-overview) file by [`make_diag_table.py`](https://github.com/COSIMA/make_diag_table)
 - [`drof_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/drof_in): sets [stream-independent](https://escomp.github.io/CDEPS/versions/master/html/introduction.html#design) data runoff [parameters](https://escomp.github.io/CDEPS/versions/master/html/drof.html) (in [Fortran namelist](https://jules-lsm.github.io/vn4.2/namelists/intro.html) format)
 - [`drof.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/drof.streams.xml): sets input files and other [stream-dependent input data](https://escomp.github.io/CDEPS/versions/master/html/introduction.html#design) for data runoff in [this XML format](https://escomp.github.io/CDEPS/versions/master/html/streams.html#data-model-stream-input)
 - [`drv_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/drv_in): NUOPC parameters for the [driver](https://github.com/search?q=repo%3AESCOMP%2FCMEPS+path%3Acesm/driver/+drv_in&type=code) (in [Fortran namelist](https://jules-lsm.github.io/vn4.2/namelists/intro.html) format)
 - [`fd.yaml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/fd.yaml): NUOPC [field dictionary](https://earthsystemmodeling.org/docs/release/ESMF_8_4_2/NUOPC_refdoc/node3.html#SECTION00032000000000000000) ([YAML](https://yaml.org/spec/1.2.2/#chapter-2-language-overview) format) read by the NUOPC [driver](https://github.com/search?q=repo%3AESCOMP%2FCMEPS+path%3Acesm/driver/+fd.yaml&type=code); defines standard metadata for fields that may be available for import and/or export from model components; `standard_name`s are used for [field pairing](https://earthsystemmodeling.org/docs/release/ESMF_8_4_2/NUOPC_refdoc/node3.html#SECTION00034200000000000000) during initialisation
 - [`ice_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/ice_in): CICE6 parameters (in [Fortran namelist](https://jules-lsm.github.io/vn4.2/namelists/intro.html) format)
 - [`input.nml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/input.nml): a few [MOM6 parameters](https://mom6.readthedocs.io/en/main/api/generated/pages/Runtime_Parameter_System.html#namelist-parameters-input-nml) (in [Fortran namelist](https://jules-lsm.github.io/vn4.2/namelists/intro.html) format)
 - [`MOM_input`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/MOM_input): most of the MOM6 parameters, in [this format](https://mom6.readthedocs.io/en/main/api/generated/pages/Runtime_Parameter_System.html#mom6-parameter-file-syntax)
 - [`MOM_override`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/MOM_override): more MOM6 parameters in [this format](https://mom6.readthedocs.io/en/main/api/generated/pages/Runtime_Parameter_System.html#mom6-parameter-file-syntax), overriding things in `MOM_input`
 - [`nuopc.runconfig`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/nuopc.runconfig): read by NUOPC [driver](https://github.com/search?q=repo%3AESCOMP%2FCMEPS+path%3Acesm/driver/+nuopc.runconfig&type=code); supplies driver-related parameters for model components; parameters documented [here](https://github.com/ESCOMP/CMEPS/blob/606eb397d4e66f8fa3417e7e8fd2b2b4b3c222b4/cime_config/namelist_definition_drv.xml); the file is a mix of [Resource File](https://earthsystemmodeling.org/docs/release/ESMF_8_6_0/ESMF_refdoc/node6.html#SECTION06091200000000000000) and [Fortran namelist](https://jules-lsm.github.io/vn4.2/namelists/intro.html) formats
 - [`nuopc.runseq`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/nuopc.runseq): read by NUOPC [driver](https://github.com/search?q=repo%3AESCOMP%2FCMEPS+path%3Acesm/driver/+nuopc.runseq&type=code); defines model component run sequence using [this syntax](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_refdoc/node4.html#SECTION000411300000000000000)

### Where to set parameters
#### Model exectuable version
  - [`modules: load:`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fconfig.yaml+load:&type=code) in `config.yaml`. This sets the [released version](https://github.com/ACCESS-NRI/ACCESS-OM3/releases) if using a pre-built executable. If using a prerelease [build](/infrastructure/Building#ad-hoc-builds), set `modules: use` to `/g/data/vk83/prerelease/modules` and `modules: load` to the prerelease version (e.g. `access-om3/pr999-9`).
#### Coupling
##### active model components
  - [`component_list`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+component_list&type=code) and entries in [`ALLCOMP_attributes`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+ALLCOMP_attributes&type=code) section in `nuopc.runconfig`, e.g.
```yaml
component_list: MED ATM ICE OCN ROF
ALLCOMP_attributes::
     ATM_model = datm  # data atmosphere
     GLC_model = sglc  # no glaciers/land ice (stub)
     ICE_model = cice  # active sea ice (cice)
     LND_model = slnd  # no land model (stub)
     MED_model = cesm  # mediator
     OCN_model = mom   # active ocean model (mom6)
     ROF_model = drof  # data runoff
     WAV_model = swav  # no wave model (stub)
     ...
```
##### components and fields to couple
  - See the coupling architecture [here](/infrastructure/Architecture)
  - Coupling is [negotiated between model components during initialization](https://earthsystemmodeling.org/nuopc/) of a model run. See [here](https://escomp.github.io/CMEPS/versions/master/html/esmflds.html): "_CMEPS advertises all possible fields that can be imported to and exported by the mediator for the target coupled system. Not all of these fields will be connected to the various components. The connections will be determined by what the components advertise in their respective advertise phase._"
  - [`fd.yaml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/fd.yaml): NUOPC [field dictionary](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_refdoc/node3.html#SECTION00032000000000000000) defines standard metadata for fields that may be available for import and/or export from model components; standard_names are used for [field pairing](https://earthsystemmodeling.org/docs/release/ESMF_8_4_2/NUOPC_refdoc/node3.html#SECTION00034200000000000000) during initialisation
  - the fields available to be imported/exported for coupling are determined by the NUOPC cap code for [MOM6](https://github.com/mom-ocean/MOM6/tree/main/config_src/drivers/nuopc_cap), [CICE6](https://github.com/ESCOMP/CICE/tree/main/cicecore/drivers/nuopc/cmeps), [WW3](https://github.com/ESCOMP/WW3/blob/dev/unified/model/src/wav_import_export.F90), [DATM](https://github.com/ESCOMP/CDEPS/tree/main/datm) and [DROF](https://github.com/ESCOMP/CDEPS/tree/main/drof) and recorded in the mediator log output file: `grep Advert archive/output000/log/med.log`
  - whether those fields are actually coupled is determined by the CMEPS mediator at run time (see [here](https://escomp.github.io/CMEPS/versions/master/html/esmflds.html)).
    - the coupling between components is recorded in the mediator log output file: `grep -A 9 "Active coupling flags" archive/output000/log/med.log`
    - the mediator log output file also lists the individual fields that are coupled and where the coupled fluxes are calculated: `grep '^ mapping' archive/output000/log/med.log`; see [here](https://escomp.github.io/CMEPS/versions/master/html/esmflds.html) for how to decode this
  - also see [`wav_coupling_to_cice`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+wav_coupling_to_cice&type=code) in `nuopc.runconfig`
##### remapping/redistribution method for coupled fields
  - The remapping method used for each field is recorded in the mediator log output file: `grep '^ mapping' archive/output000/log/med.log`; see [here](https://escomp.github.io/CMEPS/versions/master/html/esmflds.html) for how to decode this
  - [`datm.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/datm.streams.xml) and [`drof.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/drof.streams.xml) specify `<mapalgo>bilinear</mapalgo>` but there are better options - see [here](https://escomp.github.io/CDEPS/versions/master/html/streams.html) and [here](http://earthsystemmodeling.org/docs/release/ESMF_8_3_1/ESMF_refdoc/node5.html#sec:regrid)
  - [`rof2ocn_ice_rmapname`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+rof2ocn_ice_rmapname&type=code) and [`rof2ocn_liq_rmapname`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+rof2ocn_liq_rmapname&type=code) in `MED_attributes` in `nuopc.runconfig`
  - [`*map*`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+map&type=code) in `MED_attributes` in `nuopc.runconfig`
  - [`remapMethod`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runseq+remapMethod&type=code) in `nuopc.runseq`; options are `redist`, `bilinear` (the default), `patch`, `nearest_stod`, `nearest_dtos`, `conserve`. For strict bit-for-bit reproducibility `srcTermProcessing=1` and `termOrder=srcseq` are also required. See details [here](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_refdoc/node3.html#SECTION00034500000000000000) and [here](http://earthsystemmodeling.org/docs/release/ESMF_8_3_1/ESMF_refdoc/node5.html#sec:regrid) and [this detailed explanation](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/ESMF_refdoc/node5.html#RH:bfb).
##### time interpolation of coupled fields
  - specified via `tintalgo` in [`datm.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/datm.streams.xml) and [`drof.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/drof.streams.xml) - see [here](https://escomp.github.io/CDEPS/versions/master/html/streams.html#data-model-stream-input) for options
#### Processor layout - see [here](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_refdoc/node3.html#SECTION00037000000000000000)
  - entries in [`PELAYOUT_attributes`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+PELAYOUT_attributes&type=code) section in `nuopc.runconfig`
  - may need to adjust `max_blocks` in `ice_in`
  - may need a `mem: 192GB` entry in `config.yaml` if you are using less than a full node
#### IO layout
  - entries in [`*_modelio`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+_modelio&type=code) sections in `nuopc.runconfig`
  - for `pio_typename`.
     - Use `netcdf4p` for parallel IO. Don't use `netcdf4c` (deprecated) or `pnetcdf` (not included in dependencies).
     - `netcdf` only uses one PE (`pio_root`) for IO
  - MOM6 uses FMS for IO and doesn't use the settings in the `OCN_modelio` section. Instead, IO settings can be configured in the `fms2_io_nml` namelist group in `input.nml`

#### case name
  - [`case_name`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+case_name&type=code) in `ALLCOMP_attributes` in `nuopc.runconfig`
#### grids
  - [`mesh_atm`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+mesh_atm&type=code), [`mesh_ice`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+mesh_ice&type=code), [`mesh_ocn`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+mesh_ocn&type=code) in `ALLCOMP_attributes` in `nuopc.runconfig`
  - [`mesh_rof`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+mesh_rof&type=code) in `ROF_attributes` in `nuopc.runconfig`
  - grid dimensions [`*_nx`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+_nx&type=code), [`*_ny`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+_ny&type=code) in `MED_attributes` in `nuopc.runconfig`
#### coupling diagnostics
  - [`*budget*`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+budget&type=code) in `MED_attributes` in `nuopc.runconfig`
  - [`hist*`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+hist&type=code) in `MED_attributes` in `nuopc.runconfig`
    - `histaux_*_flds` is either a colon-delimited list of fields to output, or [`all` to output everything](https://github.com/ESCOMP/CMEPS/blob/606eb397d4e66f8fa3417e7e8fd2b2b4b3c222b4/mediator/med_phases_history_mod.F90#L1105-L1143); see [CMEPS field naming convention](https://escomp.github.io/CMEPS/versions/master/html/esmflds.html#field-naming-convention) to decode these
    - `grep hist archive/output000/log/med.log` will show you when data was written
#### verbosity in NUOPC log files (`archive/output*/log/*.log`)
  - [`Verbosity`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+Verbosity&type=code) in attributes for model components in `nuopc.runconfig`; can be `off`, `low`, `high`, `max` - see [here](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_refdoc/node3.html#SECTION00033000000000000000) - but doesn't seems to make any difference, perhaps due to [this issue](https://github.com/ESCOMP/CMEPS/issues/21).
#### calendar
  - [`calendar`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+calendar&type=code) in `CLOCK_attributes` in `nuopc.runconfig`; can be either [`NO_LEAP` or `GREGORIAN`](https://github.com/search?q=repo%3AESCOMP%2FCMEPS+path%3Acesm%2Fdriver%2F+NO_LEAP+GREGORIAN&type=code)
  - also set `use_leap_years = .true.` in `ice_in` for Gregorian calendar
#### start date
  - [`start_ymd`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+start_ymd&type=code) in `CLOCK_attributes` in `nuopc.runconfig`
#### run length
  - [`stop_n`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+stop_n&type=code) and [`stop_option`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+stop_option&type=code) in `CLOCK_attributes` in `nuopc.runconfig`; available units for `stop_option` are listed [here](https://escomp.github.io/CMEPS/versions/master/html/generic.html)
  - In interannual forcing configurations, there is no "stop date" - the model will ungracefully stop when then forcing data runs out (February 2024, in the default JRA55do v1.6)
#### restart frequency
  - [`restart_n`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+restart_n&type=code) and [`restart_option`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+restart_option&type=code) in `CLOCK_attributes` in `nuopc.runconfig`; available units for `restart_option` are listed [here](https://escomp.github.io/CMEPS/versions/master/html/generic.html)
  - Typically restart frequency is set the same as run length. If changing restart frequency, it is up to the user to ensure that restart frequency is set such that a restart is written at the end of the run.
#### run sequence
  - The order which components are run is specified in [`nuopc.runseq`](https://github.com/ACCESS-NRI/access-om3-configs/blob/main/doc/nuopc.runseq). The order also impacts whether components run sequentially or in parallel. Normally we specify CICE and MOM to run in subsequent lines in `nuopc.runseq`, and as long as they are [on different processors](https://github.com/ACCESS-NRI/access-om3-configs/blob/0d0a5f16a14781c7c7e5bcacf91707fc9a3cc64b/doc/nuopc.runconfig#L47-L59), they run in parallel as these steps do not depend on each other.
  - To run MOM before CICE, specify all OCN related steps in the nuopc.runseq before all ICE related steps (see example [here](https://github.com/anton-seaice/om3_025_cgrid_expts/blob/075a5f730ab9c6e49d0c4571e517db86081230a3/ocn_icn_serial/nuopc.runseq)). This will be very slow and resource inefficient and is for testing / debugging only. It does reduce the coupling related lag in stress between the sea-ice and ocean (see [Morrison 2024 slides](https://usclivar.org/sites/default/files/presentations/2024/morrison-theresa-oceanmodel-CP.pdf)

#### timesteps
  - there is a complex set of interrelated timesteps - see [here](/infrastructure/NUOPC-driver/#time-steps) and [here](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_refdoc/node3.html#SECTION00035000000000000000) to understand how they interact
  - coupling and driver timesteps - see [here](/infrastructure/NUOPC-driver/#coupling-and-driver-time-step)
    - [`*_cpl_dt`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+_cpl_dt&type=code) in `CLOCK_attributes` in `nuopc.runconfig`
    - [`nuopc.runseq`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/nuopc.runseq)
  - MOM6 timestepping - see [here](/infrastructure/NUOPC-driver/#mom6-time-steps)
    - There are 4 timesteps. From shortest to longest they are: barotropic, baroclinic (Lagrangian), tracer, vertical remapping - see [here](https://youtu.be/JKMwd8VXYcU?t=383) and [here](https://youtu.be/JKMwd8VXYcU?t=2165) and [here](https://mom6.readthedocs.io/en/main/api/generated/pages/Timestep_Overview.html)
  - CICE6 timestepping - see [here](/infrastructure/NUOPC-driver/#cice6-time-steps)
    - There are 3 timesteps. From shortest to longest they are elastic, dynamic and thermodynamic - see [here](https://cice-consortium-cice.readthedocs.io/en/cice6.5.0/user_guide/ug_implementation.html#choosing-an-appropriate-time-step)
    - The thermodynamic timestep is determined by the coupling (and driver) timestep (so _`dt` should **not** be explicitly set in `ice_in`_ - see [here](/infrastructure/NUOPC-driver/#cice6-time-steps))
    - [`ndtd`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fice_in+ndtd&type=code) in `ice_in` sets the number of dynamic timesteps in each thermodynamic timestep; increasing this can resolve "bad departure points" CFL errors
    - [`ndte`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fice_in+ndte&type=code) in `ice_in` sets the number of elastic timesteps in each dynamic timestep if the classic EVP or EAP method is used ([`kdyn`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fice_in+kdyn&type=code) = 1 or 2, [`revised_evp`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fice_in+revised_evp&type=code) = false)
#### walltime limit
  - [`walltime`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fconfig.yaml+walltime:&type=code) in `config.yaml`
#### number of ensemble members
  - [`ninst`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+ninst&type=code) in `PELAYOUT_attributes` in `nuopc.runconfig`
#### forcing data
  - see the [Forcing](/inputs/Forcing-data-models) page
  - atmospheric forcing
    - [`datm.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/datm.streams.xml) sets individual file paths relative to [this entry](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fconfig.yaml+"datm+and+drof"&type=code) in the `input` section of [`config.yaml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/config.yaml); see [DATM](https://escomp.github.io/CDEPS/versions/master/html/datm.html) and [streams](https://escomp.github.io/CDEPS/versions/master/html/streams.html) docs
  - runoff
    - [`drof.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/drof.streams.xml) sets individual file paths relative to [this entry](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fconfig.yaml+"datm+and+drof"&type=code) in the `input` section of [`config.yaml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/config.yaml); see [DROF](https://escomp.github.io/CDEPS/versions/master/html/drof.html) and [streams](https://escomp.github.io/CDEPS/versions/master/html/streams.html) docs
