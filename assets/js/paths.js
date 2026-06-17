(function () {
  const PATHS_KEY = 'tv-paths-progress';

  const TYPE_LABELS = {
    varieta: 'Varietà',
    hub: 'Approfondimento',
    controversia: 'Controversia',
  };

  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function stepTitle(step) {
    if (step.title) return step.title;
    return step.slug
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ');
  }

  function stepHref(step) {
    if (step.url) return step.url;
    if (step.type === 'controversia') return `/impara/controversie/${step.slug}/`;
    if (step.type === 'hub') return `/impara/${step.slug}/`;
    return `/varieta/${step.slug}/`;
  }

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

  function markStepDone(pathSlug, stepSlug, progress, path, li, onUpdate) {
    if (!progress[pathSlug].completed.includes(stepSlug)) {
      progress[pathSlug].completed.push(stepSlug);
      saveProgress(progress);
    }
    li.classList.add('tv-path-step--done');
    const marker = li.querySelector('.tv-path-step__status');
    if (marker) {
      marker.textContent = '✓';
      marker.classList.add('tv-path-step__status--done');
    }
    const markBtn = li.querySelector('.tv-path-step__mark');
    if (markBtn) markBtn.remove();
    const quiz = li.querySelector('.tv-path-quiz');
    if (quiz) quiz.remove();
    if (progress[pathSlug].completed.length === path.steps.length && path.badge && window.TVBadges) {
      window.TVBadges.unlockBadge(path.badge);
    }
    onUpdate();
  }

  function renderMicroQuiz(step, pathSlug, progress, path, li, onUpdate) {
    const quiz = step.quiz;
    const body = li.querySelector('.tv-path-step__body');
    if (!quiz || !body) return;

    const wrap = document.createElement('div');
    wrap.className = 'tv-path-quiz';
    wrap.innerHTML = `
      <p class="tv-path-quiz__question">${escapeHtml(quiz.question)}</p>
      <div class="tv-path-quiz__options" role="group" aria-label="Risposta al micro-quiz">
        ${quiz.options
          .map(
            (opt, i) =>
              `<button type="button" class="tv-btn tv-btn--outlined tv-path-quiz__option" data-idx="${i}">${escapeHtml(opt)}</button>`
          )
          .join('')}
      </div>
      <p class="tv-path-quiz__feedback" hidden aria-live="polite"></p>
    `;

    wrap.querySelectorAll('[data-idx]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.dataset.idx, 10);
        const ok = idx === quiz.correct;
        const feedback = wrap.querySelector('.tv-path-quiz__feedback');
        feedback.hidden = false;
        feedback.textContent = ok
          ? 'Esatto. Tappa completata.'
          : 'Non proprio. Rileggi la scheda e riprova.';
        wrap.querySelectorAll('.tv-path-quiz__option').forEach((b) => {
          b.disabled = true;
        });
        if (ok) markStepDone(pathSlug, step.slug, progress, path, li, onUpdate);
      });
    });
    body.appendChild(wrap);
  }

  function renderMarkButton(step, pathSlug, progress, path, li, onUpdate) {
    const body = li.querySelector('.tv-path-step__body');
    if (!body) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'tv-btn tv-btn--text tv-path-step__mark';
    btn.textContent = 'Segna come completata';
    btn.addEventListener('click', () => markStepDone(pathSlug, step.slug, progress, path, li, onUpdate));
    body.appendChild(btn);
  }

  async function initPathPage() {
    const article = document.querySelector('.tv-article');
    if (!article) return;
    const pathMatch = window.location.pathname.match(/\/gioca\/percorsi\/([^/]+)/);
    if (!pathMatch) return;
    const pathSlug = pathMatch[1];
    let config;
    try {
      const res = await fetch('/assets/js/config/paths.json');
      if (!res.ok) return;
      config = await res.json();
    } catch {
      return;
    }
    const path = (config.paths || []).find((p) => p.slug === pathSlug);
    if (!path) return;

    const progress = getProgress();
    if (!progress[pathSlug]) progress[pathSlug] = { completed: [] };
    progress[pathSlug].visited = true;
    saveProgress(progress);

    const total = path.steps.length;
    const wrap = document.createElement('section');
    wrap.className = 'tv-path-progress';
    wrap.setAttribute('aria-labelledby', 'path-steps-heading');

    function completedCount() {
      return progress[pathSlug].completed.length;
    }

    function updateSummary() {
      const summary = wrap.querySelector('.tv-path-progress__summary');
      if (summary) {
        const n = completedCount();
        summary.textContent = n === total ? 'Percorso completato!' : `${n} di ${total} tappe completate`;
      }
    }

    wrap.innerHTML = `
      <h2 id="path-steps-heading">Le tappe</h2>
      <p class="tv-path-progress__summary" aria-live="polite">${completedCount()} di ${total} tappe completate</p>
      <ol class="tv-path-steps"></ol>
    `;

    const ol = wrap.querySelector('ol');
    path.steps.forEach((step, index) => {
      const done = progress[pathSlug].completed.includes(step.slug);
      const li = document.createElement('li');
      li.className = `tv-path-step${done ? ' tv-path-step--done' : ''}`;
      const typeLabel = TYPE_LABELS[step.type] || '';
      li.innerHTML = `
        <span class="tv-path-step__status${done ? ' tv-path-step__status--done' : ''}" aria-hidden="true">${done ? '✓' : index + 1}</span>
        <div class="tv-path-step__body">
          <a href="${escapeHtml(stepHref(step))}" class="tv-path-step__link">${escapeHtml(stepTitle(step))}</a>
          ${typeLabel ? `<span class="tv-path-step__type">${escapeHtml(typeLabel)}</span>` : ''}
        </div>
      `;
      if (!done) {
        if (step.quiz) renderMicroQuiz(step, pathSlug, progress, path, li, updateSummary);
        else renderMarkButton(step, pathSlug, progress, path, li, updateSummary);
      }
      ol.appendChild(li);
    });

    article.appendChild(wrap);
    updateSummary();
  }

  document.addEventListener('DOMContentLoaded', initPathPage);
})();
