
<!-- some hacks to hide the table of contents and make the links sidebar smaller, 
so the table has more screen real estate -->
<style>
.md-sidebar--secondary:not([hidden]){
  display: none 
}

.md-sidebar {
    width: 8rem
}

.md-typeset table td:first-child,
.md-typeset table th:first-child {
  max-width: 200px;
}

.md-typeset table td:last-child,
.md-typeset table th:last-child {
  min-width: 200px;
}

</style>

# ACCESS-OM3 Experiments

The below lists key experiments that are being used to improve, evaluate and drive development for OM3. We welcome scientific and technical feedback on these runs. If you would like to get involved in evaluation of these runs, see instructions [here](https://github.com/acCESS-Community-Hub/access-om3-paper-1/) and an overview [here](/contributing/#help-us-evaluate-and-improve-applications-of-om3). 

As these data are from beta releases of configurations, they will not be kept long-term and will be deleted when newer control experiments are completed.

This data, and the configurations they are based on, are licensed by 
[CC-by-4.0](https://creativecommons.org/licenses/by/4.0/) and therefore can be freely shared, 
distributed and modified. Users of ACCESS-NRI models, data, tools or expert support are required
 to clearly include an [acknowledgement](https://www.access-nri.org.au/resources/acknowledging-us/)
  in all publications/reports/public releases.


{#- Rows come from experiments.yaml (next to this file). Edit that file to add or change an experiment. -#}
{%- set CONFIG = "https://github.com/ACCESS-NRI/access-om3-configs/tree/" -%}
{%- set BUILD = "https://github.com/ACCESS-NRI/ACCESS-OM3/releases/tag/" -%}

{%- macro store(e) -%}
{#- Buttons that copy the datastore path and the experiment's output folder (blank if not given) -#}
{%- if e.get('datastore') -%}
{%- set folder = e.datastore.rsplit('/', 1)[0] ~ '/' -%}
<button type="button" class="exp-copy" data-copy="{{ e.datastore }}" title="{{ e.datastore }}">Copy datastore path</button> <button type="button" class="exp-copy" data-copy="{{ folder }}" title="{{ folder }}">Copy output path</button>
{%- endif -%}
{%- endmacro -%}

{%- macro hidden(e) -%}
{#- These properties are available to be filtered by, but not shown in the table -#}
{{ e.nominal_resolution }} | {{ e.forcing }} | {{ e.components | join(' + ') }}
{%- endmacro %}

{#- Component combinations that exist in the YAML, e.g. "MOM6 + CICE + WOMBATLite" -#}
{%- set combos = experiments | map(attribute='components') | map('join', ' + ') | unique | sort -%}
{#- Resolutions that exist in the YAML, smallest first (values are "<number> km", see experiments.schema.json) -#}
{%- set resolutions = experiments | map(attribute='nominal_resolution') | map('replace', ' km', '') | map('int') | unique | sort -%}

<div class="exp-filter">
<label>Search <input type="search" autocomplete="off" data-filter="search" placeholder="name, build, description..."></label>
<label>Components <select autocomplete="off" data-filter="Components"><option value="">Any</option>{% for c in combos %}<option>{{ c }}</option>{% endfor %}</select></label>
<label>Resolution <select autocomplete="off" data-filter="Resolution"><option value="">Any</option>{% for r in resolutions %}<option>{{ r }} km</option>{% endfor %}</select></label>
<label>Forcing <select autocomplete="off" data-filter="Forcing"><option value="">Any</option><option>JRA-IAF</option><option>JRA-RYF</option><option>ERA-IAF</option></select></label>
</div>

<div class="exp-table" markdown>

| Experiment | Evaluation | Base Configuration | Date | Description | Model build | Length (years) | ESM Datastore | Resolution | Forcing | Components |
|----|----|----|----|----|----|----|----|----|----|----|
{% for e in experiments if e.group == 'control' -%}
| [{{ e.experiment }}]({{ e.runlog }}) | {% if e.get('evaluation') %}[Evaluation]({{ e.evaluation }}){% endif %} | [{{ e.config.get('branch') or e.config.commit[:7] }}]({{ CONFIG ~ e.config.commit }}) | {{ e.date }} | {{ e.get('description', '') }} | [{{ e.build }}]({{ BUILD ~ e.build }}) | {{ e.years }} | {{ store(e) }} | {{ hidden(e) }} |
{% endfor %}

</div>

## Community run sensitivity tests

The following are additional sensitivity-test experiments, exploring specific parameter choices rather than serving as control experiments. As these experiments are for specific interests, we do not necessarily track the same level of detail for these runs.

<div class="exp-table" markdown>

| Experiment | Evaluation | Base Configuration | Date | Model build | Length (years) | ESM Datastore | Resolution | Forcing | Components |
|----|----|----|----|----|----|----|----|----|----|
{% for e in experiments if e.group == 'community' -%}
| [{{ e.experiment }}]({{ e.runlog }}) | {% if e.get('evaluation') %}[Evaluation]({{ e.evaluation }}){% endif %} | [{{ e.config.get('branch') or e.config.commit[:7] }}]({{ CONFIG ~ e.config.commit }}) | {{ e.date }} | [{{ e.build }}]({{ BUILD ~ e.build }}) | {{ e.years }} | {{ store(e) }} | {{ hidden(e) }} |
{% endfor %}

</div>
