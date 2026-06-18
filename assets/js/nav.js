(function () {
  const btn = document.querySelector('.tv-header__menu-btn');
  const nav = document.querySelector('.tv-header__nav');
  if (!btn || !nav) return;

  const links = nav.querySelectorAll('a[href]');
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
    setBackgroundInert(open);
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

  document.addEventListener('click', (e) => {
    if (!nav.classList.contains('tv-header__nav--open')) return;
    if (nav.contains(e.target) || btn.contains(e.target)) return;
    setOpen(false);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('tv-header__nav--open')) {
      setOpen(false);
      btn.focus();
    }
  });
})();
