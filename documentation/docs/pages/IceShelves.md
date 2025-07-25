## Horizontal grid

Random content below, hack away!

### File formats


## Vertical grid

## Optimization

### IO

In this config, IO consumes a non-trivial amount of time. And most of the IO comes from MOM6
diagnostic and restart dumps. At this 8km resolution and if IO is serialized (i.e., performed by 1
CPU), **MOM6 IO can take around 20mins to dump the diagnostic and restart information**. Hence, a 
key optimization is to parallelize IO.

Because `AUTO_MASKTABLE = True` is being used in this config, we rely on changing number of CPUs 
allocated to MOM6 such that `NIPROC` and `NJPROC` (determined by MOM6 at runtime) share a common 
integer factor. As the procedure by which `NIPROC` and `NJPROC` isn't yet understood, finding the
correct number of CPUs is done by guess-and-check by running OM3 for 2 mins (i.e., try 1300 CPUs, 
check what MOM6 calculates `NIPROC/NJPROC` to be and if there isn't a common integer factor, keep 
trying). Once number of CPUs is chosen such that `NIPROC/NJPROC` has a common integer factor, then
set `AUTO_IO_LAYOUT_FAC = <common integer factor>` in MOM_input/MOM_override.

**The parallelization of diagnostic information reduced IO time by a few minutes**, but most of the time
gain is from paralellizing restart files. **Parallelizing restart can take off around 15mins** for this
config. However, `payu` is unable to understand parallel restarts and fails in its post-processing
of the MOM6 output. Hence, `PARALLEL_RESTARTFILES = False` until `payu` is updated with this
ability and the time gain isn't obtained.

## Aditional reading:

- 
- 

## References


