# WW3 Parameter Choices

The current configuration of **WAVEWATCH III (WW3)** in ACCESS-OM3 uses parameter values for the **ST6 source term package** in `WW3_PreProc/namelists_Global.nml`, selected following discussions with the WW3 community. These settings reflect commonly used values that are aligned with best practices in recent applications.

## 🌊 What is the ST6 Source Term?

**ST6** is an observation-based source term package for deep-water wave modeling in WW3. It includes:

- **Wind input** (positive and negative)
- **Whitecapping dissipation**
- **Swell–turbulence interaction (swell dissipation)**

The parameterizations are derived from:

- Field measurements at **Lake George, Australia** (wind input and whitecapping)
- Laboratory and field studies of **swell decay**
- **Negative wind input** based on lab testing

ST6 also imposes a physical constraint on total wind energy input using the **independently known wind stress**, improving realism and consistency in wave growth and dissipation behavior.

> 📚 Reference:
> Rogers, W. E., A. V. Babanin, and D. W. Wang (2012).  
> *Observation-consistent input and whitecapping dissipation in a model for wind-generated surface waves: Description and simple calculations.*  
> J. Atmos. Oceanic Techn., 29, 1329–1346.  
> [https://doi.org/10.1175/JTECH-D-11-00092.1](https://doi.org/10.1175/JTECH-D-11-00092.1)

## Current ST6 Parameters

```
&SIN6 SINA0=0.04 /
&SWL6 SWLB1=0.22E-03, CSTB1=T /
&SNL1 LAMBDA=0.237, NLPROP=2.13E+07 /
```

These parameters configure wind input (`SIN6`), swell dissipation (`SWL6`), and nonlinear interactions (`SNL1`) for ST6 physics.

---

## SINA0
`SINA0` is a tuning parameter in the `&SIN6` namelist that controls the **damping effect of adverse winds** in the ST6 wind input scheme. It scales the negative input term that reduces wave growth when the wind opposes wave direction, helping to prevent unrealistic wave energy buildup.

Current setting:

```
&SIN6 SINA0=0.04 /
```
---

## PR3 Tuning (Not Currently Used)

The ACCESS-OM3 WW3 configuration currently uses the **PR1** propagation scheme. However, if switching to **PR3** in the future, tuning is required to mitigate the **garden sprinkler effect (GSE)**. This tuning is done using the `&PRO3` namelist.

Recommendations for the appropriate `WDTHCG` and `WDTHTH` values are given in **Chawla and Tolman (2008)** and depend on the grid resolution.

---

## Recommended Tuning Factors for PR3

From Table A.1 in Chawla and Tolman (2008):

| Grid Resolution | Tuning Factor (`&PRO3 WDTHCG`, `WDTHTH`)  | Approx Resolution (km) |
|-----------------|-------------------------------------------|------------------------|
| 2′              | 16                                        |3.7 km                  |
| 4′              | 8                                         |7.4 km                  |
| 8′              | 4                                         |14.8 km                 |
| 15′             | 2                                         |27.8 km                 |
| 30′             | 1                                         |55.76 km                |

If PR3 is adopted, these values can be set as based on the Grid resolution:

```fortran
&PRO3 WDTHCG = <value>, WDTHTH = <value> /
```
>📚 Reference:
>Arun Chawla, Hendrik L. Tolman (2008), **Obstruction grids for spectral wave models**, *Ocean Modelling*, Volume 22, Issues 1–2, Pages 12–25,[doi.org/10.1016/j.ocemod.2008.01.003](https://doi.org/10.1016/j.ocemod.2008.01.003)

---

## 🌊 WW3 Langmuir Mixing Parameterization (`&LMPN`)

The **Langmuir Mixing Parameterization** (LMP) in WAVEWATCH III (WW3) accounts for additional vertical mixing in the ocean surface boundary layer induced by Langmuir turbulence—a phenomenon caused by the interaction between surface waves and wind-driven currents.

This feature is especially relevant when WW3 is **coupled to an active ocean model**, such as MOM6 or POP2, to improve realism in air-sea fluxes and surface mixing processes in Earth System Models.

The configuration is controlled using the `&LMPN` namelist group.

## Key Parameters

| Parameter     | Description                                                                                           | Typical Values |
|---------------|-------------------------------------------------------------------------------------------------------|----------------|
| `LMPENABLED`  | Enables Langmuir mixing parameterization                                                              | `T` or `F`     |
| `SDTAIL`      | Includes spectral tail contribution to Stokes drift (used for enhanced mixing in high-frequency tail),|                |
|               | set to false by default                                                                               | `T` or `F`     | 
| `HSLMODE`     | Controls how the **surface layer depth (HSL)** is defined:                                            | `0` or `1`     |
|               | - `0`: Fixed uniform 10m depth (testing mode)                                                         |                |
|               | - `1`: Dynamically received from ocean model via coupler                                              |                |

## Current ACCESS-OM3 Coupled Model Configuration

In the MOM6–CICE6–WW3 coupled setup, we use:

```fortran
&LMPN
  LMPENABLED = T,
  HSLMODE = 1,
/
```

- `LMPENABLED = T`  
  Activates the Langmuir mixing scheme, improving surface mixing representation in coupled runs.

- `HSLMODE = 1`  
  Ensures that the **surface layer depth (HSL)** is dynamically received from the active ocean model (MOM6) via the coupler.

> ⚠️ `SDTAIL` is **not enabled** in the current setup, meaning spectral tail contributions are excluded.

This implementation is based on:

> **Li, Qing, et al. (2016)**.  
> *Langmuir mixing effects on global climate: WAVEWATCH III in CESM.*  
> Ocean Modelling, **103**, 145–160.  
> [https://doi.org/10.1016/j.ocemod.2015.08.013](https://doi.org/10.1016/j.ocemod.2015.08.013)
