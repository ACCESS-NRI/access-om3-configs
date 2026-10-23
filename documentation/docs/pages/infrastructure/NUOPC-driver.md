We have [adopted the NUOPC driver from CESM](https://github.com/COSIMA/access-om3/discussions/13).

## Component initialisation

Model component initialisation strategy is specified through a combination of flags set in the [`nuopc.runconfig`](https://github.com/ACCESS-NRI/access-om3-configs/blob/dev-MC_100km_jra_ryf/nuopc.runconfig) configuration file and the input parameter files for each component.

The [`start_type`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+start_type&type=code) parameter in the `ALLCOMP_attributes` section of `nuopc.runconfig` can be set to one of three values (note that the `access-om3` Payu driver automatically sets this parameter depending on whether the run is an initial or restart run):

- `"startup"` specifying an initial run,
- `"continue"` specifying a run starting from restart files,
- `"branch"` specifying a run starting from restart files in which properties of the output history files may be changed - not used here.

These have the following effects on each ACCESS-OM3 component’s parameters settings:

### MOM6
See [MOM6 NUOPC cap](https://github.com/mom-ocean/MOM6/blob/b61b29ec1611ee222fcd114ee2b667bbe98ce8f4/config_src/drivers/nuopc_cap/mom_cap.F90#L545) for details.

`start_type` | Interaction with model parameters (from `input.nml`)
:-- | :--
`"startup"` | Sets parameter `restartfiles = "n"`.
`"continue"` / `"branch"` | Hardcoded to use restart file specified in a local file `rpointer.ocn`.

Note, users should let NUOPC set the `restartfiles` parameter. It should not be specified in `input.nml`.

### CICE6

See [CICE6 NUOPC cap](https://github.com/ESCOMP/CICE/blob/34dc66707f6b691b1689bf36689591af3e8df270/cicecore/drivers/nuopc/cmeps/ice_comp_nuopc.F90#L404) for details.

`start_type` | Interaction with model parameters (from `ice_in`)
:-- | :--
`"startup"` | Sets parameter `runtype = "initial"`. The type of CICE startup can be further configured using the `ice_ic` parameter in `ice_in` - see [here](https://cice-consortium-cice.readthedocs.io/en/cice6.5.0/user_guide/ug_implementation.html#initialization-and-restarts).
`"continue"` / `"branch"` | Sets parameters `restart = .true.` , `runtype = "continue"` and `use_restart_time = .true.` so uses restart specified in file specified in parameter `pointer_file`.

Note, users should let NUOPC set the `restart`, `runtype` and `use_restart_time` parameters. They should not be specified in `ice_in`.

### CDEPS components (DATM, DROF)
See e.g. the [atm NUOPC cap](https://github.com/ESCOMP/CDEPS/blob/3c70fc852aac65ea46c79d727b42d30d97a4a0e0/datm/atm_comp_nuopc.F90) and [patch](https://github.com/COSIMA/access-om3/blob/main/CDEPS/patches/atm_comp_nuopc.F90.patch), and [here](https://github.com/ESCOMP/CMEPS/blob/98dcf46c8886104b95cddfd5b02588b3dd9f6722/cesm/driver/ensemble_driver.F90#L213) for details.

`start_type` | Interaction with model parameters (from `d{model_name}_in`)
:-- | :--
`"startup"` | Does not attempt to read any restarts regardless of parameter values.
`"continue"` / `"branch"` | If parameter `skip_restart_read = .false.`, then reads restart specified in file `rpointer.{model_name}` or reads restart specified in parameter `restfilm` if it isn't set to `"null"` - see [here](https://github.com/ESCOMP/CDEPS/blob/f027aa64285fb9ddad9be5c5837a6e6e279e6051/dshr/dshr_mod.F90#L992).

Note, restarts are used for the CDEPS components in ACCESS-OM3 only for performance reasons. They’re not needed to restart exactly, but they reduce startup cost associated with reading the input dataset time axis information - see [here](https://escomp.github.io/CDEPS/versions/master/html/design_details.html#restart-files) for more detail.

## Time-steps

Also see timestepping section [here](/configurations/Overview/#timesteps).

### Coupling and driver time-step

There's an overview of the NUOPC timekeeping design [here](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_refdoc/node3.html#SECTION00035000000000000000).

The `nuopc.runseq` file specifies the run sequence of the configuration. The run sequence for current ACCESS-OM3 configurations comprises a single loop, with the coupling time-step [specified at the start of the loop](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runseq+content%3A%2F%40%5Cd%2B%2F&type=code) (this is the “timeStep” of the loop in NUOPC-speak).

Note, that there are parameters [`{model_name}_cpl_dt`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Frunconfig+content%3Acpl_dt&type=code) set in the `CLOCK_attributes` section of `nuopc.runconfig`. The only place these are used in CMEPS is to set the driver time-step as the [minimum of these values](https://github.com/ESCOMP/CMEPS/blob/e951fdc348de50e9119026ba900b84761503ed69/cesm/driver/esm_time_mod.F90#L157). However from the [NUOPC documentation](https://earthsystemmodeling.org/docs/release/ESMF_8_0_1/NUOPC_refdoc/node4.html#SECTION000411300000000000000) and [CMEPS codebase](https://github.com/ESCOMP/CMEPS/blob/e951fdc348de50e9119026ba900b84761503ed69/mediator/med.F90#L11):

> Each time loop has its own associated clock object. NUOPC manages these clock objects, i.e. their creation and destruction, as well as startTime, endTime, timeStep adjustments during the execution. The outer most time loop of the run sequence is a special case. It uses the driver clock itself. If a single outer most loop is defined in the run sequence provided by freeFormat, this loop becomes the driver loop level  directly. Therefore, setting the timeStep or runDuration for the outer most time loop results modifying the driver clock itself. However, for cases with concatenated loops on the upper level of  the run sequence in freeFormat, a single outer loop is added automatically during ingestion, and the driver clock is used for this loop instead.

So I think in our case, `{model_name}_cpl_dt` are unused and the driver time-step equals the coupling time-step set in `nuopc.runseq`. Certainly, changing these values seems to have no effect. However, I would feel more comfortable if I understood why `{model_name}_cpl_dt` are ever needed...

### CICE6 time-steps

The CICE thermodynamics time-step (`dt`; seconds) is set in the [CICE NUOPC cap](https://github.com/ESCOMP/CICE/blob/4cb296c4003014fe57d6d00f86868a78a532fc95/cicecore/drivers/nuopc/cmeps/ice_comp_nuopc.F90#L1227) to match the driver time-step, which [equals the coupling time-step](#coupling-and-driver-time-step). 
Setting `dt` in `ice_in` has no impact and can only be changed by changing the coupling timestep. [Other time-step related parameters (`ndtd` and `ndte`)](https://cice-consortium-cice.readthedocs.io/en/latest/user_guide/ug_implementation.html#choosing-an-appropriate-time-step) can be set in `ice_in`. Setting `ndtd` within `ice_in` allows for sub-cycling of the sea-ice dynamics to ensure numerical stability and may need to be increased during initial model spin up (the thermodynamics should be numerically stable for any time-step).

### MOM6 time-steps

MOM6 has 5 timesteps - see these references:

- [Lecture: MOM6 time stepping (Vertical Langrangian Remap)](https://youtu.be/JKMwd8VXYcU?t=383)
- [Lecture: MOM6 time stepping (Summary)](https://youtu.be/JKMwd8VXYcU?t=2165)
- [MOM6 ReadtheDocs](https://mom6.readthedocs.io/en/main/api/generated/pages/Timestep_Overview.html). 

From shortest to longest they are: barotropic (`DTBT`), baroclinic Lagrangian (`DT`), tracer advection (`DT_TRACER_ADVECT`), thermodynamic (`DT_THERM`) and vertical remapping. 
Note that currently in MOM6 remapping is performed as part of the thermodynamic step so their timesteps cannot be set independently. 
It is common to set at least these 3 timesteps in the `MOM_input` file:

- Barotropic time-step (`DTBT`) for integration of sea surface and depth-averaged horizontal velocity. If set negative (e.g. `DTBT = -0.95`), the magnitude of `DTBT` is interpreted a fraction of the stability limit, so can be set independently of the model configuration (e.g. resolution). `DTBT_RESET_PERIOD` controls how often the stability limit is recalculated.

- Baroclinic time-step (`DT`) for Lagrangian stacked shallow-water equations; often called "the" model timestep; needs to be short enough to resolve internal gravity waves, inertial oscillations and advection on the horizontal grid (i.e. this is resolution-dependent).

- Thermodynamics time-step (`DT_THERM`), which can be [set to resolve the relevant physics](https://youtu.be/JKMwd8VXYcU?si=dBk09lMVPsMF3aJT&t=541) (e.g. one to three hours or so to capture the diurnal cycle), independent of the horizontal grid resolution. It is possible to set `DT_THERM` longer than the coupling time-step, but only with [`DIABATIC_FIRST = False`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2FMOM_input+content%3ADIABATIC_FIRST&type=code). The tracer advection timestep (`DT_TRACER_ADVECT`) defaults to the same as `DT_THERM`.

### WAVEWATCH III time-steps

WW3 advances the wave-action spectrum using separate calculations for geographic propagation, propagation in spectral space, and source terms. It therefore has four timestep controls, rather than one fixed wave timestep. See the [versioned WW3 timestep guidance](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/nml/ww3_grid.nml#L46-L80).

For the ACCESS-OM3 coupled executable documented in the [MCW guide](/configurations/MCW_100km/), set these controls in seconds in the `&ww3_inparm` namelist in **`wav_in`**:

- **Geographic propagation (`dtcfl`, called `DTXY` in WW3 preprocessing)** controls the reference timestep for transporting wave action across the horizontal grid. Choose it using the smallest active grid-cell spacing and the fastest wave group speed, associated with the lowest spectral frequency, rather than the nominal model resolution. A typical starting point is `0.9 × minimum spacing / maximum group speed`. In the PR1 scheme used by this configuration, local propagation substeps also account for wave speed and currents.

- **Spectral propagation (`dtcfli`, or `DTKTH`)** limits the timestep for changes in wavenumber and direction, including refraction. Its appropriate value depends on spectral resolution and refraction by currents and depth variations, so it cannot be inferred from horizontal grid spacing alone. WW3 guidance suggests approximately `dtmax/2` for weak currents and potentially `dtmax/10` for strong currents; these are starting estimates to assess through tests, not universal stability limits.

- **Overall integration (`dtmax`, or `DTMAX`)** sets the maximum global wave timestep. Geographic and spectral propagation can take substeps within it, while source-term integration uses its own dynamically selected steps. A common starting choice is approximately `3 × dtcfl`, with timestep limits chosen as integer multiples where practical. It is a maximum, not a guarantee that every internal update advances by that duration.

- **Source-term integration (`dtmin`, or `DTMIN`)** sets the minimum timestep for dynamically integrating wave growth and dissipation, such as wind input and whitecapping. It is not the timestep for geographic propagation or the minimum coupling interval. WW3 gives a typical range of 5–60 s and a common starting value of 10 s; configuration-specific testing can justify other choices. The documented MCW configuration retains 50 s in its tested timestep set.

The **coupling interval** is set separately in `nuopc.runseq`: it controls when WW3 exchanges information with the other components, not its internal propagation or source-term substeps. For straightforward alignment, choose `dtmax` and `dtcfl` to divide that interval. For example, the documented MCW configuration uses a 3600 s coupling interval with `dtmax = 1800`, `dtcfl = 600`, `dtcfli = 600` and `dtmin = 50` s. Changing `wav_in` alone does not change coupling frequency; changing coupling also requires reviewing the other components' timesteps.

In this build's `CESMCOUPLED` pathway, the [WW3 cap restores these four values from `wav_in` after loading `mod_def.ww3`](https://github.com/ACCESS-NRI/WW3/blob/2026.03.001/model/src/wav_comp_nuopc.F90#L1599-L1607). Timestep-only edits therefore do not require regenerating the binary inputs, and editing only the preprocessing timestep values will not change the runtime controls. Recheck this behaviour for other executables or standalone WW3.

See the [MCW parameter rationale and comparison results](/configurations/MCW_100km/#time-stepping_1) for the selected values, and [Changing WW3 timesteps](/configurations/MCW_100km/#changing-ww3-timesteps) for editing, log checks and validation. The reported limits are distinct from adaptive internal substeps; the PR1 build also has limitations on the available CFL diagnostics, described in that procedure.
