// DataTables for the Experiments page (pages/Experiments.md).
// DataTables has no built-in filter bar shared across tables, so this wires up our own.
// Resolution / Forcing / Components are real columns, hidden from view but still searchable,
// so the filter bar above the tables can filter on them.
document$.subscribe(() => {
  const tables = [...document.querySelectorAll('.exp-table table')];
  const bar = document.querySelector('.exp-filter');
  if (!tables.length || !bar) return;

  const HIDDEN = ['Resolution', 'Forcing', 'Components'];
  const dts = tables.map(table => {
    const heads = [...table.tHead.rows[0].cells].map(th => th.textContent.trim());
    const col = name => heads.findIndex(h => h.startsWith(name));
    const newest = col('Date') >= 0 ? col('Date') : col('Model build');
    return new DataTable(table, {
      paging: false,
      autoWidth: false,
      order: [[newest, 'desc']],
      columnDefs: [
        { targets: HIDDEN.map(col), visible: false },
        { targets: [col('Date'), col('Model build')].filter(i => i >= 0), className: 'exp-nowrap' },
        { targets: '_all', orderSequence: ['asc', 'desc'] },  // no third 'unsorted' state
      ],
      layout: { topStart: null, topEnd: null, bottomStart: 'info', bottomEnd: null },
      language: { info: 'Showing _TOTAL_ of _MAX_ experiments', infoFiltered: '', infoEmpty: 'Showing 0 of _MAX_ experiments', zeroRecords: 'No matching experiments' },
    });
  });

  const escape = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // Each dropdown must match its hidden column exactly; the search box matches any column.
  function apply() {
    for (const dt of dts) {
      const heads = dt.columns().header().toArray().map(th => th.textContent.trim());
      dt.search(bar.querySelector('[data-filter="search"]').value);
      for (const name of HIDDEN) {
        const v = bar.querySelector(`[data-filter="${name}"]`).value;
        dt.column(heads.indexOf(name)).search(v ? `^${escape(v)}$` : '', true, false);
      }
      dt.draw();
    }
  }
  // Keep the selected filters in the URL (?resolution=25+km&...), so a refresh keeps them
  // and a filtered view can be shared. The controls have autocomplete="off", so the URL is
  // the only source of state and the controls always match the table.
  const controls = [...bar.querySelectorAll('[data-filter]')];
  const key = el => el.dataset.filter.toLowerCase();
  const params = new URLSearchParams(location.search);
  for (const el of controls) {
    const v = params.get(key(el)) || '';
    const valid = el.tagName !== 'SELECT' || [...el.options].some(o => o.value === v);
    el.value = valid ? v : '';
  }
  bar.addEventListener('input', () => {
    const p = new URLSearchParams(location.search);
    for (const el of controls) el.value ? p.set(key(el), el.value) : p.delete(key(el));
    const q = p.toString();
    history.replaceState(history.state, '', location.pathname + (q ? '?' + q : '') + location.hash);
    apply();
  });
  apply();
});
