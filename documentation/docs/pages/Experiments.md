
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
| Configuration | Date completed   |Description |  Model build |Length (years) | ESM Datastore (path) |  
| ---- | ---- | ---- | ---- | ---- | ---- | 
| [release-MC_25km_jra_ryf](https://github.com/ACCESS-NRI/access-om3-configs/commit/4429156d3bb1ad4e04f41be8a90329684365786d)| 9 Aug 2025      | Control experiment for model validation (RYF) | [2025.05.001](https://github.com/ACCESS-NRI/ACCESS-OM3/releases/tag/2025.05.001) | 52 years          | `/g/data/ol01/access-om3-output/access-om3-025/MC_25km_jra_ryf-1.0-beta/experiment_datastore.json` (`/g/data/ol01/access-om3-output/access-om3-025/MC_25km_jra_ryf-1.0-beta/`)       | 
|  [25km-iaf-test-for-AK](https://github.com/ACCESS-NRI/access-om3-configs/tree/25km-iaf-test-for-AK) |16 Sep 2025 | Control experiment for model validation (IAF) | [2025.05.001](https://github.com/ACCESS-NRI/ACCESS-OM3/releases/tag/2025.05.001)  | 66 years (1958-2023)  | `/g/data/ol01/access-om3-output/access-om3-025/25km-iaf-test-for-AK-expt-7df5ef4c/datastore.json` (`/g/data/ol01/access-om3-output/access-om3-025/25km-iaf-test-for-AK-expt-7df5ef4c/`) | 
