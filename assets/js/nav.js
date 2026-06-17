(function () {
  const btn = document.querySelector('.tv-header__menu-btn');
  const nav = document.querySelector('.tv-header__nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('tv-header__nav--open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('tv-header__nav--open')) {
      nav.classList.remove('tv-header__nav--open');
      btn.setAttribute('aria-expanded', 'false');
      btn.focus();
    }
  });
})();
