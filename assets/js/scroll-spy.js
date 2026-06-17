(function () {
  const links = document.querySelectorAll('.tv-mininav__link');
  const sections = ['scopri', 'prepara', 'approfondisci'].map((id) => document.getElementById(id)).filter(Boolean);
  if (!links.length || !sections.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          links.forEach((l) => {
            l.classList.toggle('tv-mininav__link--active', l.getAttribute('href') === `#${entry.target.id}`);
          });
        }
      });
    },
    { rootMargin: '-40% 0px -50% 0px', threshold: 0 }
  );
  sections.forEach((s) => observer.observe(s));
})();
