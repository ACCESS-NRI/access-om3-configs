ACCESS-OM3 configurations that utilize the same model components are maintained as separate branches in one repo. For example, all ACCESS-OM3 MOM6-CICE6 configurations are branches in the [`access-om3-configs` repo](https://github.com/ACCESS-NRI/access-om3-configs). This simplifies the syncing of changes across related configurations. In order to maintain clean and intuitive branch structure, the following practices should be followed:

# Configuration branch naming
Each configuration branch name should include as minimum the following: `dev/release-{nominal_resolution}deg_{forcing_data}_{forcing_method}` - e.g. `dev-01deg_jra55_ryf`. Additional required information can be appended if relevant, e.g. whether the configuration includes biogeochemistry.

# Feature branch naming
All modifications to configuration branches should be carried out via a pull request from a feature branch. The name of the feature branch should be as follows: `{issue_number}-{configuration_branch}`, where `{issue_number}` is the number of a corresponding issue in the GitHub repo that provides context and information about the work being done in the feature branch - e.g. `99-dev-01deg_jra55_ryf`. Feature branches should be deleted once they are merged.

# Branch synchronisation for releases
Prior to a release, configuration branches should be synchronised by cherry-picking across all configurations and across repos, and a new release number created. The `!cherry-pick` GitHub action makes this easier:
```
!cherry-pick <hash_1> <hash_2> ... <hash_n> into <branch_1> <branch_2> ... <branch_n>
```
See https://github.com/ACCESS-NRI/access-om3-configs/pull/90.

# Production runs
Production runs should be forked as separate repos, and the git runlog enabled.