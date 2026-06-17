(function () {
  const grid = document.getElementById('variety-grid');
  const countEl = document.getElementById('variety-count');
  if (!grid) return;

  const filters = { origine: new Set(), stile: new Set(), caffeina: new Set(), stagione: new Set() };
  let varieties = [];

  fetch('/varieta/index.json')
    .then((r) => r.json())
    .then((data) => {
      varieties = data.varieties || [];
      buildFilterUI(data.varieties);
      render(varieties);
    });

  function buildFilterUI(items) {
    const keys = ['origine', 'stile', 'caffeina', 'stagione'];
    keys.forEach((key) => {
      const container = document.getElementById(`filter-${key}`);
      if (!container) return;
      const values = [...new Set(items.map((v) => v[key]).filter(Boolean))].sort();
      values.forEach((val) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = val;
        btn.setAttribute('aria-pressed', 'false');
        btn.dataset.filter = key;
        btn.dataset.value = val;
        btn.addEventListener('click', () => {
          if (filters[key].has(val)) filters[key].delete(val);
          else filters[key].add(val);
          btn.setAttribute('aria-pressed', filters[key].has(val) ? 'true' : 'false');
          applyFilters();
        });
        container.appendChild(btn);
      });
    });
  }

  function applyFilters() {
    const filtered = varieties.filter((v) => {
      return ['origine', 'stile', 'caffeina', 'stagione'].every((key) => {
        if (filters[key].size === 0) return true;
        return filters[key].has(v[key]);
      });
    });
    render(filtered);
  }

  function render(items) {
    if (countEl) countEl.textContent = `${items.length} varietà`;
    grid.innerHTML = items
      .map(
        (v) => `
      <article class="tv-variety-card">
        <h3 class="tv-variety-card__title"><a href="${v.url}">${v.title}</a></h3>
        <p class="tv-variety-card__brief">${v.brief || ''}</p>
        <div class="tv-origin-chips">
          <span class="tv-chip">${v.origine}</span>
          <span class="tv-chip">${v.stile}</span>
        </div>
      </article>`
      )
      .join('');
  }
})();
