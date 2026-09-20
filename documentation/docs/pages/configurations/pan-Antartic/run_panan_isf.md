# How to run ACCESS-OM3 ice shelf configurations

Please see https://github.com/claireyung/mom6-panAn-iceshelf-tools/wiki for notes

Also refer to previous notes on the ACCESS-rOM3 panantarctic with no ice shelves here: https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc2-sapphirerapid-Charrassin-newparams-rerun-Wright-spinup-accessom2IC-yr9/panantarctic_instructions.md

**Important**: requires small timestep at the start, may need more walltime, but with default number of cores should fit within normalsr 10 hr limit 

**Also important**: Code changes are required, see https://github.com/ACCESS-NRI/MOM6/issues/29 and branch https://github.com/ACCESS-NRI/MOM6/tree/ice-shelf-dev

**Also important**: If changing files, think carefully about masks and coverage. See Claire's notes/contact her if you have questions. Otherwise you might allow the ocean to talk to the atmos in the ice shelf cavities, or have sea ice grow there... 

# Instructions for starting from rest
### Step 1: run for 1 month from rest
- In `MOM_input` set `DT = 150`, `DT_THERM = 150`
- In `input.nml` set `input_filename = 'n'`
- Change coupling timestep at corner of `nuopc.runseq` to also be 150
- To save ICs, use `SAVE_INITIAL_CONDS = True` in `MOM_input`
- do `payu setup`, `payu sweep`, `payu run` etc

### Step 2: run for February 
- Comment out `input.nml` `input_filename = 'n'`
- Change `DT`, `DT_THERM` and coupling timestep to be 400 (should work - otherwise try something in between eg 300)
- You can also set `DT_THERM` to be larger, e.g. 800
- Turn off IC saving with `SAVE_INITIAL_CONDS = False` in `MOM_input`
- run - now you can use `payu run -n XX`
- decrease walltime to 4 hours in config.yaml


# Instructions for starting from a restart
- Use `payu checkout --restart path/to/restart` (this should already be in the config.yaml)
- Jan 1 1901 restart from [this](https://github.com/claireyung/access-om3-configs/tree/ice_shelf_panan-nancheck3-150925files-notidalmix) run is saved here: `/g/data/ol01/cy8964/access-om3/restart/ice_shelf_panan-nancheck3-150925files-v2-notidalmix/restart012` 
- E.g.
```
payu checkout dev-MC_4km_jra_ryf+regionalpanan+isf+draft --restart /g/data/ol01/cy8964/access-om3/restart/ice_shelf_panan-nancheck3-150925files-v2-notidalmix/restart012
```
- Run - ensure DT is 400 (ish), input.nml has `input_filename = 'n'` commented out, CLOCK time in nuopc.runconfig is months

# Other tips
- If it crashes, drop the timestep - can check MOM CFL issues in `work/log/ocn.log`
- Might find a resub script helpful - usually it takes about 5 segfaults straight after initialisation until it finally wants to run :( e.g. https://github.com/claireyung/access-om3-configs/blob/8km_jra_ryf_obc2-sapphirerapid-Charrassin-newparams-rerun-Wright-spinup-accessom2IC-yr9/resub.sh and add `    error: resub.sh    run: rm -f resubmit.count` to `userscripts` section of `config.yaml`
