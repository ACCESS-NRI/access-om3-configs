## Building `access-om3` executable (optional)

You probably won't need to build the model yourself. ACCESS-OM3 configurations are already set up to use precompiled executables from the latest stable release. Precompiled executables from other [releases](Releases.md) are also available.

However, if you want to make code changes you'll need to [build access-om3](Building.md) yourself.


## Downloading a configuration

Configurations that use the same combination of model components (MOM6, CICE6 and/or WW3) are stored as separate branches in a single repository, as [listed here](configurations/Configurations.md).
The main branch within each of these repositories is just documentation. To get a working configuration you need to check out one of the branches with the resolution and forcing details you need, as explained in the README of the configuration repo. It's also best to create your own fork and clone that, so you can back up your work there.

For example, to run a `MOM6-CICE6` configuration under RYF JRA55-do forcing (i.e. the `1deg_jra55do_ryf` branch):
1. [fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the repo https://github.com/ACCESS-NRI/access-om3-configs on GitHub (if you haven't already), unchecking the "Copy the main branch only" box so you get all the configuration branches
2. choose a unique name for your experiment, e.g. `my_1deg_jra55do_ryf_experiment_name`
3. `cd` to somewhere in your `/home` directory on Gadi (since this is [the only filesystem that's backed up](https://opus.nci.org.au/pages/viewpage.action?pageId=90308816))
4. clone the config from your fork: `git clone git@github.com:<username>/access-om3-configs.git my_1deg_jra55do_ryf_experiment_name` (where `<username>` is your GitHub user name)
5. `cd my_1deg_jra55do_ryf_experiment_name`
6. check out the branch of interest: `git checkout dev-1deg_jra55do_ryf`
7. check out a new branch to store your run: `git checkout -b my_1deg_jra55do_ryf_experiment_name` so you can use git to easily see how your run configuration differs from the original
8. edit `config.yaml` to set the following flags. These will record your configuration settings in the git history as the run proceeds, and also generate a unique identifier for your experiment.
```yaml
runlog: true
metadata:
  enable: true
```
9. If you've compiled your own executable you'll also need to edit the [`exe`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fconfig.yaml+exe:&type=code) entry in `config.yaml` to point to it.

## Customising your experiment
You may want change the run length. This is determined by [`stop_n`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+stop_n&type=code) and [`stop_option`](https://github.com/search?q=repo%3AACCESS-NRI%2Faccess-om3-configs+path%3Adoc%2Fnuopc.runconfig+stop_option&type=code) in `CLOCK_attributes` in `nuopc.runconfig`; available units for `stop_option` are listed [here](https://escomp.github.io/CMEPS/versions/master/html/generic.html).
See the [Configurations](configurations/Configurations.md) section to find out how to set other parameters.

Before running, commit your changes with an informative message, e.g. `git commit -am "initial setup for experiment to test... bla bla"`

## Running

Running ACCESS-OM3 requires an updated `payu`, available from the `vk83` project - apply [here](https://my.nci.org.au/mancini/project/vk83) if you're not yet a member. You then need to do the following before you can run (only needs to be done once per log in, or you can put this in your `~/.bash_profile` to do it automatically each login):
```
module use /g/data/vk83/modules
module load payu
```

Now you're ready to run:
```
payu run
```

This uses the [payu](https://github.com/payu-org/payu) workflow management tool to prepare the run and submit it as a job to the PBS job queue. See the [Gadi User Guide](https://opus.nci.org.au/display/Help/Gadi+User+Guide) to learn more about PBS job management.

Check the status of the job (state 'Q'=waiting in queue, 'R'=running, 'E'=exiting, 'H'=held) with
```
#this is needed for uqstat to be available 
module use /g/data/hh5/public/modules
module load nci-scripts

uqstat -c
```

While it's running, you can check the date it's up to with
```
grep date work/log/med.log
```

To kill the run early, do `qdel N`, where N is the job number (first column given by `uqstat`). If you kill the job (or it crashes), a `work` directory will be left behind after the job has disappeared from `uqstat` and you'll need to do `payu sweep` before you can run again.

When your run has finished successfully, payu puts its output in `archive/output000` and removes the `work` directory. payu also records a log of your experiment in the git history, including the identity of the inputs and executables used (see the files in `manifests`).

To do another run, just type `payu run` again. Or to do (say) 10 runs, type `payu run -n 10` and they'll automatically be submitted one after the other.

The outputs from each run will be in numbered subdirectories in `archive`.

Each run creates a `restart` directory in `archive` which is used as the initial condition for the next run. These restarts can accumulate and consume disk space, but only the most recent one is needed (unless you plan to restart a new experiment from an intermediate state).
See the [payu documentation](http://payu.readthedocs.io/en/latest) for more information.

If the run fails, the `work` directory will be retained. You can find diagnostic messages in `access-om3.*`, `MOM6-CICE6.[oe]*`, `work/log/*`, `work/logfile*` and other files in `work`. You will need to do `payu sweep` to delete the `work` directory before you will be able to do another `payu run`. This will also save copies of the PBS logs into `archive/pbs_logs`.

**WARNING** restarts and outputs are stored on `/scratch` and will therefore [be deleted if unread for 100 days](https://opus.nci.org.au/pages/viewpage.action?pageId=156434436), so if you value them you should move them somewhere safer, e.g. `/g/data`. Note that `/home` is the only filesystem that is backed up, so your configuration should live there, but you probably won't have room for outputs and restarts.
If you put a [`sync`](https://payu.readthedocs.io/en/latest/config.html#postprocessing) section in `config.yaml`, payu will automatically copy your files to a safe location you specify.