(function () {
  const btn = document.querySelector('[data-level-toggle]');
  if (!btn) return;

  function updateButton(expanded) {
    btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    btn.textContent = expanded ? 'Vista rapida' : 'Vista completa';
    btn.setAttribute(
      'aria-label',
      expanded ? 'Nascondi sezione approfondimento' : 'Mostra sezione approfondimento'
    );
  }

  function bindToggle(targetId, applyCollapsed) {
    if (targetId) btn.setAttribute('aria-controls', targetId);
    updateButton(false);
    applyCollapsed(true);
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      updateButton(!expanded);
      applyCollapsed(expanded);
    });
  }

  const deepCard = document.getElementById('deep');
  if (deepCard) {
    bindToggle('deep', (collapsed) => {
      deepCard.hidden = collapsed;
    });
    return;
  }

  const body = document.querySelector('.tv-article__body');
  if (!body) return;

  const approfondisci =
    body.querySelector('#approfondimento') ||
    [...body.querySelectorAll('h2')].find((h) => /approfondimento/i.test(h.textContent));

  if (!approfondisci) return;

  if (!approfondisci.id) approfondisci.id = 'approfondimento';

  const hiddenNodes = [];
  let node = approfondisci;
  while (node) {
    hiddenNodes.push(node);
    node = node.nextElementSibling;
  }

  bindToggle(approfondisci.id, (collapsed) => {
    hiddenNodes.forEach((el) => {
      el.hidden = collapsed;
    });
  });
})();
