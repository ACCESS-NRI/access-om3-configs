## Releases

The main publicly announced releases related to ACCESS OM3 are releases of model configurations. Model configurations include a version of the model software, and are known to be reasonably stable. All of ACCESS-NRI's [model configuration releases can be viewed here](https://forum.access-hive.org.au/search?q=%23access-nri-releases%20tags%3Amodel%20order%3Alatest).

Releases are [announced](https://forum.access-hive.org.au/t/access-om3-release-information/4494) on the ACCESS-HIVE forum and citable through [DOI's published on zenodo](https://zenodo.org/communities/access-nri/records?q=conceptdoi:16294824&f=allversions%3Atrue).

The stages (alpha, beta, full) and standard for releases are [defined in the ACCESS-HIVE docs](https://docs.access-hive.org.au/about/releases/).

Releases are prepared in branches with the `dev-` prefix, and the merging of a pull request from a `dev-` branch in the corresponding
`release-` branch triggers an action to create the github release. As such, the pull request acts as the final approval for a release. See [contributing in model-config-template](https://github.com/ACCESS-NRI/model-configs-template/blob/main/CONTRIBUTING.md) for details on this process and explanation on versioning applied.

There is a [checklist for developers](https://forum.access-hive.org.au/t/model-release-checklist-template/4371) to follow when undertaking releases. 
When undertaking releases, the following actions are needed to implement the items on the checklist for developers:

- Move inputs from `/g/data/vk83/prerelease/configurations` into `/g/data/vk83/configurations` using [model-config-inputs](https://github.com/ACCESS-NRI/model-config-inputs/). [^1]
[^1]:
    Use the same version (CalVer) between prerelease and release folders.
    for example:
    `/g/data/vk83/prerelease/configurations/inputs/access-om3/cice/grids/global.25km/2025.11.27/kmt.nc` 
    moved to `/g/data/vk83/configurations/inputs/access-om3/cice/grids/global.25km/2025.11.27/kmt.nc`

- Update/confirm the [version](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Aconfig%2Fci.json+model-config-tests-version&type=code&page=config%2Fci.json) of [model-config-tests](https://github.com/ACCESS-NRI/model-config-tests/)

- Reserve a DOI[^2]. Go the [existing DOI](https://doi.org/10.5281/zenodo.16294824) click new version and save the draft. Add the new DOI to CITATION.cff.
[^2]:
    There is one [Concept DOI](https://zenodo.org/help/versioning) for all access-om3 configuration releases. Individual 
    releases are new versions under this DOI. Release managers will need to have the 'Curator' Role on the 
    [ACCESS-NRI Zenodo Community](https://zenodo.org/communities/access-nri/members).

- Check other details in CITATION.cff, (e.g. versions, descriptions, contributors)

- Release notes should be drafted and reviewed before completing release. Use this release note for both github and access-hive forum .

- After the release, navigate to the page for the new DOI and upload the tarball from the github release and fill in any details before publishing the DOI.

## Control Experiments

If sharing data from a control experiment, typically run the control experiment as the last action before merging `dev-` into `release-`. i.e:

- Prepare, finalise and review the configuration and have the PR from `dev-` into `release-` finalised but not merged
- Run control experiment from head of `dev-`
- If control experiment runs sucessfully, then merge release and announce on access-hive
- Add Experiment to the [Experiments](/Experiments) page