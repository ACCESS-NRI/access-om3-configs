# MOM6-CICE6-WW3 100 km configuration

The MCW_100km_era_iaf configuration couples MOM6, CICE6 and WAVEWATCH III (WW3) on the nominal 100 km ACCESS-OM3 grid. Unlike the MOM6-CICE 25 km configuration, which uses JRA55-do, this configuration uses [ERA5 atmospheric forcing](../../inputs/ERA5-atmospheric-forcing/). The forcing preparation, field mappings and configuration changes are documented in that guide. Runoff remains JRA55-do through DROF.

This page describes the MCW configuration's wave coupling and parameter choices. Shared MOM6 and CICE6 choices are documented for the [MOM6-CICE 25 km configuration](../MC_25km/); resolution-dependent settings differ. See [Forcing data models](../../inputs/Forcing-data-models/) for atmospheric forcing and runoff, and [Coupling architecture](../../infrastructure/Architecture/) for exchanges common to the configurations.

## MOM6 parameter choices

### Wave coupling

In MOM_input, `USE_WAVES = True` activates MOM6's surface-wave interface. This configuration uses `WAVE_METHOD = "SURFACE_BANDS"` and `SURFBAND_SOURCE = "COUPLER"`, so MOM6 receives the zonal and meridional Stokes drift divided into surface wavenumber bands from WW3 rather than diagnosing waves from local winds.

Three bands are exchanged:

```text
STK_BAND_COUPLER = 3
SURFBAND_WAVENUMBERS = 0.04, 0.11, 0.3305  rad m-1
```

These values must agree with WW3's `IUSSP = 3` and `STK_WN = 0.04, 0.110, 0.3305`. MOM6 checks the number of coupled bands at run time, then uses the coupled band velocities and wavenumbers to reconstruct the vertical Stokes-drift profile.

### Stokes drift and Langmuir turbulence

The closest non-wave 100 km configuration estimates the Langmuir number with `USE_LA_LI2016 = True`. The MCW configuration instead sets `EPBL_LT = True`, allowing the energetic planetary boundary layer (ePBL) scheme [@reichl2018simplified] to calculate a Langmuir number from the coupled Stokes-drift profile. `EPBL_LANGMUIR_SCHEME = "ADDITIVE"` adds the Langmuir-turbulence contribution to the other contributions to the ePBL mixing-energy factor [@reichl2019parameterization; @li2019comparing].

The selected **E12** coefficients are `LT_ENHANCE_COEF = 0.150`, `LT_ENHANCE_EXP = -1.0`, and `LT_MOD_LAC1 = LT_MOD_LAC2 = LT_MOD_LAC3 = LT_MOD_LAC4 = LT_MOD_LAC5 = 0.0`. E12 is an ACCESS-OM3 tuning, not a parameter set taken directly from the literature. It was selected through [sensitivity experiments documented in issue #950](https://github.com/ACCESS-NRI/access-om3-configs/issues/950), balancing mixed-layer-depth and Antarctic sea-ice biases and RMSE, and applied in [PR #1684](https://github.com/ACCESS-NRI/access-om3-configs/pull/1684). `LT_MOD_LAC2/3` are not explicitly set in `MOM_input`. The later Stokes-tail change below alters the coupled forcing of this tuning; it does not change these coefficients.

The literature-based E00 starting point used `LT_ENHANCE_COEF = 0.105`, `LT_ENHANCE_EXP = -1.0`, `LT_MOD_LAC1 = LT_MOD_LAC2 = LT_MOD_LAC3 = 0.0`, and `LT_MOD_LAC4 = LT_MOD_LAC5 = 0.8`, following the published surface-layer Langmuir-number formulation [@reichl2019parameterization; @li2019comparing]. E12 retains the exponent and `LT_MOD_LAC1/2/3`, but its `LT_ENHANCE_COEF = 0.150` and `LT_MOD_LAC4/5 = 0.0` come from the ACCESS-OM3 parameter sweep.

This MOM6 treatment is separate from WW3's own `LMPN` option, which is disabled below.

### Time stepping

The ocean baroclinic timestep is `DT = 1800` s, equal to the coupling interval set in `nuopc.runseq`. `DT_THERM = 7200` s and `THERMO_SPANS_COUPLING = True` allow one thermodynamic step to span four coupling intervals. `DTBT = -0.9` instructs MOM6 to choose a barotropic timestep at 90% of its estimated stable maximum and round it to an integer subdivision of `DT`. See the [MOM6 timestep guidance](../../infrastructure/NUOPC-driver/#mom6-time-steps) for the roles of these controls.

## CICE6 parameter choices

### C-grid dynamics and matching inputs

`grid_ice = "C"` selects C-grid ice dynamics. The CICE `kmt.nc`, coupling meshes, WW3 text mask/depth and preprocessed binaries must have consistent land masks and bathymetry. When changing topography, update these inputs together.

### Floe-size distribution

In `ice_in`, the MCW configuration changes `nfsd` from one to 12 and enables the prognostic floe-size-distribution tracer with `tr_fsd = .true.`. CICE therefore evolves ice area across 12 floe-radius categories as well as its five ice-thickness categories. The distribution responds to new-ice formation, lateral growth and melt, thermodynamic welding, and wave fracture; these processes affect floe perimeter and hence lateral melt rates [@roach2019advances].

### Wave forcing

`wav_coupling_to_cice = .true.` in `nuopc.runconfig` connects the models in both directions. CICE supplies ice concentration, thickness and floe diameter to WW3, while WW3 supplies its instantaneous 25-bin wave-elevation spectrum to CICE at each coupling exchange. CICE uses that spectrum in its wave-fracture step to update the floe-size distribution.

`wave_spec_type = "constant"` does **not** mean that the spectrum is constant in time. In the Icepack wave-fracture algorithm it selects a fixed phase and one fracture iteration, avoiding the random-number generator; this removes that source of nondeterminism, rather than guaranteeing reproducibility of the entire coupled model. The alternative `random` mode draws random phases and iterates fracture to convergence.

### Wave and floe-size diagnostics

The relevant fields in `icefields_fsd_nml` are written to both daily and monthly streams (`"md"`). They comprise:

- `fsdrad` and `fsdperim`: representative floe radius and perimeter per unit ice area;
- `afsd` and `afsdn`: areal floe-size distribution, respectively aggregated over and resolved by ice-thickness category;
- `dafsd_newi`, `dafsd_latg`, `dafsd_latm`, `dafsd_wave` and `dafsd_weld`: floe-size-distribution tendencies from new ice, lateral growth, lateral melt, wave fracture and welding;
- `wave_sig_ht`: significant wave height diagnosed by CICE from the instantaneous spectrum imported from WW3;
- `aice_ww`, `diam_ww` and `hice_ww`: concentration, number-mean diameter and thickness of floes larger than `Dmin`, provided as wave-related diagnostics.

These fields allow changes in floe size to be attributed to their physical processes and compared with the wave conditions that drive fracture.

## WAVEWATCH III parameter choices

### Grid and spectral discretisation

`ww3_grid.nml` configures the same 360 x 324 curvilinear, spherical tripolar grid as MOM6 and CICE6. The preprocessor also reads an unresolved-obstruction map; `FLAGTR = 4` places its static transparencies at cell centres.

The wave spectrum has 25 frequency bins beginning at 0.04118 Hz, with successive frequencies multiplied by 1.1. It has 24 directional bins, giving 15-degree directional resolution. `THOFF` offsets the first direction by −0.5 to 0.5 of that 15-degree increment; `THOFF = 0.0` leaves the directional grid unshifted. `THOFF` rotates the directional grid; it is not a dedicated garden-sprinkler correction. No explicit garden-sprinkler correction is used with `PR1` on this grid type [@ww3dg2019manual].

### Compiled physics switches

The ACCESS-OM3 executable used by this configuration compiles WW3 with the following switches:

```cmake
CESMCOUPLED DIST MPI PR1 FLX4 ST6 STAB0 LN1 NL1 BT1 DB1 MLIM TR0 BS0
RWND WNX1 WNT0 CRX1 CRT0 O0 O1 O2 O3 O4 O5 O6 O7 O14 O15 IS0 REF0
NOGRB IC4
```

The scientifically important selections are `PR1` propagation, `ST6` wind input and dissipation, `LN1` linear wave growth, `NL1` nonlinear quadruplet interactions, `BT1` bottom friction, `DB1` depth-induced breaking and `IC4` wave–ice attenuation. `PR1` is WW3's conservative first-order upwind scheme for propagating wave action; *first order* describes its numerical accuracy, and the scheme is more diffusive than the higher-order propagation options [@ww3dg2019manual]. `IS0` selects no separate wave–ice scattering source term. The parameter namelists used below correspond to these compiled packages: `SIN6` and `SWL6` to `ST6`, `SNL1` to `NL1`, and `SIC4` to `IC4`.

The executable does not contain `PR3`, `IC3` or `IS2`. Consequently, the `PRO3` garden-sprinkler-effect tuning, IC3 viscoelastic parameters, and IS2 floe-scattering parameters described in older WW3 configuration notes are inactive and should not be added to this configuration. Changing to any of those packages requires a new executable built with the matching switch, not just a namelist change.

### Time stepping

WW3 splits wave evolution into geographic propagation, propagation through frequency/direction space (including refraction), and source terms such as wind input and dissipation. These processes use separate timestep limits and internal substeps. The four controls below do not set the coupling interval between WW3, MOM6 and CICE. See [Changing WW3 timesteps](#changing-ww3-timesteps) for the editing and verification procedure.

In ACCESS-OM3's coupled WW3 pathway, selected by the historically named `CESMCOUPLED` switch, the [cap restores the controls from `wav_in` after reading `mod_def.ww3`](https://github.com/search?q=repo%3AACCESS-NRI%2FWW3+path%3Amodel%2Fsrc%2Fwav_comp_nuopc.F90+DTMAX&type=code). The preprocessing values in `ww3_grid.nml` therefore do not determine the effective runtime controls.

| `wav_in` control | WW3 name | Current value | Meaning |
| --- | --- | ---: | --- |
| `dtcfl` | `DTXY` | 600 s | Reference limit for geographic propagation, based on grid spacing and wave group speed; PR1 can apply local substeps. |
| `dtcfli` | `DTKTH` | 600 s | Maximum timestep for propagation through wavenumber–direction space, including refraction. |
| `dtmax` | `DTMAX` | 1800 s | Maximum overall wave integration timestep; individual processes can use shorter steps. |
| `dtmin` | `DTMIN` | 50 s | Minimum step for dynamically integrated source terms, rather than a fixed step used by every process. |

The geographic propagation limit depends on the smallest active grid spacing and fastest wave group speed, rather than the nominal 100 km resolution. A starting estimate is `dtcfl ≈ 0.9 Dmin / cg,max`, where `Dmin` is the minimum active spacing and `cg,max` is estimated from the lowest spectral frequency:

```text
f1 = 0.04118 Hz
cg,max = 1.15 g / (4 pi f1) ≈ 21.79 m/s
```

Using `Dmin = 15,589 m`, the reference calculation in [issue #1519](https://github.com/ACCESS-NRI/access-om3-configs/issues/1519) gives `0.9 Dmin / cg,max ≈ 644 s`, above the selected `dtcfl = 600 s`. Recalculate `Dmin` from the active mask when changing topography; the reference value is not a verified minimum for every input revision.

The selected `dtmax = 1800 s` follows the approximate `3 × dtcfl` guideline. Both divide the 1800 s coupling interval exactly. `dtcfli = 600 s` is `dtmax/3`; its suitability depends on spectral propagation and refraction and cannot be inferred from geographic spacing alone.

The [timestep selection analysis](https://github.com/ACCESS-NRI/access-om3-configs/issues/1519) supports this balance of accuracy and computational cost, including `dtmin = 50` s. Reassess the limits when changing grid, spectrum, physics or coupling; the [general WW3 timestep guidance](../../infrastructure/NUOPC-driver/#wavewatch-iii-time-steps) describes their roles and selection criteria.

### Source-term physics

`namelists_Global.nml` configures the compiled `ST6` package, which represents wind input, whitecapping dissipation and swell dissipation and constrains total wind input using the independently calculated wind stress. `SINA0 = 0.04` controls negative wind input when wind opposes the waves. For swell dissipation, `SWLB1 = 0.22e-3` is the scaling coefficient and `CSTB1 = T` selects the formulation in which that coefficient is constant rather than rescaled by peak steepness. The observation-based development of ST6 is described in [@rogers2012observation; @zieger2015observation].

`NL1` represents the nonlinear four-wave source term using the Discrete Interaction Approximation (DIA) [@hasselmann1985parameterizations]. `LAMBDA = 0.237` and `NLPROP = 2.13e7` tune the representative interacting quadruplet and its proportionality coefficient, respectively.

### Stokes-drift output and MOM6 coupling

`USSP = 1` enables partitioned Stokes-drift output, while `IUSSP = 3` requests three bands represented by decay wavenumbers `STK_WN = 0.04, 0.110, 0.3305`. WW3 exports both vector components for each band to MOM6. `E3D = 1` enables frequency-resolved energy-spectrum output; independently of that output flag, the coupled WW3 cap exports the 25-bin elevation spectrum to CICE6 at each coupling exchange. These coupled fields are calculated from the instantaneous WW3 state at the exchange time, not interval means.

`STK_TAIL = T` adds the analytic f⁻⁵ spectral-tail contribution to the highest Stokes band. The resolved spectrum ends near 0.406 Hz; the tail calculation includes unresolved high-frequency contributions to Stokes drift and therefore affects MOM6 Langmuir mixing. It does not add resolved spectral bins. This flag is stored in `mod_def.ww3`, so editing the namelist alone does not enable it.

The band count and wavenumbers are a coupling contract: changes require matching MOM6 settings and regeneration of `mod_def.ww3`. The WW3 cap advertises exactly three bands, so changing the band count also requires compatible cap/source changes and a rebuilt executable.

### Langmuir settings

WW3 is configured with `LMPENABLED = F` and `HSLMODE = 0`. Its Li et al. Langmuir-mixing parameterisation [@li2016langmuir] is therefore disabled, and the value of `HSLMODE` has no active effect. Langmuir enhancement in this configuration is instead calculated within MOM6 ePBL from the Stokes-drift bands supplied by WW3.

### Wave-ice interaction

The active attenuation choice is `SIC4 IC4METHOD = 8`. In the [ACCESS-OM3 WW3 implementation](https://github.com/search?q=repo%3AACCESS-NRI%2FWW3+path%3Amodel%2Fsrc%2Fw3sic4md.F90+IC4METHOD&type=code), method 8 combines a floe-size-dependent cubic fit associated with Meylan et al. [@meylan2021floe] with the **IC4M2** empirical attenuation of Meylan et al. [@meylan2014situ], `0.00212 / T^2 + 0.0459 / T^4`. The cubic component introduces additional dependencies on mean ice thickness and representative floe diameter supplied by CICE.

Thickness is clipped to 0.1–3.5 m and radius to 2.5–100 m. The cubic fit predicts the base-10 logarithm of energy attenuation, capped at zero before conversion back to linear units. For `5 < T < 20` s, IC4M2 is added to the cubic result; for `T > 20` s, IC4M2 is used alone. At other periods, including exactly 20 s, the code uses only the cubic result. WW3 then sets amplitude attenuation to half the energy attenuation. The coefficients are hard-coded rather than set in `namelists_Global.nml`.

This implementation differs from upstream WW3's use of the name **IC4M8** for the order-3 power-law model of Meylan et al. [@meylan2018dispersion]. That model has the form `k_i = C_hf h_ice f^3`; therefore, `IC4METHOD = 8` should not be assumed to select the same formulation across WW3 implementations.

`CICE0 = 0.25` and `CICEN = 0.75` are present in the namelist but do not control IC4 attenuation. The concentration-based propagation-transparency ramp is compiled only with `IC0`; this configuration uses `IC4`. `FLAGTR = 4` still applies the static unresolved-obstruction data at cell centres, while IC4 wave attenuation is calculated separately.

[`ICNUMERICS = T`](https://github.com/search?q=repo%3AACCESS-NRI%2FWW3+path%3Amodel%2Fsrc%2Fw3srcemd.F90+ICNUMERICS&type=code) activates the compiled sea-ice source-term calculation in the ACCESS-OM3 WW3 implementation. The source term is scaled by ice concentration before it is included in the spectral source-term integration.

### Other numerical choices

The coupled driver uses a Gregorian calendar, and WW3 uses `CALTYPE = 'standard'`. When regenerating WW3 inputs, set [`CALTYPE` in the `&MISC` namelist](https://github.com/search?q=repo%3AACCESS-NRI%2FWW3+path%3Amodel%2Fsrc%2Fw3gridmd.F90+CALTYPE&type=code); a standalone `&CALTYPE` block does not select the calendar.

WW3's initial condition is a fetch-limited JONSWAP spectrum (`ITYPE = 3`) calculated from local wind speed and direction, using the grid-cell scale as the fetch and constraining the result to the configured frequency range.

## Alternative propagation: PR3 (not active)

PR3 is WW3's third-order ULTIMATE QUICKEST propagation option with averaging to reduce the garden-sprinkler effect: artificial separation of swell into discrete directional beams [@ww3dg2019manual]. It is an alternative for propagation sensitivity studies; the current configuration uses first-order `PR1`.

Switching to `PR3` requires rebuilding ACCESS-OM3 with the matching switch and regenerating `mod_def.ww3`. Its `PRO3` averaging parameters, `WDTHCG` and `WDTHTH`, require grid-specific validation. No PR3 values are prescribed for this configuration.

## Wave-coupling fields

The MCW-specific exchanges below pass through CMEPS every 1800 s. For atmospheric forcing, runoff and exchanges shared by MOM6–CICE6 configurations, see [Forcing data models](../../inputs/Forcing-data-models/) and [Coupling architecture](../../infrastructure/Architecture/).

| Route | Field(s) | Quantity | Units |
| --- | --- | --- | --- |
| Atmosphere → WW3 | `Sa_u`, `Sa_v`; `Sa_tbot` | Zonal and meridional wind; air temperature | m s⁻¹; K |
| MOM6 → WW3 | `So_t`; `So_u`, `So_v`; `So_bldepth` | Sea-surface temperature; surface currents; ocean boundary-layer depth | K; m s⁻¹; m |
| CICE6 → WW3 | `Si_ifrac`, `Si_thick`, `Si_floediam` | Ice concentration, thickness and representative floe diameter | 1; m; m |
| WW3 → MOM6 | `Sw_pstokes_x`, `Sw_pstokes_y` | Zonal and meridional Stokes drift, each with three bands | m s⁻¹ |
| WW3 → CICE6 | `Sw_elevation_spectrum` | Instantaneous direction-integrated wave-elevation spectrum, 25 frequency bins | m² Hz⁻¹ |

Floe-size categories remain internal to CICE6; WW3 receives a representative floe diameter. The wave-elevation spectrum is a variance density per unit ordinary frequency. The `m2/s` label in `fd.yaml` is inconsistent with this quantity and should not be used to rescale the exchanged values.

## Running and regenerating WW3 inputs

On Gadi, ensure access to the input projects listed in `config.yaml` (including `vk83`, `av17` and `qv56`, plus `xp65` for postprocessing) and an allocation for running the model. Use Payu **1.3.6 or later**, as required by the configuration. Clone the ERA5 interannual-forcing branch and enter the resulting configuration directory:

```bash
module use /g/data/vk83/modules
module load payu
payu clone --branch dev-MCW_100km_era_iaf \
  git@github.com:ACCESS-NRI/access-om3-configs.git mcw_100km_era_iaf
cd mcw_100km_era_iaf
```

The supplied `mod_def.ww3` and `restart.ww3` can be used without preprocessing. For runtime timestep edits, follow [Changing WW3 timesteps](#changing-ww3-timesteps). If preprocessing inputs change, load the `access-om3` module selected by the experiment's `config.yaml`, then run:

```bash
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

2. Check the coupling interval at the start of **`nuopc.runseq`** (1800 s in this configuration). For straightforward alignment, choose `dtmax` and `dtcfl` that divide this interval, with `dtmax` an integer multiple of `dtcfl`, as in the selected values above. Alignment alone does not establish numerical stability; use the [parameter rationale](#time-stepping_1) and a comparison run to assess your choice. Editing `wav_in` does not change the coupling interval. If you intend to change coupling as well, follow the [coupling and MOM6 timestep guidance](https://docs.access-hive.org.au/models/run_a_model/run_access-om3/#change-model-time-step) and reassess the WW3 limits against the new interval.

3. For changes only to these four runtime controls in this coupled configuration, **do not regenerate `mod_def.ww3` or `restart.ww3`**. Do not edit only `WW3_PreProc/ww3_grid.nml`: its timestep values are overridden by `wav_in`. Changing grid, spectrum or preprocessing physics is a separate operation requiring the input-generation workflow above.

4. Run a short comparison experiment from the same initial state or restart as a baseline, retaining its logs and configuration. `wav.log` prints the controls read from `wav_in`; together with the cap's post-initialisation override described above, this identifies the runtime limits. During a run, inspect:

    ```bash
    grep -E 'dtcfl|dtcfli|dtmax|dtmin' work/log/wav.log
    ```

    After Payu archives the run, use `archive/outputNNN/log/wav.log`, replacing `NNN` with that run's index. Expect the values you set, not the preprocessing defaults. This reports configured limits, not every adaptive internal substep. If they differ, check the staged `work/wav_in` and the executable version before interpreting results.

5. Check for warnings, NaNs, aborts and restart/coupling failures, and compare wave height, period, direction and runtime with the baseline. For this PR1 configuration, **do not use `CFX`, `CFD` or `CFK` as timestep-validation diagnostics**: [#1519](https://github.com/ACCESS-NRI/access-om3-configs/issues/1519) records that the relevant arrays are populated only with PR3 and otherwise produce missing values. A short successful test is an initial check, not proof of long-term coupled stability.

## References

\bibliography
