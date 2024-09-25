# Contributing

## Changes to the CI Infrastructure

Changes to the CI Infrastructure are made to the `main` branch in this repository. Config branches use the `ci.yml` workflows to `workflow_call` the equivalent workflow that is in [`model-config-tests`](https://github.com/ACCESS-NRI/model-config-tests).

## Dev and Release branches

Each configuration has a `dev-*` and a `release-*` branch. They differ in the CI checks that are run when pull requests are made to update the branch. Any branch starting with either `dev-*` or  `release-*` are protected branches. You cannot (and should not) modify them directly or create new branches with names starting with either `dev-` or `release-`.

### Dev

The `dev-*` branch is where a configuration is updated. Temporary branches should be created and a pull request made to update the `dev-*` branch. Quality assurance (QA) CI checks are run on pull requests to `dev-*` branches, but not reproducibility checks. There is no requirement that the version be updated when changes are made to the `dev-` branch. So the `dev-` branch of a configuration allows for smaller changes that can be accumulated before a PR is made to the respective `release-*` branch.

### Release

Pull requests to the `release-*` branch should be made from the respective `dev-*` branch and are intended to create a new version of the configuration. These pull requests have CI quality assurance (QA) checks that ensure the model configuration is suitable for release. CI Model reproducibility checks are also conducted: a short test run of the configuration is checked for bitwise reproducibility. The success or otherwise of this check determines if a minor or major version bump is required.

It is expected that the version *will* be updated before the pull request can be merged. This in turn creates a new tag for that configuration branch. It can be confusing for users if there are a large number of versions of a configuration and it is of little benefit to them. For this reason the atomicity of updates to a released configuration should be minimised, i.e.  updates should be meaningful.

## Creation of a new ACCESS-OM3 Config

Config branches are entirely separate from the `main` history in this repository, except for a few files in `.github`. Note, you may need to be an Administrator to commit to `release-*` or `dev-*` branches directly.

### Brand new configuration

If you are creating a brand new configuration, and don't have the config stored in another repository, just checkout a `dev-*` branch from `main` and delete everything except `.github/workflows/ci.yml`, then add your config.

### Config is Stored in Another Repository

Create a `dev-*` branch by adding the config repository as a remote and checking out the config branch:

```bash
git remote add <config_repo> <config_repo_url>  # ex. git remote add config git@github.com/my/configs.git
git checkout <config_repo>/<config_branch> -b dev-<config_name>  # checkout config from new remote + add to branch, ex. git checkout config/main -b dev-1deg_abc_def
git checkout main -- .github/workflows/ci.yml
git add .
git commit -m "Initial commit for config branch"
git push  # might require admin permissions for pushes to dev-* branch
```

### Create a new release branch

For a brand new configuration there is no existing `release-*` branch, so one needs to be created. Follow the pull request process outlined below to update the dev branch so that it is passing QA checks. At this point create a `release-*` branch from the `dev-` branch and `git push` it to the repository:

```bash
git checkout -b release-<config_name>
git push release-<config_name>
```

For the CI workflows to work correctly the `release-` branch needs to have a version set, and a reproducibility checksum committed. There is a convenience workflow for this purpose: [Generate Initial Checksums](https://github.com/ACCESS-NRI/access-om3-configs/actions/workflows/generate-initial-checksums.yml). Click the "Run workflow" menu, fill in the fields and push the green "Run workflow" button.

Once the workflow is completed there should be a new commit on the `release-*` branch, and a [tag](https://github.com/ACCESS-NRI/access-om3-configs/tags) for the specified version.

Once the `release-*` branch has been updated those changes need to be merged **back** into the `dev-*` branch. This step is only necessary when the `release-*` branch is updated independently of the `dev-*` branch.

## Pull Request Process

### Update dev config

1. Make your changes, test them, and open a PR from a feature/change branch (or fork) to the `dev-*` branch of a particular configuration.
2. QA checks will run to ensure the configuration meets criteria for a released configuration, and to ensure consistency of released configurations.
3. Fix the problems identified in the QA checks, commit and push to the PR branch.
4. Once all checks pass the pull request branch can be merged.
5. Consider making a PR to the equivalent `release-*` branch.

Note: If this is a brand new configuration and there is no existing `release-*` branch you will [need to create one first](#create-a-new-release-branch).

### Update release config

1. Open a PR from the `dev-*` branch of a particular configuration to the equivalent `release-*` branch
2. QA checks will run to ensure the configuration meets criteria for a released configuration, and to ensure consistency of released configurations.
3. Checks will also run to test if changes break reproducibility with the current major version config tag on the target branch. For example, if you are opening a PR on the `release-025deg_jra55do_ryf` branch, and the last tagged version on this branch is `release-025deg_jra55do_ryf-1.2`, the checksums between the config in your PR and the checksum in the config tag are compared.
4. A comment will be posted on the PR when this is completed, notifying you whether the checksums match (in this example meaning a minor bump to `*-1.3`), or are different (meaning a major bump to `*-2.0`).
5. Optionally, you can now modify your PR and get more reproducibility checks. Particularly in the case where bitwise reproducibility should be retained this is an opportunity to modify the configuration to enable this.
6. Bump the version using the `!bump [major|minor]` command depending on the result of the reproducibility check. Additionally, if the checksums are different, the updated checksum will be automatically committed to the PR. Bumping the version in some way is a requirement before the PR will be mergable.
7. Merge the PR
