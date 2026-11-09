/*
 * Experiment filter for the ACCESS-OM3-configs "Experiments" page (MkDocs Material).
 *
 * Adds toggle buttons above the experiment tables to filter rows by
 * resolution, forcing and the optional components (WW3, WOMBAT).
 *
 *  - Type: ACCESS-NRI = main experiment table, COSIMA = the "Community run sensitivity tests" table.
 *  - Within a group (resolution, forcing, type) buttons are OR'd:  25km OR 100km.
 *  - Components are AND'd:  WW3 + WOMBAT shows runs that have both.
 *  - Groups are AND'd with each other.
 *  - Rows are listed newest first when the table has a date or model build column
 *    (see sortNewestFirst); otherwise the page's own order is kept. A caret on that column
 *    shows the order and reverses it when clicked.
 *  - Selection is stored in the URL hash so a filtered view can be shared.
 *
 * Tags are inferred from the experiment name, base-configuration text and the
 * evaluation link slug, e.g.  MC_25km_jra_iaf+wombatlite-...  ->
 *   resolution 25km, forcing JRA-IAF, components MOM6 + CICE + WOMBAT.
 *   (MC = MOM6+CICE, MCW = MOM6+CICE+WW3)
 */
(function () {
  "use strict";

  // Only the optional components get a button: every run has MOM6 and CICE.
  var COMPONENTS = ["WW3", "WOMBAT"];
  // Always offered, even before any experiment at that resolution exists.
  var KNOWN_RESOLUTIONS = ["8km", "25km", "100km"];
  // Forcing = JRA55-do or ERA5 forcing, plus IAF/RYF for JRA55-do. A name with IAF/RYF and no
  // dataset is taken as JRA55-do (the original forcing).
  var KNOWN_FORCINGS = ["JRA-IAF", "JRA-RYF", "ERA5"];

  var CSS =
    ".exp-filter{display:flex;flex-wrap:wrap;gap:.4rem 1.2rem;align-items:center;margin:1em 0;padding:.6em .8em;" +
    "border:.05rem solid var(--md-default-fg-color--lightest);border-radius:.2rem;" +
    "position:sticky;top:2.8rem;z-index:2;background:var(--md-default-bg-color)}" +
    ".exp-filter__title{font-size:.8rem;margin-right:.2rem}" +
    ".exp-filter__btn--empty{opacity:.55}" +
    ".exp-filter__group{display:flex;flex-wrap:wrap;gap:.3rem;align-items:center}" +
    ".exp-filter__label{font-size:.7rem;font-weight:700;text-transform:uppercase;opacity:.7;margin-right:.2rem}" +
    // Own button styling (not .md-button, whose colours are fixed to the banner colour and unreadable in dark mode).
    ".exp-filter .exp-filter__btn{margin:0;padding:.15em .8em;font-family:inherit;font-weight:600;font-size:.72rem;line-height:1.6;" +
    "color:var(--md-default-fg-color);background:transparent;cursor:pointer;" +
    "border:.1rem solid var(--md-default-fg-color--light,currentColor);border-radius:.1rem}" +
    ".exp-filter .exp-filter__btn:hover{background:var(--md-default-fg-color--lightest)}" +
    ".exp-filter .exp-filter__btn:focus-visible{outline:2px solid var(--md-accent-fg-color,#01adee);outline-offset:2px}" +
    // Selected button: solid blue fill and a tick, readable in both themes.
    ".exp-filter button.exp-filter__btn.exp-filter__btn--on,.exp-filter button.exp-filter__btn.exp-filter__btn--on:hover{" +
    "background:var(--md-accent-fg-color,#01adee);border-color:var(--md-accent-fg-color,#01adee);color:#0b1620;font-weight:700}" +
    ".exp-filter__btn--on::before{content:'\\2713\\00a0'}" +
    ".exp-sortable{cursor:pointer;white-space:nowrap}.exp-sort{margin-left:.35em}" +
    ".exp-filter__count{font-size:.72rem;opacity:.75;margin-left:auto}";

  function tagsFor(row) {
    var cells = row.cells;
    var name = cells[0].textContent.trim();
    var haystack = [name];
    // Where the table has Evaluation / Base Configuration columns, they help when the
    // name is non-standard (e.g. "25km-iaf-test-for-AK-expt-..." whose evaluation slug
    // is mc_25km-iaf-...). Other columns (descriptions, costs) are never read.
    var head = row.closest("table").tHead;
    var heads = head ? head.rows[0].cells : [];
    for (var i = 1; i < cells.length; i++) {
      var h = (cells[i].querySelector("a") || {}).href || "";
      var col = heads[i] ? heads[i].textContent.trim().toLowerCase() : "";
      if (/^(evaluation|base config)/.test(col)) {
        haystack.push(cells[i].textContent);
        haystack.push(decodeURIComponent(h.split("/").slice(-2).join("/")));
      }
    }
    var s = haystack.join(" ").toLowerCase();

    var res = (s.match(/(\d+(?:\.\d+)?)\s*km/) || [])[1];
    var deg = (s.match(/(?:^|[^a-z0-9])(\d+(?:\.\d+)?)deg/) || [])[1];
    var resolution = res ? res + "km" : deg ? deg + "deg" : null;

    var f = s.match(/(?:^|[^a-z])(ryf|iaf)(?![a-z])/);
    var d = s.match(/(?:^|[^a-z0-9])(jra|era5?)(?![a-z])/);
    var forcing = null;
    if (d && d[1] !== "jra") forcing = "ERA5";
    else if (f) forcing = "JRA-" + f[1].toUpperCase();

    var comps = {};
    var mc = s.match(/(^|[^a-z])mc(w?)(?=[_-]?\d)/);
    if (mc) {
      comps.MOM6 = comps.CICE = true;
      if (mc[2]) comps.WW3 = true;
    }
    if (/mom6|mom/.test(name.toLowerCase())) comps.MOM6 = true;
    if (/cice/.test(s)) comps.CICE = true;
    if (/ww3|ww-3|wavewatch/.test(s)) comps.WW3 = true;
    if (/wombat/.test(s)) comps.WOMBAT = true;

    return { resolution: resolution, forcing: forcing, components: comps };
  }

  function keys(o) { return Object.keys(o); }

  function headingBefore(table, root) {
    var el = table;
    while (el && el !== root) {
      for (var p = el.previousElementSibling; p; p = p.previousElementSibling) {
        if (/^H[1-6]$/.test(p.tagName)) return p.textContent;
      }
      el = el.parentElement;
    }
    return "";
  }

  var MONTHS = { jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5, jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11 };

  function parseDate(text) {
    var m = text.match(/(\d{1,2})-([A-Za-z]{3})[a-z]*-(\d{2,4})/);
    if (!m || !(m[2].toLowerCase() in MONTHS)) return NaN;
    var y = +m[3];
    return Date.UTC(y < 100 ? 2000 + y : y, MONTHS[m[2].toLowerCase()], +m[1]);
  }

  function buildKey(text) {
    var m = text.match(/(\d{4})\.(\d{2})\.(\d{3})/);
    return m ? +m[1] * 1e6 + +m[2] * 1e3 + +m[3] : 0;
  }

  // Newest first: by "Date completed" when the table has one, then by model build,
  // then reverse listing order (new runs are normally added at the bottom).
  function sortNewestFirst(table) {
    var head = table.tHead ? table.tHead.rows[0].cells : [];
    var di = -1, bi = -1;
    for (var i = 0; i < head.length; i++) {
      var t = head[i].textContent.trim().toLowerCase();
      if (/^date/.test(t)) di = i;
      if (/^model build/.test(t)) bi = i;
    }
    if (di < 0 && bi < 0) return; // keep the page's own order
    var body = table.tBodies[0];
    var list = Array.prototype.map.call(body.rows, function (r, idx) {
      return {
        el: r, idx: idx,
        date: di >= 0 ? parseDate(r.cells[di].textContent) : NaN,
        build: bi >= 0 ? buildKey(r.cells[bi].textContent) : 0
      };
    });
    list.sort(function (a, b) {
      var d = (isNaN(b.date) ? 0 : b.date) - (isNaN(a.date) ? 0 : a.date);
      if (d) return d;
      if (b.build !== a.build) return b.build - a.build;
      return b.idx - a.idx;
    });
    list.forEach(function (x) { body.appendChild(x.el); });

    // A caret on the sorted column: down = newest first (the default); click to reverse.
    var th = head[di >= 0 ? di : bi];
    var caret = document.createElement("span");
    caret.className = "exp-sort";
    th.classList.add("exp-sortable");
    th.appendChild(caret);
    function label(newestFirst) {
      caret.textContent = newestFirst ? "\u25BE" : "\u25B4";
      th.title = newestFirst ? "Newest first. Click to show oldest first." : "Oldest first. Click to show newest first.";
      th.setAttribute("aria-sort", newestFirst ? "descending" : "ascending");
    }
    label(true);
    th.addEventListener("click", function () {
      var next = th.getAttribute("aria-sort") === "descending" ? false : true;
      Array.prototype.slice.call(body.rows).reverse().forEach(function (r) { body.appendChild(r); });
      label(next);
    });
  }

  function sortRes(a, b) {
    return parseFloat(a) - parseFloat(b);
  }

  function init() {
    var tables = Array.prototype.filter.call(document.querySelectorAll("article table"), function (t) {
      var th = t.querySelector("thead th");
      return th && /^experiment/i.test(th.textContent.trim());
    });
    if (!tables.length || document.getElementById("exp-filter")) return;

    var st = document.createElement("style");
    st.textContent = CSS;
    document.head.appendChild(st);

    tables.forEach(sortNewestFirst);

    var rows = [];
    var article = document.querySelector("article") || document.body;
    tables.forEach(function (t) {
      var type = /community/i.test(headingBefore(t, article)) ? "COSIMA" : "ACCESS-NRI";
      Array.prototype.forEach.call(t.tBodies[0].rows, function (r) {
        var tags = tagsFor(r);
        tags.type = type;
        rows.push({ el: r, tags: tags });
      });
    });

    var resolutions = {}, forcings = {}, types = {};
    var found = { Resolution: {}, Forcing: {}, Components: {} };
    KNOWN_RESOLUTIONS.forEach(function (k) { resolutions[k] = 1; });
    KNOWN_FORCINGS.forEach(function (k) { forcings[k] = 1; });
    rows.forEach(function (r) {
      types[r.tags.type] = 1;
      if (r.tags.resolution) { resolutions[r.tags.resolution] = 1; found.Resolution[r.tags.resolution] = 1; }
      if (r.tags.forcing) { forcings[r.tags.forcing] = 1; found.Forcing[r.tags.forcing] = 1; }
      Object.keys(r.tags.components).forEach(function (c) { found.Components[c] = 1; });
    });

    var state = { Resolution: {}, Forcing: {}, Components: {}, Type: {} };

    var bar = document.createElement("div");
    bar.id = "exp-filter";
    bar.className = "exp-filter";
    var title = document.createElement("strong");
    title.className = "exp-filter__title";
    title.textContent = "Filters";
    bar.appendChild(title);
    var count = document.createElement("span");
    count.className = "exp-filter__count";

    function group(label, values) {
      var g = document.createElement("div");
      g.className = "exp-filter__group";
      var l = document.createElement("span");
      l.className = "exp-filter__label";
      l.textContent = label;
      g.appendChild(l);
      values.forEach(function (v) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "exp-filter__btn";
        b.textContent = v;
        b.setAttribute("aria-pressed", "false");
        b.addEventListener("click", function () {
          if (state[label][v]) delete state[label][v]; else state[label][v] = true;
          apply();
        });
        if (found[label] && !found[label][v]) {
          b.classList.add("exp-filter__btn--empty");
          b.title = "No " + v + " experiments listed yet";
        }
        b.dataset.group = label;
        b.dataset.value = v;
        g.appendChild(b);
      });
      bar.appendChild(g);
    }

    group("Components", COMPONENTS);
    group("Resolution", Object.keys(resolutions).sort(sortRes));
    group("Forcing", Object.keys(forcings));
    if (keys(types).length > 1) group("Type", ["ACCESS-NRI", "COSIMA"]);

    var clear = document.createElement("button");
    clear.type = "button";
    clear.className = "exp-filter__btn exp-filter__clear";
    clear.textContent = "Clear";
    clear.addEventListener("click", function () {
      state = { Resolution: {}, Forcing: {}, Components: {}, Type: {} };
      apply();
    });
    bar.appendChild(clear);
    bar.appendChild(count);
    // Insert above the table's outermost wrapper (Material wraps tables in scroll
    // containers; inserting inside one would cover the header row).
    var root = tables[0].closest("article") || document.body;
    var anchor = tables[0];
    while (anchor.parentElement && anchor.parentElement !== root) anchor = anchor.parentElement;
    anchor.parentNode.insertBefore(bar, anchor);

    function matches(t) {
      var r = keys(state.Resolution), f = keys(state.Forcing), c = keys(state.Components), ty = keys(state.Type);
      if (r.length && r.indexOf(t.resolution) < 0) return false;
      if (f.length && f.indexOf(t.forcing) < 0) return false;
      if (ty.length && ty.indexOf(t.type) < 0) return false;
      return c.every(function (x) { return t.components[x]; });
    }

    function writeHash() {
      var parts = [];
      Object.keys(state).forEach(function (g) {
        var k = keys(state[g]);
        if (k.length) parts.push(g.toLowerCase() + "=" + k.map(encodeURIComponent).join(","));
      });
      var h = parts.length ? "#" + parts.join("&") : "";
      if (location.hash !== h) history.replaceState(null, "", location.pathname + location.search + h);
    }

    function readHash() {
      var h = location.hash.replace(/^#/, "");
      if (h.indexOf("=") < 0) return;
      h.split("&").forEach(function (p) {
        var kv = p.split("=");
        var g = Object.keys(state).filter(function (x) { return x.toLowerCase() === kv[0]; })[0];
        if (!g || !kv[1]) return;
        kv[1].split(",").forEach(function (v) { state[g][decodeURIComponent(v)] = true; });
      });
    }

    var unrecognised = rows.filter(function (r) { return !r.tags.resolution || !r.tags.forcing; })
      .map(function (r) { return r.el.cells[0].textContent.trim(); });
    if (unrecognised.length && window.console) console.warn("experiment-filter: could not tag", unrecognised);

    function apply() {
      var shown = 0;
      rows.forEach(function (r) {
        var ok = matches(r.tags);
        r.el.hidden = !ok;
        if (ok) shown++;
      });
      Array.prototype.forEach.call(bar.querySelectorAll(".exp-filter__btn[data-group]"), function (b) {
        var on = !!state[b.dataset.group][b.dataset.value];
        b.setAttribute("aria-pressed", on ? "true" : "false");
        b.classList.toggle("exp-filter__btn--on", on);
      });
      count.textContent = "Showing " + shown + " of " + rows.length + " experiments" +
        (unrecognised.length ? " \u00b7 " + unrecognised.length + " with no recognised resolution/forcing" : "");
      count.title = unrecognised.length ? "Not matched by resolution/forcing filters: " + unrecognised.join(", ") : "";
      writeHash();
    }

    readHash();
    apply();
  }

  // MkDocs Material instant navigation re-renders without a page load.
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
