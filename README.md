# MOM6-CICE6-datm-drof configurations for ACCESS-OM3

This repository contains several
[ACCESS-OM3](https://github.com/COSIMA/access-om3) configurations using the
following components:

- [MOM6](https://mom6.readthedocs.io/) ocean model
- [CICE](https://github.com/CICE-Consortium/CICE) sea ice model
- [DATM](https://escomp.github.io/CDEPS/versions/master/html/datm.html) atmosphere data model
- [DROF](https://escomp.github.io/CDEPS/versions/master/html/drof.html) runoff data model

All the configurations use the [payu](https://payu.readthedocs.io/en/latest/)
workflow management tool.


## Repository structure

Each configuration is stored as a git branch. Most of the branches are named
according to the following naming scheme:

`{nominal_resolution}deg_{forcing_data}_{forcing_method}`

Additional required information, like if the configuration includes
biogeochemistry, is appended to the name.

Currently the following configurations are available:

- [`1deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/1deg_jra55do_ryf)
- [`1deg_jra55do_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/1deg_jra55do_iaf)
- [`1deg_jra55do_ryf_wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/tree/1deg_jra55do_ryf_wombatlite)
- [`025deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/025deg_jra55do_ryf)

**Note that the [`main`](https://github.com/ACCESS-NRI/access-om3-configs/tree/main) branch
does not store any configuration, only some documentation.**

This repository also contains the following configurations that are only used
for testing ACCESS-OM3:

- [`gmom_jra`](https://github.com/ACCESS-NRI/access-om3-configs/tree/gmom_jra):
  configuration based on the `GMOM_JRA` [CESM](https://github.com/ESCOMP/CMEPS/)
  compset.

These configurations should **not** be used for production runs.


## Comparison table

- [`1deg_jra55do_ryf`➡️`1deg_jra55do_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/1deg_jra55do_ryf..1deg_jra55do_iaf)
- [`1deg_jra55do_ryf`➡️`1deg_jra55do_ryf_wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/compare/1deg_jra55do_ryf..1deg_jra55do_ryf_wombatlite)
- [`1deg_jra55do_ryf`➡️`025deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/1deg_jra55do_ryf..025deg_jra55do_ryf)
- [`1deg_jra55do_iaf`➡️`1deg_jra55do_ryf_wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/compare/1deg_jra55do_iaf..1deg_jra55do_ryf_wombatlite)
- [`1deg_jra55do_iaf`➡️`025deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/1deg_jra55do_iaf..025deg_jra55do_ryf)
- [`1deg_jra55do_ryf_wombatlite`➡️`025deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/1deg_jra55do_ryf_wombatlite..025deg_jra55do_ryf)

## Setting up an experiment

The first thing to do is to clone this repository. Although it is possible to
directly clone the repository from the [COSIMA
organization](https://github.com/COSIMA/), it is better to use a fork
instead. This will allow you to push any changes you make to the configuration,
as well as use the payu run log to keep track of your experiment in your fork on
GitHub. Detailed instructions about how to set up a fork can be found
[here](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

Once you have set up your fork, we recommend cloning to a directory with a
unique name that reflects what you wish to run. This could simply be the name of
the configuration you plan to run, but the more detailed the name is, the less
likely a namespace clash will happen.

Finally, one needs to checkout the branch corresponding to the desired
configuration. It is then good practice to start a new branch with the same name
as your directory so you can use git to easily see how your run configuration
differs from the original.

Here is an step-by-step example of how to set up a `1deg_jra55do_ryf` experiment
(called `my_1deg_jra55do_ryf_experiment_name`) after setting up your fork:

```bash
$ git clone git@github.com:<username>/access-om3-configs.git my_1deg_jra55do_ryf_experiment_name
$ cd my_1deg_jra55do_ryf_experiment_name
$ git checkout 1deg_jra55do_ryf
$ git checkout -b my_1deg_jra55do_ryf_experiment_name
```

Here `<username>` should be your GitHub user name.

By default, the payu run log is turned off, but you should turn it on so that
your configuration settings will be recorded as the run proceeds. Simply edit
the `config.yaml` file and change the following line:

```yaml
runlog: false
```
to
```yaml
runlog: true
```


## Customising your experiment

See [this section of the quick start instructions in the ACCESS-OM3
wiki](https://github.com/COSIMA/access-om3/wiki/Quick-start#customising-your-experiment).


## Running your experiment

See [this section of the quick start instructions in the ACCESS-OM3
wiki](https://github.com/COSIMA/access-om3/wiki/Quick-start#running).


## Pull requests

We welcome contributions from users of these configurations. If you make a
configuration improvement which you think should be included in the COSIMA
repository, push it to your fork and then do a pull request from the relevant
branch in your fork to the branch it originated from in the COSIMA repository
(not `main`).
