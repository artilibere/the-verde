(function () {
  const btn = document.querySelector('[data-level-toggle]');
  const body = document.querySelector('.tv-article__body');
  if (!btn || !body) return;
  const sections = body.querySelectorAll('#approfondisci, h2');
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-pressed') === 'true';
    btn.setAttribute('aria-pressed', expanded ? 'false' : 'true');
    btn.textContent = expanded ? 'Vista completa' : 'Vista rapida';
    body.classList.toggle('tv-zone-collapsed', expanded);
    if (!expanded) {
      body.querySelectorAll('h2, h3, p, ul, ol, aside').forEach((el, i) => {
        if (i > 2 && !el.closest('#scopri')) el.style.display = '';
      });
    } else {
      const approfondisci = body.querySelector('[id*="approfond"]') || body.querySelectorAll('h2')[2];
      body.querySelectorAll('h2, h3, p, ul, ol').forEach((el) => {
        if (approfondisci && el.compareDocumentPosition(approfondisci) & Node.DOCUMENT_POSITION_FOLLOWING) {
          if (el !== approfondisci) el.style.display = 'none';
        }
      });
    }
  });
})();
