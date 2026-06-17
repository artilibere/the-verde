document.addEventListener('DOMContentLoaded', async () => {
  const banner = document.querySelector('.tv-season-banner');
  if (!banner) return;
  try {
    const res = await fetch('/assets/js/config/seasons.json');
    const data = await res.json();
    const month = new Date().getMonth() + 1;
    const season = (data.seasons || []).find((s) => s.months.includes(month));
    if (season) {
      banner.dataset.season = season.slug;
      const label = banner.querySelector('.tv-season-banner__label');
      const text = banner.querySelector('.tv-season-banner__text');
      if (label) label.textContent = `Stagione: ${season.name}`;
      if (text) text.textContent = season.narrative;
    }
  } catch (_) {}
});
