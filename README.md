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

Currently the following development configurations are available:

- [`dev-1deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-1deg_jra55do_ryf)
- [`dev-1deg_jra55do_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-1deg_jra55do_iaf)
- [`dev-1deg_jra55do_ryf_wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-1deg_jra55do_ryf_wombatlite)
- [`dev-025deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-025deg_jra55do_ryf)

**Note that the [`main`](https://github.com/ACCESS-NRI/access-om3-configs/tree/main) branch
does not store any configuration, only some documentation.**

This repository also contains the following configurations that are only used
for testing ACCESS-OM3:

- [`gmom_jra`](https://github.com/ACCESS-NRI/access-om3-configs/tree/gmom_jra):
  configuration based on the `GMOM_JRA` [CESM](https://github.com/ESCOMP/CMEPS/)
  compset.

These configurations should **not** be used for production runs.

## Comparison table

- [`dev-1deg_jra55do_ryf`➡️`dev-1deg_jra55do_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-1deg_jra55do_ryf..dev-1deg_jra55do_iaf)
- [`dev-1deg_jra55do_ryf`➡️`dev-1deg_jra55do_ryf_wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-1deg_jra55do_ryf..dev-1deg_jra55do_ryf_wombatlite)
- [`dev-1deg_jra55do_ryf`➡️`dev-025deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-1deg_jra55do_ryf..dev-025deg_jra55do_ryf)
- [`dev-1deg_jra55do_iaf`➡️`dev-1deg_jra55do_ryf_wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-1deg_jra55do_iaf..dev-1deg_jra55do_ryf_wombatlite)
- [`dev-1deg_jra55do_iaf`➡️`dev-025deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-1deg_jra55do_iaf..dev-025deg_jra55do_ryf)
- [`dev-1deg_jra55do_ryf_wombatlite`➡️`dev-025deg_jra55do_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-1deg_jra55do_ryf_wombatlite..dev-025deg_jra55do_ryf)

## Setting up an experiment

The first thing to do is to clone this repository. Although it is possible to
directly clone the repository from  [ACCESS-NRI/access-om3-configs](https://github.com/ACCESS-NRI/access-om3-configs), it is better to use a fork
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
git clone git@github.com:<username>/access-om3-configs.git my_1deg_jra55do_ryf_experiment_name
cd my_1deg_jra55do_ryf_experiment_name
git checkout 1deg_jra55do_ryf
git checkout -b my_1deg_jra55do_ryf_experiment_name
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
configuration improvement which you think should be included in the [ACCESS-NRI/access-om3-configs](https://github.com/ACCESS-NRI/access-om3-configs)
repository, push it to your fork and then do a pull request from the relevant
branch in your fork to the branch it originated from in [ACCESS-NRI/access-om3-configs](https://github.com/ACCESS-NRI/access-om3-configs)
(not `main`).

## Configuration CI

### PR Repro CI

This Pipeline compares configurations modified in a PR (the `source` branch) against a 'ground truth' checksum, usually the `target` branch. It also verifies that commons mistakes in configurations are not made. This allows developers to know if the changes they are about to commit lead to valid and reproducible results. Either way, if the PR is merged, the new commit is tagged in such a way that we know how reproducible it is against past configurations.

### User-Dispatchable Repro-CI Workflow

This repository contains a user-dispatchable workflow (minimum `Write` role required) for the generation of reproducibility checksums on a given Config Branch. The workflow requires sign off from [@ACCESS-NRI/ocean](https://github.com/orgs/ACCESS-NRI/teams/ocean) to run on Gadi.

Workflow inputs :

| Input | Type | Required | Default | Description | Example | Notes |
| ----- | ---- | -------- | ------- | ----------- | ------- | ----- |
| `config-branch-name` | `string` | `true` | N/A | The configuration branch that will be run that will generate the checksums | `dev-025deg_jra55do_ryf` | This can be any branch - not just `release` or `dev` branches |
| `commit-checksums` | `boolean` | `true` | `false` | Whether to commit the checksums to the target branch once generated | `true` | If unchecked, the checksums are still accessible as a workflow run artifact |
| `committed-checksum-location` | `string` | `false` | `./testing/checksum` | If checksums are being committed: Where in the repository the generated checksums should be committed | `./some/dir` | Requires the path starting with `.` |
| `committed-checksum-tag-version` | `string` | `false` | N/A | If checksums are being committed: An optional initial version for the committed checksums as a `git tag` of the form `{config-branch-name}-{version}` | `1.0` | If left blank, no tag will be added |

### Configuring the CI: `config/ci.json`

This is the `config/ci.json` configuration file for specifying different test markers, or test versions based on type of the test to run, and the name of the git branch or tag. The different types of test are defined as:

- `scheduled`: Scheduled monthly reproducibility tests. The keys under these tests represent released config tags to run scheduled checks on.
- `reproducibility`: Reproducibility tests that are run as part of pull requests. The keys under these tests represent the target branches into which pull requests are being merged.
- `qa` - Quick quality assurance tests that are run as part of pull requests. The keys under these tests represent the target branches into which pull requests are being merged.

The configuration properties needed to run the tests are:

| Name | Type | Description |  Example |
| ---- | ---- | ----------- | -------- |
| markers | `string` | Markers used for the pytest checks, in the python format | `checksum` |
| model-config-tests-version | `string` | The version of the model-config-tests | `0.0.1` |
| python-version | `string` | The python version used to create test virtual environment on Github hosted tests | `3.11.0` |
| payu-version | `string` | The Payu version used to run the model | `1.1.5` |

As most of the tests use the same test and python versions, and similar markers, there are two levels of defaults. There's a default at test type level which is useful for defining test markers - this selects certain pytests to run in `model-config-tests`. There is an outer global default, which is used if a property is not defined for a given branch/tag, and it is not defined for the test default. The `parse-ci-config` action applies the fall-back default logic. For more information on using this action see [`ACCESS-NRI/model-config-tests`](https://github.com/ACCESS-NRI/model-config-tests/).

The CI for this file (in [`config.yml`](./.github/workflows/config.yml)) validates modifications to the `ci.json` against it's schema, found in [`ACCESS-NRI/schema`](https://github.com/ACCESS-NRI/schema). It does not yet verify that modifications make sense.
