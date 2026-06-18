(function () {
  const btn = document.querySelector('.tv-header__menu-btn');
  const nav = document.querySelector('.tv-header__nav');
  const scrim = document.querySelector('.tv-nav-scrim');
  if (!btn || !nav) return;

  const links = Array.from(nav.querySelectorAll('a[href]'));
  const focusable = () => links.filter((el) => !el.hasAttribute('disabled'));
  const path = window.location.pathname.replace(/\/$/, '') || '/';
  const background = [document.getElementById('main'), document.querySelector('.tv-bottom-nav'), document.querySelector('.tv-footer')];

  function setBackgroundInert(inert) {
    background.forEach((el) => {
      if (!el) return;
      if ('inert' in el) el.inert = inert;
      else el.setAttribute('aria-hidden', inert ? 'true' : 'false');
    });
  }

  function setOpen(open) {
    nav.classList.toggle('tv-header__nav--open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Chiudi menu' : 'Apri menu');
    document.body.classList.toggle('tv-nav-open', open);
    if (scrim) scrim.hidden = !open;
    setBackgroundInert(open);
    if (open) {
      const first = focusable()[0];
      if (first) first.focus();
    }
  }

  links.forEach((link) => {
    const href = link.getAttribute('href').replace(/\/$/, '') || '/';
    if (href === path || (href !== '/' && path.startsWith(href))) {
      link.setAttribute('aria-current', 'page');
    }
    link.addEventListener('click', () => setOpen(false));
  });

  btn.addEventListener('click', () => {
    setOpen(!nav.classList.contains('tv-header__nav--open'));
  });

  scrim?.addEventListener('click', () => setOpen(false));

  document.addEventListener('click', (e) => {
    if (!nav.classList.contains('tv-header__nav--open')) return;
    if (nav.contains(e.target) || btn.contains(e.target)) return;
    setOpen(false);
  });

  document.addEventListener('keydown', (e) => {
    if (!nav.classList.contains('tv-header__nav--open')) return;
    if (e.key === 'Escape') {
      setOpen(false);
      btn.focus();
      return;
    }
    if (e.key !== 'Tab') return;
    const items = focusable();
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
})();
