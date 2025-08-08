
If you don't want to use a precompiled executable from an [ACCESS-OM3 release](Releases.md), you can build it yourself.

Most users won't need to do this, it is only if you want to change the source code of ACCESS-OM3.

For users of ACCESS-OM3 model configurations released by ACCESS-NRI, knowledge of the exact location of the model executables is not required. Model configurations will be updated with new model components when necessary.

### Executable Deployments

By default, users will run exectuables stored in the `vk83` project. These are deployed automatically on completion of a Pull Request into https://github.com/accESS-NRI/access-om3. 
Some details on that process are in the [ACCESS-OM3 Deployment README](https://github.com/accESS-NRI/access-om3) and some high level details on these builds are in the [deplyment release notes](https://github.com/ACCESS-NRI/ACCESS-OM3/releases)

Two default builds are provided:

`access-om3-MOM6-CICE6`
`access-om3-MOM6-CICE6-WW3`

These builds are optimised for the Sapphire-Rapid hardware from Intel (e.g. the _normalsr_ queue), and may not run on Cascade-Lake or older hardware (e.g. the _normal_ queue). The aim is to use the same executable for non-BGC and BGC (Wombatlite) configurations. For regional configurations, compiling with MOM symmettric memory is required, which is not the default but could become the default in the future (see [436](https://github.com/ACCESS-NRI/access-om3-configs/issues/436#issuecomment-2750119607)).

### Software Structure

ACCESS-OM3 is run as a single executable, which links to libraries for all model components, and the couples them using the NUOPC framework. This is different to previous ACCESS models which used Oasis-MCT for coupling and have one executable for each model component.

The definition of the final exectuable is in the [access3-share repository](https://github.com/accESS-NRI/access3-share), whilst model-components all have their own repositories:

- https://github.com/accESS-NRI/mom6
- https://github.com/accESS-NRI/cice
- https://github.com/ACCESS-NRI/WW3/

The [access3-share repository](https://github.com/accESS-NRI/access3-share) also contains code for some shared libraries used for data-forcing and common infrastructure. As such, the access3-share contains both dependencies for model components (access3-share libraries) and the final exectuable (access3), which dependends on model components.

The repositories for each model-component are forked from the canonical or upstream codebases for each model component and only contain minor changes for consistency with access-om3 components and to support a CMake build system.

### Ad-hoc builds

For testing and feature development, a typical approach can be:

- Clone the relevant repository for the model-component or access3-share
- Make the changes
- Open an issue in that repository and push the changes back to a branch on that repository. The branch should be named with the issue number.

This can then be built using the pre-release build infrastructure described in this [Hive Docs article](https://docs.access-hive.org.au/models/run-a-model/create-a-prerelease/).

For more complex changes and to assist in faster iterations of code changes, it may make more sense to setup a personal spack instance, as described in [Modify and build an ACCESS model source code](https://docs.access-hive.org.au/models/run-a-model/build_a_model/)

Changes only to compile time options (e.g. debug/optimisation flags, compiler choice), can normally be achieved through a pre-release build. The spack documentation has some information on how to set these options. Changes to spack variants can also be achieved through a pre-release build.
The variants for spack-packages are in the [recipes for each spack-package](https://github.com/ACCESS-NRI/spack-packages/tree/main/packages). For example, to build a MOM6 only executable, without interactive sea ice or waves, `configurations=MOM6` can be specified as the [_configurations_ variant](https://github.com/ACCESS-NRI/spack-packages/blob/b73ecc20a21859006a6e58c2c6de8c2e32eabae4/packages/access3/package.py#L37) for _access3_. 

Building a prerelease with `build_type=debug` can be useful for getting more information on model crashes, but should not be used for general model runs as they are much slower. These debug builds are largely untested, but will probably get fixed up over time.

### New Releases

When it is needed to update the model components to incorporate new upstream updates, this triggers a new major release. These are the high-level steps to update the model component versions:

1. **Choose new component versions**: These need to be chosen based on currently known issues/bugs and desired features in the new release. The versions in [https://github.com/ESCOMP/CESM/blob/cesm3.0-alphabranch/.gitmodules](https://github.com/ESCOMP/CESM/blob/cesm3.0-alphabranch/.gitmodules) are a good starting point, as we know NCAR have already checked for compatibility between these versions. Make an [new issue](https://github.com/accESS-NRI/access-om3-configs) to discuss the new versions.
2. **Choose new dependency versions**: Similarly, choose new versions for external dependencies and compilers. The current versions are listed in [spack.yaml](https://github.com/ACCESS-NRI/ACCESS-OM3/blob/main/spack.yaml). 
3. **Setup a pre-release** with the changes only to dependencies and compilers. Then use a draft-PR to test builds run and for reproducability with previous builds. A draft-PR to [dev-MC_100km_jra_ryf](https://github.com/ACCESS-NRI/access-om3-configs/blob/e836a710b4324a6f942c8bd9855afb627c16e685/config/ci.json#L28-L29) can be a good choice as it runs all reproducability tests. If changing compilers, it may make sense to run these tests without compiler optisations on (e.g. -O0).
The versions can be changed in the access-om3 deployment repository by changing the [spack.yaml](https://github.com/ACCESS-NRI/ACCESS-OM3/blob/main/spack.yaml). Unless there is an interface change between depedencies, the old access-om3 model components should still build with the new dependencies.
4. **Update component repositories**


For access3-share
1. checkout the current default branch
2. update the three submodules with the chosen upstream commit from step 1
3. test the build (e.g. using spack develop and build-CI) and fix/update patches as required
4. make a pull request into main with the new versions

For each component (MOM6, CICE, WW3)
1. checkout the current default branch
2. rebase with the chosen upstream commit
3. create a new branch with a temporary name (e.g. rc-dev/2025.08 or rc-CICE6.6.1-x)
4. test the build (e.g. using spack develop and build-CI) and fix issues. 
5. If there are bugs found, raise in the appropriate upstream repository.
5. push the new branch and make this the default branch for that repository (in the repository settings)

The strategy for branch names should be in the wiki of each access-nri fork of these repostiories.
Typically CICE branches follow the upstream version (e.g. CICE6.6.1-x is the ACCESS branch based on the upstream CICE6.6.1 release).
MOM6 and WW3 branch names follow the major part of CalVer (e.g. a branch based on upstream commits in August 2025 is 2025.08)


In the build CD PR, incrementally add each component (using a git.ref) and run repro-CI in the configuration PR for each change

e.g. 
first change the compiler, then run repro-CI and see the if the answers change
second, update external depencies
third, update access3-share and access3
fourth, update model components one by one

You may find components have interrelated changes and cannot be built seperately. Seperately, the config will often need the field dictionary updated from [upstream](https://github.com/ESCOMP/CMEPS/blob/main/mediator/fd_cesm.yaml). Each model component and cap may have other changes as described in the release note / git history for that component. Work through any issues and updates until the model runs. 

Take note of conflicts found (e.g. some new model components might need changes to depencies to build)

Once every component is updated in the PR, and you are generally happy the changes are correct, move to the next step. Hopefully you can iterate and modify such that only the model components which were expected (based on information from MOM/CICE consortia and release notes) to change answers have changed answers.


6. **Tag the build components**: Once you are happy with the build, tag each model component fork with the new release number 
Typically the first release from a 2025.08 branch would be 2025.08.000, or from the CICE6.6.1-x branch would be CICE6.6.1-0

Add the tags to spack-packages ([see example PR](https://github.com/ACCESS-NRI/spack-packages/pull/297)) and update the spack packages with any version dependencies found.


7. **Deploy**: Deploy the new version, using the new release versions using the CD process in [https://github.com/ACCESS-NRI/ACCESS-OM3](https://github.com/ACCESS-NRI/ACCESS-OM3)
8. **Update the configurations**: Update all [https://github.com/ACCESS-NRI/access-om3-configs](https://github.com/ACCESS-NRI/access-om3-configs) dev-branches with the build from the new access-om3 deployment & related changes (e.g. `fd.yaml` and other config changes needed for it to run, including minimum payu version)

For new minor releases, these steps can be simplified.

Instead of making new branches for model components and updating from upstream, instead make PRs to the existing branches and tag with an incremented minor version number (e.g. following from the examples above, the minor update would be 2025.08.001 or CICE6.6.1-1). Unless necessary, typically minor releases would not change compilers or external depedencies.
