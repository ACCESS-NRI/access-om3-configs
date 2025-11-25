# MOM6-CICE 25km Global Configurations

The sections that follow explain why we selected each model parameter for the global MOM6-CICE 25km global model configurations and how they work together across the coupled system. We start with the MOM6 ocean settings, then step through the CICE sea‑ice namelist. For every group of parameters you’ll find a description, links to the relevant code or literature, and practical guidance on when you might wish to adjust the defaults. Use this as both a quick reference and a roadmap for deeper dives into the individual configuration files such as [`MOM_parameter_doc.all`](https://github.com/ACCESS-NRI/access-om3-configs/blob/release-MC_25km_jra_ryf/docs/MOM_parameter_doc.all), the list of all [MOM6](https://github.com/ACCESS-NRI/mom6) parameters, and [`cice_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/release-MC_25km_jra_ryf/ice_in), the [CICE](https://github.com/ACCESS-NRI/cice) namelist file.

## MOM6 parameter choices

Code-formatted text in the following sections gives the parameter values set in the `MOM_input` configuration file.

### Grid resolution
The configuration uses a zonally-periodic tripolar grid to avoid a singularity at the North Pole (`REENTRANT_X = True`, `TRIPOLAR_N = True`). The horizontal grid has 1440 x 1152 tracer points providing eddy-permitting resolution similar to ACCESS-OM2-025 and GFDL's OM4/OM5 global models (1440 x 1080). See [Grids](../../inputs/Grids/) for more information. 

There are 75 vertical layers (`NK = 75`). MOM6 supports an arbitrary Lagrangian Euler (ALE) vertical coordinate scheme [@griffies2020primer] that allows for completely general vertical coordinates. A number of coordinates are supported "out-of-the-box", including isopycnal, geopotential, terrain-following, HYCOM1 etc. This configuration uses ALE with a stretched geopotential (z-star) vertical coordinate (`USE_REGRIDDING = True`, `REGRIDDING_COORDINATE_MODE = "ZSTAR"`). The layer spacing specified via an input file (`ALE_COORDINATE_CONFIG = "FILE:ocean_vgrid.nc,interfaces=zeta"`). The deepest ocean depth is set to `MAXIMUM_DEPTH = 6000.0`.

The Boussinesq approximation is used (`BOUSSINESQ = True`), meaning density variations only affect buoyancy, with other terms using a reference density `RHO_0 = 1035` $kg/m^3$.

### Thermodynamics and Equation of State (TEOS-10)
The configuration uses the "ROQUET_RHO" equation of state for seawater thermodynamic properties (`EQN_OF_STATE = "ROQUET_RHO"`). This scheme is based on TEOS-10, but uses a 75-term polynomial to compute in-situ density as a function of conservative temperature and absolute salinity, closely approximating the full TEOS-10 results [@roquet2015accurate]. The `_RHO` variant specifically fits density rather than specific volume and is well-suited for layered models. Prognostic temperature and salinity are conservative temperature and absolute salinity (`USE_CONTEMP_ABSSAL = True`), consistent with the equation of state.

The freezing conservative temperature is calculated from absolute salinity and pressure using a 23-term polynomial fit refactored from the TEOS-10 package (`TFREEZE_FORM = "TEOS_POLY"`). More relevant discussion can be found in the [COSIMA TWG 23-July-2025 meeting minutes](https://forum.access-hive.org.au/t/cosima-twg-meeting-minutes-2025/4067/17#:~:text=Freezing%20temperature%20consistency%20between%20mom6%20and%20cice). 

### Frazil formation
Frazil formation in the ocean is turned on (`FRAZIL = TRUE`). This scheme works upwards through each water column, transferring heat downwards from the layer above as needed to prevent the in-situ temperature falling below the local freezing point in each layer in turn. If the top layer is below freezing, heat is extracted from the sea ice model, which grows frazil ice in response. More details are [here](https://mom6.readthedocs.io/en/main/api/generated/pages/Frazil_Ice.html).

In regions where there is no frazil formation, sea-ice melt/freeze potential is calculated over the smaller of the top 10m of the ocean and the boundary layer depth (`HFREEZE = 10.0`).

### Surface salinity restoring
Sea surface salinity is restored toward a monthly climatological dataset calculated from the World Ocean Atlas 2023 available at [NOAA NCEI](https://www.ncei.noaa.gov/products/world-ocean-atlas) (`RESTORE_SALINITY = True`, `SALT_RESTORE_FILE = "salt_sfc_restore.nc"`). A piston velocity of 0.11 $m/day$ is applied to control the strength of the salinity relaxation (`FLUXCONST = 0.11`). The restoring is implemented as a virtual salt flux (`SRESTORE_AS_SFLUX = True`). This approach conserves salt overall, balanced globally by subtracting the mean flux to avoid altering global salinity (`ADJUST_NET_SRESTORE_TO_ZERO = True`). No effective limit is applied to the salinity restoring flux (`MAX_DELTA_SRESTORE = 999`). More discussion can be found in [issues/350](https://github.com/ACCESS-NRI/access-om3-configs/issues/350), [issues/325](https://github.com/ACCESS-NRI/access-om3-configs/issues/325), [issues/257](https://github.com/ACCESS-NRI/access-om3-configs/issues/257).

Salinity is limited to be positive to prevent the sea-ice model from asking for more salt than is available and driving the salinity negative (`BOUND_SALINITY = True`, `MIN_SALINITY = 0.0`).

### Diagnostics
Three-dimensional ocean diagnostics are output on either $z*$- or density-coordinates, depending on the diagnostic, rather than on the model's native coordinate. Specifically, `NUM_DIAG_COORDS = 2` with `DIAG_COORDS = "z Z ZSTAR", "rho2 RHO2 RHO"` and the vertical coordinate levels for each are defined by `DIAG_COORD_DEF_Z = "FILE:ocean_vgrid.nc,interfaces=zeta"` and `DIAG_COORD_DEF_RHO2 = "RFNC1:76,999.5,1020.,1034.1,3.1,1041.,0.002"` (relevant info can be found at [PR/622](https://github.com/ACCESS-NRI/access-om3-configs/pull/622)).

An ideal age tracer is configured (`USE_IDEAL_AGE_TRACER = True`). This tracer ages at a rate of 1/year once it is isolated from the surface and is useful for  understanding water mass ventilation and residence times.

### Vertical mixing parameterisations
#### Energetic planetary boundary layer (ePBL)
The configuration handles the vertical mixing in the ocean surface boundary layer with the ePBL scheme rather the the traditional KPP. The ePBL scheme is an energy-based 1D turbulence closure approach that integrates a boundary layer energy budget to determine mixing coefficients. It was developed by [@reichl2018simplified] to improve upon KPP for climate simulations by including the effect of turbulent kinetic energy input and wind-driven mixing in a more physically constrained way. Relevant discussion can be found in [issues/465](https://github.com/ACCESS-NRI/access-om3-configs/issues/465), [issues/426](https://github.com/ACCESS-NRI/access-om3-configs/issues/426), [issues/373](https://github.com/ACCESS-NRI/access-om3-configs/issues/373).

The ePBL scheme parameters in the configuration are based on the [GFDL OM5 configuration](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM5_025/MOM_parameter_doc.all), including:

- Additional mixing due to Langmuir (wave-driven) turbulence (`EPBL_LANGMUIR_SCHEME = “ADDITIVE”`). Since we do not explicitly couple to a wave model in this configuration (`USE_WAVES = False`), the Langmuir effect is parameterised via a predetermined enhancement factor using MOM6 default values. The inclusion of wave effects is expected to reduce warm SST biases by enhancing mixing under strong winds, as found in studies of Langmuir turbulence (e.g., `USE_LA_LI2016 = True` from [@li2016langmuir]).
- Using the "OM4" scheme for calculating $m*$ (`EPBL_MSTAR_SCHEME = “OM4”`  `MSTAR_CAP = 1.25`, `MSTAR2_COEF1 = 0.29`, `MSTAR2_COEF2 = 0.152`)
- Iteratively solving for a self-consistent mixed layer depth rather than using a single-pass estimate (`USE_MLD_ITERATION = True`)
- Replacing shear-induced diffusivities with ePBL diffusivities when the latter is larger than the former (`EPBL_IS_ADDITIVE = False`)

#### Interior shear-driven mixing
Shear-driven mixing is parameterised use the Jackson-Hallberg-Legg shear mixing scheme [@jackson2008parameterization] using the MOM6 default critical Richardson number (Ri) and shear mixing rate (`USE_JACKSON_PARAM = True`, `RINO_CRIT = 0.25`, `SHEARMIX_RATE = 0.089`). This scheme targets mixing in stratified shear zones, effectively adding interior vertical diffusivity when the local Ri is less than the critical value. The shear is computed at cell vertices to better capture shear between adjacent grid cells (`VERTEX_SHEAR = True`). The Jackson-Hallberg-Legg parameterisation is energetically constrained: it iteratively finds a diffusivity such that the energy extracted from the mean flow equals the energy used in mixing plus that lost to dissipation (`MAX_RINO_IT = 25`, inherited from the [GFDL OM5 configuration](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM5_025/MOM_parameter_doc.all#L2088)).

#### Internal tidal mixing
Internal tidal mixing is parameterised using the vertical profile of energy dissipation from [@polzin2009abyssal] rather than the default St. Laurent profile, following [@MeletHallbergLeggPolzin2013a] (`INT_TIDE_DISSIPATION = True`, `INT_TIDE_PROFILE = "POLZIN_09"`). Tidal mixing is informed by spatially-varying tidal amplitudes and roughness data that are read from files that [were generated](https://github.com/ACCESS-NRI/om3-scripts/tree/main/external_tidal_generation) using tidal velocities from [`TPXO10`](https://www.tpxo.net/global/tpxo10) and bathymetry from [`SYNBATH`](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2021EA002069) (`READ_TIDEAMP = True`, `TIDEAMP_FILE = "tideamp.nc"`, `H2_FILE = "bottom_roughness.nc"`). The maximum energy per area that can be injected as mixing is limited in the same way as in the [GFDL OM5 configuration](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM5_025/MOM_parameter_doc.all#L1946-L1948) (`TKE_ITIDE_MAX = 0.1`).

#### Interior background mixing
Ocean interior background mixing is also configured based on the [GFDL OM5 configuration](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM5_025/MOM_parameter_doc.all#L2004). A weak constant background diapycnal diffusivity is set for diapycnal mixing (`KD = 1.5E-05`), with a floor for numerical stability (`KD_MIN = 2.0e-6`). Vertical mixing is enhanced in the salt-fingering regime (`DOUBLE_DIFFUSION = True`) and Henyey-type internal wave scaling is configured with default MOM6 parameters (`HENYEY_IGW_BACKGROUND = True`, `HENYEY_N0_2OMEGA = 20.0`, `HENYEY_MAX_LAT = 73.0`). The total diffusivity increment from TKE-based schemes is capped to prevent unbounded growth of shear-based or convective mixing (`KD_MAX = 0.1`). This is a large upper bound that would only take effect in extremely unstable cases.

#### Bottom boundary layer
The bottom boundary layer viscosity and thickness are calculated such that the bottom stress is quadratic and depends on the average of the velocities over the bottom 10m (`BOTTOMDRAGLAW = True`, `LINEAR_DRAG = False`, `HBBL = 10.0`, `CDRAG = 0.003`). See [here](https://mom6.readthedocs.io/en/main/api/generated/pages/Vertical_Viscosity.html?highlight=bottom%20drag#viscous-bottom-boundary-layer) for more details.

An additional Rayleigh drag is applied to layers within the bottom boundary layer to account for curvature of the bottom (`CHANNEL_DRAG = True`, `SMAG_CONST_CHANNEL = 0.15`). More details can be found [here](https://mom6.readthedocs.io/en/main/api/generated/pages/Vertical_Viscosity.html?highlight=channel%20drag#channel-drag).

### Horizontal viscosity and subgrid momentum mixing
A hybrid Laplacian-biharmonic viscosity scheme is used to parameterise unresolved horizontal turbulent mixing of momentum (`LAPLACIAN = True`, `BIHARMONIC = True`). The scheme helps remove small-scale kinetic energy, while preserving large-scale eddy structures, targetting the smaller scales more selectively than just using a Laplacian scheme. See the [MOM6 documentation](https://mom6.readthedocs.io/en/main/api/generated/modules/mom_hor_visc.html#namespacemom-hor-visc-1section-horizontal-viscosity:~:text=Laplacian%20viscosity%20coefficient) for details of how the horizontal viscosity is calculated. The biharmonic viscosity includes:

- no constant background viscosity (`AH = 0.0`)
- a grid-dependent background viscosity (`AH_VEL_SCALE = 0.01`, `AH_TIME_SCALE = 0.0`)
- a dynamic Smagorinsky nonlinear eddy viscosity (`SMAGORINSKY_AH = True`, `SMAG_BI_CONST = 0.06`, `LEITH_AH = False`)

The Lapacian viscosity includes:

- no constant background viscosity (`KH = 0.0`)
- a grid-dependent background viscosity (`KH_VEL_SCALE = 0.01`)
- a latitudinally-dependent background viscosity (`KH_SIN_LAT = 2000.0`, `KH_PWR_OF_SINE = 4.0`)
- no file-base background viscosity (`USE_KH_BG_2D = False`)
- no dynamic viscosity component (`SMAGORINSKY_KH = False`, `LEITH_KH = False`)
- reduction scaling in well-resolved regions (`RESOLN_SCALED_KH = True`) 
- the two coefficient anisotropic viscosity scheme proposed by [@smith2003anisotropic] is not used (`ANISOTROPIC_VISCOSITY = False`)
The Laplacian and biharmonic coefficients are both limited locally to guarantee stability (`BOUND_KH = True`, `BETTER_BOUND_KH = True`, `BOUND_AH = True`, `BETTER_BOUND_AH = True`).

### Isopycnal mixing
At 25km resolution, the model begins to resolve some mesoscale eddies, but parameterisation is still needed for the unresolved part. The configuration uses a hybrid parameterisation for mesoscale eddies, combining neutral diffusion [@redi1982oceanic] and a dynamic Gent-McWilliams (GM) scheme [@gent1990isopycnal] based on an eddy kinetic energy budget. 

#### Isopycnal thickness diffusion (Gent McWilliams diffusion)
`GM` is turned on via `THICKNESSDIFFUSE = True`. Instead of using a fixed `GM` thickness diffusivity (`KHTH = 0.0`), the Mesoscale Eddy Kinetic Energy (MEKE) scheme (`USE_MEKE = True`) is turned on. MEKE activates a prognostic equation for eddy kinetic energy (EKE) and a spatially varying GM streamfunction. The MEKE parameterisation is based on the work of [@jansen2015parameterization], where an EKE budget is solved. The model converts that EKE into an eddy diffusivity (GM diffusivity) via mixing-length theory. In practice, this means the thickness diffusion coefficient is not a fixed number but evolves according to local conditions. Our configuration does not feed external `EKE` data (`EKE_SOURCE = "prog"`), so the model instability growth provides the source of `EKE`. `MEKE_BGSRC = 1.0E-13` prevents `EKE` from decaying to zero in very quiet regions. It serves as a floor to aid numerical stability and is analogous to a background diffusivity but in energy form. `MEKE_GMCOEFF = 1.0` means the scheme converts eddy potential energy to eddy kinetic energy with 100% efficiency for the `GM` effect. `MEKE_KHTR_FAC = 0.5` and `MEKE_KHTH_FAC = 0.5` map some of the eddy energy to tracer diffusivity and lateral thickness diffusivity, respectively. So the configuration actually uses `MEKE` to the job of `GM`: flatterning isopycnals to remove available potential energy, but in a physically informed way using a local EKE prognostic variable. We use `KHTH_USE_FGNV_STREAMFUNCTION = True` which solves a 1D boundary value problem so the `GM` streamfunction is automatically smooth in the vertical and vanishes at the surface and bottom [@ferrari2010boundary]. `FGNV_FILTER_SCALE = 0.1` is used to damp the eddy field noise.

By using `MEKE`, the model is effectively resolution-aware, as resolution increases and resolves more eddies, the diagnostic EKE and hence `GM` coefficient naturally reduces. At the same time , in coarser areas or higher latitudes where eddies are still under-resolved, `MEKE` ramps up the eddy mixing. This avoids the need for ad-hoc spatial maps of `GM` coefficients. By using `FGNV`[@ferrari2010boundary], it ensures a robust energetically consistent vertical structure. 

We set `RES_SCALE_MEKE_VISC = False`, meaning the viscosity is not explicitly scaled by MEKE.

#### Isopycnal tracer mixing (`Redi`)
Neutral tracer diffusion is turned on with `USE_NEUTRAL_DIFFUSION = True`, which means that tracers are mixed primarily along surfaces of constant density, which greatly reduces spurious diapycnal mixing in stratified oceans. The coefficient for along-isopycnal tracer diffusion is set to `KHTR = 50.0`. This number is adopted from [GFDL OM4_05 configuration](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM4_05/MOM_parameter_doc.all#L2419). In addition, we also use `USE_STORED_SLOPES = True` and keep `NDIFF_CONTINUOUS = True`. 

#### Shortwave penetration
Shortwave penetration into the ocean is calculated using the [@manizza2005bio] chlorophyll-based opacity scheme with three shortwave radiation bands (`VAR_PEN_SW = True`, `PEN_SW_NBANDS = 3`). The monthly climatology of surface chlorophyll concentration is calculated from the [Copernicus-GlobColour](https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L4_MY_009_104/description) product using [Laplace interpolation to fill missing regions](https://github.com/ACCESS-NRI/om3-scripts/blob/main/chlorophyll/chl_climatology_and_fill.py).

## CICE namelist
The CICE sea ice model is configured using a Fortran namelist file called `ice_in`. This file contains a series of named blocks, each starting with `&groupname` and ending with `/`. Each block represents a different component of the sea ice model, for example:

1. grid configuration
2. thermodynamics
3. radiation and albedo
4. dynamics and advection
5. diagnostics and output settings

This document walks through each of these namelist groups and provides a short explanation of what each group controls and some configuration
options set in this `ACCESS-OM3` configurations. In general, the `ice_in` file only includes changes from defaults. For a complete list of runtime configuration settings (including defaults)  For detailed explanations of parameters, refer to [CICE Documentation](https://cice-consortium-cice.readthedocs.io) and [Icepack Documentation](https://cice-consortium-icepack.readthedocs.io)(for vertical sea ice processes only).

### `setup_nml`
This group defines time-stepping, run length, output frequencies, initial conditions, and I/O settings.

- Time-stepping and run length
    - The timestep `dt` is not defined in `ice_in` directly; it is overwritten in the CICE NUOPC cap to match the driver timestep (coupling timestep). See [NUOPC driver](/infrastructure/NUOPC-driver/) for more information.
- Initialisation: 
    - When there is no existing restart file to set the initial state, initialisation is set by [`ice_ic`](https://cice-consortium-cice.readthedocs.io/en/cice6.0/user_guide/ug_case_settings.html#:~:text=*-,ice_ic,-default)
        - We use `"none"` and the model starts with no sea ice.
        - We don't use `"default"`, as CICE initialises sea ice concentration and thickness based on latitude and this leads to very large areas of sea ice.

- Output frequencies for history:

    - Up to five output streams are available:
   ```bash
    histfreq = "d", "m", "x", "x", "x"
    hist_suffix = ".1day.mean", ".1mon.mean", "x", "x", "x"
   ```

    - Daily averaged output: `.1day.mean`
    - Monthly averaged output: `.1mon.mean`
    - Streams marked `"x"` are unused.

   - History files use `hist_time_axis = "middle"` to centre timestamps in the averaging interval.

### `grid_nml`
This group defines the spatial grid, land mask, and ice thickness category structure.

- Horizontal Grid
    - Tripolar grid at 25 km nominal resolution: `grid_type = "tripole"`
    - Grid files:
        - The grid is defined by `grid_file = "./INPUT/ocean_hgrid.nc"` and `grid_format = "mom_nc"`. We use the MOM grid file in CICE for best consistency between model components.
        - Land mask file `kmt_file = "./INPUT/kmt.nc"`,
        - Bathymetry file `bathymetry_file = "./INPUT/topog.nc"`. (not currently used)
- Grid staggering
    - Atmosphere and ocean coupling grids use `A-grid`: `grid_atm = "A"`, `grid_ocn = "A"`,
    - Sea ice uses `B-grid`: `grid_ice = "B"`.
- Ice Thickness Categories: 
    - Five ice thickness categories: `ncat = 5`,
    - Four vertical layers in sea ice: `nilyr = 4`,
    - One snow layer: `nslyr = 1`.
- Grid output:
    - `grid_outfile = .true.` writes the cice grid into a seperate NetCDF (eg, `access-om3.cice.static.nc`).

### `thermo_nml`
Controls thermodynamic processes in sea ice.

- Uses the multi-layer thermodynamics of [@bitz1999energy].
- All parameters are left as default, except:
    - `dsdt_slow_mode = -5e-08`: tunes brine drainage (slows down salt removal from ice).

### `dynamics_nml`
Configures sea ice motion and advection.

- Dynamics:
    - Uses the default elastic-viscous-plastic (`EVP`) rheology [@hunke1997elastic], 
    - Default `EVP` subcycling count `ndte = 120`.
- Advection:
    - `advection = "remap"`: Uses incremental remapping for ice and tracer transport [@dukowicz2000incremental].
- SSH:
    - `ssh_stress = "coupled"`: ice feels drag from ocean surface slopes (important for coupling).

### `shortwave_nml`
This group deals with how solar radiation is treated in the ice model and the surface albedo parameters for ice and snow.

- Radiation scheme:
    - `shortwave = "ccsm3"`, `albedo_type = "ccsm3"`: NCAR CCSM3 scheme.
- Albedo settings:
    - `albicev = 0.86` and `albicei = 0.44` for bare ice albedo (visible (`v`) and near infrared (`i`) respectively). These two values are for thick, cold ice. An `albicev` of 0.86 means snow-free ice reflects ~86% of visible light when cold, and `albicei` of 0.44 means ~44% of near-`IR` is reflected. These values are relatively high to ensure the ice does not absorb too much sunlight when snow is absent. 
    - `albsnowv = 0.98`, `albsnowi = 0.70` are for cold snow albedo (`v` and `IR`respectively). By using these two values, we assumes fresh dry snow is bright in visible (98%)
and also high in near-`IR` (70%). 
- Albedo thickness dependence:
    - `ahmax = 0.1` is the thickness parameter for albedo, which is constant above this thickness. In our configuration, it means once ice is ~10cm thick, it is treated optically like thick ice and there will be no further albedo increase. Thinner ice, which is less than 10cm, will have a lower effective albedo. This value is set for consistency with [ACCESS-OM2](https://github.com/ACCESS-NRI/access-om2-configs/blob/0a29b451744dcbc82a90a8b663ce5f7f0d3f2bc2/ice/cice_in.nml#L107).
- Pond/algae effects:
    - [`kalg = 0.0`](https://github.com/CICE-Consortium/CICE/blob/2cdd3d007a409d26cb0c16d946678a544ada55fa/doc/source/user_guide/ug_case_settings.rst#L556:~:text=1.5-,kalg,-real) means no additional algae-related absorption,
    - [`r_snw = 0.0`](https://github.com/CICE-Consortium/CICE/blob/2cdd3d007a409d26cb0c16d946678a544ada55fa/doc/source/user_guide/ug_case_settings.rst#L556:~:text=0.0-,R_snw,-real) is a tuning parameter for snow (broadband albedo) from Delta-Eddingon shortwave, here it is 0, which means not using additional boradband albedo tuning.
    - [`sw_redist = .true.`](https://cice-consortium-icepack.readthedocs.io/en/main/science_guide/sg_thermo.html#thermodynamics) - if penetrating shortwave radiation is greater than the amount which can be absorbed, then redistribute it to the top surface

### `forcing_nml`
The forcing namelist governs how external forcing (`atm` and` ocn`) is applied to the ice, including coupling flux adjustments.

- Atmosphere
    - `highfreq = .true.`: Uses the relative atmosphere-ice velocity instead of the only atmospheric velocity for boundary layer fluxes
- Ocean
    - `update_ocn_f = .true.`: uses coupled frazil water/salt fluxes from ocean,
    - `ustar_min = 0.0005`: Minimum ocean friction velocity to ensure stability.
- Freezing temperature
    - `tfrz_option = "linear_salt"`: Freezing point depends on salinity. This is inconsistent with the [Thermodynamics and Equation of State (TEOS-10)](#thermodynamics-and-equation-of-state-teos-10) freezing point calculated in the ocean model. See [issue 235](https://github.com/ACCESS-NRI/access-om3-configs/issues/235#issuecomment-3082612603) and [CICE-Icepack issue](https://github.com/CICE-Consortium/Icepack/issues/540)
    - `ice_ref_salinity = 5`: sets the reference salinity of newly formed ice and the baseline for salt flux calculations. It means when sea water freezes, the ice is assumed to trap salt at 5 psu and the remainder is rejected to the ocean. This field is set for consistency with the constants assumed by MOM6.

### `domain_nml`
This group namelist controls how the computational domain is divided among processors.

- Global grid size
    - `nx_global = 1440`, `ny_global = 1152` define the total grid points (same as MOM6 ocean grid),
- Block size
    - we use a two-level decomposition - first into blocks of size `30x27` (`block_size_x = 30`, `block_size_y = 27`), then these blocks are distributed to MPI tasks. Each MPI task may get multiple blocks to better balance computational load. The chosen block size is a tuning for performance. Smaller blocks improve load balance but can increase halo communication overhead.
- Distribution type
    - `distribution_type = "roundrobin"`: Assigns blocks cyclically to spread out computational load. See [CICE Documentation](https://cice-consortium-cice.readthedocs.io/en/cice6.0/user_guide/ug_implementation.html?highlight=roundrobin#:~:text=While%20the%20Cartesian,needed%20to%20communicate.) for more information.
- Processor shape
    -  `processor_shape = "square-ice"` indicates the model guess on how to arrange MPI tasks in X vs Y dimension. `“square-ice”` is a pre-set suggesting a slightly X-dominated partition for sea ice. It means the decomposition of blocks to processors will result in more processor domains along x-direction (longitude) than y (latitude), roughly balancing to a square domain per proc. 
- Computational Blocks
    - `max_blocks = -1`: Internally calculated number of blocks per processor,
    - `maskhalo_bound`, `maskhalo_dyn`, `maskhalo_remap` = `.true.`: Mask unused halo cells for boundary handling.

### Output variables and diagnostics (`icefields_nml` and others)
- In the namelist, each output field is listed as `f_<var> = <code>` or as logical `.false.`. The codes are single or double letters, where,
    1. `d` = daily history files (every `histfreq_n` days, which is 1 here)
    2. `m` = monthly files
    3. `md` = both monthly and daily files
    4. `x` = do not write this field (disabled)
    5. `.false.` field disabled

- Our output diagnostics are configured to focus on:
    1. Sea ice state
        - `f_aice = "md"`: concentration (ie, fractional area of ice cover),
        - `f_hi = "md"`: sea ice volume divided by grid cell area,
        - `f_hs = "md"`: snow (on sea ice) volume divided by grid cell area,
        - `f_aicen = "m"`: ice fraction in each thickness category,
        - `f_vicen = "m"`:  ice volume (divided by grid cell area) in each category,
        - `f_snoice = "md"`: snow-ice formation,
        - `f_congel = "md"`: congelation ice growth,
        - `f_frazil = "md"`: frazil ice formation due to frazil heat flux from ocean,
        - `f_frzmlt = "md"`: freeze/melt potential,
        - `f_dvidtd = "md"`: ice volume tendency due to dynamics/transport,
        - `f_dvidtt = "md"`: ice volume tendency due to thermodynamics,

    2. Energy fluxes:
        - `f_fsens_ai = "m"`: sensible heat flux,
        - `f_flatn_ai = "m"`: latent heat flux,
        - `f_fsensn_ai = "m"`: sensible heat flux, category,
        - `f_fsurfn_ai = "m"`: net surface heat flux, categories,
        - `f_fcondtopn_ai = "m"`: top sfc conductive heat flux, cat,

    3. Momentum:
        - `f_uvel = "md"`, `f_vvel = "md"`: sea ice velocity components (u,v) ,

- Some diagnostics are on by default in CICE, and others are configured on in the `ice_in` file. For the complete list, it's best to refer to the history output files or the `ice.log` file in model output.
- Most diagnostics are averaged over grid-cell areas (not sea ice area). Where a variable name ends in `_ai` then it is averaged over grid cell area, if there is another variable of the same name without the `_ai`, then it is an ice area average. If turning on _CMIP_ style diagnostics (those starting with `si`), then refer to the metadata to confirm if it is an ice area or grid cell area average.
- For time-invarient grid information, its best to use the areas and latitutes/longitudes stored in the `access-om3.cice.static.nc` output file.

## References

\bibliography
