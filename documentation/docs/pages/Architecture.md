# ACCESS-OM3 architecture
The schematic below illustrates the structure of the MOM6-CICE6-WW3 ACCESS-OM3 executable. ACCESS-OM3 is a single executable, consisting of the NUOPC driver (the main program) and several model components, each wrapped in a NUOPC cap; the caps are coupled through the [CMEPS mediator](https://escomp.github.io/CMEPS/versions/master/html/index.html) via NUOPC connectors. NUOPC is an interoperability layer for ESMF which standardises how model components interact. See discussions [here](https://github.com/COSIMA/access-om3/discussions/7#discussioncomment-3446345) and [here](https://github.com/COSIMA/access-om3/discussions/9) for more information.

![ACCESS-OM3 architecture](../assets/nuopc_overview.png){: loading="lazy" }

The coupled fields and remapping methods used are recorded in the mediator log output file and can be found with `grep '^ mapping' archive/output000/log/med.log`; see [here](https://escomp.github.io/CMEPS/versions/master/html/esmflds.html) for how to decode this. See [the Configurations Overview page](configurations/Overview.md#coupling) for details on how the coupling is determined.

## Overview of codebase

The ACCESS-OM3 software is built from libraries containing the code for each model component.

The top level code (main program) for an ACCESS-OM3 executable is the CMEPS NUOPC driver [`CMEPS/CMEPS/cesm/driver/esmApp.F90`](https://github.com/ESCOMP/CMEPS/blob/606eb397d4e66f8fa3417e7e8fd2b2b4b3c222b4/cesm/driver/esmApp.F90).

The [software deployment](https://github.com/accESS-NRI/access-om3) compiles a single executable for the model. Each single exectuable contains the driver, [CMEPS](https://github.com/access-nri/access-om3/tree/master/CMEPS) NUOPC mediator and different selections of these model components:

- ocean: [MOM6](https://github.com/access-nri/MOM6) active model or DOCN prescribed data model from [CDEPS](https://github.com/access-nri/access-om3/tree/master/CDEPS) or nothing (stub)
- sea ice: [CICE6](https://github.com/access-nri/CICE) active model or DICE prescribed data model from [CDEPS](https://github.com/access-nri/access-om3/tree/master/CDEPS) or nothing (stub)
- waves: [WW3](https://github.com/access-nri/WW3) active model or DWAV prescribed data model or nothing (stub)
- atmosphere: DATM prescribed data model from [CDEPS](https://github.com/access-nri/access3-share/tree/master/CDEPS)
- runoff: DROF prescribed data model from [CDEPS](https://github.com/access-nri/access3-share/tree/master/CDEPS)

The default deployment [contains two builds](https://github.com/search?q=repo%3AACCESS-NRI%2FACCESS-OM3%20configurations%3D&type=code), the `access-OM3-MOM6-CICE6` executable contains the active ocean and sea ice model and no waves, and the `access-OM3-MOM6-CICE6-WW3` executable contains the active ocean, seaice and wave models. Other combinations of prescribed and active model components are possible but not probided by default.

The model components are coupled exclusively through the mediator via their NUOPC caps: [MOM6](https://github.com/mom-ocean/MOM6/tree/main/config_src/drivers/nuopc_cap), [CICE6](https://github.com/ESCOMP/CICE/tree/main/cicecore/drivers/nuopc/cmeps), [WW3](https://github.com/ESCOMP/WW3/blob/dev/unified/model/src/wav_import_export.F90), [DOCN](https://github.com/ESCOMP/CDEPS/tree/main/docn), [DICE](https://github.com/ESCOMP/CDEPS/tree/main/dice), [DATM](https://github.com/ESCOMP/CDEPS/tree/main/datm) and [DROF](https://github.com/ESCOMP/CDEPS/tree/main/drof).

## Further information coupling
- [Overview of how NUOPC works](https://earthsystemmodeling.org/nuopc/)
- [CMEPS docs](https://escomp.github.io/CMEPS/versions/master/html/index.html)
- [NUOPC and ESMF docs](https://earthsystemmodeling.org/doc/)
  - [NUOPC how-to](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_howtodoc/)
  - [NUOPC reference](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_refdoc/NUOPC_refdoc.html)
  - [ESMF superstructure](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/ESMF_refdoc/node4.html)
  - [ESMF glossary](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/ESMF_usrdoc/node15.html)
- [MOM6 NUOPC cap docs](https://ncar.github.io/MOM6/APIs/nuopc_cap.html)



