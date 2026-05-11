# Standalone WW3 ERA5 + DICE

This case runs standalone ACCESS-OM3/WW3 forced by ERA5 DATM, with CDEPS/DICE providing ERA5 sea-ice concentration to WW3 through the mediator as `Si_ifrac`.

Use the WW3-only executable selected in `config.yaml`:

```bash
module use /g/data/vk83/prerelease/modules
module load payu

./payu_setup_dice.sh
./payu_run_dice.sh
```

Do not use plain `payu run` for this case unless payu has native `dice` component metadata. `payu_run_dice.sh` sets `PAYU_PATH` to the local shim in `payu-dice-bin/`, which adds the missing DICE metadata without modifying the installed payu module.

Files:

- `dice_in`: DICE namelist. Uses `datamode = "ssmi_iaf"` on the ACCESS-OM2 100 km mesh.
- `dice.streams.xml`: ERA5 sea-ice stream definition. Reads `./INPUT/YYYY/ci_era5_oper_sfc_*.nc` and maps ERA5 `siconc` to CDEPS `Si_ifrac`.
- `payu_setup_dice.sh`: setup workaround for current payu. It temporarily lets payu setup proceed, then restores `ICE_model = dice` in control/work and copies `dice_in` and `dice.streams.xml` into `work/`.
- `payu_run_dice.sh`: run wrapper. Loads prerelease payu and submits with the local DICE-aware payu shim.

Useful checks after launch:

```bash
rg -n "Si_ifrac|siconc|ice fields|Prescribed ice" work/log
/apps/nco/5.0.5/bin/ncwa -O -y max -a time,ny,nx -v ICE work/access-om3.ww3.hi.*.nc /tmp/ice_max.nc
```
