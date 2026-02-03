# Optimisation

This documentation focuses on optimisation work that can be done through compiler flags and configuration settings without changing the ACCESS-OM3 source code. In practice, many of the largest performance differences between runs come from how the model is built and how work is distributed across components, rather than from changes to the model numerics themselves. The main areas covered here are compiler optimisation flags, and processor layout and load balancing across model components, including MOM6, CICE, the mediator (MED), and the data components (DATM and DROF).

All of the optimisation work described in this guide is driven by runtime evidence. We rely on ESMF tracing, using the ACCESS-NRI [`esmf-trace`](https://github.com/ACCESS-NRI/esmf-trace) repository, as the primary tool for understanding where time is actually spent during a run. Trace data provides a detailed breakdown of component-level timings, making it possible to see load imbalance, coupling wait times, and scaling limitations that are often hidden when looking only at overall wallclock performance.

To keep optimisation experiments consistent and reproducible, this documentation also describes a structured workflow built around,

 - [access-experiment-generator](https://github.com/ACCESS-NRI/access-experiment-generator)
 - [access-experiment-runner](https://github.com/ACCESS-NRI/access-experiment-runner)

These tools are used to generate controlled sets of configuration variants, run them in a consistent way, and collect comparable performance results with minimal manual effort. Combined with trace-based analysis, this approach makes it much easier to reproduce results, review optimisation choices, and build on previous work across different configurations and users.


## 1. Compiler flag workflow


## 2. Load balancing workflow

The following describes the workflow to generate a suite of simulations that enable load balancing to be completed. We'll take the 100km RYF configuration as an example.

### 2.1 Modules
To access [access-experiment-generator](https://github.com/ACCESS-NRI/access-experiment-generator) and [access-experiment-runner](https://github.com/ACCESS-NRI/access-experiment-runner), one needs to load `payu/dev` (not `payu` at the moment) on Gadi:

```
module purge
module use /g/data/vk83/prerelease/modules
module load payu/dev
```

### 2.2 Simulation suite


### Using the Experiment generator to create simulation suite 

At time of writing some changes to the config are not supported by [access-experiment-generator](http://github.com/accESS-NRI/access-experiment-generator). So we need to do small changes to the folowing to turn off `CICE` (we'll start by doing tests with `MOM6`):

 - `nuopc.runconfig`;
 - `nuopc.runseq`

Changes are detailed [here](https://github.com/minghangli-uni/access-om3-configs/commit/c7982c06ae8ae79f0d82fe59c52e9cef40b6eecb).

In this case, this is done a on a branch of a fork. Example for `dev-MC_100km_jra_ryf` branch, one creates a new branch based on `dev-MC_100km_jra_ryf` called `mom6_only_100kmprofiling`. Specifically, in `nuopc.runconfig`:
we remove `ICE` in this line `component_list: MED ATM ICE OCN ROF` ([example](https://github.com/chrisb13/access-om3-configs/commit/e3637a9bbb0f48deb560e6a542920f7156a69e8e)).

In `nuopc.runseq`, the following lines should be commented out ([example](https://github.com/chrisb13/access-om3-configs/commit/dd7971a31ee9f0061afd187fb9a4816d4e65e7f5)):

```fortran
  MED med_phases_prep_ice
  MED -> ICE :remapMethod=redist
  ICE

  MED med_phases_diag_ice_ice2med
  ICE -> MED :remapMethod=redist
  MED med_phases_post_ice

  MED med_phases_diag_ice_med2ice
```

We also make small modifications to the [config.yaml](https://github.com/chrisb13/access-om3-configs/commit/908df0da4970fd9128d79ec5b4c567948fe8123c), namely
```yaml
platform:
    nodesize: 104
    nodemem: 512
queue: normalsr
metadata:
  enable: true
```



We then create a `.yaml` file to set up the simulations, an example is worked through below (called `pr-mom6.yaml`), other applications should be hackable from this. 
```yaml
model_type: access-om3 # Specify the model ("access-om2", "access-om3", "access-esm1.5", or "access-esm1.6")
repository_url: git@github.com:chrisb13/access-om3-configs.git
start_point: "908df0da4970fd9128d79ec5b4c567948fe8123c" # Control commit hash for new branches
test_path: "." # All control and perturbation experiment repositories will be created here; can be relative, absolute or ~ (user-defined)
repository_directory: mom6_only # Local directory name for the central repository (user-defined)
control_branch_name: ctrl
Control_Experiment:
```
Note in the above, the `repository_url` specifies the fork and commit created earlier.

We then specify a suite of runs, here 50 `MOM6` standalone runs will be set up:
```yaml
Perturbation_Experiment:
  mom6_only:
    branches: ['mom6_1', 'mom6_2', 'mom6_3', 'mom6_4', 'mom6_5', 'mom6_6', 'mom6_7', 'mom6_8', 'mom6_9', 'mom6_10', 'mom6_11', 'mom6_12', 'mom6_13', 'mom6_14', 'mom6_15', 'mom6_16', 'mom6_17', 'mom6_18', 'mom6_19', 'mom6_20', 'mom6_21', 'mom6_22', 'mom6_23', 'mom6_24', 'mom6_25', 'mom6_26', 'mom6_27', 'mom6_28', 'mom6_29', 'mom6_30', 'mom6_31', 'mom6_32', 'mom6_33', 'mom6_34', 'mom6_35', 'mom6_36', 'mom6_37', 'mom6_38', 'mom6_39', 'mom6_40', 'mom6_41', 'mom6_42', 'mom6_43', 'mom6_44', 'mom6_45', 'mom6_46', 'mom6_47', 'mom6_48', 'mom6_49', 'mom6_50']

    MOM_input:
      AUTO_IO_LAYOUT_FAC: REMOVE
```

We also need to turn on various ESMF diagnostics to enable relevant profiling. By default `ESMF_RUNTIME_TRACE_PETLIST` will produce as many files as there are cores. Here `0` is output from NUOPC (related to choice of `atm_ntasks: &ntasks52 [52]`; discussed below) and `52` is the first ocean core (the most important for profiling purposes). `52` would go up depending on choice of `atm_ntasks`.
        
```yaml
    config.yaml:
      env:
        ESMF_RUNTIME_PROFILE: "on"
        ESMF_RUNTIME_TRACE: "on"
        ESMF_RUNTIME_TRACE_PETLIST: "0 52"
        ESMF_RUNTIME_PROFILE_OUTPUT: "SUMMARY"
```

Here in `ncpus` we specify the total number of cpus to be allocated, this effectively determines the number of cores available to `MOM6` where the `MOM6` cores are `atm_ntasks + oce_ntasks = ncpus` (see below for where `ocn_ntasks` is set). Details of how to calculate `ncpus` and `mem` below:
```yaml
      ncpus: [65, 117, 169, 221, 273, 325, 377, 429, 481, 533, 585, 637, 689, 741, 793, 845, 897, 949, 1001, 1053, 1105, 1157, 1209, 1261, 1313, 1365, 1417, 1469, 1521, 1573, 1625, 1677, 1729, 1781, 1833, 1885, 1937, 1989, 2041, 2093, 2145, 2197, 2249, 2301, 2353, 2405, 2457, 2509, 2561, 2613]

      mem: ['500GB', '1000GB', '1000GB', '1500GB', '1500GB', '2000GB', '2000GB', '2500GB', '2500GB', '3000GB', '3000GB', '3500GB', '3500GB', '4000GB', '4000GB', '4500GB', '4500GB', '5000GB', '5000GB', '5500GB', '5500GB', '6000GB', '6000GB', '6500GB', '6500GB', '7000GB', '7000GB', '7500GB', '7500GB', '8000GB', '8000GB', '8500GB', '8500GB', '9000GB', '9000GB', '9500GB', '9500GB', '10000GB', '10000GB', '10500GB', '10500GB', '11000GB', '11000GB', '11500GB', '11500GB', '12000GB', '12000GB', '12500GB', '12500GB', '13000GB']

      repeat: True

    nuopc.runconfig:
      PELAYOUT_attributes:
        atm_ntasks: &ntasks52 [52]
        cpl_ntasks: *ntasks52
        ice_ntasks: REMOVE
        ice_nthreads: REMOVE
        ice_pestride: REMOVE
        ice_rootpe: REMOVE
        ocn_ntasks: [13, 65, 117, 169, 221, 273, 325, 377, 429, 481, 533, 585, 637, 689, 741, 793, 845, 897, 949, 1001, 1053, 1105, 1157, 1209, 1261, 1313, 1365, 1417, 1469, 1521, 1573, 1625, 1677, 1729, 1781, 1833, 1885, 1937, 1989, 2041, 2093, 2145, 2197, 2249, 2301, 2353, 2405, 2457, 2509, 2561]
        ocn_rootpe: *ntasks52
        rof_ntasks: *ntasks52
```
We will be doing `3` run of each (`150` runs total) so we set `repeat` to `True`.

For defining the `ocn_ntasks` we want to increase the number of cores by `atm_ntasks` in each run. This python snippet can generate it for us: `print([13+(k*52) for k in range(50)])`. For higher resolution configurations, one would normally start at a higher number (e.g. for global 25km we would start at `52`). Hence, we can set `ncpus` using this python snippet: `print([13+(k*52)+52 for k in range(50)])`. The `mem` is determined by how many nodes are in use, each node contains 104 cores and has `500GB` of memory available. Finally, we can find `mem` with: `import math;nodenumber=[math.ceil((13+(k*52)+52) /104) for k in range(50)];print([str(n*500)+'GB' for n in nodenumber])`. In the previous snippets, when adjusting for your configuration you'll want to change `13` to the starting point that you prefer.

The following sets the run length at two days and the ice parameters are for turning off `CICE`.
```yaml
      CLOCK_attributes:
        restart_n: 2
        restart_option: ndays
        stop_n: 2
        stop_option: ndays

      ALLCOMP_attributes:
        ICE_model: sice

      ICE_attributes: REMOVE
      ICE_modelio: REMOVE
```

We can then take the above yaml (`pr-mom6.yaml`) and pass it to [access-experiment-generator](http://github.com/accESS-NRI/access-experiment-generator):
```bash
module purge
module use /g/data/vk83/prerelease/modules
module load payu/dev
module list
mkdir -p /g/data/tm70/$USER/access-om3-ptests
experiment-generator -i pr-mom6.yaml
```
This will take a while with output that looks like:

```bash
[cyb561@gadi-login-03 access-om3-ptests]$ experiment-generator -i pr-mom6.yaml 
-- Test directory . already exists!
Cloned repository from git@github.com:chrisb13/access-om3-configs.git to directory: /g/data/tm70/cyb561/access-om3-ptests/mom6_only
Created and checked out new branch: ctrl
laboratory path:  /scratch/tm70/cyb561/access-om3
binary path:  /scratch/tm70/cyb561/access-om3/bin
input path:  /scratch/tm70/cyb561/access-om3/input
work path:  /scratch/tm70/cyb561/access-om3/work
archive path:  /scratch/tm70/cyb561/access-om3/archive
Metadata and UUID generation is disabled. Experiment name used for archival: mom6_only
To change directory to control directory run:
  cd /g/data/tm70/cyb561/access-om3-ptests/mom6_only
-- Creating branch mom6_1 from ctrl!
Created and checked out new branch: mom6_1
laboratory path:  /scratch/tm70/cyb561/access-om3
binary path:  /scratch/tm70/cyb561/access-om3/bin
input path:  /scratch/tm70/cyb561/access-om3/input
work path:  /scratch/tm70/cyb561/access-om3/work
archive path:  /scratch/tm70/cyb561/access-om3/archive
Metadata and UUID generation is disabled. Experiment name used for archival: mom6_only
Updated perturbation files: ['config.yaml', 'nuopc.runconfig']
...
```

This should create a folder structure that looks like:
```bash
[cyb561@gadi-login-03 access-om3-ptests]$ tree mom6_only/
mom6_only/
├── config.yaml
├── datm_in
├── datm.streams.xml
├── diagnostic_profiles
│   ├── diag_table_standard
│   ├── README.md
│   └── source_yaml_files
│       └── diag_table_standard_source.yaml
├── diag_table -> diagnostic_profiles/diag_table_standard
├── docs
│   ├── available_diags.000000
│   ├── MOM_parameter_doc.all
│   ├── MOM_parameter_doc.debugging
│   ├── MOM_parameter_doc.layout
│   └── MOM_parameter_doc.short
├── drof_in
├── drof.streams.xml
├── drv_in
├── fd.yaml
├── ice_in
├── input.nml
├── LICENSE
├── manifests
│   ├── exe.yaml
│   ├── input.yaml
│   └── restart.yaml
├── MOM_input
├── MOM_override
├── nuopc.runconfig
├── nuopc.runseq
├── README.md
└── testing
    └── checksum
        ├── historical-6hr-checksum.json
        └── test_report.xml
```
Within the `mom6_only` folder is a git repository where each branch corresponds to a new simulation.

### Using the Experiment runner to run the load balancing tests

We now have to write another .yaml file (example here called `runner_pr-mom6.yaml`) so we can use [access-experiment-runner](http://github.com/accESS-NRI/access-experiment-runner) to run the experiments we generated in the previous section.

`runner_pr-mom6.yaml` looks like:
```bash
/g/data/tm70/cyb561/access-om3-ptests

test_path: /g/data/tm70/cyb561/access-om3-ptests # All control and perturbation experiment repositories.
repository_directory: mom6_only # Local directory name for the central repository, where the running_branches are forked from.
keep_uuid: True
# ================= 1 =================
# # 1. check different density coordinates (NUM_DIAG_COORDS = 1, 2)
running_branches: ['mom6_1', 'mom6_2', 'mom6_3', 'mom6_4', 'mom6_5', 'mom6_6', 'mom6_7', 'mom6_8', 'mom6_9', 'mom6_10', 'mom6_11', 'mom6_12', 'mom6_13', 'mom6_14', 'mom6_15', 'mom6_16', 'mom6_17', 'mom6_18', 'mom6_19', 'mom6_20', 'mom6_21', 'mom6_22', 'mom6_23', 'mom6_24', 'mom6_25', 'mom6_26', 'mom6_27', 'mom6_28', 'mom6_29', 'mom6_30', 'mom6_31', 'mom6_32', 'mom6_33', 'mom6_34', 'mom6_35', 'mom6_36', 'mom6_37', 'mom6_38', 'mom6_39', 'mom6_40', 'mom6_41', 'mom6_42', 'mom6_43', 'mom6_44', 'mom6_45', 'mom6_46', 'mom6_47', 'mom6_48', 'mom6_49', 'mom6_50']

nruns: [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]


startfrom_restart: ['cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold', 'cold']
```

We then run the following commands:
```bash
module purge
module use /g/data/vk83/prerelease/modules
module load payu/dev
module list
cd /g/data/tm70/$USER/access-om3-ptests
experiment-runner -i runner_pr-mom6.yaml
```


