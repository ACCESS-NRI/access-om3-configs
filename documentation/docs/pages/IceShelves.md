## pan-Antarctic regional OM3 configuration

Here, we describe a regional OM3 configuration covering a pan-Antarctic circumpolar domain from Antarctica to 37 degrees South. This configuration inherits some of the development of the [MOM6-SIS2 COSIMA pan-Antarctic configurations](https://github.com/COSIMA/mom6-panan).

### Truncating a global setup
One of the easiest ways to set up a pan-Antarctic configuration is to truncate a global OM3 configuration. Detailed step-by-step instructions are provided [here](https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc2-sapphirerapid-Charrassin-newparams-rerun-Wright-spinup-accessom2IC-yr9/panantarctic_instructions.md) but the main steps involve 
1. cloning the global model at desired resolution, and creating a new branch
2. truncating netcdf files from the global model using `ncks` and ensuring buth supergrid and normal grid y coordinates are correct/match
3. Generating mesh files with [`om3-scripts`](https://github.com/ACCESS-NRI/om3-scripts) 
4. Modifying namelists to use the correct cropped netcdf files (searching by `.nc` is helpful) and changing the y index size to be correct. This involves changing `datm_in`, `MOM_input`, `ice_in` (where `history_chunksize`, `grid_type = "regional"` and `ns_boundary_type = "open"` are also needed), `nuopc.runconfig`.
5. Change `config.yaml` file names if needed, and ensure you are using a symmetric MOM6 memory exe
Open boundary conditions in MOM6 can be added using input from the MOM6-SIS2 COSIMA configuration, see [this notebook](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-obcs/ACCESS-OM2_panan_boundary_forcing_8km.ipynb) for the OBC generation using ACCESS-OM2-01 data. Extra lines need to be added into `MOM_input` to define these.
6. It may be helpful to use `MOM_override` to avoid changing `MOM_input` and pick up upstream global model changes more easily.

### 1/12th degree/4km pan-Antarctic setup
Here we describe the proposed ACCESS-NRI supported alpha 1/12th degree/4km pan-Antarctic regional OM3 configuration. The configuration has a similar resolution to a future 8km global OM3, but due to its polar latitudes is better described as a 4km resolution model. Here we focus on the configuration with ice shelf cavities closed (i.e. Antarctic ice shelf melt is represented as surface runoff, and there is no circulation in cavities), though development of an equivalent model with ice shelf cavities open is ongoing.

#### Grid
The grid was generated using the `ocean_grid_generator` at 1/12th degree resolution with no displaced pole and a transition from Mercator to fixed latitude cells at 75$^\circ$S.

#### Topography
Bottom topography is generated from [Charrassin et al. (2025)](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-obcs/ACCESS-OM2_panan_boundary_forcing_8km.ipynb) product, stitched to GEBCO 2024 where the Charrassin product is not available. The topography generation process required regridding from the Antarctic polar grid EPSG:3031 to latitude-longitude coordinates and is described [here](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-draft/Generate-Charrassin-bathy.ipynb) and [here](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-draft/process-topo.ipynb). Unfortunately, the normal OM3 topography generation workflow cannot be applied here so we manually set maximum and minimum depths, perform deseas to get rid of inland lakes, and create masks. These notebooks are also used for ice shelf configuration in development. Once these new topography and masks are generated, the nuopc mesh files also need to be generated with `om3-scripts`, as well as the bottom roughness and tidal amplitude. 

#### Initial Conditions and Boundary Conditions
Initial conditions were generated using a restart at the start of year 2 of an ACCESS-OM2-01 RYF90-91 configuration spun up from WOA13, as used in the COSIMA MOM6-SIS2 pan-Antarctic models, see [here](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/initial-conditions/ACCESSOM2_IC_into_8km_grid.ipynb). Boundary conditions use daily data from the second year of this run, see [here](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/generate-obcs/ACCESS-OM2_panan_boundary_forcing_8km.ipynb). Salt restoring is regridded from ACCESS-OM2-01, as in the COSIMA MOM6-SIS2 models, see [here](https://github.com/claireyung/mom6-panAn-iceshelf-tools/blob/main/initial-conditions/salt-restoring.ipynb).

#### Model parameters

MOM6 parameters are a combination of ACCESS-OM3 25km choices, MOM6-SIS2 COSIMA pan-Antarctic models and regional models from GFDL. We use a Wright equation of state, see [this issue](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/13), and higher resolution density coordinates (taken from MOM6-SIS2 COSIMA pan-Antarctic model). These parameter choices are found in [`MOM_override_newparams`]( https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc2-sapphirerapid-Charrassin-newparams-rerun-Wright-spinup-accessom2IC-yr9/MOM_override_newparams).

#### Model behaviour

The simulation is generally stable and is being evaluated [here](https://github.com/claireyung/mom6-panAn-iceshelf-tools/issues/15). Often the model crashes with a segfault immediately on initialisation, but persistent resubmission can get over this (a `resub.sh` [script](https://github.com/COSIMA/01deg_jra55_iaf/blob/01deg_jra55v140_iaf_cycle4_rerun_from_2002/resub.sh) can be helpful) 

## Optimization of pan-Antarctic configuration

### Timestepping
In this configuration, an ocean baroclinic timestep of 600s is used, with a relatively short thermodynamic timestep of 1200s. This is due to problems with the MOM6-SIS2 COSIMA pan-Antarctic broundary conditions if the tracer timestep is too long, [see](https://github.com/COSIMA/mom6-panan/issues/28). The behaviour of the boundary condition under different thermodynamic timesteps has not been explored in this configuration. 

The coupling timestep, set by `nuopc.runseq`, is 600, and `ndtd = 3` is set in `ice_in` to increase the CICE dynamic timestep and avoid CFL-related errors with ice dynamics. There are restrictions on ratios of timesteps for NUOPC and timesteps must divide into the restart time.

### IO

In this config, IO consumes a non-trivial amount of time. And most of the IO comes from MOM6
diagnostic and restart dumps. At this 8km resolution and if IO is serialized (i.e., performed by 1
CPU), **For every run, MOM6 IO can take around 20mins to dump the diagnostic and restart 
information**. Hence, a key optimization is to parallelize IO.

Because `AUTO_MASKTABLE = True` is being used in this config, we rely on changing number of CPUs 
allocated to MOM6 such that `NIPROC` and `NJPROC` (determined by MOM6 at runtime) share a common 
integer factor. As the procedure by which `NIPROC` and `NJPROC` isn't yet understood, finding the
correct number of CPUs is done by guess-and-check by running OM3 for 2 mins (i.e., try 1300 CPUs, 
check what MOM6 calculates `NIPROC/NJPROC` to be and if there isn't a common integer factor, keep 
trying). Once number of CPUs is chosen such that `NIPROC/NJPROC` has a common integer factor, then
set `AUTO_IO_LAYOUT_FAC = <common integer factor>` in MOM_input/MOM_override.

A challenge with this is that changing the cores allocated to MOM6, naturally also affects
computation time.

**The parallelization of diagnostic information reduced IO time by a few minutes**, but most of the time
gain is from paralellizing restart files. **Parallelizing restart can take off around 15mins** for this
config. However, `payu` is unable to understand parallel restarts and fails in its post-processing
of the MOM6 output. Hence, `PARALLEL_RESTARTFILES = False` until `payu` is updated with this
ability and the time gain isn't obtained.

If IO layout blocks are completely land covered along a given latitude or longitude, the combined 
netcdf output may contain non-sensible output (NaNs) along that coordinate. Therefore it is recommended
that IO blocks are large enough that there are ocean cells in every block. This may require explicit
setting of the `IO_LAYOUT`.


### OM3 Compiler flags

In this config, time is dominated by IO and MPI communications, so the effect of compiler flags can
be quite limited. Below discusses some the effects of some of the flags investigated with the `ifx`
compiler. Note that the **improvements reported are based on total time of a 5-day run, and doesn't
dilineate time spent in IO/MPI/compute/etc. **Note that changing compiler flags can result in bitwise
differing results.**

| Flag(s) | purpose | performance change |
| --- | --- | --- |
| `-march=sapphirerapids -mtune=sapphirerapids` | This compiles code specifically for Gadi's newest (at time of writing) hardware. Code cannot be run on Gadi's `normal` queue. | This gave a roughly 2.5% improvement |
| `-march=cascadelake -mtune=sapphirerapids` | Allows the code to run on Gadi's older Cascade Lake nodes (in the `normal` queue), but tries to optimize for the newer hardware. | Relative to no `march` or `mtune` flags, this improves runtime by roughly 1.5% |
| `-O3` | Increases the optimization level (default is `-O2`). When MPI is not involved, this can increase compute performance of MOM6 by 15% | 1% performance improvement |
| `-flto -fuse-ld=lld` | Enables link-time optimization (inter-procedural optimization). `-fuse-ld=lld` is not an optimization, but is needed for `ifx -flto` to work. | ~2% performance improvement |
| `-qopt-prefetch` | A flag to enable prefetching (can improve performance in some memory bound programs). | ~1.2% improvement |

Altogether, **these resulted in a ~5-6% improvement based on default flags. If not including IO,
the improvement is probably more like 6-7%**. These flags can be applied to all OM3 builds as well.

### CICE

A basic way to check time spent on CICE is to read the `ice.log` in the output logs. The [CICE docs](https://cice-consortium-cice.readthedocs.io/en/main/user_guide/ug_implementation.html#performance)
offer a few strategies to improve performance. The below config changes are controlled in the `ice_in`
file under the `domain_nml` section.

#### Block Size

Domain block size should be optimized such that there are roughly 6-7 blocks per process (`nx_global*ny_global/(block_size_x*block_size_y)`). In a config with 254 cores on CICE and
`nx_global = 4320, ny_global = 1440`, doubling block size in each direction from `block_size_x = 30, block_size_y = 27` resulted in 5-30% performance improvement, where 5 is for little-to-no ice, and
30% is when there is unrealistically high amounts of ice.

#### Process Distribution

Changing from `roundrobin` to `sectrobin` reduced CICE time by a flat 20s, regardless of ice level.
This is likely due to `sectrobin` having a slightly better way of organising processes to ensure
neighbours are closer.

### Runsequence

The nuopc run sequence (`nuopc.runseq`) can be modified so that components aren't unnecessarily waiting for eachother.
(I just copied a [run sequence from Minghang](https://github.com/ACCESS-NRI/access-om3-configs/pull/590), which improved runtime by about 8-9%).

## Aditional reading:

- 
- 

## References


