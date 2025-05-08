If you don't want to use a precompiled executable from an [ACCESS-OM3 release](Releases.md), you can build it yourself.

Building access-om3 requires membership of the `ik11` project - apply at https://my.nci.org.au/mancini/project/ik11 if needed.

First clone access-om3 following the steps in the [README](https://github.com/COSIMA/access-om3#readme).
Then do
```
cd access-om3
./build.sh
```
After a little while you'll get shiny new executables:
```
Release/bin/access-om3-CICE6-WW3
Release/bin/access-om3-MOM6-CICE6
Release/bin/access-om3-MOM6-CICE6-WW3
Debug/bin/access-om3-CICE6-WW3
Debug/bin/access-om3-MOM6-CICE6
Debug/bin/access-om3-MOM6-CICE6-WW3
```
The executables in `Releases` are optimised for production use. The `Debug` versions may be useful for getting more information on model crashes, but should not be used for production runs as they are much slower.

The executable names are labelled by the included model components. There are additional combinations of components which can be built by changing `OFF` to `ON` in [this section of `CMakeLists.txt`](https://github.com/COSIMA/access-om3/blob/6f9085f4c0832b719ea2ae5dc4630004c3db9263/CMakeLists.txt#L20-L26) and running `./build.sh` again.

### A note on dependencies

ACCESS-OM3 has several dependencies which are unavailable from NCI, so we supply them via Spack using https://github.com/COSIMA/spack-config which is installed in `/g/data/ik11/spack/`.

### TODO
- comment here on whether the executables are suitable for all cpus (ie queues) on gadi
- We also want to coordinate with these plans https://github.com/ACCESS-NRI/model_builder

## For developers

Spack-based build instructions are here: https://github.com/ACCESS-NRI/ACCESS-OM2/blob/main/DEVELOPERS.md and the spack environment is at https://github.com/accESS-NRI/access-om3

To produce release and release-prototypes, raise a PR with the changes on https://github.com/accESS-NRI/access-om3. This will deploy at github workflow to automatically build the requested model binary.