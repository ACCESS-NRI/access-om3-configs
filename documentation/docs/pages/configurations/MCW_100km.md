# MOM6-CICE6-WW3 100 km configuration

The [`dev-MCW_100km_era_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_era_iaf) configuration couples MOM6, CICE6 and WAVEWATCH III (WW3) on the nominal 100 km ACCESS-OM3 grid. Unlike the MOM6-CICE 25 km configuration, which uses JRA55-do, this configuration uses [ERA5 atmospheric forcing](/inputs/ERA5-atmospheric-forcing/). The forcing preparation, field mappings and configuration changes are documented on that dedicated page and are not repeated here.

MOM6 and CICE6 choices shared with other configurations are documented for the [MOM6-CICE 25 km configuration](/configurations/MC_25km/). A branch-specific workflow for running this configuration and regenerating its WW3 inputs is included below.

!!! warning
    These settings describe the development branch `dev-MCW_100km_era_iaf` with `access-om3/2026.05.003` (`access-mom6 2026.05.002`, `access-cice CICE6.6.3-2` and `access-ww3 2026.03.001`). Recheck the branch inputs and model release before applying them to another configuration.

## MOM6 parameter choices

### Wave coupling

In [`MOM_input`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MCW_100km_era_iaf/MOM_input), `USE_WAVES = True` activates MOM6's surface-wave interface. This configuration uses `WAVE_METHOD = "SURFACE_BANDS"` and `SURFBAND_SOURCE = "COUPLER"`, so MOM6 receives the zonal and meridional Stokes drift divided into surface wavenumber bands from WW3 rather than diagnosing waves from local winds.

Three bands are exchanged:

```text
STK_BAND_COUPLER = 3
SURFBAND_WAVENUMBERS = 0.04, 0.11, 0.3305  rad m-1
```

These values must agree with WW3's `IUSSP = 3` and `STK_WN = 0.04, 0.110, 0.3305`. MOM6 checks the number of coupled bands at run time, then uses the coupled band velocities and wavenumbers to reconstruct the vertical Stokes-drift profile.

### Stokes drift and Langmuir turbulence

The closest non-wave 100 km configuration estimates the Langmuir number with `USE_LA_LI2016 = True`. The MCW configuration instead sets `EPBL_LT = True`, allowing the energetic planetary boundary layer (ePBL) scheme [@reichl2018simplified] to calculate a Langmuir number from the coupled Stokes-drift profile. `EPBL_LANGMUIR_SCHEME = "ADDITIVE"` adds the Langmuir-turbulence contribution to the other contributions to the ePBL mixing-energy factor [@reichl2019parameterization; @li2019comparing].

The selected **E12** coefficients are `LT_ENHANCE_COEF = 0.150`, `LT_ENHANCE_EXP = -1.0`, and `LT_MOD_LAC1 = LT_MOD_LAC2 = LT_MOD_LAC3 = LT_MOD_LAC4 = LT_MOD_LAC5 = 0.0`. E12 is an ACCESS-OM3 tuning, not a parameter set taken directly from the literature. It was selected through [sensitivity experiments documented in issue #950](https://github.com/ACCESS-NRI/access-om3-configs/issues/950), balancing mixed-layer-depth and Antarctic sea-ice biases and RMSE.

The literature-based E00 starting point used `LT_ENHANCE_COEF = 0.105`, `LT_ENHANCE_EXP = -1.0`, `LT_MOD_LAC1 = LT_MOD_LAC2 = LT_MOD_LAC3 = 0.0`, and `LT_MOD_LAC4 = LT_MOD_LAC5 = 0.8`, following the published surface-layer Langmuir-number formulation [@reichl2019parameterization; @li2019comparing]. E12 retains the exponent and `LT_MOD_LAC1/2/3`, but its `LT_ENHANCE_COEF = 0.150` and `LT_MOD_LAC4/5 = 0.0` come from the ACCESS-OM3 parameter sweep.

This MOM6 treatment is separate from WW3's own `LMPN` option, which is disabled below.

### Time stepping

The ocean baroclinic timestep is `DT = 3600` s, equal to the coupling interval. `DT_THERM = 7200` s and `THERMO_SPANS_COUPLING = True` allow one thermodynamic step to span two coupling intervals. `DTBT = -0.9` instructs MOM6 to choose a barotropic timestep at 90% of its estimated stable maximum and round it to an integer subdivision of `DT`. These settings were introduced and tested in [PR #1518](https://github.com/ACCESS-NRI/access-om3-configs/pull/1518); the shorter `DT` used by the 25 km configuration is resolution-dependent.

## CICE6 parameter choices

### Floe-size distribution

In [`ice_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MCW_100km_era_iaf/ice_in), the MCW configuration changes `nfsd` from one to 12 and enables the prognostic floe-size-distribution tracer with `tr_fsd = .true.`. CICE therefore evolves ice area across 12 floe-radius categories as well as its five ice-thickness categories. The distribution responds to new-ice formation, lateral growth and melt, thermodynamic welding, and wave fracture; these processes affect floe perimeter and hence lateral melt rates [@roach2019advances].

### Wave forcing

`wav_coupling_to_cice = .true.` in `nuopc.runconfig` connects the models in both directions. CICE supplies ice thickness and floe diameter to WW3, while WW3 supplies its instantaneous 25-bin wave-elevation spectrum to CICE at each coupling exchange. CICE uses that spectrum in its wave-fracture step to update the floe-size distribution.

`wave_spec_type = "constant"` does **not** mean that the spectrum is constant in time. In the CICE/Icepack wave-fracture algorithm it selects a fixed phase and one fracture iteration, avoiding the random-number generator and giving bit-for-bit reproducible results for an identical run. The alternative `random` mode draws random phases and iterates fracture to convergence.

### Wave and floe-size diagnostics

The relevant fields in `icefields_fsd_nml` are written to both daily and monthly streams (`"md"`). They comprise:

- `fsdrad` and `fsdperim`: representative floe radius and perimeter per unit ice area;
- `afsd` and `afsdn`: areal floe-size distribution, respectively aggregated over and resolved by ice-thickness category;
- `dafsd_newi`, `dafsd_latg`, `dafsd_latm`, `dafsd_wave` and `dafsd_weld`: floe-size-distribution tendencies from new ice, lateral growth, lateral melt, wave fracture and welding;
- `wave_sig_ht`: significant wave height [diagnosed by CICE](https://github.com/ACCESS-NRI/CICE/blob/CICE6.6.3-2/cicecore/cicedyn/general/ice_step_mod.F90#L710-L713) from the instantaneous spectrum imported from WW3.

These fields allow changes in floe size to be attributed to their physical processes and compared with the wave conditions that drive fracture.

## WAVEWATCH III parameter choices

### Grid and spectral discretisation

The branch's [`ww3_grid.nml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MCW_100km_era_iaf/WW3_PreProc/ww3_grid.nml) configures the same 360 x 324 curvilinear, spherical tripolar grid as MOM6 and CICE6. The preprocessor also reads an unresolved-obstruction map; `FLAGTR = 4` places its static transparencies at cell centres.

The wave spectrum has 25 frequency bins beginning at 0.04118 Hz, with successive frequencies multiplied by 1.1. It has 24 directional bins, giving 15-degree directional resolution. `THOFF` offsets the first direction by −0.5 to 0.5 of that 15-degree increment; `THOFF = 0.0` leaves the directional grid unshifted. Non-zero offsets can help mitigate the garden-sprinkler effect with `PR1` [@ww3dg2019manual].

### Compiled physics switches

The ACCESS-OM3 executable used by this configuration compiles WW3 with:

```cmake
CESMCOUPLED DIST MPI PR1 FLX4 ST6 STAB0 LN1 NL1 BT1 DB1 MLIM TR0 BS0
RWND WNX1 WNT0 CRX1 CRT0 O0 O1 O2 O3 O4 O5 O6 O7 O14 O15 IS0 REF0
NOGRB IC4
```

The scientifically important selections are `PR1` propagation, `ST6` wind input and dissipation, `LN1` linear wave growth, `NL1` nonlinear quadruplet interactions, `BT1` bottom friction, `DB1` depth-induced breaking and `IC4` wave–ice attenuation. `PR1` is WW3's conservative first-order upwind scheme for propagating wave action; *first order* describes its numerical accuracy, and the scheme is more diffusive than the higher-order propagation options [@ww3dg2019manual]. `IS0` selects no separate wave–ice scattering source term. The parameter namelists used below correspond to these compiled packages: `SIN6` and `SWL6` to `ST6`, `SNL1` to `NL1`, and `SIC4` to `IC4`.

The executable does not contain `PR3`, `IC3` or `IS2`. Consequently, the `PRO3` garden-sprinkler-effect tuning, IC3 viscoelastic parameters, and IS2 floe-scattering parameters described in older WW3 configuration notes are inactive and should not be added to this configuration. Changing to any of those packages requires a new executable built with the matching switch, not just a namelist change.

### Time stepping

In ACCESS-OM3's coupled WW3 pathway, selected by WW3's historically named `CESMCOUPLED` compile switch, WW3 restores the timestep controls from [`wav_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MCW_100km_era_iaf/wav_in) after reading the preprocessed `mod_def.ww3`. The `DTMAX`, `DTXY`, `DTKTH` and `DTMIN` values in `ww3_grid.nml` are therefore preprocessor inputs, not the effective runtime limits. The current runtime values are:

| `wav_in` parameter | Runtime value | Purpose |
| --- | ---: | --- |
| `dtmax` | 1800 s | maximum overall integration step |
| `dtcfl` | 600 s | horizontal-propagation CFL step |
| `dtcfli` | 600 s | spectral propagation and refraction step |
| `dtmin` | 50 s | minimum source-term integration step |

[Issue #1519](https://github.com/ACCESS-NRI/access-om3-configs/issues/1519) estimates a 643.8 s horizontal CFL limit from the smallest active grid spacing and the fastest group speed at the first spectral frequency. The selected 600 s `dtcfl` has an estimated CFL number of 0.839 and divides the 3600 s coupling interval exactly. With `PR1`, WW3 applies additional local substeps for current effects. `dtmax = 1800` s is three times `dtcfl` and also divides the coupling interval; `dtcfli = 600` s is one third of `dtmax`, but its suitability must be assessed empirically because it is not determined by spatial grid spacing alone. The issue proposes testing `dtmin = 10` s because the current 50 s value has no configuration-specific justification; the branch nevertheless still uses 50 s.

### Source-term physics

The branch's [`namelists_Global.nml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MCW_100km_era_iaf/WW3_PreProc/namelists_Global.nml) configures the compiled `ST6` package, which represents wind input, whitecapping dissipation and swell dissipation and constrains total wind input using the independently calculated wind stress. `SINA0 = 0.04` controls negative wind input when wind opposes the waves. For swell dissipation, `SWLB1 = 0.22e-3` is the scaling coefficient and `CSTB1 = T` selects the formulation in which that coefficient is constant rather than rescaled by peak steepness. The observation-based development of ST6 is described in [@rogers2012observation; @zieger2015observation].

`NL1` represents the nonlinear four-wave source term using the Discrete Interaction Approximation (DIA) [@hasselmann1985parameterizations]. `LAMBDA = 0.237` and `NLPROP = 2.13e7` tune the representative interacting quadruplet and its proportionality coefficient, respectively.

### Stokes-drift output and MOM6 coupling

`USSP = 1` enables partitioned Stokes-drift output, while `IUSSP = 3` requests three bands represented by decay wavenumbers `STK_WN = 0.04, 0.110, 0.3305`. WW3 exports both vector components for each band to MOM6. `E3D = 1` enables frequency-resolved energy-spectrum output; independently of that output flag, the coupled WW3 cap exports the 25-bin elevation spectrum to CICE6 at each coupling exchange. These coupled fields are instantaneous WW3 state at the exchange time, not interval means.

The band count and wavenumbers are a coupling contract: changing them requires matching changes to MOM6's `STK_BAND_COUPLER` and `SURFBAND_WAVENUMBERS`, followed by regeneration of `mod_def.ww3`.

### Langmuir settings

WW3 is configured with `LMPENABLED = F` and `HSLMODE = 0`. Its Li et al. Langmuir-mixing parameterisation [@li2016langmuir] is therefore disabled, and the value of `HSLMODE` has no active effect. Langmuir enhancement in this configuration is instead calculated within MOM6 ePBL from the Stokes-drift bands supplied by WW3.

### Wave-ice interaction

The active attenuation choice is `SIC4 IC4METHOD = 8`. In the pinned `access-ww3 2026.03.001` source, [`CASE (8)`](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/w3sic4md.F90#L559-L595) combines a floe-size-dependent cubic fit associated with Meylan et al. [@meylan2021floe] with the **IC4M2** empirical attenuation of Meylan et al. [@meylan2014situ], `0.00212 / T^2 + 0.0459 / T^4`. The cubic component depends on wave period, coupled ice thickness, and a radius obtained by halving the coupled floe diameter, adding dependence on the CICE ice state while that component is active.

Thickness is clipped to 0.1–3.5 m and radius to 2.5–100 m. The cubic fit predicts the base-10 logarithm of energy attenuation, capped at zero before conversion back to linear units. For `5 < T < 20` s, IC4M2 is added to the cubic result; for `T > 20` s, IC4M2 is used alone. WW3 then sets amplitude attenuation to half the energy attenuation. The coefficients are hard-coded rather than set in `namelists_Global.nml`.

This implementation differs from upstream WW3's use of the name **IC4M8** for the order-3 power-law model of Meylan et al. [@meylan2018dispersion], introduced through [NOAA-EMC/WW3 issue #1167](https://github.com/NOAA-EMC/WW3/issues/1167) and [PR #1176](https://github.com/NOAA-EMC/WW3/pull/1176). That model has the form `k_i = C_hf h_ice f^3`; therefore, `IC4METHOD = 8` should not be assumed to select the same formulation across these WW3 versions.

`CICE0 = 0.25` and `CICEN = 0.75` are present in the namelist but do not control IC4 attenuation. In `access-ww3 2026.03.001`, the [concentration-based propagation-transparency ramp](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/w3updtmd.F90#L2975-L3040) is compiled only with `IC0`; this executable instead uses `IC4`. `FLAGTR = 4` still applies the static unresolved-obstruction data at cell centres, while IC4 wave attenuation is calculated separately.

`ICNUMERICS = T` is required by the matching ACCESS-NRI WW3 implementation to activate the compiled sea-ice source-term calculation. The source term is scaled by ice concentration before it is included in the spectral source-term integration. This switch is specific to the `access-ww3 2026.03.001` implementation used by the documented configuration and should be rechecked when changing executable versions.

### Other numerical choices

WW3 uses a 365-day calendar to match the coupled model. Its initial condition is a fetch-limited JONSWAP spectrum (`ITYPE = 3`) calculated from local wind speed and direction, using the grid-cell scale as the fetch and constraining the result to the configured frequency range.

## Appendix: PR3 tuning (not active)

This configuration is compiled with the `PR1` propagation scheme, so a `PRO3` namelist would be ignored. If a future executable replaces `PR1` with `PR3`, the `WDTHCG` and `WDTHTH` parameters should be tuned to mitigate the garden-sprinkler effect. Chawla and Tolman provide the following resolution-dependent factors [@chawla2008obstruction]:

| Angular grid spacing | `WDTHCG` and `WDTHTH` | Approximate spacing |
| ---: | ---: | ---: |
| 2 arcmin | 16 | 3.7 km |
| 4 arcmin | 8 | 7.4 km |
| 8 arcmin | 4 | 14.8 km |
| 15 arcmin | 2 | 27.8 km |
| 30 arcmin | 1 | 55.6 km |

For example, the parameters are specified as:

```fortran
&PRO3 WDTHCG = <value>, WDTHTH = <value> /
```

The published table does not prescribe a value for the nominal 100 km ACCESS-OM3 grid. A migration to `PR3` would therefore require grid-appropriate analysis and validation rather than extrapolating this table. It would also require rebuilding ACCESS-OM3 with the `PR3` switch and regenerating `mod_def.ww3`.

## Running and regenerating WW3 inputs

Clone the ERA5 interannual-forcing branch and enter the resulting configuration directory:

```bash
module use /g/data/vk83/modules
module load payu
payu clone --branch dev-MCW_100km_era_iaf \
  git@github.com:ACCESS-NRI/access-om3-configs.git mcw_100km_era_iaf
cd mcw_100km_era_iaf
```

The supplied `mod_def.ww3` and `restart.ww3` can be used without preprocessing. If the WW3 preprocessing inputs are changed, load the exact `access-om3` version specified by `config.yaml`; for the version documented here this is:

```bash
module load access-om3/2026.05.003
cd WW3_PreProc
ww3_grid
ww3_strt
```

`ww3_grid` regenerates `mod_def.ww3` from `ww3_grid.nml`, including the grid, spectral discretisation and applicable parameters in `namelists_Global.nml`. `ww3_strt` regenerates `restart.ww3` from `ww3_strt.inp` and the grid definition. Update the `input` paths in `config.yaml` to point to the regenerated files before running. A change only to parameter values for already compiled packages requires regeneration of `mod_def.ww3`; selecting a different physics or propagation package also requires an ACCESS-OM3 executable built with the corresponding WW3 switch.

From the configuration directory, initialise and submit the experiment with:

```bash
payu sweep
payu run
```

## References

\bibliography
