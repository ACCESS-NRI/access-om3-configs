# ACCESS-OM3 Topography Workflow

## Introduction
The supported ACCESS-OM3 configurations now use a topography based on the [GEBCO2024](https://www.gebco.net/data_and_products/gridded_bathymetry_data/gebco_2024/) global topography dataset. This dataset maintains a high resolution of 15 arc-seconds (i.e., 1/240 deg = ~460m at the equator and finer zonally near the poles).

## Bathymetry Tools
The workflow described below uses `bathymetry-tools` to perform specific tasks, such as removing seas or generating the land/sea mask. Instructions to install `bathymetry-tools` can be found [here](https://github.com/COSIMA/bathymetry-tools).

## General Workflow
The general workflow for generating the OM3 topography and corresponding land/sea masks is as follows:

1. **Interpolate GEBCO2024 data** onto the model grid.
2. **Adjust C-grid connectivity** using the `deseas` algorithm to ensure marginal seas with 1-cell-wide outlets (e.g., Gibraltar) remain connected to the ocean.
3. **Remove T cells** that are smaller than the given threshold.
4. **Fill cells** with a sea area fraction smaller than 0.5.
5. **Apply manual topography edits** using `editTopo.py`.
6. **Remove isolated seas**.
7. **Apply minimum and maximum allowed ocean depths**.
8. **Generate the land/sea mask** from the topography.
9. **Generate additional necessary model input files**, such as ESMF meshes and runoff remapping weights.

This workflow assumes that a horizontal super-grid has already been created and that the model uses a C-grid. Some manual editing may still be necessary to refine the topography.

For a complete workflow and instructions on generating OM3 topography, refer to the [make_OM3_025deg_topo](https://github.com/ACCESS-NRI/make_OM3_025deg_topo/tree/main) repository.

## Updating restarts for new bathymetry

If the MOM bathymetry file (topog.nc) needs to be changed on an existing run it's ocean and coupler restarts will need to be fixed up. Otherwise the restarts may not contain valid data at all points. This section describes a method for doing this. This github [issue](https://github.com/ACCESS-NRI/access-om3-configs/issues/502) comment may also be helpful.

### Updating Ocean restart files
The approach taken is to create ocean restart files that match the new bathymetry (we call these the template restarts), then copy over all valid data from restarts for the existing run (call these the old restarts). The end result will be a restart that is the same as the existing run at all points which exist in both the old and the template (we call these the new restarts). Any new points that don't exist in the old restarts will contain whatever existed in the template restarts. This approach is simple but has a drawback — if the bathymetry has changed a lot, some points will use values from the template that may not match the surrounding fields from the old restart, leading to possible inconsistencies.

Step by step:

1. Download `om3-scripts`. This contains `apply_bathy_mom_restarts.py` script in `restart_modifications` directory that does the copying described above.

`git clone https://github.com/ACCESS-NRI/om3-scripts/tree/main`
2. Generate new restart files using new bathymetry

New template restart files must be generated from a simulation using the updated topog.nc bathymetry. If such a simulation doesn't exist, you will need to create the restart files by performing a short ACCESS-OM3 run from rest—typically a single time step is sufficient. This run must use the new topog.nc file along with the corresponding land mask file for CICE: kmt.nc for the CICE mask.
3. Get an interactive PBS session with additional CPUs and memory, e.g.:

`qsub -I -v DISPLAY -q normalbw -l ncpus=4,mem64Gb,walltime=10:00:00,storage=gdata/ik11+gdata/vk83+gdata/xp65`

(add other storage points as appropriate)
4. Run the `apply_bathy_mom_restarts.py` script from `restart_modifications` directory to create new MOM restarts based on the old restarts but with the new bathymetry and any new ocean points filled in with the template, e.g.:

```
cd om3-scripts/restart_modifications
python apply_bathy_mom_restarts.py --help
python apply_bathy_mom_restarts.py --template_dir new_restart_dir --old_dir old_restart_dir --output_dir patched_restart_dir --template_prefix access-om3.mom6.r.1900-01-01-00000 --old_prefix access-om3.mom6.r.1900-01-01-00000 --nprocs 4
```
This can take quite a while. Note that `apply_bathy_mom_restarts.py` requires Python 3 -- you might need to do `module use /g/data/xp65/public/modules; module load conda/analysis3` first.
5. The patched restart files will be written to the directory given by `--output_dir` (e.g., patched_restart_dir). These files are updated versions of the template restarts, with valid ocean data from the old restarts inserted where applicable.

### Updating Coupler Restart Files 

1. Prepare required files

Ensure you have the following:

The old coupler restart file from the run using the old bathymetry (e.g., `access-om3.cpl.r.0000-01-01-00000.nc`)

The new land mask file corresponding to the updated bathymetry (e.g., kmt.nc)

The name of the land mask variable inside the mask file (usually kmt)
2. Start an interactive PBS session (if needed)
`qsub -I -v DISPLAY -q normalbw -l ncpus=2,mem=32GB,walltime=02:00:00,storage=gdata/ik11+gdata/vk83+gdata/xp65`

Add any additional storage paths your data resides in.
3. Run the coupler restart fix script `remask_cpl_restart.py` from `om3-scripts/restart_modifications`

```bash
cd om3-scripts/restart_modifications
python3 remask_cpl_restart.py --input_file /path/to/access-om3.cpl.r.0000-01-01-00000.nc --output_file /path/to/access-om3.cpl.r.0000-01-01-00000.nc --mask_file /path/to/kmt.nc --mask_var kmt

`python3 remask_cpl_restart.py --input_file /path/to/access-om3.cpl.r.0000-01-01-00000.nc --output_file /path/to/access-om3.cpl.r.0000-01-01-00000.nc --mask_file /path/to/kmt.nc --mask_var kmt`

You may need to load a compatible Python module, e.g.: `module use /g/data/xp65/public/modules && module load conda/analysis3`.
4. Check the output

The script will produce a new coupler restart file in the filename as specified by --output_file, 

This file contains surface-level fields where missing values have been filled and re-masked using kmt.nc. It is now ready for use in your ACCESS-OM3 simulation with updated bathymetry.
5. Copy other restart files into the new restart directory
Create a new directory in `archive` to hold the complete set of restart files for your simulation.

Place the modified MOM6 and coupler restart files (produced by the scripts) in this directory.

Copy the unmodified restart files from other components (e.g., CICE, DATM, DROF) from your old restart directory into this same directory.

Example files to copy alongside MOM6 and CPL restarts:
```
access-om3.cice.r.1900-01-01-00000.nc  
access-om3.datm.r.1900-01-01-00000.nc  
access-om3.drof.r.1900-01-01-00000.nc  
```

This ensures the new restart directory contains a complete, consistent set of restart files with updates only to MOM6 and the coupled components.
