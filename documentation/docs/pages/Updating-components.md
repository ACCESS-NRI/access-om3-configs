All the components that make up OM3 (models, coupler, etc) are currently included as [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) and built using [CMake](https://cmake.org/). This means that, in a nutshell, updating a given component usually requires updating the git submodule and the CMake build system.

## Step by step instructions

### Submodule update

Although not required, we recommend starting the process from a clean git repository:
```console
git clone --recursive https://github.com/COSIMA/access-om3.git
```
Next, go to the directory of the component to update. For example, to update MOM6:
```console
cd access-om3/MOM6/MOM6
```
and checkout the branch/tag/commit you want to update to:
```console
git checkout <branch/tag/commit>
```
Some of the components have git submodules themselves. If that's the case, they need also need to be updated:
```console
git submodule update --recursive
```

### CMake update

Quite often the changes to the component's sources will include addition and/or removal of files. When this happens, the CMake build system also need to be updated accordingly. The sources are listed in the `CMakeLists.txt` files that one can find in each component subdirectory. For example, in the case of WW3, that's the WW3/CMakeLists.txt` (not `WW3/WW3/CMakeLists.txt`!).

At this point, it might also happen that some patches are not necessary anymore and they will throw an error when building the code. If this happens, one needs to update the corresponding patch. If no patch at all is needed after the update, the corresponding patch should be removed from the git repository:
```console
git rm <COMPONENT>/patches/<file>.F90_patch
```
and the original source file needs to be moved from the list of sources to patch to the "normal" source files list in `CMakeLists.txt`. The changes should look like this:
```diff
 target_sources(OM3_<target> PRIVATE
   ...
+  <file>
   ...
 )
 ...
-add_patched_source(OM3_<target> <file>)
```

## New Releases

When it is needed to update the model components to incorporate new upstream updates, this triggers a new minor release. These are the high-level steps to update the model component versions:
1. **Choose new component versions**: These need to be chosen based on currently known issues/bugs and desired features in the new release. The versions in https://github.com/ESCOMP/CESM/blob/cesm3.0-alphabranch/.gitmodules are a good starting point, as we know NCAR have already checked for compatibility between these versions.
2. **Update ACCESS-NRI forks**: Where a component is built from an ACCESS-NRI fork, this fork needs updating (at time of writing this is MOM6 & CICE6). Before changing the default branch of the fork, ensure the current state is captured in a `<<version>>` branch, where version is typically `YYYY.MM` . The branching practice is described for MOM6 [here](https://github.com/accESS-NRI/mom6/wiki#repository-overview) and the CICE process is very similar. The default branch of the fork then needs updating to the desired code version and any ACCESS specific commits that are not included in the upstream version reapplied (e.g. through a git rebase or cherry-pick). This probably requires a force push to change the history on the default branch.
3. **Update dependency versions**: Based on any new releases available, update the dependencies. These are releases of code which are not access-om3 model components, they are code which the models depend on (e.g. openmpi, netcdf, fms etc). The versions can be changed in the access-om deployment repository by changing the [spack.yaml](https://github.com/ACCESS-NRI/ACCESS-OM3/blob/main/spack.yaml). Unless there is an interface change, the old access-om3 model components should still build with the new dependencies (try building through spack).
4. **Update model components**: Its easiest to use a spack "develop" [environment](https://access-hive.org.au/models/run-a-model/build_a_model/) at this point. For each model component, update the submodule to the desired version. Fix any patches applies by CMAKE so that the model builds. If there are bugs found, raise in the appropriate upstream repository.
5. **Test the build**: Once you have a build with the new components, try running the build using typical configs (e.g. https://github.com/accESS-NRI/access-om3-configs and https://github.com/accESS-NRI/access-om3-wav-configs). The config will often need the field dictionary updated from [upstream](https://github.com/ESCOMP/CMEPS/blob/main/mediator/fd_cesm.yaml). Each model component and cap may have other changes as described in the release note / git history for that component. Work through any issues and updates until the model runs. 
6. **Release the build**: Once you are happy with the build, tag each model component fork with the new release number (typically CalVer) and this repository with a new release minor release number (e.g. 0.x.0).
7. **Deploy**: Deploy the new version, using the new release numbers using the CD process in https://github.com/ACCESS-NRI/ACCESS-OM3
8. **Update the configurations**: Update all https://github.com/accESS-NRI/access-om3-configs and https://github.com/accESS-NRI/access-om3-wav-configs dev-branches with the build from the new access-om3 deployment & related changed (e.g. `fd.yaml` and other config changes needed for it to run, including minimum payu version)
9. **Tag the update configurations**: Tag the updated configuration with the new access-om3 release version.