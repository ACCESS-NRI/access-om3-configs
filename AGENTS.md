# AGENTS.md

Guidance for AI coding agents working in ACCESS-NRI/access-om3-configs.

The human docs are the reference for how this repo works: [`CONTRIBUTING.md`](CONTRIBUTING.md) and `documentation/docs/` on `main` (published at https://access-om3-configs.access-hive.org.au), especially `pages/infrastructure/Git-practices.md`, `pages/infrastructure/Building.md` and `pages/Tips-and-tricks.md`. Read them before making changes. This file only lists rules and pitfalls an agent is likely to miss.

## Terminology

- **Config files:** the text files stored in this git repository on each configuration branch (`config.yaml`, `MOM_input`, `ice_in`, `nuopc.runconfig`, `diag_table`, `manifests/`, `docs/`, ...).
- **Inputs:** the binary files (grids, meshes, initial conditions, forcing, remap weights, ...) listed in `config.yaml` under `input:`. They are not stored in git; they live under `/g/data/vk83/` and are tracked by path and hash in `manifests/input.yaml`.

## Branches

- `main` holds CI and documentation only. Each configuration is a separate `dev-<config>` / `release-<config>` branch with no shared history with `main`.
- Never commit to, or create, branches starting with `dev-` or `release-`. Make a feature branch named `{issue_number}-{config_branch}` and open a PR to the `dev-` branch.
- To apply the same change to other configs, comment on the merged PR with `!cherry-pick <hash...> into <branch...>` (the commits must already be merged into that PR's base branch). See [Commits](#commits) for which commits to include.

## Changing a configuration

- **Changing an input:** every path in `config.yaml` `input:` has an entry in `manifests/input.yaml` (`fullpath`, `binhash`, `md5`). If you change the path, update the entry too. Compute hashes with payu's own library (`yamanifest.hashing.hash(path, "binhash")` and `"md5"`, run from payu's Python environment), or by running `payu setup`.
- Inputs must be under `/g/data/vk83/{prerelease/,}configurations/inputs/`, in a new date-versioned directory (`YYYY.MM.DD`). They get there through ACCESS-NRI/model-config-inputs, never by copying them yourself.
- **`MOM_input`:** everything from the "This file was written by the model..." header onwards must be an exact copy of `docs/MOM_parameter_doc.short`. Replace that section whole; don't edit individual lines.
- **`docs/` on a config branch** is updated automatically by payu when the configuration is run (payu copies the model's parameter output into it). Run the model to refresh it rather than editing it by hand. The `doc/` folder on `main` is updated by the `update-doc-folder` workflow; don't edit it directly either.
- **Default values:** config files generally only list settings that differ from the default. Don't add a setting at its default value.
- **payu features:** when adding a new option to `config.yaml`, check which payu version introduced it (payu changelog and docs). If it's newer than `payu_minimum_version` in `config.yaml`, raise `payu_minimum_version` in the same commit.
- **Executable:** `dev-` and `release-` branches must load a released `access-om3` module from `/g/data/vk83/modules`. Prerelease modules (`access-om3/prNNN-M`) are for testing in a draft PR or a local copy only.

## Commits

Structure commits so they can be cherry-picked cleanly into other configs:
- **One change per commit.** If a PR makes several unrelated changes, put each in its own commit and reference its issue in the commit message (e.g. `Raise MAXTRUNC (#1595)`). Merge the PR with a **merge commit**, not squash, so each change keeps its own commit. A PR that makes one change (e.g. a docs fix on `main`) can be squashed.
- **Checksums in a separate commit.** Keep the config change and the updated checksums (from `!test repro --commit`) in separate commits. Cherry-pick only the config change, then run `!test repro --commit` on each bot-opened PR so each target branch gets its own checksums.

## Pull requests

- Fill in [`.github/pull_request_template.md`](.github/pull_request_template.md) for every PR except bot-created cherry-picks or documentation only changes.
- Say in section 3 "AI Tooling" how AI tools were used (see `pages/contributing/Overview.md`).

## CI commands (PR comments)

- `!test repro`: short run on Gadi comparing checksums.
  - `--commit` (or `-c`) commits the new checksums when answers change: `!test repro --commit`.
  - `-m`/`--markers <markers>` selects tests, e.g. `-m repro_historical`. Valid markers are listed in model-config-tests (`config_tests/conftest.py`). `-m historical` matches nothing and fails.
  - `-w`/`--walltime <HH:MM:SS>` sets the PBS walltime for the test job.
- `!cherry-pick <hash...> into <branch...>`: on a merged PR; opens PRs on the target branches.
- `!bump major|minor`: on `dev-` to `release-` PRs.

## QA checks

QA tests from model-config-tests run on every PR to `dev-`/`release-`. Before fixing a failure, check whether it also fails on the base branch. If it does, it isn't caused by the PR, so leave it for a separate PR. For example:
- `test_access_om3_manifest_exe_in_release_spack_location`: a prerelease module is loaded.

## Reviewing

- Check that the grid size (nx, ny) is the same in every place it is set, especially when the grid or land mask changes:
  - `datm_in` and `drof_in`: `nx_global`, `ny_global`
  - `ice_in`: `nx_global`, `ny_global`
  - `nuopc.runconfig`: `atm_nx`/`atm_ny`, `ice_nx`/`ice_ny`, `ocn_nx`/`ocn_ny`, `rof_nx`/`rof_ny` (and `wav_nx`/`wav_ny` for WW3 configs)
  - `MOM_input`: `NIGLOBAL`, `NJGLOBAL`
- A change to `NIPROC`/`NJPROC`/`LAYOUT` in `docs/MOM_parameter_doc.layout` is expected when the land mask or `ncpus` changes (`AUTO_MASKTABLE` drops land-only blocks). Check the arithmetic against `ocn_ntasks` in `nuopc.runconfig` before raising it.
- Because payu updates `docs/` when it runs, a local run directory can contain `docs/` changes that aren't on the remote branch. Compare against the remote branch tip, not a run clone.

## Gadi

These configurations are only developed and tested on Gadi at NCI. Paths, modules, PBS settings and CI all assume Gadi and access to the NCI projects they use (e.g. `vk83`).

- `gh`: `module use /g/data/vk83/modules && module load gh`
- payu: `module use /g/data/vk83/modules && module load payu` (in the same shell as `payu`)
- Python with xarray/netCDF4: `module use /g/data/xp65/public/modules && module load conda/analysis3`
