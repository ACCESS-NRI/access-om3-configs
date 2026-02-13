# ACCESS‐OM3 config with ice shelves ‐ input files and config details

In this wiki, we first describe some aspects of the ACCESS-OM3 pan-Antarctic model with ice shelves at 1/12th degree (approximately 4km around the Antarctic continental shelf) horizontal resolution. We then show how the files were made (drawing from notes on the [MOM6-SIS2 version](https://github.com/claireyung/mom6-panAn-iceshelf-tools/wiki/How-to-make-a-new-panan-MOM6%E2%80%90SIS2-config-with-ice-shelves), which was developed first), for reference and for future modified configurations. Also refer to the config without ice shelves, documented [here](https://access-om3-configs.access-hive.org.au/pr-previews/573/configurations/pan-Antartic/Overview/).

## Configuration overview

The 4km ACCESS-OM3 pan-Antarctic model with ice shelves is built on the ACCESS-OM3 25km development, using the same ocean model MOM6 and sea ice model CICE6 with a data atmosphere and runoff, and NUOPC coupler. The domain spans -86.5 degrees to -37.5 degrees S at 1/12th degree resolution, nominally 4km near Antarctica (but nominally 8km near the equator). Similar to previous MOM6-SIS2 pan-Antarctic models (e.g. [Schmidt et al. 2025](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024MS004621)), the northern boundary uses open boundary conditions forced by an ACCESS-OM2-01 repeat year forced simulation, with daily output from a simulation close to initial conditions. 

The configuration includes static ice shelves as part of the MOM6 model (see [Stern et al. 2017](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2017MS001002), [Stern et al. 2019](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2018JC014876), [Yung et al. 2024](https://tc.copernicus.org/articles/19/5827/2025/),  [Yung et al. 2025a](https://egusphere.copernicus.org/preprints/2025/egusphere-2025-1942/) and [Yung et al. 2025b](https://essopenarchive.org/users/1005425/articles/1366578-assessment-of-a-finite-volume-discretization-of-the-horizontal-pressure-gradient-force-beneath-sloping-ice-shelves) for examples of idealised versions of MOM6 ice shelves and some details on the implementation). The vertical coordinate uses the Arbitrary Lagrangian-Eulerian coordinate of MOM6, with the target coordinate `SIGMA_SHELF_ZSTAR`, developed by [Stern et al. 2017](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2017MS001002). This vertical coordinate is zstar (geopotential) in the open ocean, but follows the ice draft below ice shelves in a quasi-sigma coordinate fashion, with some layers outcropping into the bottom bathymetry but none into the ice shelf, except at the grounding line. 75 vertical levels are used with a top layer thickness of 1.08m in the open ocean, which is compressed beneath the ice shelf leading to upper layers beneath the ice shelf of ~0.1 m. 

As in the ACCESS-OM3 25km version, we use GEBCO 2024 data to create the bathymetry, which is stitched to [Charrassin et al. 2025](https://www.nature.com/articles/s41598-024-81599-1) bathymetry data where it is available (EPSG:3031 Polar Stereographic grid). Ice thickness is also from [Charrassin et al. 2025](https://www.nature.com/articles/s41598-024-81599-1). We do not use the dynamic ice sheet capability of MOM6, instead making the static ice shelf assumption where mass loss to the ice shelf by melting is instantaneously offset by snowfall and ice movement to keep the same ice shelf shape. Meltwater is added as a volume and heat flux, so sea level could rise. The [Holland and Jenkins (1999)](https://journals.ametsoc.org/view/journals/phoc/29/8/1520-0485_1999_029_1787_mtioia_2.0.co_2.xml) ice shelf basal melt parameterisation with [McPhee (1981)](https://link.springer.com/article/10.1007/BF00119277) stability parameter is used, with a larger drag coefficient tuned to achieve melt rates on the order of other simulations and satellite melt rate estimates. Initial conditions use [Yamazaki et al. 2025 data](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024JC020920) and World Ocean Atlas 2023 below 2000 m and north of 45 degrees S. 

## Input files

_Steps used to make input files for the ACCESS-OM3 ice shelf pan-Antarctic model._

Please note that file names refer to those made in the https://github.com/claireyung/mom6-panAn-iceshelf-tools/ repo. They have been moved and renamed in [this issue](https://github.com/ACCESS-NRI/access-om3-configs/issues/880).

### 1. Grid
The first step is to generate a supergrid. We used the [ocean_model_grid_generator](https://github.com/ACCESS-NRI/ocean_model_grid_generator). Something like the following would generate a global grid at 1/12th resolution with a transition from Mercator to fixed latitude at 75S and no shifted South Pole. These can require a lot of memory, so a PBS or interactive PBS job is a good idea:

```
python ocean_grid_generator.py -r 12 --no_south_cap --ensure_nj_even --bipolar_lower_lat 65 --mercator_lower_lat -75 --mercator_upper_lat 65 --match_dy so --shift_equator_to_u_point --south_ocean_lower_lat -86.5 --lower-lon -280.0 -f /scratch/x77/cy8964/grids/ocean_hgrid_025_ext.nc
```

Discussion: https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/7

### 2. Topography
We used the [Charrassin et al. 2025](https://www.nature.com/articles/s41598-024-81599-1) bathymetry and ice products, since GEBCO didn't have the required data (see [this discussion](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/2)). However, we still need the topography where Charrassin data is not available (it's on the EPSG:3051 polar stereographic grid). So, using the topography generation pipeline is still needed. Something like this [make_OM3_025deg_topo](https://github.com/ACCESS-NRI/make_OM3_025deg_topo) but [WITHOUT the topo edits](https://github.com/ACCESS-NRI/make_OM3_025deg_topo/blob/main/gen_topo.sh#L50) which are hardcoded for the 0.25deg config. This will generate a GEBCO topography for a global context with NaNs beneath the Antarctic ice sheet.

The next step is to generate topography and ice thickness files for the new product. Similar steps are used if you want to use BedMachine. This is done in a few steps, explained in [this notebook](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-draft/Generate-Charrassin-bathy.ipynb)
1. Download the data from https://datadryad.org/dataset/doi:10.5061/dryad.rbnzs7hkc
2. Read the polar stereographic data and assign lat/lon values to each point using pyproj, and save the file as a netcdf with lat and lon variables
3. Use the ESMF regridder in a PBS job to create regridding weights from the polar grid to the model grid
```
qsub -I -P YOUR_PROJECT -q hugemem -l ncpus=192,mem=5880G,walltime=05:00:00,storage=gdata/hh5+gdata/ik11+gdata/vk83+gdata/YOUR_PROJECT
module load esmf/8.6.1 openmpi/4.1.7


mpirun -np 192 ESMF_RegridWeightGen -p none -i --ignore_degenerate -s /g/data/x77/cy8964/Charrassin2025_Data/BED_ANTGG2022_lat_lon.nc -d /g/data/x77/ahg157/inputs/mom6/global-8km/topog.nc -w /g/data/x77/cy8964/mom6/input/input-8km/Regridd_Charrassin_to_8km_global_grid_Bilinear.nc -m bilinear --netcdf4 --src_regional --check
```
4. Open the topography file you generated for the global grid
5. Regrid the polar depth data to the global grid, using precalculated weights. This will look something like the following
<img width="949" height="526" alt="image" src="https://github.com/user-attachments/assets/9ded6652-e77e-4e16-bdbe-bd3542cddd76" />

6. Where data is not available in this regridded polar grid, fill with GEBCO topography we already generated
7. Save file and add metadata, maybe check if there is a discontinuity at the join.
8. Repeat for the variables `ICE_THICKNESS` and `SURFACE` (and maybe `WATER_HEIGHT`); skip the step of joining to existing topography because that doesn't exist.
This will leave you with topography files on the new grid, including in ice shelf cavities. It also has it for all of Antarctica, not just the ocean bits; this allows you to run the model with a vanished ocean and dynamic ice sheet if you so desire.

### 3. Initial Conditions and Salt Restoring
We generate initial conditions by regridding Yamazaki et al. 2025 and WOA2023 data, see [this notebook](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/claire_working/initial-conditions/Yamazaki_IC_into_8km_grid-Copy1.ipynb). Alternatives could be using ACCESS-OM2-01 data from the Jan 1 after second year restart (similar to WOA) or WOA data, but one must be careful about which temperature/salinity variable you use, and we've found the WOA data is [quite cold on the Amundsen shelf](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/45). While extrapolating southwards, we also manually extrapolate in a different direction for parts of some cavities (Weddell, Ross, Larsen C) where otherwise the southward-extrapolated initial conditions are very warm in the cavities.

<img width="703" height="571" alt="Screenshot 2026-01-13 at 3 19 07 pm" src="https://github.com/user-attachments/assets/29d3a030-995f-4bcd-b166-bd15fc7edb48" />

Salt restoring [used a similar method](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/initial-conditions/salt-restoring.ipynb) and data based on WOA13. We use a [salt restoring mask](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/claire_working/generate-draft/process-topo-8k-minimal-topoedited.ipynb) defined by 1000m isobath (the continental shelf), saved as `salt_restore_mask.nc`.

*Ensure your E-W boundaries are correct! And make sure your files don't have a NaN fill value of NaN, this can cause problems.*

Discussion: https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/3 and https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/13

### 4. Boundary Conditions
We generated boundary conditions at our chosen boundary latitude using the same method as the COSIMA panan using [this script](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-obcs/ACCESS-OM2_panan_boundary_forcing_8km.ipynb). This script uses daily output from the second year of ACCESS-OM2-01 output, potential temperature and practical salinity, to be consistent with the initial conditions. **Didn't work with recent conda environments, so may need a code update**

### 5. Truncating files
If our files are on a global grid, then we need to truncate them to the pan-Antarctic domain. We need to ensure this is consistent with all the files. We can use `nco` as an efficient `netcdf` chopper.
```
module load nco/5.0.5
module load netcdf
```
You can use `ncdump -h XX.nc` to check what the y coordinate name and size are. To crop the domain to approximately 37.5 degrees S, we did trial and error to get the right index. For `ocean_hgrid.nc`, it is on a supergrid so has twice the number of points (ish) as the other variables.

```
ncks -d nyp,0,2884 -d ny,0,2883 ocean_hgrid.nc ocean_hgrid_cropped.nc
ncdump -v "y" ocean_hgrid_cropped.nc | tail -5
```

Note `nyp` number is one larger than `ny` number. The output of the second command will tell you the latitude it finishes at. Adjust the nyp and ny numbers until satisfied.

Now we do the same for the smaller netcdf files, noting ny in `ocean_hgrid`=2 times ny in other files. These numbers do need to work out!
As before, this is a global grid, so we truncate to get the desired grid size. I chose the top boundary to be so that the top `nyp` `y` value is -37.4627.

We do the same for `topog` with the different smaller numbers since it's not on the supergrid (and same for other files as necessary)
```
ncks -d ny,0,1441 topog.nc topog_cropped.nc
```

I copied the vertical grid from the 25km model.
```
cp ../input-25km/ocean_vgrid_cropped.nc .
```

### 5. NUOPC input
We need to provide the coupler with a mesh mask of where to apply coupling between atmosphere - sea ice - ocean. Similar to the pan-Antarctic [version without ice shelves](https://access-om3-configs.access-hive.org.au/pr-previews/573/configurations/pan-Antartic/Overview/), but using the [sea ice topography](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/claire_working/generate-draft/process-topo-8k-minimal-topoedited.ipynb) (topography file with only open ocean) since NUOPC shouldn't be exchanging fields between the atmosphere and ocean below ice shelves. This requires [code changes to MOM6](https://github.com/ACCESS-NRI/MOM6/issues/29) to allow this to run so ensure an appropriate MOM6 executable is being used.

In the final version I used the following, which draws on these [python scripts for mesh generation](https://github.com/ACCESS-NRI/om3-scripts/tree/main/mesh_generation) 
```
python3 generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-8km/150925/access-om3-8km-ESMFmesh_Charrassin_opencavity_cropped.nc --mask-filename=/g/data/x77/cy8964/mom6/input/input-8km/150925/mask_Charrassin_sea_ice_from_iceelev_new150925.nc --wrap-lons

python3 generate_mesh.py --grid-type=mom --grid-filename=/g/data/x77/cy8964/mom6/input/input-8km/ocean_hgrid_cropped.nc --mesh-filename=/g/data/x77/cy8964/mom6/input/input-8km/150925/access-om3-8km-nomask-ESMFmesh_Charrassin_nocavity_cropped.nc --wrap-lons

python3 generate_rof_weights.py --mesh-filename=/g/data/x77/cy8964/mom6/input/input-8km/150925/access-om3-8km-ESMFmesh_Charrassin_nocavity_cropped.nc --weights_filename=/g/data/x77/cy8964/mom6/input/input-8km/150925/access-om3-8km-rof-remap-weights_Charrassin_nocavity_cropped.nc

```

> [!IMPORTANT]
> When we run the model for real, we need to make sure the exact **sea ice** topography is used for making the coupling mesh files (i.e. the topography file but with 0s or NaNs in the ice shelf cavities, since we don't want sea ice or atmospheric fluxes in there). For now it doesn't really matter, since we will regenerate the file later. So we could probably get away with using the version of the file for the no ice shelf configuration here and replace it later.

Copy these files to your input directory.

### 6. Set up config

The easiest place to start is by cloning an existing ice shelf config, e.g. the alpha release **when it is available **(https://github.com/ACCESS-NRI/access-om3-configs/pull/814)

You can use `payu` to do this, for example
```
module use /g/data/vk83/modules
module load payu
payu clone --new-branch expt --branch dev-MC_4km_jra_ryf+regionalpanan+isf https://github.com/ACCESS-NRI/access-om3-configs dev-MC_4km_jra_ryf+regionalpanan+isf
```
This config has ice shelf parameters, links to input files, `diag_table` with diagnostics for ice shelves (make sure to save the `e` variable for plotting, and the `ice_shelf_model` diagnostics e.g. `melt_rate`), and modified runoff streams files `drof.streams.xml` without the liquid runoff file (remove the [`FRIVER` related lines](https://github.com/ACCESS-NRI/access-om3-configs/issues/728)). You can update `config.yaml` with the correct project, shortpath, input files etc. You may need to update other files elsewhere, e.g. in `MOM_input` the initial conditions, topo file etc, tidal amplitude file (see step 13 and turn `READ_TIDEAMP = False` for now), and other grid-related files in `ice_in`, `nuopc.runconfig`, `drof_in`, `datm_in`. If changing layout, it might be easiest to not use a mask table and just use the automatic layout method.

Alternatively, you could start with a non-ice shelf config and modify it. See section 9 for ice shelf-related parameters I recommend.

### 7. Quick run to get area

We are going to quickly run the model to get area files, as this is needed for the ice shelf input and let's assume we haven't made ice shelf input files yet.

If we cloned the ice shelf version, we'll need to turn ice shelves off if we don't have the ice shelf input file. Modify the MOM_input so that
```
ICE_SHELF = False
TRIM_IC_FOR_P_SURF = False
```
Also set the following, so that we get the area everywhere
```
#override WRITE_GEOM = 1
#override TOPO_CONFIG = "flat"
#override MAX_DEPTH = 6000
```
and then run the model:
```
payu setup
```
Check the files are in `work/INPUT`
```
payu sweep
payu run
```
The model will probably crash, but it should generate the file `work/ocean_geometry.nc`. If it doesn't crash, you can `qdel` the job.

Save this file! It should have area of tracer cells everwhere in the variable `Ah`. You can just save one variable. 
```
ncks -v Ah work/ocean_geometry.nc /g/data/x77/cy8964/mom6/input/input-8km/area_everywhere.nc
```
### 8. Make ice draft
Now that we have ice area, we can make an ice shelf input file, which requires ice thickness (!! not draft, thickness!!) and area of the cell.

Following [this notebook](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-draft/process-topo-8k-minimal.ipynb), we make an ice thickness file, setting it to be area where there is nonzero elevation in the `ICE_SURFACE` file we regridded earlier (if you use just thickness there might be some holes in it). We also create a sea ice topography file based on where the ice surface is zero. This means that the ice sheet and sea ice will NOT overlap.  Both of these ocean and sea ice topography files need to have unconnected cells removed, as these unconnected cells crash both MOM6 and CICE6.

I am not totally sure if this is essential, but I also make a `h_mask` variable in the ice file and change thicknesses that are zero where the elevation is nonzero (probably nunataks or non-ice covered rock above ground in Antarctica) to a very small amount. Otherwise, MOM makes an ice mask based on the value of the thickness, which might mean the ice coverage + sea ice coverage is not quite equal to ocean coverage.

### 9. Ice shelf config parameters

If you cloned an ice shelf version of the config you can ignore this step (and simply set `ICE_SHELF` and `TRIM_IC_FOR_P_SURF` back to True and get rid of the extra topo lines), but if you did not, here is a list of parameters you may want to add to a non-ice shelf config as a `MOM_override` file. 

- `input.nml`: Ensure that in `&MOM_input_nml` there is a line `input_filename = 'n'`. Also add the name of your `MOM_override_IS` as another parameter filename.
- [`MOM_override_IS`](https://github.com/claireyung/mom6-panan/blob/1_12_IS_ALE_working_faster/MOM_override_IS): Make this new file where we add ice shelf info
```
ICE_SHELF = True ! turns on ice shelf
SHELF_INSULATOR = False ! do ice shelf heat conduction (extra term in melt parameterisation)
SHELF_THERMO = True ! melt/freeze the ice shelf
ICE_SHELF_TEMPERATURE = -20.0 ! temperature of the ice for heat conduction term
DENSITY_ICE = 917. ! ice density
USTAR_SHELF_BG = 0.0006 ! minimum background friction velocity, taken from Jourdain et al 2019
ICE_PROFILE_CONFIG = "FILE"
ICE_THICKNESS_FILE ="ice_thickness_Charrassin_regridded_cropped_add_area_where_iceelev_noGL5m_ADDHMASKFILLTHICK_190825.nc" !name of ice thickness and area file
ICE_THICKNESS_VARNAME = "thick" !variable name
ICE_AREA_VARNAME = "area" !variable name
#override TRIM_IC_FOR_P_SURF = True !initialise ice shelf properly in ALE coordinates using SURFACE_PRESSURE_FILE
#override COL_THICK_MELT_THRESHOLD = 1e-3 ! don't melt when thickness less than 1mm
#override MIN_THICKNESS = 1.e-12 ! minimum ocean thickness
#override ANGSTROM = 1.e-15 ! not sure why, but seems to work
SURFACE_PRESSURE_FILE ="ice_thickness_Charrassin_regridded_cropped_add_area_where_iceelev_noGL5m_ADDHMASKFILLTHICK_190825.nc" !same file as ICE_THICKNESS_FILE
SURFACE_PRESSURE_VAR = "thick" !variable name
SURFACE_PRESSURE_SCALE = 8986.6 !! Ensure this is DENSITY_ICE X G_EARTH
#override REGRIDDING_COORDINATE_MODE = "SIGMA_SHELF_ZSTAR" !recommended coordinate for ice shelves as it does not vanish at the ice-ocean interface

!Melt parameterisation modifications
HMIX_SFC_PROP = 1.08 ! sampling distance of temp and salt in melt param (set to open ocean top cell value since it also affects open ocean)
HMIX_UV_SFC_PROP = 1.08 ! sampling distance of u and v in melt param (set to open ocean top cell value since it also affects open ocean)
MINIMUM_FORCING_DEPTH = 1.08 ! meltwater flux distribution distance (set to open ocean top cell value since it also affects open ocean)
CDRAG_SHELF = 0.007

!Custom changes (https://github.com/ACCESS-NRI/MOM6/pull/38)
FRAZIL_NOT_UNDER_ICESHELF = True !don't use frazil under ice shelves
ICE_SHELF_TIDEAMP_SCALING_FACTOR = 0.66 !use a different scaled tidal velocity file

ICE_SHELF_USTAR_FROM_VEL_BUGFIX = True !recent GFDL bug fix

! Recommended pressure gradient ice shelf fixes (see https://essopenarchive.org/users/1005425/articles/1366578-assessment-of-a-finite-volume-discretization-of-the-horizontal-pressure-gradient-force-beneath-sloping-ice-shelves)
#override MASS_WEIGHT_IN_PRESSURE_GRADIENT_TOP = True
#override RESET_INTXPA_INTEGRAL = True
#override RESET_INTXPA_INTEGRAL_FLATTEST = True
#override MASS_WEIGHT_IN_PGF_VANISHED_ONLY = True
#override HARMONIC_BL_SCALE = 1

! Recommended to fix remapping and initialisation (particularly if using sigma coords)
#override INIT_BOUNDARY_EXTRAP = True 
#override TRIMMING_USES_REMAPPING = True
#override TRIM_IC_Z_TOLERANCE = 1.0E-10
#override REMAPPING_USE_OM4_SUBCELLS = False 
#override Z_INIT_REMAP_GENERAL = True

! init ice shelf bugfix nonlineos
#override FRAC_DP_AT_POS_NEGATIVE_P_BUGFIX = True

! Add drag (can increases time before crashing but not always, depending on other parameters)
#override LINEAR_DRAG = True
#override DRAG_BG_VEL = 0.05

! Make sure DTBT is allowed to be small at the start of the run
#override DTBT_RESET_PERIOD = 0

! linear eqn of state freezing point dependence on pressure
#override DTFREEZE_DP = -7.75E-08  

! generates ocean_geometry file
#override WRITE_GEOM = 1

! other options (off unless required)
!!! #override PRESSURE_RECONSTRUCTION_SCHEME = 2 ! use a higher order pressure gradient vertical reconstruction scheme (more expensive)
!!! #override HARMONIC_VISC = True ! can be helpful if having problems near grounding line, but otherwise don't use it

```
In the above files, make sure to edit `ICE_THICKNESS_FILE` and `SURFACE_PRESSURE_FILE` to be your new ice file. The above is for `SIGMA_SHELF_ZSTAR` coordinates (ice draft following but can incrop at the bottom, and is zstar in open ocean), `SIGMA` (terrain-following) probably also works but `ZSTAR` has [known problems](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/5) beneath thermodynamically active ice shelves due to having vanished layers at the ice interface.

### 10. Layer run to get grounding line

For some reason, in my experience of this config, ALE mode requires no grounded ocean to initialise (i.e. ocean thickness always finite; it is odd since this is not requirement in idealised models). So, we initialise with layer mode to look at the output and determine where the cavity is grounded or not.
We add the following to `MOM_input` or `MOM_override_IS`, which we will remove later
```
!Turn on layer mode
#override USE_REGRIDDING = False
#override ENERGETICS_SFC_PBL = False
#override BULKMIXEDLAYER = True
#override MIXEDLAYER_RESTRAT = True
#override HMIX_MIN = 10.0
#override SAVE_INITIAL_CONDS = True
#override BULK_RI_ML = 0.05

```
Also replace the `TOPO_CONFIG` that we changed earlier back to `TOPO_CONFIG = "file"` and make sure the `TOPO_FILE` is for the whole continent (`topog_Charrassin_nocavity_cropped.nc`) and so is `ICE_THICKNESS_FILE` = `SURFACE_PRESSURE_FILE` = `ice_thickness_Charrassin_regridded_cropped_add_area.nc`

Run the model again with these parameters (`payu sweep` first). This should create a file `MOM_IC.nc` or several of them if the model is big. The model might run in layer mode but it also might crash! 

### 11. File making, again

Using the initialised model, we can now make topography files, ice files and nuopc mesh and runoff files without a grounding line, as done in [this notebook](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-draft/process-topo-8k-minimal-topoedited.ipynb). I haven't tested the sensitivity of parameters, but masking `MOM_IC.h.sum('Layer')>5` gives only floating ocean. Make sure to remove unconnected cells again. Save these new files, and then regenerate the nuopc coupler input using step 5 
> [!IMPORTANT]
> Use the sea ice topography when generating the nuopc mask!
> If you have a nonzero masking depth in `MOM_input`it might affect the mask, make sure the masks are all consistent. Sea ice coverage plus ice sheet coverage should exactly equal ocean coverage - you can check this with `ocean_geometry.nc` and `access-om3.cice.static.nc`

### 12. Run for real in ALE mode!
Update the file paths in your `MOM_input` to use these files with no grounding line, and remove the lines that say to use `layer` mode that we added in step 10. Might need to update the `config.yaml` to point to the new files.

Think carefully about the timestep as it's quite unstable from rest -- `DT=150` and `DT_THERM = 150` is usually pretty safe at the start with `nuopc.runseq` also having the coupling timestep which needs to be made the same time, and make sure `DT_BT_RESET_PERIOD` isn't hardcoded to be something large. Increasing the sea ice timestep ratio `ndtd` may also be helpful if you get sea ice errors.

While it is running, you can track the progress with 
```
tail -f work/log/ocn.log
```
And if it crashes `access-om3.err` will give the error message.

If you want to run month 2, you can increase the timestep as it should be more stable (monitor the maxCFL in the `ocn.log` file). To restart, you will also need to remove the `input_filename = 'n'` line in `input.nml`. See more run instructions [here](https://access-om3-configs.access-hive.org.au/pr-previews/573/configurations/pan-Antartic/run_panan_isf/) 

### 13. Other files
We also use tidal velocity files for the internal tide mixing and melt parameterisation - https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/claire_working/generate-draft/tidal_roughness_extrap.ipynb and extrapolate the roughness file outside the cavities southward down to the critical latitude. The file outside the cavity can be generated with [om3-scripts](https://access-om3-configs.access-hive.org.au/pr-previews/573/configurations/pan-Antartic/Detailedpananinstructions/)


### 14. Debugging

Common issues that get disguised by unhelpful MOM error messages like "saturation vapour pressure overflow" or "SSH beneath bathymetry" or "NaN in reproducing EPF overflow"
- NaNs in input files
- instabilities after intialisation - drop the timestep and try `HARMONIC_VISC = True` which should arrest flows into vanished layers
- have a look at the `ocean_geometry` file and `MOM_IC` files to check things are what you expected. Check the `work/INPUT` that the paths to the files is correct.
- check the masking coverage of ice/sea ice/ocean

Alternatively, you might have a [random segfault](https://github.com/ACCESS-NRI/access-om3-configs/issues/863) that goes away if you simply submit the job again.

<img width="474" height="360" alt="image" src="https://github.com/user-attachments/assets/2183b695-231b-4d9b-a0f3-6b22501a67ae" />

There are ongoing issues with the model config that require further development - see this list https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/49
