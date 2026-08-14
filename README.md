# Template configuration for regional OM3 forced with ERA5 and GLORYS

This configuration serves two purposes:

1. It is a template used by the regional-mom6/ACCESS-rOM3 workflow for generic, relocatable regional configurations of MOM6. The template matches the [Tasmania demo](https://github.com/COSIMA/regional-mom6/blob/main/demos/ACCESS-rOM3-demo.ipynb). See https://github.com/COSIMA/regional-mom6/ and associated documentation for details.
2. This configuration serves as a case for the global OM3 development team to test against. 

**WARNING: Unlike other configurations, this is used to set up generic regional OM3 configurations using the regional-mom6 software package. Such domains aren't immediately producion ready, and the user needs to undertake validation and testing**

See [`main` branch
README](https://github.com/COSIMA/MOM6-CICE6/blob/main/README.md) for usage
information.

## Features

- data atmosphere (DATM) = ERA5 modified by the regional-mom6 package to fit chosen domain
- data runoff (DROF) = JRA55-do v1-4, IAF 1958-2018

## Requirements

This configuration requires [Payu](https://github.com/payu-org/payu) > v1.1.3 to run.
