## Horizontal grid

All ACCESS global ocean and sea-ice models use a tripolar grid.
For ACCESS-OM3, new grids will be created from scratch for all resolutions. So-far a new grid  (1142 x 1440 cells) has been created for 25km configurations. 
The 25km grid and future OM3 grids largely follows the grids used in OM2, with some refinements to increase resolution and extent around Antarctica, and align the equator with model cell centres, rather than edges. 

The following paragraph is adapted from [Kiss 2020](https://gmd.copernicus.org/articles/13/401/2020/gmd-13-401-2020.pdf),
with updates for the OM3 grids:

Ocean cells cover the global ocean from the North Pole to
south of the Antarctic ice shelf edge (81&deg; S). The longitude range is −280 to +80&deg; E,
placing the join in the middle of the Indian Ocean. The grid is defined using the conventional tripolar definition (Murray, 1996) 
in all configurations, with two northern poles placed on land at 65&deg; N, −100&deg; E and 65&deg; N, 80&deg; E,
and a third pole at the South Pole; consequently, the grid
directions are zonal and meridional only south of 65&deg; N. The grid is Mercator (i.e. the
meridional spacing scales as the cosine of latitude) between
65&deg; N and 65&deg; S; south of 65&deg; S, the meridional grid spacing
is held at the same value as at 65&deg; S.


### File formats

The grid is defined in two file formats, the MOM supergrid and the ESMF mesh, however they represent the same grid.
First the grid is created using the python [Ocean Model Grid Generator](https://github.com/ACCESS-NRI/ocean_model_grid_generator/), 
to generate a MOM supergrid file. The MOM supergrid splits each model cell into four supergrid cells. 

As an example, the 25km grid was once generated using the python based ocean model grid generator using these arguments:

```python
ocean_grid_generator.py -r 4 --no_south_cap --ensure_nj_even --bipolar_lower_lat 65 --mercator_lower_lat -75 --mercator_upper_lat 65 --match_dy so --shift_equator_to_u_point --south_ocean_lower_lat -81
```

However refer to the metadata of the latest `ocean_hgrid.py` to find the latest setup.

Secondly, an _ESMF Mesh_ file is [derived](https://github.com/COSIMA/om3-scripts/blob/main/mesh_generation/generate_mesh.py) from the MOM supergrid. 
The MOM supergrid file is used by the MOM and CICE model components, whilst the ESMF Mesh file is used in the coupler. 
(Additional ESMF mesh files exist for the data atmosphere and runoff components). How to configure these in the model is captured in the [configurations](configurations/Configurations.md) page.

For analysis, it's best to use model grids output by the models:

- MOM6 outputs the model grid, [typically](https://github.com/ACCESS-NRI/access-om3-configs/blob/6c0942224adf8cd4644927ad357b68827e837dd9/diagnostic_profiles/diag_table_standard#L13C2-L13C24) in a file named _access-mom6.static..._
- The [next release](https://github.com/ACCESS-NRI/access-om3-configs/issues/470) of CICE6 will also output the model grid into a seperate file.

If you are using coupler diagnostics (off by default), note that the grid areas used in the coupler are calculated internally, 
are subtly different to the grid areas used in the model components. The model component caps [apply a correction](https://escomp.github.io/CMEPS/versions/master/html/introduction.html#area-corrections) between
model areas and mediator areas. 

## Vertical grid

In the ocean model, we use a [75 level vertical grid](https://github.com/COSIMA/om3-scripts/blob/main/grid_generation/generate_vertical_grid.py) unchanged from many OM2 configurations, following Stewart et al 2017.

## Aditional reading:

- [Cheat sheet for using a Mosaic grid with MOM6 output](https://gist.github.com/adcroft/c1e207024fe1189b43dddc5f1fe7dd6c#file-cheat-sheet-for-using-a-mosaic-grid-with-mom6-output-ipynb)
- [Gridspec: A standard for the description of grids used in Earth System models](https://extranet.gfdl.noaa.gov/~vb/pdf/gridstd.pdf)

## References

Ross J. Murray,
Explicit Generation of Orthogonal Grids for Ocean Models,
Journal of Computational Physics,
Volume 126, Issue 2,
1996,
Pages 251-273,
ISSN 0021-9991,
https://doi.org/10.1006/jcph.1996.0136.

K.D. Stewart, A.McC. Hogg, S.M. Griffies, A.P. Heerdegen, M.L. Ward, P. Spence, M.H. England,
Vertical resolution of baroclinic modes in global ocean models,
Ocean Modelling,
Volume 113,
2017,
Pages 50-65,
ISSN 1463-5003,
https://doi.org/10.1016/j.ocemod.2017.03.012.

