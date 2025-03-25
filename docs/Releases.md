## Releases

There are several [ACCESS-OM3 releases](https://github.com/COSIMA/access-om3/releases) available.

Precompiled executables of these are available via spack packages in
```
/g/data/ik11/spack/*/modules/access-om3
```
(Access requires membership of the `ik11` project - apply [here](https://my.nci.org.au/mancini/project/ik11) if needed.)

Those matching [ACCESS-OM3 releases](https://github.com/COSIMA/access-om3/releases) are stable, and generally the newest is the recommended version for general use.
Those containing "x" are unstable development versions which can change without notice.

Executables themselves can be found via
```
find /g/data/ik11/spack/*/opt -name "access-om3-*CICE6*"
```
The file path includes the full [ACCESS-OM3 commit hash](https://github.com/COSIMA/access-om3/commits/main/) indicating the sources used.

To switch to one of these you need to change the `exe:` and `modules: use:` entries in `config.yaml` in a consistent way - see [here](https://github.com/COSIMA/access-om3/issues/93) for full details. You also need to change the `input:` entries to the matching version number.