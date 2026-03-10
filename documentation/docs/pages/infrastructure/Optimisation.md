# Optimisation

This documentation focuses on optimisation work that can be achieved without changing the ACCESS-OM3 source code. For a fixed model configuration and resolution, performance differences between runs are typically driven by build choices and processor layout rather than changes to the model source itself. This includes load balancing across components such as MOM6, CICE, the mediator (MED), and the data components (DATM and DROF), as well as build-time compiler settings.

All of the optimisation work described in this guide is driven by runtime evidence. We rely on ESMF tracing, using the ACCESS-NRI [`esmf-trace`](https://github.com/ACCESS-NRI/esmf-trace) repository, as the primary tool for understanding where time is actually spent during a run. Trace data provides a detailed breakdown of component-level timings, making it possible to see load imbalance, coupling wait times, and scaling limitations that are often hidden when looking only at overall wallclock performance.

To keep experiments consistent and reproducible, this documentation also outlines a structured *ACCESS-style* workflow built around the following tools,

 - [access-experiment-generator](https://github.com/ACCESS-NRI/access-experiment-generator)
 - [access-experiment-runner](https://github.com/ACCESS-NRI/access-experiment-runner)
 - [access-profiling](https://github.com/ACCESS-NRI/access-profiling)
 - [access-config-utils](https://github.com/ACCESS-NRI/access-config-utils)

!!! note 
    These packages are **not** runtime requirements of [`esmf-trace`](https://github.com/ACCESS-NRI/esmf-trace). Instead they define a curated working environment that supports controlled profiling studies. They are used to generate systematic configuration variants, run them in a consistent manner, and collect comparable performance results with minimal manual effort. Combined with trace-based analysis, this workflow makes it easier to reproduce results, review optimisation decisions, and build on previous work across configurations and users.

## 1. Installation and Setup

Within the [`esmf-trace`](https://github.com/ACCESS-NRI/esmf-trace) repository, a `setup_gadi.sh` script is provided to simplify installation on Gadi, NCI,

```bash
./setup_gadi.sh
```
On Gadi, this setup relies on a pre-deployed version of [`babeltrace2`](https://babeltrace.org/#bt2-get), which is required to read CTF (common trace format) traces and convert them into human-readable formats such as `.json`. The deployment is managed through the ACCESS-NRI [model-tools](https://github.com/ACCESS-NRI/model-tools) using Spack, with the corresponding spack package recipe maintained under Spack build-in [babeltrace2](https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/babeltrace2/package.py) package.

The module can be loaded directly with,

```bash
module use /g/data/vk83/modules
module load model-tools/babeltrace2/2.1.2
```
which is already handled inside `setup_gadi.sh`.

!!! note
    As of 26 Feb 2026, there's a known issue related to a CPU `target` mismatch that prevents use via [ARE](http://are.nci.org.au/) on Gadi. The tool currently works on login nodes. Since `esmf-trace` does not do heavy computation, running it on a login node is acceptable until the issue is resolved. More details can be found in [model-tools#20](https://github.com/ACCESS-NRI/model-tools/pull/20) and in a Zulip discussion [Deploy babeltrace2 targeting x86_64 or x86_64_v3](https://access-nri.zulipchat.com/#narrow/channel/470325-model-release/topic/Deploy.20babeltrace2.20targeting.20x86_64.20or.20x86_64_v3/with/573172880). The release team is keen to address it once they have capacity.

For use within a VS Code Jupyter kernel on Gadi, setup instructions are available in the [documentation](https://esmf-trace.readthedocs.io/latest/vscode_jupyter_kernel).


## 2. Workflow demonstration - processor layout

### 2.1 Overview

In this section, we demonstrate how processor layout profiling is carried out using the structured workflow described above based on the 25km configuration. The aim is to show how different component layouts influence runtime behaviour and overall performance. Using trace-driven analysis, we systematically generate and evaluate alternative processor splits, examine load balance across components, and identify where coupling or wait times limit scaling. This example provides a concrete example of how layout decisions can be guided by runtime evidence rather than trial and error.

### 2.2 Practical constraints

For the 25km configuration, walltime can reach up to 6 hours per run (see [access-om3-configs#334](https://github.com/ACCESS-NRI/access-om3-configs/issues/334#issuecomment-2750085308)). In a recent [25km release](https://github.com/ACCESS-NRI/access-om3-configs/releases#:~:text=Expected%20Performance), expected performance has improved to approximately 3 hours with a cost of around 17 kSU. Even at this improved level, running multiple full test cases to evaluate performance remains time-consuming and computationally expensive. This challenge becomes more pronounced at higher resolutions - the global 8km configuration.

### 2.3 Profiling strategy

`esmf-trace`, however, provides a practical alternative. By extracting detailed timing samples over a short integration window, it allows statistical analysis of runtime behaviour without requiring full-length simulations. In climate modelling, seasonal variability must also be considered, as sea ice can contribute substantially more computational load in winter than in summer. One approach is to restart from a season with active ice growth and perform similar profiling.

For demonstration purposes, the following analysis uses a 10-model-day period from a "cold" start. Since the [initial sea ice state is none](https://access-om3-configs.access-hive.org.au/configurations/MC_25km/#cice-namelist:~:text=When%20there%20is,of%20sea%20ice.), this setup does not fully represent performance under developed ice conditions. However further profiling experiments indicate that processor layout conclusions derived from the cold start remain broadly valid at the annual scale.

### 2.4 Real workflow

A complete example notebook is available [here](https://github.com/minghangli-uni/sandbox/blob/master/scalings/access_om3_25km_scaling_access-profiling_esmf-trace.ipynb). This section provides the necessary background and walks through the workflow demonstrated in that notebook.

#### 2.4.1 Experiment generator -> Generate experiments

[access-experiment-generator](https://github.com/ACCESS-NRI/access-experiment-generator) is used to create ensembles of experiments from a single control configuration. It operates from a structured input file, written either in yaml or as a Python dictionary. Below is a yaml example - additional examples are available in the [repository examples/ directory](https://github.com/ACCESS-NRI/access-experiment-generator/tree/main/examples).

The configuration yaml file is located at: `/path/to/experiment_generator.yaml`. A minimal setup looks like,

```yaml
model_type: access-om3 # available models can be checked via `payu list` -> Supported models: access access-esm1.6 access-om2 access-om3 cice cice5 gold yatm mitgcm mom nemo oasis roms test um ww3 mom6 qgcm cable staged_cable default model
repository_url: https://github.com/ACCESS-NRI/access-om3-configs.git
start_point: "b0eddf9" # Control commit hash for new branches
test_path: /g/data/tm70/ml0072/COMMON/git_repos/access-experiment-generator/performance_runnings_ncmas/new_workflow/om3_scalings # All control and perturbation experiment repositories will be created here; can be relative, absolute or ~ (user-defined)
repository_directory: Scaling_MC-25km-ryf-10days # Local directory name for the central repository (user-defined)
```

Two top-level sections are then required: `Control_Experiment` and `Perturbation_Experiment`. 

- For `Control_Experiment`, the structure mirrors the layout of the configuration files being modified. For example, to enable `metadata` in `config.yaml`,

```yaml
Control_Experiment:
  config.yaml:
    metadata:
      enable: true
```
The key names follow the file structure directly.

- For `Perturbation_Experiment`, it defines changes relative to the control. Experiments inherit all control settings, and modifications are grouped under named paramter blocks (e.g. `Parameter_block1`). For example to set both runlength and restart interval to 10 model days in `nuopc.runconfig`,

```yaml
Perturbation_Experiment:
  Parameter_block1:
    branches:
      - perturb_1

    nuopc.runconfig:
      CLOCK_attributes:
        restart_n: 10
        restart_option: ndays
        stop_n: 10
        stop_option: ndays
```
Here, `branches` defines the new experiment branch names and the configuration structure under `nuopc.runconfig` matches the original file hierachy.

Once the yaml file is prepared, experiments can be generated with,

```bash
experiment-generator -i /path/to/experiment_generator.yaml
```

This creates a repository at `$test_path / $repository_directory`. Within that repository, the generated branches can be inspected,

```bash
$ git branch
  main
  ctrl
  perturb_1
```

#### 2.4.2 Experiment runner -> Execute experiments



#### 2.4.3 ACCESS-style workflow

Coming back to the ACCESS-style workflow from the notebook,

```python
repository_url = "https://github.com/ACCESS-NRI/access-om3-configs.git"
start_point = "b0eddf9"
test_path = Path("/g/data/tm70/ml0072/COMMON/git_repos/access-experiment-generator/performance_runnings_ncmas/new_workflow/om3_scalings")
repository_directory = "Scaling_MC-25km-ryf-10days"
branch_name_prefix = "MC-25km-ryf-10days"
```


1. First import relevant modules. 
```python
from pathlib import Path
import numpy as np
from access.profiling.access_models import ACCESSOM3Profiling
from access.config.accessom3_layout_input import OM3LayoutSearchConfig, generate_om3_core_layouts_from_node_count, quote_env_for_yaml
```

2. Experiment generation

3. 
