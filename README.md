# ACCESS-OM3 Model Configurations

**Note that the [`main`](https://github.com/ACCESS-NRI/access-om3-configs/tree/main) branch
does not store any configuration, only some documentation.** If you are looking to fork this repo, we suggest you fork all branches.
 
Detailed documentation on the configurations, including how to make modifications, is provided at [https://access-om3-configs.access-hive.org.au](https://access-om3-configs.access-hive.org.au/).

## Running OM3 and the configurations in this repository

If you would like to run the model, see the [How to Run ACCESS OM3 documentation](https://docs.access-hive.org.au/models/run-a-model/run-access-om3/).

## Contributions

We welcome contributions from users of these configurations. If you make a configuration improvement which you think should be included in the [ACCESS-NRI/access-om3-configs](https://github.com/ACCESS-NRI/access-om3-configs)
repository, please [open an issue](https://github.com/ACCESS-NRI/access-om3-configs/issues) in this repo describing the change. Other kinds of contributions are very welcome, [see the configuration documentation contributions pages](https://access-om3-configs.access-hive.org.au/).



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
