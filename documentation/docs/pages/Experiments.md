
<!-- some hacks to hide the table of contents and make the links sidebar smaller, 
so the table has more screen real estate -->
<style>
.md-sidebar--secondary:not([hidden]){
  display: none 
}

.md-sidebar {
    width: 8rem
}

</style>

# ACCESS-OM3 Experiments

The below lists are key experiments that are being used to improve, evaluate and drive development for OM3. We welcome scientific and technical feedback on these runs. If you would like to get involved in evaluation of these runs, see instructions [here](https://github.com/acCESS-Community-Hub/access-om3-paper-1/) and an overview [here](/contributing/#help-us-evaluate-and-improve-applications-of-om3). 

As these data are from beta releases of configurations, they will not be kept long-term and will be deleted when newer control experiments are completed.

This data, and the configurations they are based on, are licensed by 
[CC-by-4.0](https://creativecommons.org/licenses/by/4.0/) and therefore can be freely shared, 
distributed and modified. Users of ACCESS-NRI models, data, tools or expert support are required
 to clearly include an [acknowledgement](https://www.access-nri.org.au/resources/acknowledging-us/)
  in all publications/reports/public releases.


|Experiment | Base Configuration                                                                                                          | Date completed | Description                                   | Model build                                                                      | Length (years)       | ESM Datastore <br/>  (output path)                                                               |
|----| --------------------------------------------------------------------------------------------------------------------------- | -------------- | --------------------------------------------- | -------------------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------ |
|[MC_25km_jra_ryf-1.0-beta-cdfb3543](https://github.com/ACCESS-Community-Hub/access-om3-experiments/tree/MC_25km_jra_ryf-1.0-beta-cdfb3543) | [release-MC_25km_jra_ryf](https://github.com/ACCESS-NRI/access-om3-configs/tree/4429156d3bb1ad4e04f41be8a90329684365786d) | 9-Aug-25       | Control experiment for model validation | [2025.05.001](https://github.com/ACCESS-NRI/ACCESS-OM3/releases/tag/2025.05.001) | 52 years             | `/g/data/ol01/outputs/access-om3-25km/MC_25km_jra_ryf-1.0-beta-cdfb3543/experiment_datastore.json` <br/> (`/g/data/ol01/outputs/access-om3-25km/MC_25km_jra_ryf-1.0-beta-cdfb3543/`)|
|[25km-iaf-test-for-AK-expt-7df5ef4c](https://github.com/ACCESS-Community-Hub/access-om3-experiments/tree/25km-iaf-test-for-AK-expt-7df5ef4c) | [25km-iaf-test-for-AK](https://github.com/ACCESS-NRI/access-om3-configs/tree/96ae801c9f2d786bb710a3cb0a29a05e0ab471c2)                          | 16-Sep-25      | Control experiment for model validation | [2025.05.001](https://github.com/ACCESS-NRI/ACCESS-OM3/releases/tag/2025.05.001) | 66 years (1958-2023) | `/g/data/ol01/outputs/access-om3-25km/25km-iaf-test-for-AK-expt-7df5ef4c/datastore.json`  <br/> (`/g/data/ol01/outputs/access-om3-25km/25km-iaf-test-for-AK-expt-7df5ef4c/`) |
|[MC_25km_jra_iaf-1.0-beta-5165c0f8](https://github.com/ACCESS-Community-Hub/access-om3-experiments/tree/MC_25km_jra_iaf-1.0-beta-5165c0f8) | [dev-MC_25km_jra_iaf](https://github.com/ACCESS-NRI/access-om3-configs/tree/f1307b65ee6b06ad9e92a560ae64bc0b4c91e6ee)                          | started 9-Dec-25      | Control experiment for model validation | [2025.08.001](https://github.com/ACCESS-NRI/ACCESS-OM3/releases/tag/2025.08.001) | 57 years (1958-2014) ([crashed](https://github.com/ACCESS-NRI/access-om3-configs/issues/1010#issuecomment-3672861969)) | `/g/data/ol01/outputs/access-om3-25km/MC_25km_jra_iaf-1.0-beta-5165c0f8/datastore.json`  <br/> (`/g/data/ol01/outputs/access-om3-25km/MC_25km_jra_iaf-1.0-beta-5165c0f8/`) |
| [MC_100km_jra_ryf+wombatlite-1e74abf-11f9df5c](https://github.com/ACCESS-Community-Hub/access-om3-experiments/tree/MC_100km_jra_ryf%2Bwombatlite-1e74abf-11f9df5c) | [dev-MC_100km_jra_ryf+wombatlite](https://github.com/ACCESS-NRI/access-om3-configs/tree/1e74abf43317d25dcd2c82d681a13cbb7b1b60ed) | 19-Dec-25  | Control experiment for model validation | [2025.08.001](https://github.com/ACCESS-NRI/ACCESS-OM3/releases/tag/2025.08.001) | 50 years | `/g/data/ol01/outputs/access-om3-100km/MC_100km_jra_ryf+wombatlite-1e74abf-11f9df5c/experiment_datastore.json`  <br/> (`/g/data/ol01/outputs/access-om3-100km/MC_100km_jra_ryf+wombatlite-1e74abf-11f9df5c`) |
| [MC_25km_jra_ryf+wombatlite-81ad20e-c4347f5a](https://github.com/ACCESS-Community-Hub/access-om3-experiments/tree/MC_25km_jra_ryf%2Bwombatlite-81ad20e-c4347f5a) | [dev-MC_25km_jra_ryf+wombatlite](https://github.com/ACCESS-NRI/access-om3-configs/tree/81ad20ec37661632dd8d7859ef6d6ded7f90664b) | 22-Dec-25  | Control experiment for model validation | [2025.08.001](https://github.com/ACCESS-NRI/ACCESS-OM3/releases/tag/2025.08.001) | 30 years | `/g/data/ol01/outputs/access-om3-25km/MC_25km_jra_ryf+wombatlite-81ad20e-c4347f5a/experiment_datastore.json`  <br/> (`/g/data/ol01/outputs/access-om3-25km/MC_25km_jra_ryf+wombatlite-81ad20e-c4347f5a`) |