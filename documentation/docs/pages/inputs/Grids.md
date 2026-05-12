## Horizontal grid

All ACCESS global ocean and sea-ice models use a tripolar grid.
For ACCESS-OM3, new grids will be created from scratch for all resolutions. So-far a new grid  (1142 x 1440 cells) has been created for 25km configurations. 
For ACCESS-OM3, new grids will be created from scratch for all resolutions. New grids  (1142 x 1440 cells) have been created for 25km configurations and 100km (360 x 324 cells) configurations. 
The OM3 grids largely follows the grids used in OM2, with some refinements to increase resolution and extent around Antarctica, and align the equator with model cell centres, rather than edges.

Ocean cells cover the global ocean from the North Pole to
south of the Antarctic ice shelf edge. The longitude range is −280 to +80&deg; E,
placing the join in the middle of the Indian Ocean. The grid is defined using the conventional tripolar definition[@Murray1996a] 
in all configurations, with two northern poles placed on land at 65&deg; N, −100&deg; E and 65&deg; N, 80&deg; E,
and a third pole at the South Pole; consequently, the grid
directions are zonal and meridional only south of 65&deg; N. The 25km grid is Mercator (i.e. the
meridional spacing scales as the cosine of latitude) between
65&deg; N and 75&deg; S; south of 75&deg; S, the meridional grid spacing
is held at the same value as at 75&deg; S. 
The 100km grid is similar but also refines the meridional spacing between 10&deg; S and 10&deg; N to increase equatorial resolution. 


### File formats

The grid is defined in two file formats, the MOM supergrid and the ESMF mesh, however they represent the same grid. 
The MOM supergrid splits each model cell into four supergrid cells. 
First the grid is created using the python [Ocean Model Grid Generator](https://github.com/ACCESS-NRI/ocean_model_grid_generator/), 
There are two tools which can be used to generate the MOM supergrid. Grids can be created using the python
[Ocean Model Grid Generator](https://github.com/ACCESS-NRI/ocean_model_grid_generator/), or [`make_hgrid`](https://github.com/NOAA-GFDL/FRE-NCtools/blob/main/src/make-hgrid/make_hgrid.c).

The 25km grid was once generated using the python based ocean model grid generator using these arguments:

```python
ocean_grid_generator.py -r 4 --no_south_cap --ensure_nj_even --bipolar_lower_lat 65 --mercator_lower_lat -75 --mercator_upper_lat 65 --match_dy so --shift_equator_to_u_point --south_ocean_lower_lat -81
```


The 100km grid was generated using this command:

```bash
make_hgrid --verbose --grid_type tripolar_grid --nxbnds 2 --nybnds 8 --xbnds -280,80 --ybnds -82.25,-75,-30,-10,10,30,65,90 --dlon 1,1 --dlat 0.25,0.25,1,0.33333333,0.333333333,1.00000001,0.4583335,0.4507575 --center c_cell --rotate_poly
```

This creates a MOM supergrid with `nx = 720` and `ny = 648`, corresponding to a 360 x 324 grid. The grid uses a tripolar projection, spherical geometry, a logically rectangular conformal discretization, and `small_circle` x-direction arcs. The `--center c_cell` option places the C-grid zonal points exactly on the equator, and `--rotate_poly` calculates polar polygon areas using rotated copies away from the pole.

!!! info
    A precomplied version of `make_hgrid` is available in `model-tools/fre-nctools` module. To load this module:
        
    ```bash
    module use /g/data/vk83/modules
    module load model-tools/fre-nctools/2024.05-1
    ```
    

However refer to the metadata of the latest `ocean_hgrid.nc` to find the latest setup.

Secondly, an _ESMF Mesh_ file is [derived](https://github.com/COSIMA/om3-scripts/blob/main/mesh_generation/generate_mesh.py) from the MOM supergrid. 
The MOM supergrid file is used by the MOM and CICE model components, whilst the ESMF Mesh file is used in the coupler. 
(Additional ESMF mesh files exist for the data atmosphere and runoff components). How to configure these in the model is captured in the [configurations](/configurations/Overview.md) page.

For analysis, it's best to use model grids output by the models:

- MOM6 outputs the model grid, [typically](https://github.com/ACCESS-NRI/access-om3-configs/blob/6c0942224adf8cd4644927ad357b68827e837dd9/diagnostic_profiles/diag_table_standard#L13C2-L13C24) in a file named _access-mom6.static..._
- CICE6 also outputs the model grid, in a file named `access-om3.cice.static.nc`

If you are using coupler diagnostics (off by default), note that the grid areas used in the coupler are calculated internally and 
are subtly different to the grid areas used in the model components. The model component caps [apply a correction](https://escomp.github.io/CMEPS/versions/master/html/introduction.html#area-corrections) between
model areas and mediator areas. 

## Vertical grid

In the ocean model, we use a [75-level vertical grid](https://github.com/COSIMA/om3-scripts/blob/main/grid_generation/generate_vertical_grid.py), unchanged from many OM2 configurations, following Stewart et al. (2017)[@StewartHoggGriffiesHeerdegenWardSpenceEngland2017a].

The vertical spacing is generated using:

$\Delta z(z) = \Delta z_{\max}\\tanh\left(-\frac{2\pi}{S_h} H_{\max}\right) + \varepsilon$

where \( \varepsilon = 10^{-3}\,\text{m} \).  

The parameters used to generate the vertical grid correspond to:

- \( H_{\max} = 6000m \) — maximum ocean depth  
- \( \Delta z_{\max} = 200m \) — maximum layer thickness at depth  
- \( \Delta z_{\min} = 1m \) — minimum layer thickness at the surface  
- \( S_h \approx 1.101 \) — dimensionless stretching parameter controlling the “knee” depth and steepness of the tanh profile  

These settings reproduce the standard OM2/OM3 75-level vertical grid used in ACCESS-OM2 and ACCESS-OM3 configurations.

## Aditional reading:

- [Cheat sheet for using a Mosaic grid with MOM6 output](https://gist.github.com/adcroft/c1e207024fe1189b43dddc5f1fe7dd6c#file-cheat-sheet-for-using-a-mosaic-grid-with-mom6-output-ipynb)
- [Gridspec: A standard for the description of grids used in Earth System models](https://www.researchgate.net/publication/228641121_Gridspec_A_standard_for_the_description_of_grids_used_in_Earth_System_models) <!-- https://extranet.gfdl.noaa.gov/~vb/pdf/gridstd.pdf is busted? -->
