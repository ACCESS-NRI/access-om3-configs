
# Restart files

ACCESS-OM3 uses a directory of restart files to record how to initialise the model
when continuing or branching from an existing experiment.

## Changing Restart Dates

The current date and time corresponding to the model state is also saved in these
restart files. It may make sense to change this date in restart files, so that a
new experiment can use model state from one experiment while applying surface
forcing conditions from a different time. For example, a repeat cycle of an
inter-annual forcing (IAF) experiment reuses the model state from the end of the
previous cycle, but restarts the forcing from the beginning of the forcing period.

The `modify_restart_date.py` script handles this: it renames the restart
files, updates the internal date metadata that `cpl`/`cice` restarts carry,
and points your new experiment's `config.yaml` at the result. This script is run
in the configuration folder for a new experiment. To use this script:

1. Check out the configuration for the new experiment

    Use `payu clone` and specify the restart as the path to the directory of existing
    (unmodified) restart files

2. `cd` into the new experiment, double check the `restart:` path in `config.yaml` and run the script:
    ```bash
    python3 /g/data/vk83/apps/om3-scripts/restart_modifications/modify_restart_date.py --new_date <YYYY-MM-DD>
    ```
    `--new_date` defaults to `1958-01-01` if omitted.

    The `restart:` path will now be updated, and the modified restarts are in
    `initial_restart/` inside the configuration directory

3. Run the experiment
    ```bash
    payu sweep && payu run
    ```

!!! note
    The script doesn't currently support WavewatchIII (WW3) restarts.