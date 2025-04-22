# ACCESS-OM3 Topography Workflow

## Introduction
The supported ACCESS-OM3 configurations now use a topography based on the [GEBCO2024](https://www.gebco.net/data_and_products/gridded_bathymetry_data/gebco_2024/) global topography dataset. This dataset maintains a high resolution of 15 arc-seconds (i.e., 1/240 deg = ~460m at the equator and finer zonally near the poles).

## Bathymetry Tools
The workflow described below uses `bathymetry-tools` to perform specific tasks, such as removing seas or generating the land/sea mask. Instructions to install `bathymetry-tools` can be found [here](https://github.com/COSIMA/bathymetry-tools).

## General Workflow
The general workflow for generating the OM3 topography and corresponding land/sea masks is as follows:

1. **Interpolate GEBCO2024 data** onto the model grid.
2. **Adjust C-grid connectivity** using the `deseas` algorithm to ensure marginal seas with 1-cell-wide outlets (e.g., Gibraltar) remain connected to the ocean.
3. **Remove T cells** that are smaller than the given threshold.
4. **Fill cells** with a sea area fraction smaller than 0.5.
5. **Apply manual topography edits** using `editTopo.py`.
6. **Remove isolated seas**.
7. **Apply minimum and maximum allowed ocean depths**.
8. **Generate the land/sea mask** from the topography.
9. **Generate additional necessary model input files**, such as ESMF meshes and runoff remapping weights.

This workflow assumes that a horizontal super-grid has already been created and that the model uses a C-grid. Some manual editing may still be necessary to refine the topography.

For a complete workflow and instructions on generating OM3 topography, refer to the [make_OM3_025deg_topo](https://github.com/ACCESS-NRI/make_OM3_025deg_topo/tree/main) repository.