## MOM6 parameter choices

### Horizontal grid

The 25km global configuration uses a tripolar grid to avoid a singularity at the North Pole. The domain is zonally periodic `REENTRANT_X = True` and open at the north via a tripolar fold `TRIPOLAR_N = True` while closed in the south `REENTRANT_Y = False`. The horizontal grid has `1440x1142` tracer points. This matches the resolution of prior models (eg, ACCESS-OM2-025 and GFDL OM4/OM5) and provides eddy-permitting detail in the ocean while maintaining numerical stability.