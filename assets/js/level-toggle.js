(function () {
  const btn = document.querySelector('[data-level-toggle]');
  const body = document.querySelector('.tv-article__body');
  if (!btn || !body) return;

  const approfondisci =
    body.querySelector('#approfondimento') ||
    [...body.querySelectorAll('h2')].find((h) => /approfondimento/i.test(h.textContent));

  if (!approfondisci) return;

  const hiddenNodes = [];
  let node = approfondisci;
  while (node) {
    hiddenNodes.push(node);
    node = node.nextElementSibling;
  }

  function setCollapsed(collapsed) {
    btn.setAttribute('aria-pressed', collapsed ? 'true' : 'false');
    btn.textContent = collapsed ? 'Vista completa' : 'Vista rapida';
    btn.setAttribute(
      'aria-label',
      collapsed ? 'Mostra sezione approfondimento' : 'Nascondi sezione approfondimento'
    );
    hiddenNodes.forEach((el) => {
      el.hidden = collapsed;
    });
  }

  setCollapsed(true);

  btn.addEventListener('click', () => {
    const collapsed = btn.getAttribute('aria-pressed') === 'true';
    setCollapsed(!collapsed);
  });
})();
