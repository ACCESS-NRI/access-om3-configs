# MOM6-CICE6-WW3 100 km configuration

The [`dev-MCW_100km_era_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_era_iaf) configuration couples MOM6, CICE6 and WAVEWATCH III (WW3) on the nominal 100 km ACCESS-OM3 grid. Unlike the MOM6-CICE 25 km configuration, which uses JRA55-do, this configuration uses [ERA5 atmospheric forcing](https://github.com/ACCESS-NRI/access-om3-configs/blob/c1a4ed2cbe66b3003fbf04285487a7daaf2bbf03/documentation/docs/pages/inputs/ERA5-atmospheric-forcing.md). The forcing preparation, field mappings and configuration changes are documented in that guide, pending [PR #1662](https://github.com/ACCESS-NRI/access-om3-configs/pull/1662); the link points to its PR source while it is not yet part of this site. Runoff remains JRA55-do through DROF.

Background on MOM6 and CICE6 parameter choices is documented for the [MOM6-CICE 25 km configuration](/configurations/MC_25km/). Resolution-dependent settings should not be copied unchanged. A branch-specific workflow for running this configuration and regenerating its WW3 inputs is included below.

!!! warning
    These settings describe `dev-MCW_100km_era_iaf` at [commit `bbf1c86`](https://github.com/ACCESS-NRI/access-om3-configs/tree/bbf1c86c50dfa0716c47fd9be2e261169fd911e7) (checked 16 October 2026), using `access-om3/2026.05.004`. The deployed executable uses [MOM6 `2026.05.003`](https://github.com/ACCESS-NRI/MOM6/tree/d11a149ccba676d524312328f7eb62560a156dc3), [CICE `CICE6.6.3-2`](https://github.com/ACCESS-NRI/CICE/tree/2b267226f6c2a67a0e6bafcd4a1c0bd772850611) and [WW3 `2026.03.001`](https://github.com/ACCESS-NRI/WW3/tree/0a23b2c358150b420919f47545ae81b76fa39a0f), linked by `access3 2026.03.002`. Recheck the branch inputs and model release before applying these settings to another revision.

## MOM6 parameter choices

### Wave coupling

In [`MOM_input`](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/MOM_input), `USE_WAVES = True` activates MOM6's surface-wave interface. This configuration uses `WAVE_METHOD = "SURFACE_BANDS"` and `SURFBAND_SOURCE = "COUPLER"`, so MOM6 receives the zonal and meridional Stokes drift divided into surface wavenumber bands from WW3 rather than diagnosing waves from local winds.

Three bands are exchanged:

```text
STK_BAND_COUPLER = 3
SURFBAND_WAVENUMBERS = 0.04, 0.11, 0.3305  rad m-1
```

These values must agree with WW3's `IUSSP = 3` and `STK_WN = 0.04, 0.110, 0.3305`. MOM6 checks the number of coupled bands at run time, then uses the coupled band velocities and wavenumbers to reconstruct the vertical Stokes-drift profile.

### Stokes drift and Langmuir turbulence

The closest non-wave 100 km configuration estimates the Langmuir number with `USE_LA_LI2016 = True`. The MCW configuration instead sets `EPBL_LT = True`, allowing the energetic planetary boundary layer (ePBL) scheme [@reichl2018simplified] to calculate a Langmuir number from the coupled Stokes-drift profile. `EPBL_LANGMUIR_SCHEME = "ADDITIVE"` adds the Langmuir-turbulence contribution to the other contributions to the ePBL mixing-energy factor [@reichl2019parameterization; @li2019comparing].

The selected **E12** coefficients are `LT_ENHANCE_COEF = 0.150`, `LT_ENHANCE_EXP = -1.0`, and `LT_MOD_LAC1 = LT_MOD_LAC2 = LT_MOD_LAC3 = LT_MOD_LAC4 = LT_MOD_LAC5 = 0.0`. E12 is an ACCESS-OM3 tuning, not a parameter set taken directly from the literature. It was selected through [sensitivity experiments documented in issue #950](https://github.com/ACCESS-NRI/access-om3-configs/issues/950), balancing mixed-layer-depth and Antarctic sea-ice biases and RMSE, and applied in [PR #1684](https://github.com/ACCESS-NRI/access-om3-configs/pull/1684). `LT_MOD_LAC2/3` are not explicitly set in `MOM_input`: both have effective defaults of zero in this build, also recorded in its [parameter documentation](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/docs/MOM_parameter_doc.all). The later Stokes-tail change below alters the coupled forcing of this tuning; it does not change these coefficients.

The literature-based E00 starting point used `LT_ENHANCE_COEF = 0.105`, `LT_ENHANCE_EXP = -1.0`, `LT_MOD_LAC1 = LT_MOD_LAC2 = LT_MOD_LAC3 = 0.0`, and `LT_MOD_LAC4 = LT_MOD_LAC5 = 0.8`, following the published surface-layer Langmuir-number formulation [@reichl2019parameterization; @li2019comparing]. E12 retains the exponent and `LT_MOD_LAC1/2/3`, but its `LT_ENHANCE_COEF = 0.150` and `LT_MOD_LAC4/5 = 0.0` come from the ACCESS-OM3 parameter sweep.

This MOM6 treatment is separate from WW3's own `LMPN` option, which is disabled below.

### Time stepping

The ocean baroclinic timestep is `DT = 3600` s, equal to the coupling interval. `DT_THERM = 7200` s and `THERMO_SPANS_COUPLING = True` allow one thermodynamic step to span two coupling intervals. `DTBT = -0.9` instructs MOM6 to choose a barotropic timestep at 90% of its estimated stable maximum and round it to an integer subdivision of `DT`. These settings were introduced and tested in [PR #1518](https://github.com/ACCESS-NRI/access-om3-configs/pull/1518); the shorter `DT` used by the 25 km configuration is resolution-dependent.

## CICE6 parameter choices

### C-grid dynamics and matching inputs

`grid_ice = "C"` selects C-grid ice dynamics. [PR #1739](https://github.com/ACCESS-NRI/access-om3-configs/pull/1739) updated the WW3 preprocessing mask and binaries to match the CICE land mask; its restart test passed after that correction. Keep the CICE `kmt.nc`, coupling meshes, WW3 text mask/depth and preprocessed binaries consistent when changing topography. The current input set is described below.

### Floe-size distribution

In [`ice_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/ice_in), the MCW configuration changes `nfsd` from one to 12 and enables the prognostic floe-size-distribution tracer with `tr_fsd = .true.`. CICE therefore evolves ice area across 12 floe-radius categories as well as its five ice-thickness categories. The distribution responds to new-ice formation, lateral growth and melt, thermodynamic welding, and wave fracture; these processes affect floe perimeter and hence lateral melt rates [@roach2019advances].

### Wave forcing

`wav_coupling_to_cice = .true.` in [`nuopc.runconfig`](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/nuopc.runconfig) connects the models in both directions. CICE supplies ice concentration, thickness and floe diameter to WW3, while WW3 supplies its instantaneous 25-bin wave-elevation spectrum to CICE at each coupling exchange. CICE uses that spectrum in its wave-fracture step to update the floe-size distribution.

`wave_spec_type = "constant"` does **not** mean that the spectrum is constant in time. In the [Icepack wave-fracture algorithm](https://github.com/CICE-Consortium/Icepack/blob/daa41638c6cef298583f35ee4dec5ab1bb077aea/columnphysics/icepack_wavefracspec.F90#L450-L488) it selects a fixed phase and one fracture iteration, avoiding the random-number generator; this removes that source of nondeterminism, rather than guaranteeing reproducibility of the entire coupled model. The alternative `random` mode draws random phases and iterates fracture to convergence.

### Wave and floe-size diagnostics

The relevant fields in `icefields_fsd_nml` are written to both daily and monthly streams (`"md"`). They comprise:

- `fsdrad` and `fsdperim`: representative floe radius and perimeter per unit ice area;
- `afsd` and `afsdn`: areal floe-size distribution, respectively aggregated over and resolved by ice-thickness category;
- `dafsd_newi`, `dafsd_latg`, `dafsd_latm`, `dafsd_wave` and `dafsd_weld`: floe-size-distribution tendencies from new ice, lateral growth, lateral melt, wave fracture and welding;
- `wave_sig_ht`: significant wave height [diagnosed by CICE](https://github.com/ACCESS-NRI/CICE/blob/CICE6.6.3-2/cicecore/cicedyn/general/ice_step_mod.F90#L710-L713) from the instantaneous spectrum imported from WW3;
- `aice_ww`, `diam_ww` and `hice_ww`: [concentration, number-mean diameter and thickness of floes larger than `Dmin`](https://github.com/ACCESS-NRI/CICE/blob/2b267226f6c2a67a0e6bafcd4a1c0bd772850611/cicecore/cicedyn/analysis/ice_history_fsd.F90#L162-L176), provided as wave-related diagnostics.

These fields allow changes in floe size to be attributed to their physical processes and compared with the wave conditions that drive fracture.

## WAVEWATCH III parameter choices

### Grid and spectral discretisation

The branch's [`ww3_grid.nml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/WW3_PreProc/ww3_grid.nml) configures the same 360 x 324 curvilinear, spherical tripolar grid as MOM6 and CICE6. The preprocessor also reads an unresolved-obstruction map; `FLAGTR = 4` places its static transparencies at cell centres.

The wave spectrum has 25 frequency bins beginning at 0.04118 Hz, with successive frequencies multiplied by 1.1. It has 24 directional bins, giving 15-degree directional resolution. `THOFF` offsets the first direction by −0.5 to 0.5 of that 15-degree increment; `THOFF = 0.0` leaves the directional grid unshifted. `THOFF` rotates the directional grid; it is not a dedicated garden-sprinkler correction. The [versioned manual](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/manual/num/GSE_null.tex) states that no such correction is available or needed for `PR1` on this grid type.

### Compiled physics switches

The deployed WW3 library (`bjzidie`), linked into the `access3` executable (`26wbxup`), was compiled with the following switches, matching its [version-pinned CMake configuration](https://github.com/ACCESS-NRI/WW3/blob/0a23b2c358150b420919f47545ae81b76fa39a0f/CMakeLists.txt#L20):

```cmake
CESMCOUPLED DIST MPI PR1 FLX4 ST6 STAB0 LN1 NL1 BT1 DB1 MLIM TR0 BS0
RWND WNX1 WNT0 CRX1 CRT0 O0 O1 O2 O3 O4 O5 O6 O7 O14 O15 IS0 REF0
NOGRB IC4
```

The scientifically important selections are `PR1` propagation, `ST6` wind input and dissipation, `LN1` linear wave growth, `NL1` nonlinear quadruplet interactions, `BT1` bottom friction, `DB1` depth-induced breaking and `IC4` wave–ice attenuation. `PR1` is WW3's conservative first-order upwind scheme for propagating wave action; *first order* describes its numerical accuracy, and the scheme is more diffusive than the higher-order propagation options [@ww3dg2019manual]. `IS0` selects no separate wave–ice scattering source term. The parameter namelists used below correspond to these compiled packages: `SIN6` and `SWL6` to `ST6`, `SNL1` to `NL1`, and `SIC4` to `IC4`.

The executable does not contain `PR3`, `IC3` or `IS2`. Consequently, the `PRO3` garden-sprinkler-effect tuning, IC3 viscoelastic parameters, and IS2 floe-scattering parameters described in older WW3 configuration notes are inactive and should not be added to this configuration. Changing to any of those packages requires a new executable built with the matching switch, not just a namelist change.

### Time stepping

WW3 splits wave evolution into geographic propagation, propagation through frequency/direction space (including refraction), and source terms such as wind input and dissipation. These processes use separate timestep limits and internal substeps. The four controls below do not set the coupling interval between WW3, MOM6 and CICE. See [Changing WW3 timesteps](#changing-ww3-timesteps) for the editing and verification procedure.

In this build's `CESMCOUPLED` pathway, the [cap restores the controls from `wav_in` after reading `mod_def.ww3`](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/wav_comp_nuopc.F90#L1599-L1607). The preprocessing values in `ww3_grid.nml` therefore do not determine the effective runtime controls.

| `wav_in` control | WW3 name | Current value | Meaning |
| --- | --- | ---: | --- |
| `dtcfl` | `DTXY` | 600 s | Reference limit for geographic propagation, based on grid spacing and wave group speed; PR1 can apply local substeps. |
| `dtcfli` | `DTKTH` | 600 s | Maximum timestep for propagation through wavenumber–direction space, including refraction. |
| `dtmax` | `DTMAX` | 1800 s | Maximum overall wave integration timestep; individual processes can use shorter steps. |
| `dtmin` | `DTMIN` | 50 s | Minimum step for dynamically integrated source terms, rather than a fixed step used by every process. |

The original calculation in [issue #1519](https://github.com/ACCESS-NRI/access-om3-configs/issues/1519) used the smallest active grid spacing, not the nominal 100 km resolution:

```text
f1 = 0.04118 Hz
cg,max = 1.15 g / (4 pi f1) ≈ 21.79 m/s
Dmin = 15,589 m
0.9 Dmin / cg,max ≈ 644 s
```

The selected `dtcfl = 600 s` lies below this estimate. `dtmax = 1800 s` follows the approximate `3 × dtcfl` guideline. Both divide the coupling interval exactly.

The selected `dtcfli = 600 s` equals `dtmax/3`. Its suitability depends on spectral propagation, including refraction, and cannot be inferred from minimum geographic cell spacing alone. The [WW3 timestep guidance](https://github.com/NOAA-EMC/WW3/blob/e9792e4210d640bb3c341dd0e6e27f10daae9451/model/nml/ww3_grid.nml#L46-L75) describes these as selection guidelines, not universal stability guarantees.

The [full-year comparison in #1519](https://github.com/ACCESS-NRI/access-om3-configs/issues/1519#issuecomment-5126327350) tested `dtcfl/dtcfli/dtmax = 600/600/1800 s` against `180/300/600 s`, retaining `dtmin = 50 s` in both. Runtime decreased by 24.8%; mean absolute differences were 0.022 m in significant wave height, 0.043 s in mean wave period, and 0.65° in mean wave direction. The discussion retained 50 s for this low-resolution configuration; the initial proposal of 10 s was not adopted. These results support the selected values for the tested configuration, but predate the October topography change. Reassess timestep suitability when changing grid, spectrum, physics or coupling.

### Source-term physics

The branch's [`namelists_Global.nml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/WW3_PreProc/namelists_Global.nml) configures the compiled `ST6` package, which represents wind input, whitecapping dissipation and swell dissipation and constrains total wind input using the independently calculated wind stress. `SINA0 = 0.04` controls negative wind input when wind opposes the waves. For swell dissipation, `SWLB1 = 0.22e-3` is the scaling coefficient and `CSTB1 = T` selects the formulation in which that coefficient is constant rather than rescaled by peak steepness. The observation-based development of ST6 is described in [@rogers2012observation; @zieger2015observation].

`NL1` represents the nonlinear four-wave source term using the Discrete Interaction Approximation (DIA) [@hasselmann1985parameterizations]. `LAMBDA = 0.237` and `NLPROP = 2.13e7` tune the representative interacting quadruplet and its proportionality coefficient, respectively.

### Stokes-drift output and MOM6 coupling

`USSP = 1` enables partitioned Stokes-drift output, while `IUSSP = 3` requests three bands represented by decay wavenumbers `STK_WN = 0.04, 0.110, 0.3305`. WW3 exports both vector components for each band to MOM6. `E3D = 1` enables frequency-resolved energy-spectrum output; independently of that output flag, the coupled WW3 cap exports the 25-bin elevation spectrum to CICE6 at each coupling exchange. These coupled fields are [calculated from the instantaneous WW3 state](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/wav_import_export.F90#L840-L865) at the exchange time, not interval means.

`STK_TAIL = T`, enabled in [PR #1754](https://github.com/ACCESS-NRI/access-om3-configs/pull/1754), adds the analytic f⁻⁵ spectral-tail contribution to the highest Stokes band. The resolved spectrum ends near 0.406 Hz; the [tail calculation](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/w3iogomd.F90#L4020-L4027) includes unresolved high-frequency contributions to Stokes drift and therefore affects MOM6 Langmuir mixing. It does not add resolved spectral bins. This flag is stored in `mod_def.ww3`, so editing the namelist alone does not enable it.

The band count and wavenumbers are a coupling contract: changes require matching MOM6 settings and regeneration of `mod_def.ww3`. The [WW3 cap in this build advertises exactly three bands](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/wav_import_export.F90#L150-L159), so changing the band count also requires compatible cap/source changes and a rebuilt executable.

### Langmuir settings

WW3 is configured with `LMPENABLED = F` and `HSLMODE = 0`. Its Li et al. Langmuir-mixing parameterisation [@li2016langmuir] is therefore disabled, and the value of `HSLMODE` has no active effect. Langmuir enhancement in this configuration is instead calculated within MOM6 ePBL from the Stokes-drift bands supplied by WW3.

### Wave-ice interaction

The active attenuation choice is `SIC4 IC4METHOD = 8`. In the pinned `access-ww3 2026.03.001` source, [`CASE (8)`](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/w3sic4md.F90#L559-L595) combines a floe-size-dependent cubic fit associated with Meylan et al. [@meylan2021floe] with the **IC4M2** empirical attenuation of Meylan et al. [@meylan2014situ], `0.00212 / T^2 + 0.0459 / T^4`. The cubic component introduces additional dependencies on mean ice thickness and representative floe diameter supplied by CICE.

Thickness is clipped to 0.1–3.5 m and radius to 2.5–100 m. The cubic fit predicts the base-10 logarithm of energy attenuation, capped at zero before conversion back to linear units. For `5 < T < 20` s, IC4M2 is added to the cubic result; for `T > 20` s, IC4M2 is used alone. At other periods, including exactly 20 s, the code uses only the cubic result. WW3 then sets amplitude attenuation to half the energy attenuation. The coefficients are hard-coded rather than set in `namelists_Global.nml`.

This implementation differs from upstream WW3's use of the name **IC4M8** for the order-3 power-law model of Meylan et al. [@meylan2018dispersion], introduced through [NOAA-EMC/WW3 issue #1167](https://github.com/NOAA-EMC/WW3/issues/1167) and [PR #1176](https://github.com/NOAA-EMC/WW3/pull/1176). That model has the form `k_i = C_hf h_ice f^3`; therefore, `IC4METHOD = 8` should not be assumed to select the same formulation across these WW3 versions.

`CICE0 = 0.25` and `CICEN = 0.75` are present in the namelist but do not control IC4 attenuation. In `access-ww3 2026.03.001`, the [concentration-based propagation-transparency ramp](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/w3updtmd.F90#L2975-L3040) is compiled only with `IC0`; this executable instead uses `IC4`. `FLAGTR = 4` still applies the static unresolved-obstruction data at cell centres, while IC4 wave attenuation is calculated separately.

[`ICNUMERICS = T`](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/w3srcemd.F90#L1320-L1342) is required by the matching ACCESS-NRI WW3 implementation to activate the compiled sea-ice source-term calculation. The source term is scaled by ice concentration before it is included in the spectral source-term integration. This switch is specific to the `access-ww3 2026.03.001` implementation used by the documented configuration and should be rechecked when changing executable versions.

### Other numerical choices

The coupled driver uses a Gregorian calendar. The supplied `mod_def.ww3` stores `CALTYPE = 'standard'`, and the [WW3 cap derives its output calendar from the driver](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/wav_comp_nuopc.F90#L625-L632). The standalone `&CALTYPE = '365_day' /` line in `namelists_Global.nml` is misleading: [`CALTYPE` belongs to `&MISC`](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/w3gridmd.F90#L1096-L1102), and its [default is `standard`](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/w3gridmd.F90#L2710). Do not treat that line as an active no-leap setting.

WW3's initial condition is a fetch-limited JONSWAP spectrum (`ITYPE = 3`) calculated from local wind speed and direction, using the grid-cell scale as the fetch and constraining the result to the configured frequency range.

## Appendix: PR3 tuning (not active)

This configuration is compiled with `PR1`, so the [`PRO3` namelist](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/w3gridmd.F90#L1073-L1075) is inactive. A future switch to `PR3` would require rebuilding ACCESS-OM3, regenerating `mod_def.ww3`, and validating the `WDTHCG` and `WDTHTH` averaging parameters for this grid (see the [WW3 description of GSE averaging](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/manual/num/GSE_avg.tex)). No configuration-specific values are established here.

## Current inputs, forcing and run coverage

The pinned [`config.yaml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/config.yaml) selects the **2026.10.13** topography and dependent inputs from [PR #1787](https://github.com/ACCESS-NRI/access-om3-configs/pull/1787): CICE mask, coupling meshes, runoff weights and iceberg-melt distribution, tidal inputs, chlorophyll, and WW3 binaries. The 17 km topography cutoff removes 23 ocean cells relative to the previous mask; bottom roughness also changes across the ocean because its source data were updated. These inputs must be used together. The horizontal grid remains `2026.03.13`; do not replace every input date with the topography date. Many paths remain under `vk83/prerelease`, and ERA5 is under `av17`, so this is still a development configuration.

[`datm.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/datm.streams.xml) lists ERA5 for 1940–2025, while [`drof.streams.xml`](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/drof.streams.xml) lists JRA55-do runoff for 1958–2024. Their common listed period is 1958–2024; `taxmode = extend` is not evidence of new forcing beyond those dates. The default startup is 1 January 1958, with one year per submission and annual coupled restarts (`restart_freq: 1YS` in Payu).

CICE writes daily and monthly means. WW3's `WAV_modelio` settings request daily history, while the [coupled cap uses driver restart/history alarms](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/wav_comp_nuopc.F90#L1135-L1170). The native schedules in [`wav_in`](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/wav_in) still span 1 January 1958 to 1 January 2024 with daily field/restart strides and disabled point output; these dates are not the coupled run's stop date. Check both the coupled alarms and native schedules when changing run dates or switching to standalone WW3. Longer experiments also require checking actual forcing-file availability.

## Exchanged fields

The tables below list **all 73 component-to-component mapping records** in `/scratch/tm70/ek4684/test1/work/log/med.log`, inspected on 16 October 2026. This run uses the deployed executable described above; its `fd.yaml` and `nuopc.runseq` match configuration commit `bbf1c86`, and its `nuopc.runconfig` differs only by `start_type = continue`. This is an inventory of fields mapped by CMEPS, not a list of every advertised field or history diagnostic. A mapped field can be an intermediate used by the mediator rather than a field passed unchanged into the receiving model.

Here `atm` is DATM (ERA5), `rof` is DROF (JRA55-do runoff), `ocn` is MOM6, `ice` is CICE6, and `wav` is WW3. All routes pass through CMEPS on the 3600 s coupling sequence. Names and units follow the pinned [field dictionary](https://github.com/ACCESS-NRI/access-om3-configs/blob/bbf1c86c50dfa0716c47fd9be2e261169fd911e7/fd.yaml), with the spectrum-unit caveat below. Paired names denote separate fields; the three Stokes bands and 25 spectrum bins are array dimensions, not separate mapping records.

### Atmospheric forcing

Each field below is mapped to **both ocean and ice** (`atm→ocn`: 19; `atm→ice`: 19). Only the three fields marked in the final column are also mapped to WW3 (`atm→wav`: 3).

| Field(s) | Quantity | Units | Also to WW3 |
| --- | --- | --- | --- |
| `Sa_u`, `Sa_v` | Zonal and meridional wind | m s⁻¹ | Yes |
| `Sa_z` | Atmospheric reference height | m | |
| `Sa_tbot` | Air temperature at the reference level | K | Yes |
| `Sa_pbot` | Pressure at the reference level | Pa | |
| `Sa_shum` | Specific humidity | kg kg⁻¹ | |
| `Sa_ptem` | Potential temperature | K | |
| `Sa_dens` | Air density | kg m⁻³ | |
| `Sa_pslv` | Sea-level pressure | Pa | |
| `Faxa_rainc`, `Faxa_rainl` | Convective and large-scale rain | kg m⁻² s⁻¹ | |
| `Faxa_snowc`, `Faxa_snowl` | Convective and large-scale snow | kg m⁻² s⁻¹ | |
| `Faxa_swnet` | Net shortwave radiation | W m⁻² | |
| `Faxa_lwdn` | Downward longwave radiation | W m⁻² | |
| `Faxa_swndr`, `Faxa_swndf` | Direct and diffuse near-infrared shortwave radiation | W m⁻² | |
| `Faxa_swvdr`, `Faxa_swvdf` | Direct and diffuse visible shortwave radiation | W m⁻² | |

These are coupler fields after DATM processing, not necessarily separate ERA5 input variables; see the ERA5 guide linked above for forcing preparation.

### Ocean exports

| Route | Field(s) | Quantity | Units |
| --- | --- | --- | --- |
| `ocn→ice` | `So_omask` | Ocean mask | 1 |
| `ocn→ice`, `ocn→wav` | `So_t` | Sea-surface temperature | K |
| `ocn→ice` | `So_s` | Sea-surface salinity | g kg⁻¹ |
| `ocn→ice`, `ocn→wav` | `So_u`, `So_v` | Zonal and meridional surface currents | m s⁻¹ |
| `ocn→ice` | `So_dhdx`, `So_dhdy` | Sea-surface slopes | m m⁻¹ |
| `ocn→ice` | `Fioo_q` | Freezing/melting potential | W m⁻² |
| `ocn→wav` | `So_bldepth` | Ocean boundary-layer depth | m |

There are eight mappings to ice and four to waves.

### Ice exports

| Route | Field(s) | Quantity | Units |
| --- | --- | --- | --- |
| `ice→ocn` | `Faii_swnet` | Net shortwave radiation over ice | W m⁻² |
| `ice→ocn`, `ice→wav` | `Si_ifrac` | Ice concentration | 1 |
| `ice→ocn` | `Fioi_swpen` | Total shortwave radiation penetrating ice into ocean | W m⁻² |
| `ice→ocn` | `Fioi_swpen_vdr`, `Fioi_swpen_vdf` | Visible direct and diffuse penetrating shortwave | W m⁻² |
| `ice→ocn` | `Fioi_swpen_idr`, `Fioi_swpen_idf` | Near-infrared direct and diffuse penetrating shortwave | W m⁻² |
| `ice→ocn` | `Fioi_melth` | Ice–ocean heat flux | W m⁻² |
| `ice→ocn` | `Fioi_taux`, `Fioi_tauy` | Zonal and meridional ice stress on ocean | N m⁻² |
| `ice→ocn` | `Fioi_meltw` | Freshwater flux from ice to ocean | kg m⁻² s⁻¹ |
| `ice→ocn` | `Fioi_salt` | Salt flux from ice to ocean | kg m⁻² s⁻¹ |
| `ice→wav` | `Si_thick` | Ice thickness | m |
| `ice→wav` | `Si_floediam` | Floe diameter | m |

There are 12 mappings to ocean and three to waves. FSD categories themselves are not exchanged: WW3 receives floe diameter, while CICE retains the category distribution.

### Runoff and wave exports

| Route | Field(s) | Quantity | Units |
| --- | --- | --- | --- |
| `rof→ocn` | `Forr_rofl` | Liquid runoff | kg m⁻² s⁻¹ |
| `rof→ocn` | `Forr_rofi` | Frozen runoff | kg m⁻² s⁻¹ |
| `wav→ocn` | `Sw_pstokes_x`, `Sw_pstokes_y` | Zonal and meridional Stokes drift, each with three bands | m s⁻¹ |
| `wav→ice` | `Sw_elevation_spectrum` | Instantaneous, direction-integrated wave-elevation spectrum, 25 frequency bins | See note below |

There are two runoff mappings, two wave-to-ocean mappings and one wave-to-ice mapping. Significant wave height, wave period, radiation stress and wave-induced bottom currents are **not** among this run's mapped fields. The log sets a `rof→ice` connection flag but records no field mappings on that route; there are also no mapped return fields to DATM or DROF.

!!! note "Spectrum units need a metadata check"
    `fd.yaml` declares `Sw_elevation_spectrum` in `m2/s`. The [WW3 spectrum calculation](https://github.com/ACCESS-NRI/WW3/blob/0a23b2c358150b420919f47545ae81b76fa39a0f/model/src/wav_import_export.F90#L1337-L1376) integrates over directions and converts to ordinary frequency, consistent with a variance density in m² Hz⁻¹ (m² s). Treat the dictionary label as an unresolved metadata discrepancy, not as an instruction to rescale the exchanged values.

### Mapping and mediator processing

The log reports `fcopy` for atmosphere–ocean, atmosphere–ice and ocean–ice transfers. Atmosphere/ocean to waves use `bilnr`; ice to waves and waves to ocean/ice use `bilnr_nstod`, all with `one` normalization. Liquid runoff uses `rof2ocn_liq`, `none` normalization and `access-om3-100km-rof-remap-weights.nc`; frozen runoff uses `consd` with `one` normalization. These are the logged mapping identifiers. The log also enables frozen-runoff spreading using `access-om3-100km-rofi-climatology.nc`.

CMEPS combines and transforms fields before model import. In particular, the logged merge rules sum convective and large-scale precipitation into `Faxa_rain` and `Faxa_snow`, rename runoff to `Foxx_rofl` and `Foxx_rofi`, and weight ocean-directed atmospheric and ice flux contributions by open-water and ice fractions. The logged initial contributions to `Foxx_taux`, `Foxx_tauy` and `Foxx_lwnet` are not their complete flux budgets: air–ocean flux calculations also occur in the mediator. Thus the 73 mappings above should not be read as 73 independent model import variables.

For completeness, the same log lists these **14 internal air–ocean calculation fields**, separately from the mapping inventory:

| Field(s) | Role |
| --- | --- |
| `Faox_taux`, `Faox_tauy` | Air–ocean stress components |
| `Faox_lat`, `Faox_sen` | Latent and sensible heat fluxes |
| `Faox_evap`, `Faox_lwup` | Evaporation and upward longwave flux |
| `So_tref`, `So_qref` | Reference temperature and specific humidity |
| `So_u10`, `So_u10res` | Wind diagnostics from the air–ocean flux calculation |
| `So_ssq`, `So_re`, `So_ustar`, `So_duu10n` | Additional air–ocean flux diagnostics |

These internal bundle entries are not evidence of additional component-to-component transfers. To recheck the mapping inventory after changing configuration or executable, inspect the new run's log:

```bash
grep '^ mapping' work/log/med.log
```

## Running and regenerating WW3 inputs

On Gadi, ensure access to the input projects listed in `config.yaml` (including `vk83`, `av17` and `qv56`, plus `xp65` for postprocessing) and an allocation for running the model. Use Payu **1.3.6 or later**, as required by the configuration. Clone the ERA5 interannual-forcing branch and enter the resulting configuration directory:

```bash
module use /g/data/vk83/modules
module load payu
payu clone --branch dev-MCW_100km_era_iaf \
  git@github.com:ACCESS-NRI/access-om3-configs.git mcw_100km_era_iaf
cd mcw_100km_era_iaf
```

Review the cloned `config.yaml` and input paths: cloning the development branch obtains its latest revision, which may be newer than the snapshot above. The supplied `mod_def.ww3` and `restart.ww3` can be used without preprocessing. For runtime timestep edits, follow [Changing WW3 timesteps](#changing-ww3-timesteps) below. If the WW3 preprocessing inputs are changed, load the exact `access-om3` version specified by `config.yaml`; for the version documented here this is:

```bash
module load access-om3/2026.05.004
cd WW3_PreProc
ww3_grid
ww3_strt
```

`ww3_grid` regenerates `mod_def.ww3` from `ww3_grid.nml`, including the grid, spectral discretisation and applicable parameters in `namelists_Global.nml`. `ww3_strt` regenerates `restart.ww3` from `ww3_strt.inp` and the grid definition. Return to the configuration directory (`cd ..`) and replace the two corresponding `input` paths in `config.yaml` with absolute paths to the regenerated files; do not leave duplicate basenames.

This branch enforces input and executable manifest checks. For deliberately changed inputs, temporarily set `manifest.reproduce.input: false`, run `payu setup`, review the updated `manifests/input.yaml`, then restore `manifest.reproduce.input: true` and run `payu sweep` to remove the setup work directory before submission (see [Payu manifest controls](https://payu.readthedocs.io/en/latest/config.html#manifests)). Keep executable checking enabled unless the executable was deliberately changed.

Preserve the Gregorian calendar and matching CICE/WW3 masks, and inspect the preprocessor report for the three Stokes bands and enabled tail. A change to preprocessing parameter values for already compiled packages requires regeneration of `mod_def.ww3`; selecting a different physics or propagation package also requires an ACCESS-OM3 executable built with the corresponding WW3 switch.

From the configuration directory, submit the experiment with:

```bash
payu run
```

### Changing WW3 timesteps

1. In the experiment's control directory, edit the existing `&ww3_inparm` block in **`wav_in`**. The documented configuration contains the following values (seconds); replace the relevant values for your test, preserving `initfile` and the other namelists:

    ```fortran
    &ww3_inparm
      dtcfl  = 600.
      dtcfli = 600.
      dtmax  = 1800.
      dtmin  = 50.
      initfile = "./INPUT/restart.ww3"
    /
    ```

2. Check the coupling interval at the start of **`nuopc.runseq`** (3600 s in this configuration). For straightforward alignment, choose `dtmax` and `dtcfl` that divide this interval, with `dtmax` an integer multiple of `dtcfl`, as in the selected values above. Alignment alone does not establish numerical stability; use the [parameter rationale](#time-stepping_1) and a comparison run to assess your choice. Editing `wav_in` does not change the coupling interval. If you intend to change coupling as well, follow the [coupling and MOM6 timestep guidance](https://docs.access-hive.org.au/models/run_a_model/run_access-om3/#change-model-time-step) and reassess the WW3 limits against the new interval.

3. For changes only to these four runtime controls in this coupled build, **do not regenerate `mod_def.ww3` or `restart.ww3`**. Do not edit only `WW3_PreProc/ww3_grid.nml`: its timestep values are overridden by `wav_in`. Changing grid, spectrum or preprocessing physics is a separate operation requiring the input-generation workflow above.

4. Run a short comparison experiment from the same initial state or restart as a baseline, retaining its logs and configuration. In this build, `wav.log` prints the controls read from `wav_in`; together with the cap's post-initialisation override described above, this identifies the runtime limits. During a run, inspect:

    ```bash
    grep -E 'dtcfl|dtcfli|dtmax|dtmin' work/log/wav.log
    ```

    After Payu archives the run, use `archive/outputNNN/log/wav.log`, replacing `NNN` with that run's index. Expect the values you set, not the preprocessing defaults. This reports configured limits, not every adaptive internal substep. If they differ, check the staged `work/wav_in` and the executable version before interpreting results.

5. Check for warnings, NaNs, aborts and restart/coupling failures, and compare wave height, period, direction and runtime with the baseline. For this PR1 build, **do not use `CFX`, `CFD` or `CFK` as timestep-validation diagnostics**: [#1519](https://github.com/ACCESS-NRI/access-om3-configs/issues/1519) records that the relevant arrays are populated only with PR3 and otherwise produce missing values. A short successful test is an initial check, not proof of long-term coupled stability.

## References

\bibliography
