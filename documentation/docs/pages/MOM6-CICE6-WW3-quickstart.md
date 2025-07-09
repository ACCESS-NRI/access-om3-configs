# Running the MOM6–CICE6–WW3 Coupled Model

This guide provides a workflow for running the coupled **MOM6–CICE6–WW3** model in ACCESS-OM3 using **prebuilt executables** and existing configuration input files. It assumes **no local builds or compilation**.

---

## 1. Load Required Modules

First, configure your environment by loading the appropriate modules:

```bash
module use /g/data/vk83/modules
module load payu
```

---

## 2. Clone the Wave Configuration

Use `payu` to clone one of the existing wave-coupled ACCESS-OM3 configurations:

### For **RYF forcing**:
```bash
payu clone --branch dev-MCW_100km_jra_ryf   git@github.com:ACCESS-NRI/access-om3-configs.git wav_config_ryf
```

### For **IAF forcing**:
```bash
payu clone --branch dev-MCW_100km_jra_iaf   git@github.com:ACCESS-NRI/access-om3-configs.git wav_config_iaf
```

This creates a working directory (`wav_config_ryf/` or `wav_config_iaf/`) containing the configuration files.

---

## 3. (Optional) Regenerate WW3 Input Files

This step is **only required** if you modify the WW3 pre-processing inputs:

- `WW3_PreProc/ww3_grid.nml` — to change grid or spectral discretization  
- `WW3_PreProc/ww3_strt.inp` — to change restart/initialization setup

> **Important:**  
> If you modify `WW3_PreProc/namelists_Global.nml`, this affects WW3 physics and **requires recompiling ACCESS-OM3** with matching WW3 compile-time switches. This cannot be handled by namelists alone.

### To regenerate input files:

1. **Load the module version matching your `config.yaml`:**

```bash
module use /g/data/vk83/modules
module load access-om3/<version>  # Use exact version listed in config.yaml
```

2. **Run preprocessing tools from the config directory:**

```bash
cd <wave_config_directory>/WW3_PreProc

# Generate mod_def.ww3
ww3_grid

# Generate restart.ww3
ww3_strt
```

This creates updated `mod_def.ww3` and `restart.ww3` in the `WW3_PreProc` directory.

---

## 4. Modify `config.yaml` (if using regenerated WW3 files)

If you regenerated WW3 input files, update your `config.yaml` file:

### Replace the default WW3 input paths with the regenerated ones:
```
input:
  - /g/data/$PROJECT/$USER/<wave_config_directory>/WW3_PreProc/restart.ww3
  - /g/data/$PROJECT/$USER/<wave_config_directory>/WW3_PreProc/mod_def.ww3
```

> Replace `<wave_config_directory>`, `$PROJECT`, and `$USER` with your actual path values.

### (Only if you recompiled ACCESS-OM3) Remove any default module loading like:
``
- access-om3/2024.09.0
```

> This step is only necessary if you're using your own compiled version of ACCESS-OM3 instead of a prebuilt module

If you **haven’t changed anything** in `WW3_PreProc`, you can skip steps 3 and 4 entirely.

---

## 5. Run the Model

From the configuration directory:

### Clean and initialize:

```bash
payu sweep
```

### Start the run:

```bash
payu run
```

This will launch the MOM6–CICE6–WW3 coupled model using your configured setup and inputs.

---
