(function () {
  const PATHS_KEY = 'tv-paths-progress';

  function getProgress() {
    try {
      return JSON.parse(localStorage.getItem(PATHS_KEY) || '{}');
    } catch {
      return {};
    }
  }

  function saveProgress(data) {
    localStorage.setItem(PATHS_KEY, JSON.stringify(data));
  }

  async function initPathPage() {
    const article = document.querySelector('.tv-article');
    if (!article) return;
    const pathMatch = window.location.pathname.match(/\/gioca\/percorsi\/([^/]+)/);
    if (!pathMatch) return;
    const pathSlug = pathMatch[1];
    let config;
    try {
      config = await (await fetch('/assets/js/config/paths.json')).json();
    } catch {
      return;
    }
    const path = (config.paths || []).find((p) => p.slug === pathSlug);
    if (!path) return;

    const progress = getProgress();
    if (!progress[pathSlug]) progress[pathSlug] = { completed: [] };
    progress[pathSlug].visited = true;
    saveProgress(progress);

    const wrap = document.createElement('section');
    wrap.className = 'tv-path-progress';
    wrap.innerHTML = '<h2>Le tappe</h2><ol></ol>';
    const ol = wrap.querySelector('ol');
    path.steps.forEach((step) => {
      const li = document.createElement('li');
      const done = progress[pathSlug].completed.includes(step.slug);
      let href = step.url || `/varieta/${step.slug}/`;
      if (step.type === 'controversia') href = `/impara/controversie/${step.slug}/`;
      li.innerHTML = `${done ? '[x]' : '[ ]'} <a href="${href}">${step.slug}</a>`;
      if (step.quiz) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'tv-btn tv-btn--text';
        btn.textContent = 'Micro-quiz';
        btn.addEventListener('click', () => {
          const ok = window.confirm(`${step.quiz.question}\n(1=${step.quiz.options[0]}, 2=${step.quiz.options[1]})`);
          const choice = ok ? 1 : 2;
          if (choice === step.quiz.correct + 1) {
            if (!progress[pathSlug].completed.includes(step.slug)) {
              progress[pathSlug].completed.push(step.slug);
              saveProgress(progress);
            }
            if (progress[pathSlug].completed.length === path.steps.length && path.badge && window.TVBadges) {
              window.TVBadges.unlockBadge(path.badge);
            }
            alert('Tappa completata!');
            location.reload();
          } else {
            alert('Riprova dopo aver letto la scheda.');
          }
        });
        li.appendChild(btn);
      }
      ol.appendChild(li);
    });
    article.appendChild(wrap);
  }

  document.addEventListener('DOMContentLoaded', initPathPage);
})();
