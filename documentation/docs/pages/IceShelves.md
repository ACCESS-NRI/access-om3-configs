## Horizontal grid



### File formats


## Vertical grid

## Optimization

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


