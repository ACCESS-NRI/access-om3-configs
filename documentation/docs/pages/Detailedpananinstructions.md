**Note**: The below docs are a copy of [this markdown file](https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc2-sapphirerapid-Charrassin-newparams-rerun-Wright-spinup-accessom2IC-yr9/panantarctic_instructions.md)

# Instructions to generate pan-Antarctic regional domain from global ACCESS-OM3 Configuration

Contents:

1. Make 25km panan from 25km OM3 and add boundary conditions
2. Convert to 8km panan using GEBCO bathy
3. Use Charrassin bathy instead
4. Use new parameters
5. Fix bugs

# 1.  Make 25km panan from 25km OM3 and add boundary conditions

These instructions were used by Claire and Helen to make a 25km pan-An regional config. There are no open boundary conditions yet. We start with a global domain, truncate it, and then change configuration files as required. This is a work in progress!!

First, we load modules so that we can use `payu`:
```
module use /g/data/vk83/modules
module load payu
```

We chose the clone the current dev 25km branch:

```
payu clone --new-branch expt --branch dev-MC_25km_jra_ryf https://github.com/ACCESS-NRI/access-om3-configs 25km_jra_ryf
```

Entering this folder, `cd 25km_jra_ryf`, you can see in `config.yaml` what the input files are. These need to be modified for the regional domain. We did this by creating a new folder **Make generic, uses Claire's folder right now**

```
mkdir /g/data/x77/cy8964/mom6/input
mkdir /g/data/x77/cy8964/mom6/input/input-25km
```

We enter this folder and then copy the files listed in the `config.yaml` so we have a local copy and don't accidentally touch anything we didn't want to! If using a different starting configuration your file names will be different.

```
cd /g/data/x77/cy8964/mom6/input/input-25km
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/cice/grids/global.025deg/2025.02.17/kmt.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/mom/grids/mosaic/global.025deg/2025.01.30/ocean_hgrid.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/mom/grids/vertical/global.025deg/2025.03.12/ocean_vgrid.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/mom/initial_conditions/global.025deg/2025.03.19/ocean_temp_salt.res.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/mom/surface_salt_restoring/global.025deg/2025.01.30/salt_sfc_restore.nc .
cp /g/data/vk83/prerelease/configurations/inputs/access-om3/share/grids/2025.02.17/topog.nc .
```

In this case, `ocean_mask.nc` was not listed in the `config.yaml`, and we could not find it, so we had to generate it. **Skip to next section if you already have `ocean_mask.nc`.**

### Generating `ocean_mask.nc` (and other bathymetry files)
First we need to clone the `make_OM3_025deg_topo` tools. First `cd` into a suitable directory (for me I chose in my `home` drive)
```
git clone git@github.com:ACCESS-NRI/make_OM3_025deg_topo.git
```

Since it contains import submodules, we do

```
git submodule update --init --recursive
```

which downloads the correct branch of the submodules. Note that for some reason I was getting a conflict with the xp86 conda environemnt and starting a new gadi terminal fixed the issue.

We then follow the instructions on `https://github.com/ACCESS-NRI/make_OM3_025deg_topo` which requires modifying the `gen_topog.sh` script to 1. Add the gdata to your project in the `#PBS -l storage=` line and 2. Use `qsub` to submit.
```
qsub -v INPUT_HGRID="/path/to/ocean_hgrid.nc",INPUT_VGRID="/path/to/ocean_vgrid.nc",INPUT_GBCO="/path/to/GEBCO_2024.nc" -P $PROJECT gen_topo.sh
```
For me this looked like
```
qsub -v INPUT_HGRID=/g/data/x77/cy8964/mom6/input/input-25km/ocean_hgrid.nc,INPUT_VGRID=/g/data/x77/cy8964/mom6/input/input-25km/ocean_vgrid.nc,INPUT_GBCO=/g/data/ik11/inputs/GEBCO_2024/GEBCO_2024.nc -P x77 gen_topo.sh
```
**(Note it looks like a missed the last step, to finalise output files. Oops)**

This generates the file where you cloned the `make_OM3_025deg_topo` repo and you can copy it to the place where your input files are.

### Cropping netcdf files to regional domain

Now you have all your files copied over. Note that we assumed `ocean_mask.nc` was created using the same script as the rest: it probably would have been better to generate all the files together and then copy them over! Also, the bathymetry-tools pipeline has built in topo edits for the 025 deg config so the line calling that text file would need to be removed and some renaming of sunsequent calls if using a different grid where the topo edits indices don't match up.

We can now use `nco` as an efficient `netcdf` chopper. Load module:
```
module load nco/5.0.5
module load netcdf
```
You can use `ncdump -h XX.nc` to check what the y coordinate name and size are. To crop the domain to approximately 37.5 degrees S, we did trial and error to get the right index. For `ocean_hgrid.nc` it is on a supergrid so has twice the number of points (ish) as the other variables.

```
ncks -d nyp,0,790 -d ny,0,789 ocean_hgrid.nc ocean_hgrid_cropped.nc
ncdump -v "y" ocean_hgrid_cropped.nc | tail -5
```

Note `nyp` number is one larger than `ny` number. The output of the second command will tell you the latitude it finishes at, adjust the nyp and ny numbers until satisfied.

Now we do the same for the smaller netcdf files, noting ny in `ocean_hgrid`=2 times ny in other files. These numbers do need to work out!

```
ncks -d ny,0,394 kmt.nc kmt_cropped.nc
ncks -d ny,0,394 topog.nc topog_cropped.nc
ncks -d GRID_Y_T,0,394 ocean_temp_salt.res.nc ocean_temp_salt.res_cropped.nc
ncks -d lat,0,394 salt_sfc_restore.nc salt_sfc_restore_cropped.nc
ncks -d ny,0,394 ocean_mask.nc ocean_mask_cropped.nc
```

We also renamed the `ocean_vgrid.nc` file even though it has no y coordinate.

```
mv ocean_vgrid.nc ocean_vgrid_cropped.nc
```

There are some more input files related to meshes for the nuopc coupler. These need to be generated from the new files, they can't simply be cropped from the global version. Using the `om3-scripts` submodule in the `make_OM3_025deg_topo` repository, there are scripts to make them. Alternatively if you didn't already use `make_OM3_025deg_topo`, you could do `git clone git@github.com:ACCESS-NRI/om3-scripts.git` and then check out the right branch (looks like some updates happening).

**Hint**: The metadata at the end of `ncdump -h XX.nc` of the original input files in `config.yaml` have instructions for what to do!

If not already loaded, need conda env:

```
module use /g/data/xp65/public/modules
module load conda/analysis3
```

Then generate the mesh files, first `access-om3-025deg-ESMFmesh_cropped.nc ` and then `access-om3-025deg-nomask-ESMFmesh_cropped.nc`. Modify path names as necessary to point to your input directory.

```
python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-25km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-25km/access-om3-025deg-ESMFmesh_cropped.nc --mask-filename=/g/data/x77/cy8964/mom6/input/input-25km/ocean_mask_cropped.nc --wrap-lons

python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-25km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-25km/access-om3-025deg-nomask-ESMFmesh_cropped.nc --wrap-lons
```

For the `access-om3-025deg-rof-remap-weights_cropped.nc` file I got a segfault so instead submitted a similar PBS script to that that made `ocean_mask.nc`. Perhaps related to hh5 vs xp86 environemnt, or to memory issue? Anyway, generated this new file `gen_rof.sh`:
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

Now you have all the input files, yay!

### Modifying namelist files
The next step is to modify the namelists in the run directory folder where we originally cloned the global model. First, we modify `config.yaml`. This needs the following:
- project code
- set `runlog: true`
- change access-om3 executable to be symmetric (the pr75-1 build)
```
modules:
    use:
        - /g/data/vk83/prerelease/modules
    load:
        - access-om3/pr75-1
        - nco/5.0.5

```

Update input paths to where your new cropped input files are stored. For me, this looked like:

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
Noting that the JRA55do atmosphere input stays the same and does not need to change. Also, we start from a deafult CIC initial condition; otherwise that could also be an input file.

Next we modify `datm_in` with the new y length (ny in the kmt_cropped file i.e. real grid size not supergrid):
```
model_maskfile = "./INPUT/access-om3-025deg-nomask-ESMFmesh_cropped.nc"
  model_meshfile = "./INPUT/access-om3-025deg-nomask-ESMFmesh_cropped.nc"
  nx_global = 1440
  ny_global = 395

```
We do the same changes in `drof_in`.

In `MOM_input` we need to change `NJ_GLOBAL = 395` and `TRIPOLAR = False`. Additionally, change all the netcdf files (seach for "nc") to be the cropped name.

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

`nuopc.runconfig` also needs the updated netcdf file names (search nc)

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
The default CICE IC is "default" which has full ice cover below 60S (and above 60N). Since starting in January, makes more sense to start with zero ice cover. I haven't done this but imagine it is controlled in `ice_in` with

`setup_nml`: `ice_ic` to `'none'` instread of `'deafult'`.

### OBC instructions

Firstly, generate file using script. Needs hh5 analysis-22.10 at the moment. https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-obcs/ACCESS-OM2_panan_boundary_forcing_005.ipynb

Check files, sensible numbers e.g. temperature in celcius.

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
These are copied from MOM6-SIS2 panantarctic: https://github.com/COSIMA/mom6-panan/blob/panan-005/MOM_input


# 2. Moving to 8km domain

Thus far I've used the [25km domain](https://github.com/claireyung/access-om3-configs/tree/25km_jra_ryf-obc) subsetted from the [global 25km dev model](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_25km_jra_ryf). 

Now we want to use an 8km model domain.

First, we use the 8km [global grid that Angus made](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/7). Copy files from Angus `/g/data/x77/ahg157/inputs/mom6/global-8km/`

As before, this is a global grid so we truncate to get the desired grid size. I chose the top boundary to be so the top `nyp` `y` value is -37.4627 (which matches the [initial conditions Wilton has set up](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/3)).

```
ncks -d nyp,0,2884 -d ny,0,2883 ocean_hgrid.nc ocean_hgrid_cropped.nc
ncdump -v "y" ocean_hgrid_cropped.nc | tail -5
```
We do the same for `ocean_mask` and `topog` with the different smaller numbers since it's not on the supergrid
```
ncks -d ny,0,1441 topog.nc topog_cropped.nc
ncks -d ny,0,1441 ocean_mask.nc ocean_mask_cropped.nc
```

Copy the vertical grid from the 25km model **thoughts??**
```
cp ../input-25km/ocean_vgrid_cropped.nc .
```

The kmt (sea ice mask file) is in this case the same as ocean_mask (**it won't be with ice shelf cavities!**) so rename it:
```
ncrename -O -v mask,kmt ocean_mask_cropped.nc kmt_cropped.nc
ncks -O -x -v geolon_t,geolat_t kmt_cropped.nc kmt_cropped.nc
```
Then follow the previous pipeline in `make_OM3_025deg_topo` to generate the new mesh files. I did this in a PBS script with the following commands.

```
python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-ESMFmesh_cropped.nc --mask-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_mask_cropped.nc --wrap-lons

python3 /home/156/cy8964/model-tools/om3-scripts/mesh_generation/generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-nomask-ESMFmesh_cropped.nc --wrap-lons

python3 ./om3-scripts/mesh_generation/generate_rof_weights.py --mesh_filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-ESMFmesh_cropped.nc --weights_filename=/g/data/x77/cy8964/mom6/input/input-8km/access-om3-8km-rof-remap-weights_cropped.nc
```

I also repeated the OBC script as for 8km.

Next step was to modify all the names in `config.yaml` to point to the correct, new files. 

Then, change the latitude AND longitude size numbers in `datm_in`, `drof_in`, `ice_in`, `nuopc.runcofig` as well as update names. (**note in previous 25km I didn't change any sizes of lat/lon in nuopc.runconfig and that for some reason didn't cause issues???**)

I also turned salt restoring OFF since I didn't manage to generate the file yet in the `MOM_override` and decreased the timesteps `DT` and `DT_THERM` by 3 (25km/8km ~ 3).

```
#override RESTORE_SALINITY = False

#override FATAL_UNUSED_PARAMS = False ! because there are a bunch of salt restoring stuff in the MOM_input
#override DT = 360
#override DT_THERM = 3600 
!#override DEBUG = True
```

Finally, I updated the `nuopc.runconfig` to have an updated `PELAYOUT_attributes::` section based on what Minghang has been working on. Since that has more processors going to ocean than current CPUs, I also increased the number of CPUs to 2016 (a multiple of 48) **but this choice was arbirary and I don't know what to choose**.

To run for a shorter time (since it is expensive) I changed `nuopc.runconfig` `CLOCK_attributes` section to have `nmonths`. `ndays` probably works too. Killing the job early still allowed me to look at output netcdf files.

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

To monitor the progress of the job after submitting it via `payu` I did
```
tail -f work/log/ocn.log
```
which updates with some information every day.

# Optimisation

It is slow. Some suggestions from Manodeep, Minghang and Anton on optimisation.

1. use sapphire rapids. requires extra lines in `config.yaml`

```
platform:
  nodesize: 104
  nodemem: 512
```

2. try to monitor state using aps profiler
requires adding
`modules: load: - intel-vtune/2025.0.1` in `config.yaml`, and `exe_prefix: aps`.

This seems to slow the model down.... but you can look at output by following instructions here https://www.intel.com/content/www/us/en/docs/vtune-profiler/cookbook/2025-0/profiling-mpi-applications.html

```
module load intel-vtune/2025.0.1
aps --report ./work/aps_result_20250528_141890971.gadi-pbs
```

and then download the .html file produced and look at it
(requries model to not crash during run - having problems with the restart generation in runtime and timestep not consistent- try modifying ocn_cpl_dt and runtime in nuopc.runconfig)

3. try sea ice settings
`ice.log` tells you about blocks
maybe block sizes are too small - ideal is 3-8

chance `domain_nml` block size in `ice_in` 

Unfortunately when I changed it it crashed - maybe a specific number is required.


# 3. Step 3: add Charrassin bathymetry (still no ice shelves)

Follow notebooks in https://github.com/claireyung/mom6-panAn-iceshelf-tools/generate-draft/Generate-Charrassin-bathy.ipynb and https://github.com/claireyung/mom6-panAn-iceshelf-tools/generate-draft/process-topo.ipynb.These notebooks also generate files for ice shelf cavities opened.

As before, truncate files, and regenerate mesh files. Rename in config.yaml, and other files, no other changes needed since same grid size

Copy config dir 
```
cp -r 8km_jra_ryf_obc2-sapphirerapid 8km_jra_ryf_obc2-sapphirerapid-Charrassin
cd 8km_jra_ryf_obc2-sapphirerapid-Charrassin
ls
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

and make rof, mask files etc (`cd /home/156/cy8964/model-tools/make_OM3_8k_topo`)

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

Added files and renamed netcdf names to `config.yaml`, `datm_in`, `ice_in`, `drof_in`, `nuopc.runconfig`, `MOM_override`

# 4. Add new parameters
Firstly, note that the coupling timestep is actually controlled in `nuopc.runseq` by the number in the top right hand corner. Making this not a ratio of 3x the timestep makes it work i.e. produces restart files

Also, using cascade lake nodes removes the segfault from running from a restart

I updated MOM_input to match the new OM3 parameters (similar to GFDL OM5). Requires some changes mentioned in `MOM_override`

Changes that I want to make to these parameters for a high res model setup are in `MOM_override_newparams`

The new internal tide mixing scheme requires two new files with roughness and tidal amplitude. I found Minghang's script through the netcdf metadata of OM3 versions, and am reproducing them:

https://github.com/ACCESS-NRI/om3-scripts/pull/53 

```
qsub -I -P x77 -q normalbw -l ncpus=28,mem=120G,walltime=05:00:00,storage=gdata/hh5+gdata/ik11+gdata/x77+scratch/x77+gdata/xp65
module use /g/data/xp65/public/modules
module load conda/analysis3

cd /home/156/cy8964/model-tools/om3-scripts/external_tidal_generation

mpirun -n 28 python3 generate_bottom_roughness_polyfit.py --topo-file=/g/data/ik11/inputs/SYNBATH/SYNBATH.nc --hgrid-file=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mask-file=/g/data/x77/cy8964/mom6/input/input-8km/ocean_mask_Charrassin_nocavity_cropped.nc --chunk-lat=800 --chunk-lon=1600 --output=/g/data/x77/cy8964/mom6/input/input-8km/bottom_roughness_Charrassin_nocavity_cropped.nc

python3 generate_tide_amplitude.py --hgrid-file=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mask-file=/g/data/x77/cy8964/mom6/input/input-8km/ocean_mask_Charrassin_nocavity_cropped.nc --method=conservative_normed --data-path=/g/data/ik11/inputs/TPXO10_atlas_v2 --output=/g/data/x77/cy8964/mom6/input/input-8km/tideamp_Charrassin_nocavity_cropped.nc
```

**Do these work with cavities?** No: https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/8

bottom_roughness took about an hour, tideamp half an hour

Also aiming to increase the  timestep after a few days of spinup. However, also need to make sure dt_therm not too big: https://bb.cgd.ucar.edu/cesm/threads/limit-on-dt_therm-in-regional-configs.8226/

Also copied diag rho coordinates from the panan. not sure about the formatting....

And diag z coordinates regridded (ocean_month_z) since I spent a good morning freaking out about warm western boundary currents that were actually vanished.


# Step 5: Fix bugs

Northern boundary issue (fast velocities due to SSH gradient at northerb boundary) resolved by reverting to `WRIGHT_REDUCED` EOS

Just kidding, not resolved. Need to use ACCESS-OM2-01 second year output https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/claire_working/initial-conditions/ACCESSOM2_IC_into_8km_grid.ipynb

Also changed to `WRIGHT_FULL` (https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/13)

And added Stewart Allen's suggested Antarctic ice thickness categories ("I might suggest ncat=7, with similar spacing (kcatbound=2), but that has it's highest at about 2.2m.")

### Sapphire rapid bug
Originally SR crashed with a segfault and unhelpful link to sea ice initialisation not being able to find a file on restart, despite being fine the first time.

This was resolved by moving to Minghang's optimised and working number of cores/layout for the ACCESS-OM3 global 25km config /github.com/ACCESS-NRI/access-om3-configs/pull/591/files - ignore the `MOM_parameter_doclayout` stuff because it is for a different domain. The sea ice block size could be a useful change though, and I added it to the current spinup run.

To change number of CPUs in the run, you can change ncpus in config.yaml, to a multiple of 104 for SR. I guess mem would also need to change accordingly - 500 GB max per SR node.
If you decrease ncpus below one of the numbers in `nuopc.runconfig`>`PE_LAYOUT` which afaik assigns processors to each model component, then it will complain, so then the numbers in `nuopc.runconfig` may need to change

I don't really understand the `nuopc.runconfig` part of it, so I just copied the numbers that Minghang found best for the 25km global OM3: https://github.com/ACCESS-NRI/access-om3-configs/pull/591/files
It looks to me though that in `nuopc.runseq` this has the instructions for `nuopc`, and I don't think it's a coincidence that 1300 (the ocean number) + 364 (other components that might happen in parallel) = 1664 (total CPUs) but I'm not really sure how these particular numbers were chosen. Potentially other combinations would prevent waiting if some parts of the model are faster/slower than eachother

This change also slightly improved the efficiency (comparing the first run only)

### Timestep
Running on cascade lake, I bumped into a lot of `bad_depature_points` errors which are CICE going over the CFL limit. I reduced the timesteps to be
```
DT = 450
DT_THERM = 900
nuopc.runseq corner number 450 (coupling timestep)
```
I tried to change `ndtd` and `dt` in `ice_in` to force CICE to use a different timestep (default is the coupling timestepm, you can see this in `work/log/ice.log`. However I got a lot of segfaults when I changed the ice timesteps (straight away on initialisation) so the most stable configuration is just to run it like this. However, the ocean component has CFLs of 0.2ish which is quite low suggesting it could be improved.

After the first year of simulation on CL, I decided to try again and add `ndtd = 3`, `DT_THERM = 1200`, `DT = 600`, coupling timestep 600. This seems to be working well and in ran for the second year a bit cheaper than the first. I am not sure why I was getting so many segfaults before, but I think it is best to optimise for the stable one without sporadic segfaults that I can't explain..

A further restriction on timesteps for future reference is that
1. we want the timesteps to all go into 1 day and ideally into 1 hour since almost all runlengths will be integer multiples of those. So 450, 600, 900 all good. Also, they need to be multiples of each other and match at the restart time, otherwise you get an unused buoyancy flux crash https://github.com/ACCESS-NRI/access-om3-configs/pull/556#issuecomment-2939907442
2. the coupling timestep cannot be 3x dt, then you have a problem https://github.com/ACCESS-NRI/access-om3-configs/issues/380 for unknown reasons
3. the thermodynamic timestep cannot be too long from past experience with the MOM6 panan https://github.com/COSIMA/mom6-panan/issues/28
                                                                                                                                                                    532,1         Bot

### Optimisation improvements

Merged improvements from Ed's optimisation into my CL branch https://github.com/claireyung/access-om3-configs/pull/1 which has the most upto date config

Note the executable is one Ed made i.e. not the most up to date MOM6 codebase, but rather, same as before.

Also fixed bug that had salinity restoring zero at E-W boundary
