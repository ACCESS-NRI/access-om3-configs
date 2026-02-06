## Tips and tricks

### MOM6 velocity truncations

#### 1. Background

MOM6 includes a safety mechanism to prevent numerical instability from excessively large velocities. In ACCESS-OM3 configurations, truncation is based on a CFL criterion ([`CFL_BASED_TRUNCATIONS = True`](https://github.com/ACCESS-NRI/access-om3-configs/blob/16b2eca8f711aee5cd5e64529fecacef61e5903e/docs/MOM_parameter_doc.all#L1517-L1518)), with the default trigger at [CFL > 0.5](https://github.com/ACCESS-NRI/access-om3-configs/blob/16b2eca8f711aee5cd5e64529fecacef61e5903e/docs/MOM_parameter_doc.all#L1519-L1521). When this threshold is exceeded, MOM6 truncates the velocity and writes a detailed diagnostic record to `U_velocity_truncations` and/or `V_velocity_truncations`, which lists all relevant terms in the momentum equation at the affected grid point. To prevent the model from continuing in an unstable state, MOM6 will abort the run if truncations occur too frequently, controlled by [`MAXTRUNC = 10000`](https://github.com/ACCESS-NRI/access-om3-configs/blob/16b2eca8f711aee5cd5e64529fecacef61e5903e/docs/MOM_parameter_doc.all#L2447-L2450).

#### 2. Interpret truncation log files

For provenance, the examples below use truncation records from the 25 km IAF experiment [MC_25km_jra_iaf-1.0-beta-5165c0f8](https://github.com/ACCESS-Community-Hub/access-om3-experiments/tree/MC_25km_jra_iaf-1.0-beta-5165c0f8).


The discussion here only focuses on `U_velocity_truncations` but `V_velocity_truncations` are similar:

```
Time  1958   0  1.88 U-velocity violation at 2009:  21  5 ( -65.25 E   61.37 N) Layers   1 to   1. dt =  900.0    

Layers:         1 
u(m):  -1.113E+01 
u(3):  -9.386E+00 
CFL u:  7.523E-01 
CFL0 u: 7.523E-01 
CAu:    1.183E+00 
PFu:    4.514E-02 
diffu:  8.407E-01 
a:      0.000E+00  2.155E-09 
hvel:   1.843E-02 
Stress:  -1.662E-01
dubt:  -4.312E-02 


h--:    4.495E-01 
h+-:    1.041E-01 
h-0:    3.484E-02 
h+0:    2.015E-03 
h-+:    2.473E-03 
h++:    1.000E-03 
e-:     3.032E-02 -4.524E-03 
e+:    -3.531E-02 -3.733E-02 
T-:    -1.702E+00 
T+:    -1.707E+00 
S-:     3.140E+01 
S+:     3.149E+01 
vh--:  -1.095E-01 
 vhC--:-1.907E+00 
vh-+:  -7.915E-03 
 vhC-+:-2.059E-01 
vh+-:  -3.593E-03 
 vhC+-:-5.881E-01 
vh++:   0.000E+00 
 vhC++: 0.000E+00 
D:      2.985E+02 2.019E+02
```

- The first line of the above `U_velocity_truncations` log entry gives the time and location.

    - `Time  1958   0  1.88`: Model time when truncation occurred. Here `1958` is the model year, `0` is the yearday, and `1.88` is the fractional day. A helper (`convert_to_date_time`) for converting this into a readable datetime is provided in [Examine_truncation_data.ipynb](https://github.com/ACCESS-NRI/access-eval-recipes/blob/main/ocean/Examine_truncation_data.ipynb).
    - `U-velocity violation`: Indicates truncation of the zonal velocity. Meridional truncations appears as `V-velocity violation`.
    - `2009:  21  5`: Indicates where the truncation occurred in the model decomposition. Here `2009` is the `processor id`, and the truncation happened at local grid indices (`i=21, j=5`) on that processor.
    - `( -65.25 E   61.37 N)`: The geographic longitude and latitude of the affected grid cell - global coordinates.
    - `Layers   1 to   1`: The vertical layer range affected. Here it is confined to layer 1 (the surface layer).
    - `dt =  900.0`: The model timestep (seconds) in use when the truncation was triggered.

- Velocities and CFLs

    - `u(m):  -1.113E+01;  u(3):  -9.386E+00 `: [`u(m)`](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L172-L173) is the updated zonal velocity (m/s) after completing the momentum solve over the baroclinic timestep. This value is used to evaluate the [CFL condition](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L181-L190) that triggers truncation. [`u(3)`](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L178-L179) is the time-averaged u-velocity (`u_av`, m/s) over the baroclinic timestep. It represents the reference baroclinic velocity used for transport, layer-thickness advection and construction of fluxes.
    - `CFL u:  7.523E-01; CFL0 u: 7.523E-01 `: [`CFL0 u`](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L188-L190) is the local CFL number at the `U` point using the local grid spacing, while [`CFL u`](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L181-L187) is the local CFL number scaled by the effective `T`-cell area adjacent to the `U` point. In this case, the two values are nearly identical, indicating locally uniform grid geometry. However, both exceed the default threshold (0.5), hence trigger velocity truncation.

- Momentum tendency contributions - reported as velocity changes (m/s)

    - All below tendency terms are scaled by `dt` and expressed as equivalent velocity increments to make their importance clear.
    - [`CAu:    1.183E+00 `](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/core/MOM_variables.F90#L147): Combined zonal Coriolis and horizontal advection contribution to the zonal momentum update.
    - [`PFu:    4.514E-02`](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/core/MOM_variables.F90#L149): Zonal pressure-gradient acceleration contribution.
    - [`diffu:  8.407E-01 `](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/core/MOM_variables.F90#L151): Zonal acceleration due to lateral viscosity.
    - [`a:      0.000E+00  2.155E-09 `](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L227-L230): Vertical viscosity layer coupling coefficients from vertvisc. For a single layer, two values are printed because the layer has an upper and lower interface.
    - [`hvel:   1.843E-02 `](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L231-L234): Scaled layer thickness at `U` grid points from vertvisc.
    - [`Stress:  -1.662E-01`](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L235-L237): Contribution from surface wind stress over the timestep.
    - [`dubt:  -4.312E-02 `](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L239-L243): Barotropic acceleration contribution to the baroclinic `U` velocity over one timestep. This term helps diagnose if the barotropic solver injects a large velocity into the baroclinic field.

- Layer thicknesses and interfaces

    - [`h--:    4.495E-01; h+-:    1.041E-01; h-0:    3.484E-02; h+0:    2.015E-03; h-+:    2.473E-03; h++:    1.000E-03 `](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L246-L257): These are the horizontal layer thicknesses (meters) sampled from surrounding tracer (`T`) cells. They define the effective layer thickness at the velocity point, which is used by the momentum equation to form the volume fluxes (`uh`/`vh`). In this case, `h+0 = 2.015E-03` and `h++ = 1.000E-03` are nearly zero, indicating local mass collapse. This strongly suggests that the truncation is driven by vanishing layer thickness instead of unusually large forcings. For example, `CAu` appears large, but this is the consequence of the collapsed `h` not an indication of excessive Coriolis forcing.
    - [`e-:     3.032E-02 -4.524E-03; e+:    -3.531E-02 -3.733E-02 `](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L260-L268): Vertical coordinates of layer interfaces for the left tracer column (`e-`) - the left side of the `U` point (`T(i,j)`), and `e+` to the column on the right (`T(i+1,j)`). Hence there are two values for either `e-` or `e+`.

- State variables

    - [`T-:    -1.702E+00; T+:    -1.707E+00; S-:     3.140E+01; S+:     3.149E+01 `](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L269-L280): temperature and salinity sampled in the left tracer column (`-`) and right tracer column (`+`) adjacent to the `U` point. These fields directly influence the pressure-gradient force at the truncation location. Here differences are small, indicating that a sharp T/S front is unlikely to be the primary cause of instability.

- Transport terms feeding the `U` momentum equation

    - [`vh--:  -1.095E-01;  vhC--:-1.907E+00; vh-+:  -7.915E-03;  vhC-+:-2.059E-01; vh+-:  -3.593E-03;  vhC+-:-5.881E-01; vh++:   0.000E+00;  vhC++: 0.000E+00 `](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L293-L339): Meridional mass fluxes (`vh--`, `vh-+`, `vh+-`, and `vh++`)  surrounding the `U` point, used to construct the meridional advection of zonal momentum, where terms with `C` represent reconstructed centered estimates.

- Bathymetry

    - [`D:      2.985E+02 2.019E+02`](https://github.com/ACCESS-NRI/MOM6/blob/3a82c07a999d51cf1cc645edd593d35871c2fba8/src/diagnostics/MOM_PointAccel.F90#L341): Local water depth at the two tracer columns that sits on either side of the `U` velocity point. In this case, the depth difference can create sharp pressure-gradient or thickness gradients and may provide important geometric context for the truncation.

#### 3. Read and plot truncation log output

- A [notebook](https://github.com/ACCESS-NRI/access-eval-recipes/blob/main/ocean/Examine_truncation_data.ipynb) is provided to demonstrate how to read, interpret, and visualise truncation log output.

### Payu cloning access-om3-configs quickly
`payuexp`: A trivial bash function to help one payu clone an access-om3-config. The idea is that one can very quickly run a new experiment and doesn't have to remember the full git urls/payu syntax.

```bash
function payuexp()
{
    if [[ ( $# -eq 0 ) || ( $1 == "--help" ) || ( $1 == "-h" ) ]] ; then
        echo "Usage:   payuexp BRANCH."
        echo "Purpose: clone an access-om3-config and path to the folder on Gadi (NCI)."
        echo "       "
        echo "Mandatory arguments: "
        echo "BRANCH:   branch on om3-configs we'll clone"
        echo "This:"
        echo "  payuexp dev-MC_100km_jra_ryf"
        echo "       "
        echo "Becomes:"
        echo "  payu clone -b expt -B dev-MC_100km_jra_ryf https://github.com/ACCESS-NRI/access-om3-configs dev-MC_100km_jra_ryf"
        echo "       "
        echo "To make payuexp available in your shell, copy the function into your shell startup file, such as '. ~/.bashrc' for bash then reload your environment by 'source ~/.bashrc'"
        return 1
    fi
    echo "We are payu cloning branch "$1
    echo ""
    module purge
    module use /g/data/vk83/modules
    module load payu
    module list
    work_dir=/g/data/$PROJECT/$USER/access-om3-runs
    mkdir -p $work_dir
    cd $work_dir
    payu clone -b expt -B $1 https://github.com/ACCESS-NRI/access-om3-configs $1
    echo ""
    cd $1
    CWD="$(pwd)"
    echo "Experiment folder is: "$CWD
    echo ""
}
```

For more complicated experiment generation operations take a look at the [experiment generator tool](https://access-experiment-generator.access-hive.org.au/). If you would like to only clone a repository, then this `gh` alias may be useful `'!gh repo clone access-nri/$1 -- --recursive && cd $1 && gh repo set-default access-nri/$1'`. This has the advantage that you do not have to remember the full url for the repository.

### Making small configuration updates using ACCESS Github cherry-pick workflow

Imagine one wants to update a few parameters across multiple configs. One option is to open multiple PRs, update checksums, get reviews, and merge them one by one. That works but it can be a bit slow. In these cases, It's faster to use the ACCESS Github cherry-pick workflow.

There are a number of advantages to this, when it works:

 - You don't need to manually apply the same change to multiple branches;
 - The cherry-picked PRs are opened by the access-bot so you can review and merge them yourself.

#### A GM example
We've done a series of tests with the MEKE GM parameters, documented [here](https://github.com/ACCESS-Community-Hub/access-om3-paper-1/blob/main/notebooks/GM-Testing-in-ACCESS-OM3.ipynb). In short, the original `1.0-beta` release yielded quite high GM values in the Southern Ocean that gave poor upwelling behaviour and we wanted to change the following parameters:

```
MEKE_KHTH_FAC = 0.3
MEKE_KHTR_FAC = 0.3
MEKE_VISCOSITY_COEFF_KU = 0.6
```

Here is a [PR](https://github.com/ACCESS-NRI/access-om3-configs/pull/1101) with the changes applied.

Here are the steps to use the Git Hub cherry-pick workflow

1. Open one PR to one config ([example](https://github.com/ACCESS-NRI/access-om3-configs/pull/1101)).
1. If answer-changing, update checksums with `!test repro commit`.
1. Get review and merge.
1. Use `!cherry-pick` workflow to cherry-pick changes (except for commit updating checksums) into other configs (see [example](https://github.com/ACCESS-NRI/access-om3-configs/pull/1098) and where it came [from](https://github.com/ACCESS-NRI/access-om3-configs/pull/1092#issuecomment-3815178906)). This will automatically open PRs for you.
1. Run `!test repro commit` in each of the cherry-picked PRs.
2. Review and merge.


