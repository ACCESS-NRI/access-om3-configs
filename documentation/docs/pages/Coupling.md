As shown on the [model architecture](https://github.com/COSIMA/access-om3/wiki/Architecture) page, we couple the model components using NUOPC with the [CMEPS mediator](https://escomp.github.io/CMEPS/versions/master/html/index.html). NUOPC is an interoperability layer for ESMF which standardises how model components interact. See discussions [here](https://github.com/COSIMA/access-om3/discussions/7#discussioncomment-3446345) and [here](https://github.com/COSIMA/access-om3/discussions/9) for more information.

## Coupler docs
- [Overview of how NUOPC works](https://earthsystemmodeling.org/nuopc/)
- [CMEPS docs](https://escomp.github.io/CMEPS/versions/master/html/index.html)
- [NUOPC and ESMF docs](https://earthsystemmodeling.org/doc/)
  - [NUOPC how-to](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_howtodoc/)
  - [NUOPC reference](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/NUOPC_refdoc/NUOPC_refdoc.html)
  - [ESMF superstructure](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/ESMF_refdoc/node4.html)
  - [ESMF glossary](https://earthsystemmodeling.org/docs/release/ESMF_8_3_1/ESMF_usrdoc/node15.html)
- [MOM6 NUOPC cap docs](https://ncar.github.io/MOM6/APIs/nuopc_cap.html)

## How to determine which fields are coupled

The coupled fields and remapping methods used are recorded in the mediator log output file and can be found with `grep '^ mapping' archive/output000/log/med.log`; see [here](https://escomp.github.io/CMEPS/versions/master/html/esmflds.html) for how to decode this. See [the Configurations page](https://github.com/COSIMA/access-om3/wiki/Configurations#coupling) for details on how the coupling is determined.