# ACCESS-OM3 architecture

The schematic below illustrates the structure of the MOM6-CICE6-WW3 ACCESS-OM3 executable. ACCESS-OM3 is a single executable, consisting of the NUOPC driver (the main program) and several model components, each wrapped in a NUOPC cap; the caps are coupled through the CMEPS mediator via NUOPC connectors (see the [coupling page](Coupling) for more information).

![ACCESS-OM3 architecture](https://github.com/COSIMA/access-om3/assets/31054815/8a438302-75a2-47c6-81dd-722a94b00333){: loading="lazy" }

## Overview of codebase

The ACCESS-OM3 code repository consists mostly of submodules containing the code for each model component.

The top level code (main program) for an ACCESS-OM3 executable is the CMEPS NUOPC driver [`CMEPS/CMEPS/cesm/driver/esmApp.F90`](https://github.com/ESCOMP/CMEPS/blob/606eb397d4e66f8fa3417e7e8fd2b2b4b3c222b4/cesm/driver/esmApp.F90).

The [build system](Building) compiles a set of executables containing the driver, [CMEPS](https://github.com/access-nri/access-om3/tree/master/CMEPS) NUOPC mediator and different selections of these model components:
- ocean: [MOM6](https://github.com/access-nri/access-om3/tree/master/MOM6) active model or DOCN prescribed data model from [CDEPS](https://github.com/access-nri/access-om3/tree/master/CDEPS) or nothing (stub)
- sea ice: [CICE6](https://github.com/access-nri/access-om3/tree/master/CICE) active model or DICE prescribed data model from [CDEPS](https://github.com/access-nri/access-om3/tree/master/CDEPS) or nothing (stub)
- waves: [WW3](https://github.com/access-nri/access-om3/tree/master/WW3) active model or nothing (stub)
- atmosphere: DATM prescribed data model from [CDEPS](https://github.com/access-nri/access-om3/tree/master/CDEPS)
- runoff: DROF prescribed data model from [CDEPS](https://github.com/access-nri/access-om3/tree/master/CDEPS)

The model components are coupled exclusively through the mediator via their NUOPC caps: [MOM6](https://github.com/mom-ocean/MOM6/tree/main/config_src/drivers/nuopc_cap), [CICE6](https://github.com/ESCOMP/CICE/tree/main/cicecore/drivers/nuopc/cmeps), [WW3](https://github.com/ESCOMP/WW3/blob/dev/unified/model/src/wav_import_export.F90), [DOCN](https://github.com/ESCOMP/CDEPS/tree/main/docn), [DICE](https://github.com/ESCOMP/CDEPS/tree/main/dice), [DATM](https://github.com/ESCOMP/CDEPS/tree/main/datm) and [DROF](https://github.com/ESCOMP/CDEPS/tree/main/drof).

NUOPC is provided via the ESMF library in `/g/data/ik11/spack/` and was built by https://github.com/COSIMA/spack-config