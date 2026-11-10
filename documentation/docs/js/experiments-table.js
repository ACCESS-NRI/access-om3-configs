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
  function apply() {
    // Selected components are AND'd: a run must include every one that is switched on.
    const comps = [...bar.querySelectorAll('[data-component][aria-pressed="true"]')].map(b => b.dataset.component);
    const compRe = comps.map(c => `(?=.*\\b${escape(c)}\\b)`).join('');
    for (const dt of dts) {
      const heads = dt.columns().header().toArray().map(th => th.textContent.trim());
      dt.search(bar.querySelector('[data-filter="search"]').value);
      for (const name of ['Resolution', 'Forcing']) {
        const v = bar.querySelector(`[data-filter="${name}"]`).value;
        dt.column(heads.indexOf(name)).search(v ? `^${escape(v)}$` : '', true, false);
      }
      dt.column(heads.indexOf('Components')).search(compRe && `^${compRe}`, true, false);
      dt.draw();
    }
  }
  bar.addEventListener('input', apply);
  bar.addEventListener('click', e => {
    const b = e.target.closest('[data-component]');
    if (!b) return;
    b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
    apply();
  });
});
