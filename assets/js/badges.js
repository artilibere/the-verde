const STORAGE_KEY = 'tv-badges';
const GLOSSARY_KEY = 'tv-glossary-views';
const CONTROVERSY_KEY = 'tv-controversies-read';

function getBadges() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  } catch {
    return [];
  }
}

function unlockBadge(id) {
  const badges = getBadges();
  if (!badges.includes(id)) {
    badges.push(id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(badges));
  }
  updateBadgeUI();
}

function updateBadgeUI() {
  const unlocked = getBadges();
  document.querySelectorAll('[data-badge-id]').forEach((el) => {
    const id = el.dataset.badgeId;
    if (unlocked.includes(id)) el.classList.add('tv-badge--unlocked');
  });
}

function trackGlossaryView() {
  if (!window.location.pathname.startsWith('/glossario/')) return;
  const slug = window.location.pathname.split('/').filter(Boolean).pop();
  const views = JSON.parse(localStorage.getItem(GLOSSARY_KEY) || '[]');
  if (!views.includes(slug)) {
    views.push(slug);
    localStorage.setItem(GLOSSARY_KEY, JSON.stringify(views));
    if (views.length >= 10) unlockBadge('glossario-10');
  }
}

function trackControversyRead() {
  if (!window.location.pathname.includes('/controversie/')) return;
  const slug = window.location.pathname.split('/').filter(Boolean).pop();
  if (slug === 'controversie') return;
  const read = JSON.parse(localStorage.getItem(CONTROVERSY_KEY) || '[]');
  if (!read.includes(slug)) {
    read.push(slug);
    localStorage.setItem(CONTROVERSY_KEY, JSON.stringify(read));
    if (read.length >= 6) unlockBadge('controversie-tutte');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateBadgeUI();
  trackGlossaryView();
  trackControversyRead();
});

window.TVBadges = { unlockBadge, getBadges, updateBadgeUI };
