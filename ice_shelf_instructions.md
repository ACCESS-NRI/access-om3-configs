# Ice shelf instructions

Please see https://github.com/claireyung/mom6-panAn-iceshelf-tools/wiki for notes

Also refer to previous notes on the ACCESS-rOM3 panantarctic with no ice shelves here: https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc2-sapphirerapid-Charrassin-newparams-rerun-Wright-spinup-accessom2IC-yr9/panantarctic_instructions.md

**Important**: requires small timestep at the start, so running for a month will go over the allowed wall time. Therefore I run the first month in two steps. 

**Also important**: Code changes are required, see https://github.com/ACCESS-NRI/MOM6/issues/29 and branch https://github.com/ACCESS-NRI/MOM6/tree/ice-shelf-dev

**Also important**: If changing files, think carefully about masks and coverage. See Claire's notes/contact her if you have questions. Otherwise you might allow the ocean to talk to the atmos in the ice shelf cavities, or have sea ice grow there... 

# Instructions for starting from rest
### Step 1: run for 5 days from rest
- Remove the restart at the end of config.yaml
- In `MOM_override` set `DT = 150`, `DT_THERM = 150`
- In `input.nml` set `input_filename = 'n'`
- Use the `diag_table` for daily only diagnostics, otherwise this will bite you later since intake will load these NaN filled empty monthly netcdfs: 
`ln -s diagnostic_profiles/diag_table_isf_daily_only diag_table `
- Change coupling timestep at corner of `nuopc.runseq` to also be 150
- Change runtime in `CLOCK` section of `nuopc.runconfig` to be `ndays` and `5` for `stop_n`, `restart_n`, `stop_option`, `restart_option` etc
- do `payu setup`, `payu sweep`, `payu run` etc

### Step 2: run for 26 more days
- Comment out `input.nml` `input_filename = 'n'`
- Change `DT`, `DT_THERM` and coupling timestep to be 400 (should work - otherwise try something in between eg 300)
- Change `CLOCK` runtime in `nuopc.runconfig` to 26 days
- run

### Step 3: run February as normal
- Change `diag_table` to use monthly diagnostics: `ln -s diagnostic_profiles/diag_table_isf diag_table`
- Change runtime in `CLOCK` section of `nuopc.runconfig` to use `nmonths`, and `1` for `stop_n`, `restart_n`, `stop_option`, `restart_option` etc
- Hopefully it runs

# Instructions for starting from a restart
- Use `payu checkout --restart path/to/restart` (this should already be in the config.yaml)
- Jan 1 1901 restart from [this](https://github.com/claireyung/access-om3-configs/tree/ice_shelf_panan-nancheck3-150925files-notidalmix) run is saved here: `/g/data/ol01/cy8964/access-om3/restart/ice_shelf_panan-nancheck3-150925files-v2-notidalmix/restart012` 
- E.g.
```
payu checkout dev-MC_4km_jra_ryf+regionalpanan+isf+draft --restart /g/data/ol01/cy8964/access-om3/restart/ice_shelf_panan-nancheck3-150925files-v2-notidalmix/restart012
```
- Run - ensure diag table is `diag_table_isf`, DT is 400 (ish), input.nml has `input_filename = 'n'` commented out, CLOCK time in nuopc.runconfig is months

# Other tips
- If it crashes, drop the timestep - can check MOM CFL issues in `work/log/ocn.log`
- Might find a resub script helpful - usually it takes about 5 segfaults straight after initialisation until it finally wants to run :( e.g. https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc2-sapphirerapid-Charrassin-newparams-rerun-Wright-spinup-accessom2IC-yr9/resub.sh and add `    error: resub.sh    run: rm -f resubmit.count` to `userscripts` section of `config.yaml`
