# MOM6-CICE 25km Global Configurations

The sections that follow explain why we selected each model parameter for the global MOM6-CICE 25km global model configuration and how they work together across the coupled system. We start with the MOM6 ocean settings, then step through the CICE sea‑ice namelist. For every group of parameters you’ll find a description, links to the relevant code or literature, and practical guidance on when you might wish to adjust the defaults. Use this as both a quick reference and a roadmap for deeper dives into the individual configuration files such as [`MOM_parameter_doc.all`](https://github.com/ACCESS-NRI/access-om3-configs/blob/release-MC_25km_jra_ryf/docs/MOM_parameter_doc.all), the list of all [MOM6](https://github.com/ACCESS-NRI/mom6) parameters, and [`cice_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/release-MC_25km_jra_ryf/ice_in), the [CICE](https://github.com/ACCESS-NRI/cice) namelist file.

## MOM6 parameter choices

### Horizontal grid

The 25km configuration uses a tripolar grid to avoid a singularity at the North Pole. The domain is zonally periodic `REENTRANT_X = True` and open at the north via a tripolar fold `TRIPOLAR_N = True` while closed in the south `REENTRANT_Y = False`. The horizontal grid has `1440x1152` tracer points. This is closely aligned with prior models, such as `ACCESS-OM2-025` and `GFDL OM4/OM5` (`1440x1080`) and provides eddy-permitting detail in the ocean while maintaining numerical stability. See [Grids](/inputs/Grids/) for more information. 

### Vertical resolution and ALE coordinate
This configuration uses 75 vertical layers (`NK=75`) with an arbitrary Lagrangian Euler (`ALE`) vertical coordinate scheme [@griffies2020primer]. The `ALE` scheme is enabled by `USE_REGRIDDING = True` (activating the “split-explicit” layered/regridding algorithm). MOM6 also supports true hybrid vertical coordinates, such as "layered isopycnal-z", where layers follow density surfaces in the ocean interior but transition to z-coordinates near the surface or bottom. However, that mode is not used in this configuration. We adopt a stretched $z^*$ vertical coordinate `REGRIDDING_COORDINATE_MODE = "ZSTAR"`. The vertical grid spacing is specified via an input file (`ALE_COORDINATE_CONFIG = "FILE:ocean_vgrid.nc,interfaces=zeta"`). The deepest ocean depth is set to `MAXIMUM_DEPTH = 6000.0`. The gravitational acceleration is `G_EARTH = 9.8` $m/s^2$. The Boussinesq approximation is made (`BOUSSINESQ = True`), meaning density variations only affect buoyancy, with all other terms using a reference density `RHO_0 = 1035` $kg/m^3$, the standard value. In our configuration, sea level is computed assuming a reference density (here using the fixed reference density for sea-level calc since `CALC_RHO_FOR_SEA_LEVEL = False`).

### Thermodynamics and Equation of State (TEOS-10)
The configuration uses `EQN_OF_STATE = "ROQUET_RHO"` for seawater. [`ROQUET_RHO`](<https://mom6.readthedocs.io/en/main/api/generated/pages/Equation_of_State.html#:~:text=in%20situ%20temperature).-,ROQUET_RHO%20Equation%20of%20State,-%C2%B6>) is based on TEOS-10, but uses a 75-term polynomial to compute in-situ density as a function of conservative temperature and absolute salinity, closely approximating the full TEOS-10 results [@roquet2015accurate]. The `_RHO` variant specifically fits density rather than specific volume, ideal for layered models and ensuring that neutral density calculations are precise. Prognostic temperature and salinity are conservative temperature and absolute salinity (`USE_CONTEMP_ABSSAL = True`), consistent with the equation of state. However, the cold-start initial conditions in our configuration use an inconsistent temperature–salinity pair - specifically, conservative temperature combined with practical salinity (see [issues/235](https://github.com/ACCESS-NRI/access-om3-configs/issues/235)).

The freezing conservative temperature is calculated from absolute salinity and pressure using a 23-term polynomial fit refactored from the TEOS-10 package (`TFREEZE_FORM = "TEOS_POLY"`). More relevant discussions or notes can be found in [TWG-23-July-2025](https://forum.access-hive.org.au/t/cosima-twg-meeting-minutes-2025/4067/17#:~:text=Freezing%20temperature%20consistency%20between%20mom6%20and%20cice). 

### Surface freezing and salinity constraints
At the ocean surface, we've turned on frazil ice formation (`FRAZIL = TRUE`), which works upwards through each water column, transferring heat downwards from the layer above as needed to prevent the in-situ temperature falling below the local freezing point in each layer in turn. If the top layer is below freezing, heat is extracted from the sea ice model, which grows frazil ice in response. More details are [here](https://mom6.readthedocs.io/en/main/api/generated/pages/Frazil_Ice.html).

We ensure salinity never goes negative by setting `BOUND_SALINITY = True`. In coupled models, sea-ice formation and melting can generate large salinity fluxes at the ocean surface. This setting clips salinity at a minimum of `MIN_SALINITY = 0.0`. However, if the lower bound is hit, it clips the salinity value and discards any excess, which may violate salt conservation in rare cases. This can occasionally trigger sea-ice model crashes due to thermodynamic conservation errors. We also set `SALINITY_UNDERFLOW = 0.0`, which resets very small salinity values to exactly zero.

Another parameter we adjust is `HFREEZE = 10.0`. This means the model computes a "melt potential" over a `10m` layer for sea-ice melt/freeze processes. If `HFREEZE >0`, the ocean will calculate how much heat is available in the top 10 meters to melt ice. 

### Surface salinity restoring
Sea surface salinity is restored toward a reference climatology by enabling `RESTORE_SALINITY = True`. The restoration uses a monthly climatological dataset from the World Ocean Atlas 2023 (SALT_RESTORE_FILE = "salt_sfc_restore.nc"), available at [NOAA NCEI](https://www.ncei.noaa.gov/products/world-ocean-atlas). A piston velocity of 0.11 $m/day$ (`FLUXCONST = 0.11`) is applied to control the strength of the salinity relaxation. The restoring is implemented as a virtual salt flux ( `SRESTORE_AS_SFLUX = True`). This approach conserves salt overall (balanced globally by subtracting the mean flux, because we set `ADJUST_NET_SRESTORE_TO_ZERO = True` to avoid altering global salinity). No effective limit is applied to the salinity restoring applied (`MAX_DELTA_SRESTORE = 999`). More discussions and decisions can be found at [issues/350](https://github.com/ACCESS-NRI/access-om3-configs/issues/350), [issues/325](https://github.com/ACCESS-NRI/access-om3-configs/issues/325), [issues/257](https://github.com/ACCESS-NRI/access-om3-configs/issues/257).

### Diagnostics and age tracer
The configuration introduces some passive tracers and diagnostics for analysis. For example, we enable `USE_IDEAL_AGE_TRACER = True`, which measures the time since water left the surface. This tracer ages at a rate of 1/year once it is isolated from the surface (`DO_IDEAL_AGE = True`). It doesn’t affect dynamics but is a diagnostic to understand water mass ventilation and residence times.

We also output 3D diagnostics on both $z*$- and density-coordinates. Specifically, `NUM_DIAG_COORDS = 2` with `DIAG_COORDS = "z Z ZSTAR", "rho2 RHO2 RHO"`, which the vertical coordinate levels for each are defined by `DIAG_COORD_DEF_Z = "FILE:ocean_vgrid.nc,interfaces=zeta"` and `DIAG_COORD_DEF_RHO2 = "RFNC1:76,999.5,1020.,1034.1,3.1,1041.,0.002"` (relevant info can be found at [PR/622](https://github.com/ACCESS-NRI/access-om3-configs/pull/622)).

### Vertical mixing parameterisations
#### Energetic planetary boundary layer (`ePBL`)
The configuration handles the vertical mixing in the ocean surface boundary layer (`OSBL`) with the `ePBL` scheme rather the the traditional `KPP`. The `ePBL` scheme is an energy-based 1D turbulence closure approach that integrates a boundary layer energy budget to determine mixing coefficients. It was developed by [@reichl2018simplified] to improve upon `KPP` for climate simulations by including the effect of turbulent kinetic energy input and wind-driven mixing in a more physically constrained way. Relevant discussions and decisions can be found at [issues/465](https://github.com/ACCESS-NRI/access-om3-configs/issues/465), [issues/426](https://github.com/ACCESS-NRI/access-om3-configs/issues/426), [issues/373](https://github.com/ACCESS-NRI/access-om3-configs/issues/373).

We keep most of parameters by default the same as the [GFDL OM5 configuration](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM5_025/MOM_parameter_doc.all). We incorporate Langmuir turbulence effects - `EPBL_LANGMUIR_SCHEME = “ADDITIVE”`. This choice adds another mixing contribution due to Langmuir circulations (wave-driven mixing). Since we do not explicitly couple to a wave model in this configuration (`USE_WAVES = False`), the Langmuir effect is parameterised via a predetermined enhancement factor in `ePBL`. We also leave the Langmuir enhancement factors at their defaults (eg, `VSTAR_SURF_FAC = 1.2`, `LT_ENHANCE_EXP = –1.5`). This inclusion of wave effects is expected to reduce warm SST biases by enhancing mixing under strong winds, as found in studies of Langmuir turbulence (e.g., `USE_LA_LI2016 = True` from [@li2016langmuir]). The `ePBL` approach overall provides a physically-based estimate of vertical diffusivities constrained by available turbulent kinetic energy, rather than relying on prescribed profiles as in `KPP`.

We have adjusted some `ePBL` parameters to match the [`GFDL` OM4 scheme](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM5_025/MOM_parameter_doc.all#L2247) (`EPBL_MSTAR_SCHEME = “OM4”`). We set `MSTAR_CAP = 1.25` (caps the mixing length scale factor `m` to 1.25) and adjusted coefficients: `MSTAR2_COEF1 = 0.29` and `COEF2 = 0.152`. These tweaks are inherited from the [GFDL OM5 configuration](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM5_025/MOM_parameter_doc.all#L2255-L2260). We also enable `USE_MLD_ITERATION = True`, which allows `ePBL` to iteratively solve for a self-consistent mixed layer depth (`MLD`) rather than a single-pass estimate. This provides a more accurate `MLD`, especially when multiple criteria (buoyancy, shear) are at play, but at the cost of a few more iterations (`EPBL_MLD_MAX_ITS = 20`). Additionally, we set `EPBL_IS_ADDITIVE = False`, which means that the diffusivity from `ePBL` is not simply added to other sources of diffusivity, instead we let `ePBL` replace shear mixing when it is more energetic, rather than always adding on top. This avoids double counting turbulence. It is a choice that effectively transitions between schemes, for example, in weak wind conditions, shear-driven mixing might dominate, but in strong wind conditions, `ePBL` mixing dominates.

#### Interior shear-driven mixing
Below the surface layer, we use a parameterisation for shear-driven mixing in stratified interior. Specifically we enable the [@jackson2008parameterization] shear instability scheme (`USE_JACKSON_PARAM = True`). This scheme targets mixing in stratified shear zones. It uses a local Richardson number (`Ri`). We keep the default critical Richardson number `RINO_CRIT = 0.25` and the nondimensional shear mixing rate `SHEARMIX_RATE = 0.089`. We also set `VERTEX_SHEAR = True`, meaning the shear is computed at cell vertices (horizontally staggered grid) to better capture shear between adjacent grid cells. That is a technical detail to get more accurate shear estimates on a C-grid. The Jackson et al. (2008) parameterisation is energetically constrained hence it iteratively finds a diffusivity such that the energy extracted from the mean flow equals the energy used in mixing plus that lost to dissipation. Our settings allow up to `MAX_RINO_IT = 25` iterations for this solve (inherited from [GFDL OM5 configuration](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM5_025/MOM_parameter_doc.all#L2088)). The Jackson scheme effectively adds interior diffusivity when `Ri<0.25`, gradually reducing it as `Ri` increases beyond critical.

#### Internal tidal mixing
`INT_TIDE_DISSIPATION = True` turns on the internal tidal mixing. It activates the parameterisation of internal tidal energy dissipation. We use `INT_TIDE_PROFILE = "POLZIN_09"`, which vertically distributes the internal tidal energy using stretched exponential profile from [@polzin2009abyssal] rather than the default St. Laurent exponential, following [@MeletHallbergLeggPolzin2013a]. We also set `READ_TIDEAMP = True` with a `tideamp.nc` file and roughness data (`H2_FILE = "bottom_roughness.nc"`). The files were generated using  tidal velocities from [`TPXO10`](https://www.tpxo.net/global/tpxo10) and updated bottom roughness calculated from [`SYNBATH`](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2021EA002069), processed via [om3-scripts/external_tidal_generation](https://github.com/ACCESS-NRI/om3-scripts/tree/main/external_tidal_generation). This indicates the model reads spatial maps of tidal velocity amplitude and topographic roughness to inform where internal tides dissipate energy. By doing so, the vertical diffusivity can be enhanced in regions of rough bathymetry and high tidal speeds. `TKE_ITIDE_MAX = 0.1` limits the energy per area that can be injected as mixing. Overall, turning on the internal tidal mixing is crucial for simulating the deep ocean stratification and circulation. 

#### Interior background mixing
For the ocean interior background mixing, we follow the approach from the [GFDL OM5 configuration](https://github.com/NOAA-GFDL/MOM6-examples/blob/3c1de3512e2200bfc10d9e5150715c9df76dbd30/ice_ocean_SIS2/Baltic_OM5_025/MOM_parameter_doc.all#L2004) of using a weak constant background diapycnal diffusivity (`KD = 1.5E-05`) for diapycnal mixing. A floor `KD_MIN = 2.0e-6` is also applied, so it won’t go below 2e-6 $m^2/s$ anywhere, ensuring numerical stability. We enable `DOUBLE_DIFFUSION = True`, which enhances vertical mixing for salt-fingering. Henyey-type internal wave scaling is set through `HENYEY_IGW_BACKGROUND = True`. The parameters `HENYEY_N0_2OMEGA = 20.0` and `HENYEY_MAX_LAT = 73.0` are kept at default. At the same time, to prevent unbounded growth of shear-based or convective mixing, we cap the total diffusivity increment from TKE-based schemes with `KD_MAX = 0.1`. This is a large upper bound that would only be triggered in extremely unstable cases.

The bottom drag is quadratic with coefficient `CDRAG = 0.003`, which is a typical value from ocean observations. `BOTTOMDRAGLAW = True` with `LINEAR_DRAG = False` means a quadratic bottom drag law rather than a linear damping. The thickness of the bottom boundary layer is set to `HBBL = 10.0` $m$.

### Horizontal viscosity and subgrid momentum mixing
In our configuration, we use a hybrid Laplacian-biharmonic viscosity scheme (`LAPLACIAN = True` - 2nd order, `BIHARMONIC = True` - 4th order) to manage unresolved subgrid momentum processes. It helps remove small-scale kinetic energy, while preserving large-scale eddy structures. Biharmonic viscosity targets the smaller scales more selectively than Laplacian (harmonic). From the [MOM6 documentation](https://mom6.readthedocs.io/en/main/api/generated/modules/mom_hor_visc.html#namespacemom-hor-visc-1section-horizontal-viscosity:~:text=Laplacian%20viscosity%20coefficient), the harmonic Laplacian viscosity coefficient is computed as following,

$$
\kappa_{\text{static}} = \min\left[\max\left(\kappa_{\text{bg}}, U_\nu \Delta(x,y), \kappa_{2d}(x,y), \kappa_{\phi}(x,y)\right), \kappa_{max}(x,y)\right]
$$

where,

1. $\kappa_{\text{bg}}$ (`USE_KH_BG_2D = False`) is constant but spatially variable 2D map, also there is no constant background viscosity (`KH = 0`).
2. $U_\nu \Delta(x,y)$ ($U_\nu$ = `KH_VEL_SCALE = 0.01`) is a constant velocity scale,
3. $\kappa_{\phi}(x,y) = \kappa_\pi|sin(\phi)|^n$ (`KH_SIN_LAT = 2000.0`, `KH_PWR_OF_SINE = 4`) is a function of latitude,

The full viscosity includes the dynamic components,

$$
\kappa_h(x,y,t) = r(\Delta, L_d)\max\left(\kappa_{\text{static}}, \kappa_{\text{Smagorinsky}}, \kappa_{\text{Leith}}\right)
$$

where,

1. $r(\Delta, L_d)$ (`RESOLN_SCALED_KH = True`) is a resolution function. This will scale down the Laplacian component of viscosity in well-resolved regions.
2. $\kappa_{\text{Smagorinsky}}$ (`SMAGORINSKY_KH = False`) is from the dynamic Smagorinsky scheme,
3. $\kappa_{\text{Leith}}$ (`LEITH_KH = False`) is the Leith viscosity.

We enable `BOUND_KH = True` to locally limit the Laplacian diffusivity ensuring CFL stability. Specifically, a coefficient `Kh_Limit = 0.3 / (dt * 4.0)` is applied, taking grid spacing into account. To further improve numerical stability, we enable both `BETTER_BOUND_KH = True` and `BETTER_BOUND_AH = True`, which apply more refined constraints on Laplacian and biharmonic viscosities, respectively. We set `RES_SCALE_MEKE_VISC = False`, meaning the viscosity is not explicitly scaled by MEKE. For biharmonic viscosity, we apply a flow-dependent Smagorinsky parameterisation with no background value (`AH = 0.0`). The viscosity is dynamically computed based on the local strain rate by enabling `SMAGORINSKY_AH = True`, and is scaled using `SMAG_BI_CONST = 0.06` (the MOM6 default). Anisotropic viscosity is disabled via `ANISOTROPIC_VISCOSITY = False`. Finally, to maintain numerical stability, the biharmonic viscosity is locally bounded using `BOUND_AH = True`, with a coefficient limit `Ah_Limit = 0.3 / (dt * 64.0)`.

For the channel drag, a Laplacian Smagorinsky constant ([`SMAG_CONST_CHANNEL = 0.15`](https://github.com/ACCESS-NRI/MOM6/blob/569ba3126835bfcdea5e39c46eeae01938f5413c/src/parameterizations/vertical/MOM_set_viscosity.F90#L967-L969)) is used.

### Isopycnal mixing
At 25km resolution, the model begins to resolve some mesoscale eddies, but parameterisation is still needed for the unresolved part. The configuration uses a hybrid parameterisation for mesoscale eddies, combining neutral diffusion [@redi1982oceanic] and a dynamic Gnet-McWilliams scheme [@gent1990isopycnal] based on an eddy kinetic energy budget. 


#### Isopycnal thickness diffusion (`GM`)
`GM` is turned on via `THICKNESSDIFFUSE = True`. Instead of using a fixed `GM` thickness diffusivity (`KHTH = 0.0`), the Mesoscale Eddy Kinetic Energy (MEKE) scheme (`USE_MEKE = True`) is turned on. MEKE activates a prognostic equation for eddy kinetic energy (EKE) and a spatially varying GM streamfunction. The MEKE parameterisation is based on the work of [@jansen2015parameterization], where an EKE budget is solved. The model converts that EKE into an eddy diffusivity (GM diffusivity) via mixing-length theory. In practice, this means the thickness diffusion coefficient is not a fixed number but evolves according to local conditions. Our configuration does not feed external `EKE` data (`EKE_SOURCE = "prog"`), so the model instability growth provides the source of `EKE`. `MEKE_BGSRC = 1.0E-13` prevents `EKE` from decaying to zero in very quiet regions. It serves as a floor to aid numerical stability and is analogous to a background diffusivity but in energy form. `MEKE_GMCOEFF = 1.0` means the scheme converts eddy potential energy to eddy kinetic energy with 100% efficiency for the `GM` effect. `MEKE_KHTR_FAC = 0.5` and `MEKE_KHTH_FAC = 0.5` map some of the eddy energy to tracer diffusivity and lateral thickness diffusivity, respectively. So the configuration actually uses `MEKE` to the job of `GM`: flatterning isopycnals to remove available potential energy, but in a physically informed way using a local EKE prognostic variable. We use `KHTH_USE_FGNV_STREAMFUNCTION = True` which solves a 1D boundary value problem so the `GM` streamfunction is automatically smooth in the vertical and vanishes at the surface and bottom [@ferrari2010boundary]. `FGNV_FILTER_SCALE = 0.1` is used to damp the eddy field noise.

By using `MEKE`, the model is effectively resolution-aware, as resolution increases and resolves more eddies, the diagnostic EKE and hence `GM` coefficient naturally reduces. At the same time , in coarser areas or higher latitudes where eddies are still under-resolved, `MEKE` ramps up the eddy mixing. This avoids the need for ad-hoc spatial maps of `GM` coefficients. By using `FGNV`[@ferrari2010boundary], it ensures a robust energetically consistent vertical structure. 

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

This document walks through each of these namelist groups and provides a short explanation of what each group controls and how it is configured in our `ACCESS-OM3` setup.

### `setup_nml`
This group defines time-stepping, run length, output frequencies, initial conditions, and I/O settings.

- Time-stepping and run length
    - The timestep `dt` is not defined in `ice_in` directly; it is overwritten in the CICE NUOPC cap to match the driver timestep (coupling timestep). See [NUOPC driver](/infrastructure/NUOPC-driver/) for more information.
- Initialisation: 
    - [`ice_ic`](https://cice-consortium-cice.readthedocs.io/en/cice6.0/user_guide/ug_case_settings.html#:~:text=*-,ice_ic,-default)
        - When set to `"default"`, CICE initialises sea ice concentration and thickness based on latitude.
        - If set to `"none"`, the model starts with no sea ice.
- Ouput frequencies
   - Defines up to five output streams:
   ```bash
    histfreq = "d", "m", "x", "x", "x"
    hist_suffix = ".1day.mean", ".1mon.mean", "x", "x", "x"
   ```

    - Daily averaged output: `.1day.mean`
    - Monthly averaged output: `.1mon.mean`
    - Streams marked `"x"` are unused.

   - History files use `hist_time_axis = "middle"` to center timestamps in the averaging interval.

### `grid_nml`
This groups defines the spatial grid, land mask, and ice thickness category structure.

- Horizontal Grid
    - Tripolar grid at 25 km nominal resolution: `grid_type = "tripole"`
    - Grid files:
        - The grid is defined by `grid_file = "./INPUT/ocean_hgrid.nc"`. We use the MOM grid file in CICE for best consistency between model components.
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
    - Uses elastic-viscous-plastic (`EVP`) rheology [@hunke1997elastic],
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
    - `ahmax = 0.1` is the thickness parameter for albedo, which is constant above this thickness. In our configuration, it means once ice is ~10cm thick, it is treated optically like thick ice and there will be no further albedo increase. Thinner ice, which is less than 10cm, will have a lower effective albedo. 
- Pond/algae effects:
    - [`kalg = 0.0`](https://github.com/CICE-Consortium/CICE/blob/2cdd3d007a409d26cb0c16d946678a544ada55fa/doc/source/user_guide/ug_case_settings.rst#L556:~:text=1.5-,kalg,-real) means no additional algae-related absorption,
    - [`r_snw = 0.0`](https://github.com/CICE-Consortium/CICE/blob/2cdd3d007a409d26cb0c16d946678a544ada55fa/doc/source/user_guide/ug_case_settings.rst#L556:~:text=0.0-,R_snw,-real) is a tuning parameter for snow (broadband albedo) from Delta-Eddingon shortwave, here it is 0, which means not using additional boradband albedo tuning.

### `forcing_nml`
The forcing namelist governs how external forcing (`atm` and` ocn`) is applied to the ice, including coupling flux adjustments.

- Atmosphere
    - `highfreq = .true.`: Uses the relative atmosphere-ice velocity instead of the only atmospheric velocity for boundary layer fluxes
- Ocean
    - `update_ocn_f = .true.`: uses coupled frazil water/salt fluxes from ocean,
    - `ustar_min = 0.0005`: Minimum ocean friction velocity to ensure stability.
- Freezing temperature
    - `tfrz_option = "linear_salt"`: Freezing point depends on salinity. [Thermodynamics and Equation of State (TEOS-10)](#thermodynamics-and-equation-of-state-teos-10) for more information,
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
- Max Blocks
    - `max_blocks = -1` Internally calculated number of blocks per processor,
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
        - `f_hi = "md"`: grid-cell mean ice thickness,
        - `f_hs = "md"`: snow depth on ice,
        - `f_aicen = "m"`: ice area in each thickness category,
        - `f_vicen = "m"`:  ice volume in each category,
        - `f_snoice = "md"`: snow-ice formation field,
        - `f_congel = "md"`: congelation ice growth; “congel” refers to new ice freezing at the bottom of existing ice (opposite of frazil which is open-water freezing),
        - `f_frazil = "md"`: frazil ice formation (freezing of open water),
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

    4. Snow and Pond:
        - `f_fsloss = "m"`: rate of snow loss to leads,
        - `f_meltsliq = "m"`: melted snow liquid,
        - `f_rhos_cmp = "m"`: density of snow due to wind compaction,
        - `f_rhos_cnt = "m"`: density of ice and liquid content of snow,
        - `f_rsnw = "m"`: snow grain radius,
        - `f_smassice = "m"`: mass of ice in snow from smice tracer,
        - `f_smassliq = "m"`: mass of liquid in snow from smliq tracer,

## References

\bibliography
