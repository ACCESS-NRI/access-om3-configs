# Generating MOM6 Initial Conditions Using WOA23 dataset

This guide outlines the steps to generate initial-condition fields for MOM6 from **World Ocean Atlas 2023 (WOA23)** data. The workflow produces **Conservative Temperature (CT)** and **Absolute Salinity (SA)**, the prognostic variables required by the TEOS-10 equation of state (EOS) for use in ACCESS-OM3.


## Repository and Requirements

Clone the repository that includes all necessary tools and submodules:

```bash
git clone --recursive https://github.com/ACCESS-NRI/initial_conditions_access-om3.git
cd initial_conditions_access-om3
```

A recursive clone is needed because this repository includes Nic Hannah’s [ocean-ic](https://github.com/COSIMA/ocean-ic) code as a submodule, used to interpolate WOA23 data onto MOM6 3D grids.

---

## Step 1: (Optional) Regenerate Temperature & Salinity from Raw WOA23

Use this step **only** if you want to regenerate T/S fields from a **different version** of World Ocean Atlas dataset, or are changing the EOS in MOM6, 
and the form of temperature and salinity used prognostically in MOM6 is changing.

```
./inte.csh
```

The `inte.csh` script processes World Ocean Atlas 2023 (WOA23) data to create consistent monthly temperature and salinity fields suitable for generating MOM6 initial conditions.

### Purpose

By default, WOA23 provides:
- Full-depth **annual mean** data (`XX = 00`)
- **Monthly** data (`XX = 01–12`) only for the **upper 1500 m**
- **Seasonal** data (`XX = 13–16`) covering **full depth**

To use full-depth data with **monthly resolution**, `inte.csh` reconstructs it by combining seasonal deep data with monthly shallow data. The WOA23 dataset is based on oceanographic observations collected over the period 1955 to 2022.

### What the Script Does

1. **Extract salinity (`s_an`)** from seasonal full-depth data and expand it to monthly resolution.
2. Use `ncks --mk_rec time` to add an unlimited time dimension to make the NetCDF files record-aware.
3. **Rename the salinity variable** from `s_an` to `practical_salinity` for compatibility with the processing pipeline.
4. Run `setup_WOA_initial_conditions.py` to merge the monthly upper-ocean data with the seasonal lower-ocean data. During this step, in-situ temperature is converted to **CT** and practical salinity is converted to **SA**, ensuring consistency with the TEOS-10 EOS.

The processed monthly files are output to:
```
/g/data/ik11/inputs/access-om3/woa23/monthly/YYYY.MM.DD
```

> 💡 You only need to run this script if you're updating or modifying the WOA23 dataset or prognostic form of temperature or salinity. Otherwise, skip this step and proceed directly to regridding using `make_initial_conditions.sh`.

---

## Step 2: Regrid to MOM6 Grid

Use the regridding script to interpolate temperature and salinity to your MOM6 model grid.

```
cd initial_conditions_WOA/
qsub -v VGRID="<path_to_vgrid_file>",HGRID="<path_to_hgrid_file>",INPUT_DIR="<path_to_input_directory>",OUTPUT_DIR="<path_to_output_directory>" -P $PROJECT make_initial_conditions.sh
```

Replace the variables with your grid and directory paths:

- `VGRID`: MOM6 vertical grid file
- `HGRID`: MOM6 horizontal grid file
- `INPUT_DIR`: Directory with processed WOA23 monthly files
- `OUTPUT_DIR`: Where regridded output will be saved

> Note: This code is not parallelised and may take approximately 24 hours to run for the 25km (0.25°) resolution grid.

---

## Step 3: Finalize & Tag Metadata

Once satisfied with the output, run:

```
./finalise.sh -o /g/data/ik11/inputs/access-om3/woa23/025/
```

This:
- Commits any changes with `git`
- Adds Git metadata to the NetCDF metadata

---

##  Notes

- Make sure to adjust paths in `inte.csh` if you change the WOA23 dataset.
- You can repeat Step 2 to generate initial conditions for any resolution. Step 1 is agnostic of the model resolution as the data is on the WOA23 grid.

