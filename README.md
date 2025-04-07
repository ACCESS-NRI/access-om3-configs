# ACCESS-OM3 Model Configurations

This repository contains several
[ACCESS-OM3](https://github.com/COSIMA/access-om3) configurations using the
following components:

- [MOM6](https://mom6.readthedocs.io/) ocean model
- [CICE](https://cice-consortium-cice.readthedocs.io/en/) sea ice model
- [WW3](https://github.com/NOAA-EMC/WW3/wiki/About-WW3) wave model
- [DATM](https://escomp.github.io/CDEPS/versions/master/html/datm.html) atmosphere data model
- [DROF](https://escomp.github.io/CDEPS/versions/master/html/drof.html) runoff data model

All the configurations use the [Payu](https://payu.readthedocs.io/en/latest/)
workflow management tool.

## Repository structure

Each configuration is stored as a git branch. Most of the branches are named
according to the following naming scheme:

`{dev|release}-{MODEL_COMPONENTS}_{nominal_resolution}km_{forcing_data}_{forcing_method}[+{modifier}]`

where `{MODEL_COMPONENTS}` is an acronym specifying the active model components in the following order:
- `M`: MOM6
- `C`: CICE6
- `W`: WW3

and the nominal resolution is given in kilometers, corresponding to the nominal resolution in degrees as follows:
- `100km`: 1°
- `25km`: 0.25°
- `10km`: 0.1°
- `8km`: 1/12°

Additional configuration information, like if the configuration includes
biogeochemistry, is appended to the name as a modifier, e.g.
- `+wombatlite` if the configuration uses WOMBATlite

Currently the following development configurations are available:

**MOM6-CICE6-DATM-DROF configurations**
- [`dev-MC_100km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_100km_jra_ryf)
- [`dev-MC_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_100km_jra_iaf)
- [`dev-MC_100km_jra_ryf+wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_100km_jra_ryf+wombatlite)
- [`dev-MC_25km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MC_25km_jra_ryf)

**MOM6-CICE6-WW3-DATM-DROF configurations**
- [`dev-MCW_100km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_jra_ryf)
- [`dev-MCW_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/tree/dev-MCW_100km_jra_iaf)

**Note that the [`main`](https://github.com/ACCESS-NRI/access-om3-configs/tree/main) branch
does not store any configuration, only some documentation.**

> [!WARNING]
> These configurations are still under development and should **not** be used for production runs.

## Comparison table
The following links can be used to easily compare different configuration branches

**MC → MC**
- [`dev-MC_100km_jra_ryf`➡️`dev-MC_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf..dev-MC_100km_jra_iaf)
- [`dev-MC_100km_jra_ryf`➡️`dev-MC_100km_jra_ryf+wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf..dev-MC_100km_jra_ryf+wombatlite)
- [`dev-MC_100km_jra_ryf`➡️`dev-MC_25km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf..dev-MC_25km_jra_ryf)
- [`dev-MC_100km_jra_iaf`➡️`dev-MC_100km_jra_ryf+wombatlite`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_iaf..dev-MC_100km_jra_ryf+wombatlite)
- [`dev-MC_100km_jra_iaf`➡️`dev-MC_25km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_iaf..dev-MC_25km_jra_ryf)
- [`dev-MC_100km_jra_ryf+wombatlite`➡️`dev-MC_25km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf+wombatlite..dev-MC_25km_jra_ryf)

**MCW → MCW**
- [`dev-MCW_100km_jra_ryf`➡️`dev-MCW_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MCW_100km_jra_ryf..dev-MCW_100km_jra_iaf)

**MC → MCW**
- [`dev-MC_100km_jra_ryf`➡️`dev-MCW_100km_jra_ryf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_ryf..dev-MCW_100km_jra_ryf)
- [`dev-MC_100km_jra_iaf`➡️`dev-MCW_100km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/dev-MC_100km_jra_iaf..dev-MCW_100km_jra_iaf)

## Setting up an experiment

The configurations in this repository are intended for use with the [Payu workflow manager](https://github.com/payu-org/payu).
A tutorial on [how to use Payu to run model experiments](https://forum.access-hive.org.au/t/running-model-experiments-with-payu-and-git/2285)
can be found on the ACCESS-Hive Forum.

As an example, to set up an experiment directory from the `dev-MC_100km_jra_ryf` configuration on a new branch called `my_expt`:

```bash
payu clone --new-branch my_expt --branch dev-MC_100km_jra_ryf git@github.com:ACCESS-NRI/access-om3-configs.git OM3_MC_100km_jra_ryf
cd OM3_MC_100km_jra_ryf
```

Note that, by default, the Payu run log is turned off for configurations under development. However, you
should turn it on so that your configuration settings will be recorded as the run proceeds. Simply edit
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

To run the configurations in this repo, you need to be a member of the `vk83` and `xp65` [projects](https://my.nci.org.au/mancini) on [Gadi](https://nci.org.au/our-systems/hpc-systems)

See [this section of the quick start instructions in the ACCESS-OM3
wiki](https://github.com/COSIMA/access-om3/wiki/Quick-start#running).

## Contributions

We welcome contributions from users of these configurations. If you make a
configuration improvement which you think should be included in the [ACCESS-NRI/access-om3-configs](https://github.com/ACCESS-NRI/access-om3-configs)
repository, please [open an issue](https://github.com/ACCESS-NRI/access-om3-configs/issues)
in this repo describing the change.

## Configuration Continuous Integration (CI)

### Pull Request Reproducibility CI

This pipeline compares configurations modified in a PR against the current current configuration in the `target` branch. The pipeline does a short model run using the proposed change (the `source` branch) against a 'ground truth' checksum, stored in the `target` branch. It also verifies that commons mistakes in configurations are not made. This allows developers to know if the changes they are about to commit lead to valid and reproducible results. Either way, if the PR is merged, the new commit is tagged in such a way that we know how reproducible it is against past configurations.

For pull requests into _release_ branches, this runs automatically, see [this section in ACCESS-NRI/model-config tests readme](https://github.com/ACCESS-NRI/model-config-tests?tab=readme-ov-file#config-pr-yml-pipeline)

For pull requsts into other branches, it needs triggering manually, using a `!test` comment. See [this section in model-config-tests readme](https://github.com/ACCESS-NRI/model-config-tests?tab=readme-ov-file#config-comment-test-reusable-workflow)

### User-Dispatchable Repro-CI Workflow

This repository contains a user-dispatchable workflow (minimum `Write` role required) for the generation of reproducibility checksums on a given Config Branch. The workflow requires sign off from [@ACCESS-NRI/ocean](https://github.com/orgs/ACCESS-NRI/teams/ocean) to run on Gadi.

Workflow inputs :

| Input | Type | Required | Default | Description | Example | Notes |
| ----- | ---- | -------- | ------- | ----------- | ------- | ----- |
| `config-branch-name` | `string` | `true` | N/A | The configuration branch that will be run that will generate the checksums | `dev-MC_25km_jra_ryf` | This can be any branch - not just `release` or `dev` branches |
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
