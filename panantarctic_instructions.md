# Instructions to generate pan-Antarctic regional domain from global ACCESS-OM3 Configuration

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


# Moving to 8km domain

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
