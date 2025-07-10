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

### Current ST6 Parameters

```
&SIN6 SINA0=0.04 /
&SWL6 SWLB1=0.22E-03, CSTB1=T /
&SNL1 LAMBDA=0.237, NLPROP=2.13E+07 /
```

These parameters configure wind input (`SIN6`), swell dissipation (`SWL6`), and nonlinear interactions (`SNL1`) for ST6 physics.

---

### SINA0
`SINA0` is a tuning parameter in the `&SIN6` namelist that controls the **damping effect of adverse winds** in the ST6 wind input scheme. It scales the negative input term that reduces wave growth when the wind opposes wave direction, helping to prevent unrealistic wave energy buildup.

Current setting:

```
&SIN6 SINA0=0.04 /
```
---

### Swell Dissipation in WW3 (`&SWL6`)

Swell dissipation in WW3 accounts for wave energy loss due to interactions with oceanic turbulence, especially in non-breaking swell conditions. While its effect is small in regions dominated by wind waves, it becomes significant for long swells or parts of the wave spectrum below the breaking threshold.

The dissipation is controlled through the `&SWL6` namelist group in `namelists_Global.nml`.

### Parameters Used

```
&SWL6 SWLB1 = 0.22E-03, CSTB1 = T /
```

- SWLB1: Sets the dissipation coefficient for swell energy loss.

- CSTB1: Enables a steepness-based formulation for improved spatial consistency in wave heights.

---

### Nonlinear Interactions (`&SNL1`)

The `&SNL1` namelist configures nonlinear wave–wave interactions, which redistribute energy within the wave spectrum.

```
&SNL1 LAMBDA = 0.237, NLPROP = 2.13E+07 /
```
LAMBDA: Tuning factor for interaction strength.

NLPROP: Constant in the nonlinear source term.

---
## 🌊 PR3 Tuning (Not Currently Used)

The ACCESS-OM3 WW3 configuration currently uses the **PR1** propagation scheme. However, if switching to **PR3** in the future, tuning is required to mitigate the **garden sprinkler effect (GSE)**. This tuning is done using the `&PRO3` namelist.

Recommendations for the appropriate `WDTHCG` and `WDTHTH` values are given in **Chawla and Tolman (2008)** and depend on the grid resolution.

---

### Recommended Tuning Factors for PR3

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

### Key Parameters

| Parameter     | Description                                                                                           | Typical Values |
|---------------|-------------------------------------------------------------------------------------------------------|----------------|
| `LMPENABLED`  | Enables Langmuir mixing parameterization                                                              | `T` or `F`     |
| `SDTAIL`      | Includes spectral tail contribution to Stokes drift (used for enhanced mixing in high-frequency tail),|                |
|               | set to false by default                                                                               | `T` or `F`     | 
| `HSLMODE`     | Controls how the **surface layer depth (HSL)** is defined:                                            | `0` or `1`     |
|               | - `0`: Fixed uniform 10m depth (testing mode)                                                         |                |
|               | - `1`: Dynamically received from ocean model via coupler                                              |                |

### Current ACCESS-OM3 Coupled Model Configuration

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
> [https://doi.org/10.1016/j.ocemod.2015.07.020](https://doi.org/10.1016/j.ocemod.2015.07.020)


## Wave-Ice Interaction: IC3 and IC4M2 Parameterizations

The coupled MOM6–CICE6–WW3 configuration primarily uses **IC3**, a visco-elastic wave–ice interaction scheme. This document summarizes the parameter choices and also describes an alternative empirical scheme, **IC4M2**, that has been tested.

---

### IC3: Visco-Elastic Model (Wang and Shen, 2010)

IC3 treats sea ice as a **visco-elastic layer**, accounting for:
- Ice thickness
- Effective viscosity
- Ice density
- Effective shear modulus

This method attenuates wave energy as it propagates into ice-covered regions.

#### Parameters Used in ACCESS Configuration:

```
&SIC3
  IC3CHENG = .TRUE.,
  USECGICE = .FALSE.,
  IC3VISC  = 1.0e3,
  IC3DENS  = 917.0,
  IC3ELAS  = 1.0e3 /
```

- `IC3CHENG`: Enables a stable numerical solver.
- `USECGICE`: When `FALSE`, group velocity is not affected by ice.
- `IC3VISC`: Effective viscosity (m²/s)
- `IC3DENS`: Ice density (kg/m³)
- `IC3ELAS`: Effective shear modulus (Pa)

#### Reference:
>Wang, R., & Shen, H. H. (2010). *Gravity waves propagating into an ice-covered ocean: A viscoelastic model*.  
>[https://doi.org/10.1029/2009JC005591](https://doi.org/10.1029/2009JC005591)

---

### IC4M2: Empirical Wave Attenuation Scheme (Meylan et al., 2014)

IC4M2 is an empirical scheme based on polynomial fits to observational data, including a roll-over effect where attenuation levels off at high frequencies.

#### Equation:
The attenuation α is given by:

α = C₁ + C₂·σ/2π + C₃·(σ/2π)² + C₄·(σ/2π)³ + C₅·(σ/2π)⁴

Recommended coefficients (from Meylan et al. 2014):

```
Cice,1...5 = [0, 0, 2.12 × 10⁻³, 0, 4.59 × 10⁻²]
```

WW3 must be compiled with the `IC4` switch to use this wave attenuation scheme.

#### Reference:
Meylan, M. H., Bennetts, L. G., & Kohout, A. L. (2014). *In situ measurements and analysis of ocean waves in the Antarctic marginal ice zone*.  
[https://doi.org/10.1002/2014GL060809](https://doi.org/10.1002/2014GL060809)

---

### Wave-Ice Interaction:  Floe-size dependent Scattering and dissipation (IS2)

The **IS2** source term in WAVEWATCH III accounts for wave scattering and dissipation by sea ice floes. This implementation is based on the approach by Meylan and Masson (2006), with additional processes including:

- **Floe size–dependent scattering**
- **Wave-induced ice breakup** (updating maximum floe diameter)
- **Anelastic dissipation**, representing internal energy loss in sea ice due to stress oscillations.

#### Parameters Used

```
&IS2ANDISB = .TRUE.,
IS2BACKSCAT = 0.2,
```

#### Description

- `IS2ANDISB = .TRUE.` enables anelastic dissipation, allowing energy loss from wave-induced cyclic stress in sea ice.
- `IS2BACKSCAT = 0.2` sets the fraction of wave energy that is backscattered by ice. Default is 1.0.

#### Notes

- `IS2UPDATE` is set to `.FALSE.` by default in our configuration, so maximum floe diameter is updated dynamically at every time step.
- `IS2UPDATE` `TRUE` – updates the maximum floe diameter based on external forcing only, and `FALSE` – updates the maximum floe diameter at every model time step.

#### Reference:
Meylan, M. H., & Masson, D. (2006). A linear Boltzmann equation to model wave scattering in the marginal ice zone. Ocean Modelling, 11(3-4), 417-427.
---
