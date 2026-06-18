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
  const quickRail = document.getElementById('catalog-quick-filters');
  const activeRail = document.getElementById('catalog-active-filters');
  if (!grid) return;

  const filters = { origine: new Set(), stile: new Set(), caffeina: new Set(), stagione: new Set() };
  const QUICK_KEYS = ['origine', 'caffeina'];
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
      params.getAll(key).forEach((val) => {
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

  function syncFilterButtonStates(key, value) {
    const active = filters[key].has(value);
    document.querySelectorAll(`[data-filter="${key}"][data-value="${value}"]`).forEach((btn) => {
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
      btn.classList.toggle('tv-filter-options__btn--active', active);
      btn.classList.toggle('tv-chip--filter-active', active);
    });
  }

  function syncAllFilterButtonStates() {
    document.querySelectorAll('[data-filter][data-value]').forEach((btn) => {
      syncFilterButtonStates(btn.dataset.filter, btn.dataset.value);
    });
  }

  function toggleFilter(key, value) {
    if (filters[key].has(value)) filters[key].delete(value);
    else filters[key].add(value);
    syncFilterButtonStates(key, value);
    applyFilters();
  }

  function createFilterButton(key, value, className) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = className;
    btn.textContent = humanize(value);
    btn.dataset.filter = key;
    btn.dataset.value = value;
    btn.setAttribute('aria-pressed', filters[key].has(value) ? 'true' : 'false');
    if (filters[key].has(value)) btn.classList.add('tv-filter-options__btn--active', 'tv-chip--filter-active');
    btn.addEventListener('click', () => toggleFilter(key, value));
    return btn;
  }

  function showError() {
    grid.classList.remove('tv-catalog-results__grid--loading');
    grid.setAttribute('aria-busy', 'false');
    if (countEl) countEl.textContent = 'Catalogo non disponibile';
    if (quickRail) quickRail.hidden = true;
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
      buildQuickFilters(data.varieties);
      applyFilters();
    })
    .catch(showError);

  function buildFilterUI(items) {
    ['origine', 'stile', 'caffeina', 'stagione'].forEach((key) => {
      const container = document.getElementById(`filter-${key}`);
      if (!container) return;
      const values = [...new Set(items.map((v) => v[key]).filter(Boolean))].sort();
      values.forEach((val) => {
        container.appendChild(createFilterButton(key, val, 'tv-filter-options__btn'));
      });
    });
  }

  function buildQuickFilters(items) {
    if (!quickRail) return;
    quickRail.innerHTML = '';
    QUICK_KEYS.forEach((key) => {
      const values = [...new Set(items.map((v) => v[key]).filter(Boolean))].sort();
      values.forEach((val) => {
        quickRail.appendChild(createFilterButton(key, val, 'tv-chip tv-chip--filter'));
      });
    });
    quickRail.hidden = quickRail.children.length === 0;
  }

  function updateActiveFiltersRail() {
    if (!activeRail) return;
    activeRail.innerHTML = '';
    let hasAny = false;
    ['origine', 'stile', 'caffeina', 'stagione'].forEach((key) => {
      filters[key].forEach((val) => {
        hasAny = true;
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'tv-chip tv-chip--filter tv-chip--filter-active';
        btn.dataset.filter = key;
        btn.dataset.value = val;
        btn.setAttribute('aria-label', `Rimuovi filtro ${humanize(val)}`);
        btn.innerHTML = `${escapeHtml(humanize(val))} <span aria-hidden="true">×</span>`;
        btn.addEventListener('click', () => toggleFilter(key, val));
        activeRail.appendChild(btn);
      });
    });
    if (hasAny) {
      const reset = document.createElement('button');
      reset.type = 'button';
      reset.className = 'tv-btn tv-btn--text tv-catalog-active-filters__clear';
      reset.textContent = 'Azzera tutti';
      reset.addEventListener('click', resetFilters);
      activeRail.appendChild(reset);
    }
    activeRail.hidden = !hasAny;
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
    updateActiveFiltersRail();
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
    syncAllFilterButtonStates();
    applyFilters();
  }

  document.getElementById('filter-reset')?.addEventListener('click', resetFilters);

  const filterToggle = document.getElementById('catalog-filter-toggle');
  const filterPanel = document.getElementById('catalog-filters');
  const filterScrim = document.querySelector('.tv-filter-scrim');

  function setFilterOpen(open) {
    if (!filterPanel) return;
    filterPanel.classList.toggle('tv-filter-bar--open', open);
    filterToggle?.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.classList.toggle('tv-filter-open', open);
    if (filterScrim) filterScrim.hidden = !open;
  }

  if (filterToggle && filterPanel) {
    filterToggle.addEventListener('click', () => {
      setFilterOpen(!filterPanel.classList.contains('tv-filter-bar--open'));
    });
    filterScrim?.addEventListener('click', () => setFilterOpen(false));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && filterPanel.classList.contains('tv-filter-bar--open')) {
        setFilterOpen(false);
        filterToggle.focus();
      }
    });
  }

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
      <a href="${escapeHtml(v.url)}" class="tv-variety-card">
        <h3 class="tv-variety-card__title">${escapeHtml(v.title)}</h3>
        <p class="tv-variety-card__brief">${escapeHtml(v.brief || '')}</p>
        <div class="tv-origin-chips">
          <span class="tv-chip">${escapeHtml(humanize(v.origine))}</span>
          <span class="tv-chip">${escapeHtml(humanize(v.stile))}</span>
        </div>
      </a>`
      )
      .join('');
  }
})();
