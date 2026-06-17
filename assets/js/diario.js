const DIARIO_KEY = 'tv-diario';

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function entryVarieta(entry) {
  return entry.varieta ?? entry.varietà ?? '';
}

function getEntries() {
  try {
    return JSON.parse(localStorage.getItem(DIARIO_KEY) || '[]');
  } catch {
    return [];
  }
}

function saveEntries(entries) {
  localStorage.setItem(DIARIO_KEY, JSON.stringify(entries));
}

function renderList() {
  const list = document.getElementById('diario-list');
  const stats = document.getElementById('diario-stats');
  if (!list) return;
  const entries = getEntries().sort((a, b) => new Date(b.date) - new Date(a.date));
  if (!entries.length) {
    list.innerHTML =
      '<p class="tv-diario-empty">Nessuna infusione ancora. <a href="/diario/nuova/">Registra la prima</a> dopo una tazza di sencha, genmaicha o gyokuro.</p>';
    if (stats) stats.textContent = '';
    return;
  }
  list.innerHTML = entries
    .map(
      (e) => `
    <article class="tv-diario-list__item">
      <strong>${escapeHtml(entryVarieta(e))}</strong> — ${new Date(e.date).toLocaleDateString('it-IT')}
      ${e.temp ? `<span>${escapeHtml(e.temp)}°C</span>` : ''}
      <p>${escapeHtml(e.note || '')}</p>
      ${e.tags?.length ? `<p>${e.tags.map((t) => `<span class="tv-chip">${escapeHtml(t)}</span>`).join(' ')}</p>` : ''}
    </article>`
    )
    .join('');
  if (stats) stats.textContent = `${entries.length} infusioni registrate`;
  if (entries.length >= 1 && window.TVBadges) window.TVBadges.unlockBadge('prima-infusione');
  if (entries.length >= 10 && window.TVBadges) window.TVBadges.unlockBadge('diario-10');
  const seasons = new Set(entries.map((e) => e.season).filter(Boolean));
  if (seasons.size >= 4 && window.TVBadges) window.TVBadges.unlockBadge('quattro-stagioni');
}

function getSeason() {
  const m = new Date().getMonth() + 1;
  if (m >= 3 && m <= 5) return 'primavera';
  if (m >= 6 && m <= 8) return 'estate';
  if (m >= 9 && m <= 11) return 'autunno';
  return 'inverno';
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('diario-form');
  const exportBtn = document.getElementById('diario-export');
  const syncBtn = document.getElementById('diario-sync');
  const params = new URLSearchParams(window.location.search);
  const prefill = params.get('varieta') || params.get('varietà');
  if (prefill) {
    const sel = document.getElementById('diario-varieta');
    if (sel) sel.value = prefill;
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const fd = new FormData(form);
      const entry = {
        id: Date.now(),
        varieta: fd.get('varieta') || fd.get('varietà'),
        date: new Date().toISOString(),
        temp: fd.get('temp'),
        grams: fd.get('grams'),
        seconds: fd.get('seconds'),
        note: fd.get('note'),
        momento: fd.get('momento'),
        season: getSeason(),
        tags: fd.getAll('tags'),
      };
      const entries = getEntries();
      entries.push(entry);
      saveEntries(entries);
      window.location.href = '/diario/';
    });
  }

  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      const blob = new Blob([JSON.stringify(getEntries(), null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'diario-te-verde.json';
      a.click();
    });
  }

  if (syncBtn) {
    syncBtn.addEventListener('click', () => {
      if (window.TVSupabase?.sync) window.TVSupabase.sync(getEntries());
      else alert('Sincronizzazione disponibile con account Supabase (fase 3).');
    });
  }

  renderList();
});

window.TVDiario = { getEntries, saveEntries };
