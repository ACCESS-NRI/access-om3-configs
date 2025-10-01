# Optimisation

## Load balancing

The following describes the workflow to generate a suite of simulations that enable load balancing to be completed. We use the folowing tools: [access-experiment-generator](http://github.com/accESS-NRI/access-experiment-generator) and [access-experiment-runner](http://github.com/accESS-NRI/access-experiment-runner)

To access these python modules, one needs to on Gadi: `module purge;module use /g/data/vk83/prerelease/modules; module load payu/dev;module list`. Documentation for the experiment generator [is available here](https://access-experiment-generator.access-hive.org.au/).

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

We then create two `.yaml` files to set up and run the somulations, two examples are given below, other applications should be hackable from these:

 - `pr-mom6.yaml`;
 - `runner_pr-mom6.yaml`.

Firstly `pr-mom6.yaml`.

Note in the following the `repository_url` specifies the fork and commit created above:
```yaml
model_type: access-om3 # Specify the model ("access-om2", "access-om3", "access-esm1.5", or "access-esm1.6")
repository_url: git@github.com:chrisb13/access-om3-configs.git
start_point: "dd7971a31ee9f0061afd187fb9a4816d4e65e7f5" # Control commit hash for new branches
test_path: "." # All control and perturbation experiment repositories will be created here; can be relative, absolute or ~ (user-defined)
repository_directory: mom6_only # Local directory name for the central repository (user-defined)
control_branch_name: ctrl
Control_Experiment:
```

We then specify a suite of runs, here 50 `MOM6` standalone runs will be set up:
```yaml
Perturbation_Experiment:
  Parameter_block_cice_cores:
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

Here in `ncpus` we specify the total number of cpus to be allocated, this effectively determines the number of cores available to `MOM6` where the `MOM6` cores are `atm_ntasks + oce_ntasks = ncpus` (see below for where `ocn_ntasks` is set):
```yaml
      ncpus: [104, 156, 208, 260, 312, 364, 416, 468, 520, 572, 624, 676, 728, 780, 832, 884, 936, 988, 1040, 1092, 1144, 1196, 1248, 1300, 1352, 1404, 1456, 1508, 1560, 1612, 1664, 1716, 1768, 1820, 1872, 1924, 1976, 2028, 2080, 2132, 2184, 2236, 2288, 2340, 2392, 2444, 2496, 2548, 2600, 2652]

      mem: ['500GB', '1000GB', '1000GB', '1500GB', '1500GB', '2000GB', '2000GB', '2500GB', '2500GB', '3000GB', '3000GB', '3500GB', '3500GB', '4000GB', '4000GB', '4500GB', '4500GB', '5000GB', '5000GB', '5500GB', '5500GB', '6000GB', '6000GB', '6500GB', '6500GB', '7000GB', '7000GB', '7500GB', '7500GB', '8000GB', '8000GB', '8500GB', '8500GB', '9000GB', '9000GB', '9500GB', '9500GB', '10000GB', '10000GB', '10500GB', '10500GB', '11000GB', '11000GB', '11500GB', '11500GB', '12000GB', '12000GB', '12500GB', '12500GB', '13000GB']

      repeat: True
```
We will be doing `3` run of each (`150` runs total) so we set `repeat` to `True`.

For defining the `ocn_ntasks` we want to increase the number of cores by `atm_ntasks` in each run. This python snippet can generate it for us: `print([13+(k*52) for k in range(50)])`

```yaml
    nuopc.runconfig:
      PELAYOUT_attributes:
        atm_ntasks: &ntasks52 [52]
        cpl_ntasks: *ntasks52
        ice_ntasks: REMOVE
        ice_nthreads: REMOVE
        ice_pestride: REMOVE
        ice_rootpe: REMOVE
        ocn_ntasks: [52, 104, 156, 208, 260, 312, 364, 416, 468, 520, 572, 624, 676, 728, 780, 832, 884, 936, 988, 1040, 1092, 1144, 1196, 1248, 1300, 1352, 1404, 1456, 1508, 1560, 1612, 1664, 1716, 1768, 1820, 1872, 1924, 1976, 2028, 2080, 2132, 2184, 2236, 2288, 2340, 2392, 2444, 2496, 2548, 2600]
        ocn_rootpe: *ntasks52
        rof_ntasks: *ntasks52

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



respectively in `/g/data/tm70/$USER/ptests_om3/`

each node contains 104 cores

ncpus: [13+52, 



atm_ntasks [52]

ncn_ntasks
13,26,52




### Using the Experiment runner to run the load balancing tests


`experiment-runner -i runner_pr-mom6.yaml`

