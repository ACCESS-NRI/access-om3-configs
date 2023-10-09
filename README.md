# MOM6-CICE6-datm-drof configurations for ACCESS-OM3

This repository contains several
[ACCESS-OM3](https://github.com/COSIMA/access-om3) configurations using the following components:

- [MOM6](https://github.com/mom-ocean/MOM6)
- [CICE](https://github.com/CICE-Consortium/CICE)
- [datm](https://github.com/ESCOMP/CDEPS) data model
- [drof](https://github.com/ESCOMP/CDEPS) data model

All the configurations use the [payu](https://github.com/payu-org/payu) workflow
management tool.


## Repository structure

Each configuration is stored as a git branch. Most of the branches are named
according to the following naming scheme:

`{nominal_resolution}deg_{forcing_data}_{forcing_method}`

Additional required information, like if the configuration includes
biogeochemistry, is appended to the name.

Currently the following configurations are available:

- [`1deg_jra55do_ryf`](https://github.com/COSIMA/MOM6-CICE6/tree/1deg_jra55do_ryf)

Note that the [`main`](https://github.com/COSIMA/MOM6-CICE6/tree/main) branch
does not store any configuration, only some documentation.

This repository also contains the following configurations that are only used
for testing ACCESS-OM3:

- [`gmom_jra`](https://github.com/COSIMA/MOM6-CICE6/tree/gmom_jra):
  configuration based on the `GMOM_JRA` [CESM](https://github.com/ESCOMP/CMEPS/)
  compset.

These configurations should **not** be used for production runs.


## Setting up an experiment

The first thing to do is to clone this repository. Although it is possible to
directly clone the repository from the [COSIMA
organization](https://github.com/COSIMA/), it is better to use a fork
instead. This will allow you to push any changes you make to the configuration,
as well as use the payu run log to keep track of your experiment in your fork on
GitHub. Detailed instructions about how to set up a fork can be found
[here](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

Once you have set up your fork, we recommend cloning to a directory with an
unique name that reflects what you wish to run. This could simply be the name of
the configuration you plan to run, but the more detailed the name is, the less
likely a namespace clash will happen.

Finally, one needs to checkout the branch corresponding to the desired
configuration.

Here is an step-by-step example of how to set up a `1deg_jra55do_ryf` experiment
after setting up your fork:

```bash
$ git clone git@github.com:<username>/MOM6-CICE6.git 1deg_jra55do_ryf
$ cd 1deg_jra55do_ryf
$ git checkout 1deg_jra55do_ryf
```

Here `<username>` should be your GitHub user name.

By default, the payu run log is turned off, but you probably want to turn this
on. To do so, one needs to edit the `config.yaml` file and change the following
line:

```yaml
runlog: false
```
to
```yaml
runlog: true
```
