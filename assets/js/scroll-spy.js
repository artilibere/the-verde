(function () {
  const links = document.querySelectorAll('.tv-mininav__link');
  const sections = ['scopri', 'prepara', 'approfondisci']
    .map((id) => document.getElementById(id))
    .filter(Boolean);
  if (!links.length || !sections.length) return;

  const ratios = new Map();

  function setActive(id) {
    links.forEach((link) => {
      const active = link.getAttribute('href') === `#${id}`;
      link.classList.toggle('tv-mininav__link--active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }

  links.forEach((link) => {
    link.addEventListener('click', () => {
      const id = link.getAttribute('href').slice(1);
      if (id) setActive(id);
    });
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        ratios.set(entry.target.id, entry.isIntersecting ? entry.intersectionRatio : 0);
      });
      const visible = [...ratios.entries()]
        .filter(([, ratio]) => ratio > 0)
        .sort((a, b) => b[1] - a[1]);
      if (visible.length) setActive(visible[0][0]);
    },
    { rootMargin: '-20% 0px -55% 0px', threshold: [0, 0.15, 0.35, 0.55, 0.75, 1] }
  );
  sections.forEach((section) => observer.observe(section));
})();
