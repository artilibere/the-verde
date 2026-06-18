(function () {
  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  const grid = document.getElementById('variety-grid');
  const countEl = document.getElementById('variety-count');
  if (!grid) return;

  const filters = { origine: new Set(), stile: new Set(), caffeina: new Set(), stagione: new Set() };
  let varieties = [];

  const LABELS = {
    giappone: 'Giappone',
    cina: 'Cina',
    india: 'India',
    taiwan: 'Taiwan',
    bassa: 'Bassa',
    media: 'Media',
    alta: 'Alta',
    estate: 'Estate',
    primavera: 'Primavera',
    autunno: 'Autunno',
    inverno: 'Inverno',
  };

  function humanize(value) {
    if (!value) return '';
    if (LABELS[value]) return LABELS[value];
    return value
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ');
  }

  function readUrlFilters() {
    const params = new URLSearchParams(window.location.search);
    ['origine', 'stile', 'caffeina', 'stagione'].forEach((key) => {
      const vals = params.getAll(key);
      vals.forEach((val) => {
        if (val) filters[key].add(val);
      });
    });
  }

  function syncUrl() {
    const params = new URLSearchParams();
    ['origine', 'stile', 'caffeina', 'stagione'].forEach((key) => {
      filters[key].forEach((val) => params.append(key, val));
    });
    const qs = params.toString();
    const next = qs ? `${window.location.pathname}?${qs}` : window.location.pathname;
    window.history.replaceState({}, '', next);
  }

  function showError() {
    grid.classList.remove('tv-catalog-results__grid--loading');
    grid.setAttribute('aria-busy', 'false');
    if (countEl) countEl.textContent = 'Catalogo non disponibile';
    grid.innerHTML =
      '<p class="tv-catalog-results__empty">Non riusciamo a caricare le varietà. <a href="">Riprova</a>.</p>';
    grid.querySelector('a')?.addEventListener('click', (e) => {
      e.preventDefault();
      window.location.reload();
    });
  }

  fetch('/assets/js/config/varieties.json')
    .then((r) => {
      if (!r.ok) throw new Error('fetch failed');
      return r.json();
    })
    .then((data) => {
      varieties = data.varieties || [];
      readUrlFilters();
      buildFilterUI(data.varieties);
      render(varieties);
    })
    .catch(showError);

  function buildFilterUI(items) {
    const keys = ['origine', 'stile', 'caffeina', 'stagione'];
    keys.forEach((key) => {
      const container = document.getElementById(`filter-${key}`);
      if (!container) return;
      const values = [...new Set(items.map((v) => v[key]).filter(Boolean))].sort();
      values.forEach((val) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = humanize(val);
        const pressed = filters[key].has(val);
        btn.setAttribute('aria-pressed', pressed ? 'true' : 'false');
        btn.dataset.filter = key;
        btn.dataset.value = val;
        if (pressed) btn.classList.add('tv-filter-options__btn--active');
        btn.addEventListener('click', () => {
          if (filters[key].has(val)) filters[key].delete(val);
          else filters[key].add(val);
          const active = filters[key].has(val);
          btn.setAttribute('aria-pressed', active ? 'true' : 'false');
          btn.classList.toggle('tv-filter-options__btn--active', active);
          applyFilters();
        });
        container.appendChild(btn);
      });
    });
  }

  function applyFilters() {
    syncUrl();
    const filtered = varieties.filter((v) =>
      ['origine', 'stile', 'caffeina', 'stagione'].every((key) => {
        if (filters[key].size === 0) return true;
        return filters[key].has(v[key]);
      })
    );
    updateResetButton();
    render(filtered);
  }

  function updateResetButton() {
    const resetBtn = document.getElementById('filter-reset');
    if (!resetBtn) return;
    const active = ['origine', 'stile', 'caffeina', 'stagione'].some((key) => filters[key].size > 0);
    resetBtn.hidden = !active;
  }

  function resetFilters() {
    ['origine', 'stile', 'caffeina', 'stagione'].forEach((key) => filters[key].clear());
    document.querySelectorAll('.tv-filter-options button').forEach((btn) => {
      btn.setAttribute('aria-pressed', 'false');
      btn.classList.remove('tv-filter-options__btn--active');
    });
    applyFilters();
  }

  document.getElementById('filter-reset')?.addEventListener('click', resetFilters);

  function render(items) {
    grid.classList.remove('tv-catalog-results__grid--loading');
    grid.setAttribute('aria-busy', 'false');
    const n = items.length;
    if (countEl) {
      countEl.textContent = n === 1 ? '1 varietà' : `${n} varietà`;
    }
    if (items.length === 0) {
      grid.innerHTML =
        '<p class="tv-catalog-results__empty">Nessuna varietà corrisponde ai filtri. <button type="button" class="tv-btn tv-btn--text" id="filter-empty-reset">Azzera filtri</button></p>';
      document.getElementById('filter-empty-reset')?.addEventListener('click', resetFilters);
      return;
    }
    grid.innerHTML = items
      .map(
        (v) => `
      <article class="tv-variety-card">
        <h3 class="tv-variety-card__title"><a href="${escapeHtml(v.url)}">${escapeHtml(v.title)}</a></h3>
        <p class="tv-variety-card__brief">${escapeHtml(v.brief || '')}</p>
        <div class="tv-origin-chips">
          <span class="tv-chip">${escapeHtml(humanize(v.origine))}</span>
          <span class="tv-chip">${escapeHtml(humanize(v.stile))}</span>
        </div>
      </article>`
      )
      .join('');
  }
})();
