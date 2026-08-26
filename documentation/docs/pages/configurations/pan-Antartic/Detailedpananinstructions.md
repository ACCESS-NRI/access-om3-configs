
# Instructions to generate pan-Antarctic regional domain from global ACCESS-OM3 Configuration 

Contents:

1. Introduction
2. Make 25km panan from 25km OM3 and add boundary conditions
3. Convert to 8km pan-An using GEBCO bathy
4. Optimisation
5. Use Charrassin bathy instead
6. Use new parameters
7. Fix bugs
  

# 1. Introduction 
This page outlines the steps followed to create the pan-Antarctic configurations (ACCESS-rOM3-panan). It also describes some of the bugs encountered and outlines remaining issues to investigate. The purpose of this document is to:
1. have a record of the steps followed to create the domain and,
2. Document an example workflow for creating a regional domain as a subset of a global domain.

When modifying this workflow to create a user-defined regional domain, be aware that subsetting of the global domain will need to occur in the x- and y- directions for non-polar domains.
**Note**: The below docs are based off [this markdown file](https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc2-sapphirerapid-Charrassin-newparams-rerun-Wright-spinup-accessom2IC-yr9/panantarctic_instructions.md)
# 2.  Make 25km panan from 25km OM3 and add boundary conditions

These instructions were used to make a test 25km pan-An regional config. This configuration is a test configuration used for development, including developing the workflow for creating a regional domain from a global domain. We start with a global domain, truncate it, and then change configuration files as required.

First, load modules for `payu`:
```
module use /g/data/vk83/modules
module load payu
```

Then clone the current dev 25km branch:

```
mkdir  ~/access-om3-configs/
cd  ~/access-om3-configs/
payu clone --new-branch expt --branch dev-MC_25km_jra_ryf https://github.com/ACCESS-NRI/access-om3-configs 25km_jra_ryf
```

`config,yaml`, in the folder `25km_jra_ryf`, shows the location of the input files. These need to be modified for the regional domain which can be done in a new folder:

```
mkdir /g/data/x77/cy8964/mom6/input
mkdir /g/data/x77/cy8964/mom6/input/input-25km
```

Then copy the files listed in the `config.yaml` so there is a local copy. Note that file names and paths may differ for different varients of the base global configuration.

```
cd /g/data/x77/cy8964/mom6/input/input-25km
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/cice/grids/global.025deg/2025.02.17/kmt.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/mom/grids/mosaic/global.025deg/2025.01.30/ocean_hgrid.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/mom/grids/vertical/global.025deg/2025.03.12/ocean_vgrid.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/mom/initial_conditions/global.025deg/2025.03.19/ocean_temp_salt.res.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/mom/surface_salt_restoring/global.025deg/2025.01.30/salt_sfc_restore.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/share/grids/2025.02.17/topog.nc .
```

In this case, `ocean_mask.nc` is not listed in `config.yaml` and if it can't be found then a new one needs generating 

### Generating `ocean_mask.nc`
Clone the `make_OM3_025deg_topo` tools. First `cd` into a suitable directory (e.g, your `home` drive)
```
git clone git@github.com:ACCESS-NRI/make_OM3_025deg_topo.git
```

To download the import submodules,do:

```
git submodule update --init --recursive
```

which downloads the correct branch of the submodules. Note starting a new gadi terminal will fix conflict with the xp86 conda environemnt.

We then follow the instructions on `https://github.com/ACCESS-NRI/make_OM3_025deg_topo` which requires modifying the `gen_topog.sh` script to 1. Add the gdata to your project in the `#PBS -l storage=` line and 2. Use `qsub` to submit:
```
qsub -v INPUT_HGRID="/path/to/ocean_hgrid.nc",INPUT_VGRID="/path/to/ocean_vgrid.nc",INPUT_GBCO="/path/to/GEBCO_2024.nc" -P $PROJECT gen_topo.sh
```
For the 25km Pan-an development this looked like:
```
qsub -v INPUT_HGRID=/g/data/x77/cy8964/mom6/input/input-25km/ocean_hgrid.nc,INPUT_VGRID=/g/data/x77/cy8964/mom6/input/input-25km/ocean_vgrid.nc,INPUT_GBCO=/g/data/ik11/inputs/GEBCO_2024/GEBCO_2024.nc -P x77 gen_topo.sh
```
This generates the files where you cloned the `make_OM3_025deg_topo` repo and needs to be copied to the folder containing the input files (e.g. `/g/data/x77/cy8964/mom6/input/input-25km`.
 
Note that bathymetry-tools pipeline used here has built in topo edits for the 025 deg config and these topo edits will need removing.

### Cropping netcdf files to regional domain

We can now use `nco` as an efficient `netcdf` chopper. Load module:
```
module load nco/5.0.5
module load netcdf
```
The command `ncdump -h XX.nc` (where 'XX.nc' is your netcdf file) can be used to check the y coordinate name and size. To crop the domain to approximately 37.5 degrees S, some trial and error may be needed get the right index. 

```
ncks -d nyp,0,790 -d ny,0,789 ocean_hgrid.nc ocean_hgrid_cropped.nc
ncdump -v "y" ocean_hgrid_cropped.nc | tail -5
```

The output of the second command will tell you the latitude that the model was cropped to. Adjust the nyp and ny numbers until satisfied with the cropping latitude.
Note that  `ocean_hgrid.nc` it is on a supergrid so has twice the number of points as variables in other netcdf files not on the supergrid.
Note also that the `nyp` index is one larger than the `ny` index. 

Now do the same for the smaller netcdf files, noting ny in `ocean_hgrid`=2 times ny in other files.

```
ncks -d ny,0,394 kmt.nc kmt_cropped.nc
ncks -d ny,0,394 topog.nc topog_cropped.nc
ncks -d GRID_Y_T,0,394 ocean_temp_salt.res.nc ocean_temp_salt.res_cropped.nc
ncks -d lat,0,394 salt_sfc_restore.nc salt_sfc_restore_cropped.nc
ncks -d ny,0,394 ocean_mask.nc ocean_mask_cropped.nc
```

For consistency, rename the `ocean_vgrid.nc` file even though it has no y coordinate.

```
mv ocean_vgrid.nc ocean_vgrid_cropped.nc
```

There are some more input files related to meshes for the nuopc coupler. These need to be generated from the new files, they can't simply be cropped from the global version. Using the `om3-scripts` submodule in the `make_OM3_025deg_topo` repository, there are scripts to make them. 

If not already loaded:
```
module use /g/data/xp65/public/modules
module load conda/analysis3
```

Then generate the mesh files, first `access-om3-025deg-ESMFmesh_cropped.nc ` and then `access-om3-025deg-nomask-ESMFmesh_cropped.nc`. Modify path names as necessary to point to your input directory.

```
python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-25km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-25km/access-om3-025deg-ESMFmesh_cropped.nc --mask-filename=/g/data/x77/cy8964/mom6/input/input-25km/ocean_mask_cropped.nc --wrap-lons

python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-25km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-25km/access-om3-025deg-nomask-ESMFmesh_cropped.nc --wrap-lons
```

Generating the `access-om3-025deg-rof-remap-weights_cropped.nc` file requires a PBS submission using a PBS script similar to this:

```
#!/usr/bin/env sh
# Copyright 2025 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

#PBS -q normal
#PBS -l walltime=4:00:00,mem=10GB
#PBS -l wd
#PBS -l storage=gdata/hh5+gdata/ik11+gdata/x77+gdata/vk83

module use /g/data/hh5/public/modules
module load conda/analysis3
module load nco

set -x #print commands to e file
set -e #exit on error

python3 ./om3-scripts/mesh_generation/generate_rof_weights.py --mesh_filename=/g/data/x77/cy8964/mom6/input/input-25km/access-om3-025deg-ESMFmesh_cropped.nc --weights_filename=/g/data/x77/cy8964/mom6/input/input-25km/access-om3-025deg-rof-remap-weights_cropped.nc

```
Adjust file names and project storage as appropriate.

All input files have now been generated and the next steps are to modify the input configuration files.

### Modifying namelist files
The next step is to modify the namelists in the run directory folder where we originally cloned the global model (`cd  ~/access-om3-configs/25km_jra_ryf`). First, we modify `config.yaml`. This needs the following:
- project code
- set `runlog: true`

Update input paths to where your new cropped input files are stored. For the pan-An 25 km configurations, this looks like:

```
input:
    - /g/data/x77/cy8964/mom6/input/input-25km/kmt_cropped.nc
    - /g/data/x77/cy8964/mom6/input/input-25km/ocean_hgrid_cropped.nc
    - /g/data/x77/cy8964/mom6/input/input-25km/ocean_vgrid_cropped.nc
    - /g/data/x77/cy8964/mom6/input/input-25km/ocean_temp_salt.res_cropped.nc
    - /g/data/x77/cy8964/mom6/input/input-25km/salt_sfc_restore_cropped.nc
    - /g/data/x77/cy8964/mom6/input/input-25km/topog_cropped.nc
    - /g/data/x77/cy8964/mom6/input/input-25km/access-om3-025deg-ESMFmesh_cropped.nc
    - /g/data/x77/cy8964/mom6/input/input-25km/access-om3-025deg-nomask-ESMFmesh_cropped.nc
    - /g/data/vk83/configurations/inputs/access-om3/share/meshes/share/2024.09.16/JRA55do-datm-ESMFmesh.nc
    - /g/data/vk83/configurations/inputs/access-om3/share/meshes/share/2024.09.16/JRA55do-drof-ESMFmesh.nc
    - /g/data/x77/cy8964/mom6/input/input-25km/access-om3-025deg-rof-remap-weights_cropped.nc
    - /g/data/vk83/experiments/inputs/JRA-55/RYF/v1-4/data
```
Noting that the JRA55do atmosphere input stays the same and does not need to change. Also, we start from a deafult CICE initial condition; otherwise that could also be an input file.

Next modify `datm_in` with the new y length (ny in the kmt_cropped file i.e. real grid size not supergrid):

```
model_maskfile = "./INPUT/access-om3-025deg-nomask-ESMFmesh_cropped.nc"
model_meshfile = "./INPUT/access-om3-025deg-nomask-ESMFmesh_cropped.nc"
nx_global = 1440
ny_global = 395
```
Do the same changes in `drof_in`.

In `MOM_input` we need to change `NJ_GLOBAL = 395` and `TRIPOLAR = False`. Additionally, change all the netcdf files (seach for "*.nc") to align with the new cropped name (e.g. `ocean_hgrid.nc` => `ocean_hgrid_cropped.nc`.

For `ice_in`, the `history_chunksize` needs to be changed. Choose something proportional to the original i.e. decrease second number by ratio of new ny to old ny):
```
history_chunksize = 720, 186
```

Also change grid info:
```
  grid_type = "regional"

  ns_boundary_type = "open"
  nx_global = 1440
  ny_global = 395
```
Where `ny_global` is the new non-supergrid y-dimention

and file names:
```
&grid_nml
  bathymetry_file = "./INPUT/topog_cropped.nc"
  grid_atm = "A"
  grid_file = "./INPUT/ocean_hgrid_cropped.nc"
  grid_format = "mom_nc"
  grid_ice = "B"
  grid_ocn = "A"
  grid_type = "regional"
  kcatbound = 0
  kmt_file = "./INPUT/kmt_cropped.nc"
```

`nuopc.runconfig` also needs the updated netcdf file names (search "*.nc")

Then add into `MOM_override`:
```
#override TOPO_FILE = "topog_cropped.nc"
```
This is because the default MOM6 topo file name is topog.nc but we have changed it.

To run, do `payu setup`, check file paths look right and work directory was made. Then
`payu sweep`
and `payu run`. You can check the status with the command `uqstat`. Errors will come up in the access-om3.eXXXX file.

The 25km panAn ran in 2.5 hours and used 6.9 kSU.

### CICE initial conditions
The default CICE IC is "default" which has full ice cover below 60S (and above 60N). Since the simulation starts in January, a zero ice cover initial condition may be more appropriate. This wasn't tested by we suggest it could be controlled in `ice_in` with

`setup_nml`: `ice_ic` to `'none'` instread of `'deafult'`.

### OBC instructions

The boundary condition files can be generated by using [this script](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-obcs/ACCESS-OM2_panan_boundary_forcing_8km.ipynb). However, this script is now depreciated and will need some minor updates to the xarray syntax to allow the notebook to run with updated xarray versions in newer analysis environments (the notebook previously ran on hh5).

Before running, check that the files give sensible numbers e.g. temperature in celcius.

Then add file to `config.yaml`:
```
input:
   - /g/data/x77/cy8964/mom6/input/input-25km/forcing_access_yr2_25km_fill.nc
```

Then add to `MOM_override`:
```
! === module MOM_open_boundary ===
OBC_NUMBER_OF_SEGMENTS = 1
OBC_FREESLIP_VORTICITY = True
OBC_FREESLIP_STRAIN = True
!OBC_COMPUTED_VORTICITY = True
OBC_ZERO_BIHARMONIC = True

OBC_SEGMENT_001 = "J=N,I=N:0,FLATHER,ORLANSKI,NUDGED"
OBC_SEGMENT_001_VELOCITY_NUDGING_TIMESCALES = .3, 360.0 ! inflow and outflow timescales
BRUSHCUTTER_MODE = True ! read data on supergrid
OBC_SEGMENT_001_DATA = "U=file:forcing_access_yr2_25km_fill.nc(u),V=file:forcing_access_yr2_25km_fill.nc(v),SSH=file:forcing_access_yr2_25km_fill.nc(eta_t),TEMP=file:forcing_access_yr2_25km_fill.nc(pot_temp),SALT=file:forcing_access_yr2_25km_fill.nc(salt)"
!RAMP_OBCS = True

OBC_TRACER_RESERVOIR_LENGTH_SCALE_OUT = 30000
OBC_TRACER_RESERVOIR_LENGTH_SCALE_IN = 3000

! sponges
SPONGE = False
```
These parameter choices are copied from MOM6-SIS2 panantarctic: https://github.com/COSIMA/mom6-panan/blob/panan-005/MOM_input


# 3. Moving to 8km domain

The above instructions create a [25km domain](https://github.com/claireyung/access-om3-configs/tree/25km_jra_ryf-obc) subsetted from the [global 25km dev model](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_25km_jra_ryf). 

Now we want to use an 8km model domain.

First, we use the 8km [global grid that Angus made](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/7). Copy files from Angus `/g/data/x77/ahg157/inputs/mom6/global-8km/`

As before, this is a global grid which needs truncating to get the desired grid size. The top boundary is chosen such that the top `nyp` `y` value is -37.4627 (to matche the [initial conditions](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/3)).

```
ncks -d nyp,0,2884 -d ny,0,2883 ocean_hgrid.nc ocean_hgrid_cropped.nc
ncdump -v "y" ocean_hgrid_cropped.nc | tail -5
```
A similar operation is needed for for `ocean_mask` and `topog` except the different `ny` as these are not on the supergrid
```
ncks -d ny,0,1441 topog.nc topog_cropped.nc
ncks -d ny,0,1441 ocean_mask.nc ocean_mask_cropped.nc
```

The vertical grid can be used from the 25km model (which was a renamed version of the global model vertical grid)
```
cp ../input-25km/ocean_vgrid_cropped.nc .
```

The kmt (sea ice mask file) is in this case the same as ocean_mask (not that it won't be when ice shelf cavities are introduced) so rename it:
```
ncrename -O -v mask,kmt ocean_mask_cropped.nc kmt_cropped.nc
ncks -O -x -v geolon_t,geolat_t kmt_cropped.nc kmt_cropped.nc
```
Then follow the previous pipeline in `make_OM3_025deg_topo` to generate the new mesh files.This was done in a PBS script with the following commands.

```
python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-ESMFmesh_cropped.nc --mask-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_mask_cropped.nc --wrap-lons

python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-nomask-ESMFmesh_cropped.nc --wrap-lons

python3 ./om3-scripts/mesh_generation/generate_rof_weights.py --mesh_filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-ESMFmesh_cropped.nc --weights_filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-rof-remap-weights_cropped.nc
```

The OBC conditions are created in a similar manner to the 25 km pan-An domain by using [this script](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-obcs/ACCESS-OM2_panan_boundary_forcing_8km.ipynb). Note that this script is now depreciated and will need some minor updates to the xarray syntax before rerunning.

Next step are to modify all the names in `config.yaml` to point to the correct, new files. 
```
    - /g/data/tm70/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc
    - /g/data/tm70/cy8964/mom6/input/input-8km/ocean_vgrid_cropped.nc
    - /g/data/tm70/cy8964/mom6/input/input-8km/ACCESS-OM2_IC_bfilled_smoothedland.nc
    - /g/data/tm70/cy8964/mom6/input/input-8km/salt_restore_interpolated_nearest.nc
    - /g/data/tm70/cy8964/mom6/input/input-8km/topog_Charrassin_nocavity_cropped.nc
    - /g/data/tm70/cy8964/mom6/input/input-8km/access-om3-8km-ESMFmesh_Charrassin_nocavity_cropped.nc 
    - /g/data/tm70/cy8964/mom6/input/input-8km/access-om3-8km-nomask-ESMFmesh_Charrassin_nocavity_cropped.nc
```
Then, change the latitude AND longitude size numbers in `datm_in`, `drof_in`, `ice_in`, `nuopc.runcofig` as well as update names. 
In datm_in:
```
ny_global = 1142
  model_maskfile = "./INPUT/access-om3-8km-nomask-ESMFmesh_Charrassin_nocavity_cropped.nc"
  model_meshfile = "./INPUT/access-om3-8km-nomask-ESMFmesh_Charrassin_nocavity_cropped.nc"
  nx_global = 4320
  ny_global = 1442
```

In drof_in:
```
  model_maskfile = "./INPUT/access-om3-8km-nomask-ESMFmesh_Charrassin_nocavity_cropped.nc"
  model_meshfile = "./INPUT/access-om3-8km-nomask-ESMFmesh_Charrassin_nocavity_cropped.nc"
  nx_global = 4320
  ny_global = 1442
```
In ice_in:
```
  history_chunksize = 720, 186
  ndtd = 3
  bathymetry_file = "./INPUT/topog_Charrassin_nocavity_cropped.nc"
  grid_file = "./INPUT/ocean_hgrid_cropped.nc"
  grid_type = "regional"
  kcatbound = 2
  kmt_file = "./INPUT/kmt_Charrassin_nocavity_cropped.nc"
  ncat = 7
```

For now, turn salt restoring OFF since as the file has not been generated. Alse decrease the timesteps `DT` and `DT_THERM` by 3 (25km/8km ~ 3).

In MOM_override:

```
#override RESTORE_SALINITY = False

#override FATAL_UNUSED_PARAMS = False ! because there are a bunch of salt restoring stuff in the MOM_input
#override DT = 360
#override DT_THERM = 3600 
!#override DEBUG = True
```

Finally,  `nuopc.runconfig`  `PELAYOUT_attributes::` are updated with optimisation experinment layout. 

Since that has more processors going to ocean than current CPUs, increase thw number of CPUs to 2016 (a multiple of 48 but otherwise the number choice was somewhat arbitrary). 

Change `nuopc.runconfig` `CLOCK_attributes` section to have `nmonths` as the model runs slower than the global models.

```
restart_n = 1
restart_option = nmonths
restart_ymd = -999
rof_cpl_dt = 99999 #not used
start_tod = 0
start_ymd = 19000101
stop_n = 1
stop_option = nmonths
```

To monitor the progress of the job after submitting it via `payu` use:
```
tail -f work/log/ocn.log
```
which updates with some information every day.

# 4. Optimisation
Optimisation experinments that [improve runtime](https://github.com/claireyung/access-om3-configs/pull/1) have been pulled into the cascade lakes branch. Note the executable is not the most up to date MOM6 codebase.

This configurations is slow and below are some more suggestions to help optimise the configuration and others like it.

1. use sapphire rapids. This requires an extra lines in `config.yaml`

```
platform:
  nodesize: 104
  nodemem: 512
```
Note that the ACCESS-NRI released executables are optised to work on saffhire rapids and we strongly suggest trying this.
2. try to monitor state using aps profiler. This requires adding `modules: load: - intel-vtune/2025.0.1` in `config.yaml`, and `exe_prefix: aps`.

This seems to slow the model down.... but you can look at output by following instructions here https://www.intel.com/content/www/us/en/docs/vtune-profiler/cookbook/2025-0/profiling-mpi-applications.html

```
module load intel-vtune/2025.0.1
aps --report ./work/aps_result_20250528_141890971.gadi-pbs
```

and then download the .html file produced and look at it. This will only work if the model does not crash during run. 

3. try sea ice settings
`ice.log` tells you about blocks. If block sizes are too small it could slow the model down. The ideal number is 3-8.

To explore this option, change `domain_nml` block size in `ice_in` 

This is still experinmental as tests on these settings thus far have crashed.


# 5. Add Charrassin bathymetry (no ice shelves)

Bathymetry files for the Charrissin bathymetry were created in [these](https://github.com/claireyung/mom6-panAn-iceshelf-tools/generate-draft/Generate-Charrassin-bathy.ipynb) [notebooks](https://github.com/claireyung/mom6-panAn-iceshelf-tools/generate-draft/process-topo.ipynb).These notebooks also generate files for ice shelf cavities opened when this configuration comes online.

As before: truncate files, regenerate mesh files and update the netcdf name in the configuration files. No changes are needed to the grid-size parameters (`nx', `ny') when using the above 8k pan-An configuration as a stencil as the grid size is the same.

Copy config dir 
```
cp -r 8km_jra_ryf_obc2-sapphirerapid 8km_jra_ryf_obc2-sapphirerapid-Charrassin
cd 8km_jra_ryf_obc2-sapphirerapid-Charrassin
module use /g/data/vk83/modules
module load payu
payu checkout -b 8km_jra_ryf_obc2-sapphirerapid-Charrassin
```

Now crop files (`cd /g/data/x77/cy8964/mom6/input/input-8km`)

```
ncks -d ny,0,1441 topog_Charrassin_nocavity.nc topog_Charrassin_nocavity_cropped.nc
ncks -d ny,0,1441 ocean_mask_Charrassin_nocavity.nc ocean_mask_Charrassin_nocavity_cropped.nc
ncks -d ny,0,1441 kmt_Charrassin_nocavity.nc kmt_Charrassin_nocavity_cropped.nc
```

and make rof, mask files etc (`cd /home/156/cy8964/model-tools/make_OM3_8k_topo`) through submission of below PBS script on Gadi.

```
# Copyright 2025 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

#PBS -q normal
#PBS -l walltime=4:00:00,mem=10GB
#PBS -l wd
#PBS -l storage=gdata/hh5+gdata/ik11+gdata/tm70+gdata/vk83+gdata/x77

# Input files - Using the environment variables passed via -v
INPUT_HGRID=$INPUT_HGRID
INPUT_VGRID=$INPUT_VGRID
INPUT_GBCO=$INPUT_GBCO
# Minimum allowed y-size for a cell (in m)
CUTOFF_VALUE=6000
# Output filenames
ESMF_MESH_FILE='access-om3-8km-ESMFmesh.nc'
ESMF_NO_MASK_MESH_FILE='access-om3-8km-nomask-ESMFmesh.nc'
ROF_WEIGHTS_FILE='access-om3-8km-rof-remap-weights.nc'

# Build bathymetry-tools
./build.sh

module purge
module use /g/data/hh5/public/modules
module load conda/analysis3
module load nco

set -x #print commands to e file
set -e #exit on error

python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-ESMFmesh_Charrassin_nocavity_cropped.nc --mask-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_mask_Charrassin_nocavity_cropped.nc --wrap-lons

python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-nomask-ESMFmesh_Charrassin_nocavity_cropped.nc --wrap-lons

python3 ./om3-scripts/mesh_generation/generate_rof_weights.py --mesh_filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-ESMFmesh_Charrassin_nocavity_cropped.nc --weights_filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-rof-remap-weights_Charrassin_nocavity_cropped.nc

```

Move files to the input directory ('/g/data/x77/cy8964/mom6/input/input-8km') and update the netcdf names in `config.yaml`, `datm_in`, `ice_in`, `drof_in`, `nuopc.runconfig`, `MOM_override`

# 6. Add new parameters
A few parameters were changed as outlined below.
1. The coupling timestep is set on line 2 of `nuopc.runseq`. This needs to not a ratio of 3x the timestep to produce restart files

2. Parameters in `MOM_input` were altered to match the new OM3 parameters (similar to GFDL OM5). Note that this was done in `MOM_override`

3. The new internal tide mixing scheme requires two new files with roughness and tidal amplitude. This is done by reproducung the method for creating these in ACCESS-OM3 models:
https://github.com/ACCESS-NRI/om3-scripts/pull/53 
```
qsub -I -P x77 -q normalbw -l ncpus=28,mem=120G,walltime=05:00:00,storage=gdata/hh5+gdata/ik11+gdata/x77+scratch/x77+gdata/xp65
module use /g/data/xp65/public/modules
module load conda/analysis3

cd /home/156/cy8964/model-tools/om3-scripts/external_tidal_generation

mpirun -n 28 python3 generate_bottom_roughness_polyfit.py --topo-file=/g/data/ik11/inputs/SYNBATH/SYNBATH.nc --hgrid-file=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mask-file=/g/data/x77/cy8964/mom6/input/input-8km/ocean_mask_Charrassin_nocavity_cropped.nc --chunk-lat=800 --chunk-lon=1600 --output=/g/data/x77/cy8964/mom6/input/input-8km/bottom_roughness_Charrassin_nocavity_cropped.nc

python3 generate_tide_amplitude.py --hgrid-file=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mask-file=/g/data/x77/cy8964/mom6/input/input-8km/ocean_mask_Charrassin_nocavity_cropped.nc --method=conservative_normed --data-path=/g/data/ik11/inputs/TPXO10_atlas_v2 --output=/g/data/x77/cy8964/mom6/input/input-8km/tideamp_Charrassin_nocavity_cropped.nc
```
This takes about an hour to calculate bottom_roughness and about 30 minutes for tideamp.


Note that this [will not work in configurations with ice-shelf cavities] .(https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/8)


4. For stability the timestep is reduces although it might be able to be increased after a few days of spinup. Note that `dt_therm` cannot be [too big](https://bb.cgd.ucar.edu/cesm/threads/limit-on-dt_therm-in-regional-configs.8226/)

5. The diag rho coordinates were copied from a [previous panantactic configuration](https://github.com/COSIMA/mom6-panan).

6. Diag z coordinates were regridded (ocean_month_z) to address a warmer than expected western boundary currents. This issue did vanish so the regridding may not be needed.


# 7. Fix bugs

### Minor bugs
There was a Northern boundary issue where fast velocities were generated due to SSH gradient at northern boundary. A few different changes were made in an attempt to resolve this: 
1. Reverting to `WRIGHT_REDUCED` equation of state(EOS) (to make the initial and boundary conditions). This didn't fix the issue but does mean that the boundary inputs and internal model has consistent EOS.

2. Using the ACCESS-OM2-01 second year output https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/claire_working/initial-conditions/ACCESSOM2_IC_into_8km_grid.ipynb

We also changed to `WRIGHT_FULL`. See [here](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/13) for details.

We added Stewart Allen's suggested Antarctic ice thickness categories (He suggested ncat=7, with similar spacing (kcatbound=2), noting that this has it's highest at about 2.2m.)

Salinity was restoring to zero at E-W boundary and this was deactivated.
### Sapphire rapid bugs
The model crashed when running on Sapphire rapid (SR) with a segfault as the model was unable to find an exisiting and previously findable file for seaice initialisation during the restart. This was resolved by moving to Minghang's optimised and working number of cores/layout for the [ACCESS-OM3 global 25km config](github.com/ACCESS-NRI/access-om3-configs/pull/591/files) (note the`MOM_parameter_doclayout` file can be ignored as it is for a different domain). 

The number of CPUs used in the run can be set by `ncpus` in `config.yaml`, to a multiple of 104 for SR. The `mem` can also change accordingly (500 GB max per SR node). Note that if you decrease `ncpus` below to be less than any values set in `PELAYOUT_attributes`'s (set in `nuopc.runconfig`) then you will get an error message (`PELAYOUT_attributes` distributes the CPUs to different components of the model) 

### Timestep
When running on cascade lake (CL), a lot of `bad_depature_points` errors were reported. These occurs when CICE goes over the CFL limit. To fix this, the timesteps were reduced to be
```
DT = 450
DT_THERM = 900
nuopc.runseq corner number 450 (coupling timestep)
```
Attempts were made to change `ndtd` and `dt` in `ice_in` to force CICE to use a different timestep (default is the coupling timestep, you can see this in `work/log/ice.log`). However this produced segfaults and the timestemps are not decoupled. The resulting ocean component has CFLs of 0.2ish which is quite low. 

Further attempts to decouple the ocean and ice timesteps were attempted after a year of simulation:
```
ndtd = 3`
DT_THERM = 1200
DT = 600
coupling timestep 600
```
This worked but it is still unknown why the decoupling did not work in the first year of the simulation. 

Note that when varing timesteps during the simulation, we want to impose these restrictions:
1. timesteps are divisors of 1 day and ideally 1 hour since almost all runlengths will be integer multiples of those. So 450, 600, 900 all good. They also need to be multiples of each other and match at the restart time, otherwise you get a [buoyancy flux crash](https://github.com/ACCESS-NRI/access-om3-configs/pull/556#issuecomment-2939907442).
2. the coupling timestep [cannot be 3x dt](https://github.com/ACCESS-NRI/access-om3-configs/issues/380) this issue needs further investigation.
3. the thermodynamic timestep [cannot be too long](https://github.com/COSIMA/mom6-panan/issues/28)





