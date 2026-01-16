## Tips and tricks

### How to interpret truncation log files

Below is a line by line explanation for each output line in the truncation files

```
Time  1900 290  2.85 V-velocity violation at 1207:  37 16 (  58.28 E   70.49 N) Layers  13 to  14. dt =  1080.
```

```
1900: year,
290: day,
2.85: time -> 2(hours), 51(0.85*60)minutes, 0 seconds,
1207: processor id,
37 16: local lon, lat index in that processor,
58.28 E 70.49 N: geolon, geolat,
13 to 14: vertical layers,
1080: timestep
```

```
v(m):   2.897E+00  2.926E+00  -> updated meridional velocity
v(3):   2.699E+00  2.720E+00  ->  averaged meridional velocity over this timestep
CFL v:  5.001E-01  5.051E-01 ->  CFL based on open zonal grid spacing at v points
CFL0 v: 5.001E-01  5.052E-01 ->  CFL based on dy at v points
CAv:   -1.067E-01 -7.923E-02 -> Net acceleration resulting from the combined Coriolis and advection terms over the timestep
PFv:    3.982E-01  4.381E-01 -> Meridional pressure force acceleration over the timestep
diffv: -1.377E-01 -1.341E-01 -> Meridional diffusive acceleration over the timestep
a:      5.175E-01  5.772E-01  5.654E-01 -> Layer coupling coefficient
hvel:   2.183E+00  2.458E+00 -> Layer thickness at v points
Stress:   6.744E-01-> surface wind stress
dvbt:   9.098E-02  9.102E-02 -> Barotropic v acceleration
Below shows variables at neighbouring points for the layer thickness h only.
--: i, j-1, k
+-: i+1, j-1, k
-+: i-1, j, k
++: i+1,j+1,k
0-: i,j,k
0+: i,j+1,k

h--:    1.415E+00  1.066E+00
h0-:    1.284E+00  1.357E+00
h+-:    7.723E-03  1.409E-03
h-+:    2.149E+00  6.346E+00
h0+:    3.172E+00  3.703E+00
h++:    9.996E-04  1.003E-03
e-:    -1.644E+01 -1.772E+01 -1.908E+01  -> (i,j) estimate of interface heights based on the sum of thickness
e+:    -3.156E+01 -3.473E+01 -3.844E+01  -> (i+1,j)
T-:     1.208E+00  1.119E+00 -> (i,j) temperature
T+:     1.952E+00  1.641E+00 -> (i+1,j)
S-:     3.353E+01  3.364E+01 -> (i,j) salinity
S+:     2.989E+01  3.217E+01 -> (i+1,j)
uh--:  -1.628E-01 -1.977E-01  zonal transport at i-1, j,k
 uhC--: -1.619E-01 -1.949E-01 averaged zonal transport between i,j,k and i-1, j,k over this timestep
uh-+:   1.683E+00  2.203E+00  i-1,j+1,k
 uhC-+:  1.753E+00  1.967E+00 averaged zonal transport between the local point (i,j,k) and i-1, j,k over this timestep
uh+-:   9.218E-04  8.521E-04 i,j,k
 uhC+-:  9.845E-04  8.517E-04 averaged zonal transport between the local point (i,j,k) and i+1, j,k over this timestep
```

uh++:  -1.980E-06 -1.907E-06 i,j+1,k
 uhC++: -7.857E-04 -8.803E-04 averaged zonal transport between the local point (i,j+1,k) and i+1, j+1,k over this timestep
D:      5.911E+01 7.093E+01-> water depth i,j and i,j+1
