document.addEventListener('DOMContentLoaded', async () => {
  const app = document.getElementById('quiz-app');
  if (!app) return;
  const slug = app.dataset.quizSlug;

  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  app.setAttribute('aria-busy', 'true');
  app.innerHTML = '<p class="tv-quiz__loading">Caricamento quiz…</p>';

  let config;
  try {
    const res = await fetch('/assets/js/config/quizzes.json');
    if (!res.ok) throw new Error('fetch failed');
    config = await res.json();
  } catch {
    app.setAttribute('aria-busy', 'false');
    app.innerHTML = '<p class="tv-quiz__error">Quiz non disponibile. <a href="">Riprova</a>.</p>';
    app.querySelector('a')?.addEventListener('click', (e) => {
      e.preventDefault();
      window.location.reload();
    });
    return;
  }

  const quiz = (config.quizzes || []).find((q) => q.slug === slug);
  if (!quiz) {
    app.setAttribute('aria-busy', 'false');
    app.innerHTML = '<p class="tv-quiz__error">Quiz non trovato.</p>';
    return;
  }

  let step = 0;
  let score = 0;

  function renderQuestion() {
    const q = quiz.questions[step];
    if (!q) return showResult();
    app.setAttribute('aria-busy', 'false');
    app.innerHTML = `
      <div class="tv-quiz__question">
        <p class="tv-quiz__progress" aria-live="polite"><strong>${step + 1}/${quiz.questions.length}</strong></p>
        <p class="tv-quiz__prompt">${escapeHtml(q.q)}</p>
        <div class="tv-quiz__options" role="group" aria-label="Scegli una risposta">
          ${q.options
            .map(
              (opt, i) =>
                `<button type="button" class="tv-btn tv-btn--outlined tv-quiz__option" data-idx="${i}">${escapeHtml(opt)}</button>`
            )
            .join('')}
        </div>
        <p class="tv-quiz__feedback" hidden aria-live="polite"></p>
      </div>`;
    app.querySelectorAll('[data-idx]').forEach((btn) => {
      btn.addEventListener('click', () => answer(q, parseInt(btn.dataset.idx, 10)));
    });
  }

  function answer(q, idx) {
    const feedback = app.querySelector('.tv-quiz__feedback');
    const buttons = app.querySelectorAll('.tv-quiz__option');
    buttons.forEach((b) => {
      b.disabled = true;
    });

    if (q.correct !== undefined) {
      const ok = idx === q.correct;
      if (ok) score++;
      feedback.hidden = false;
      const explain = q.explain ? ` ${q.explain}` : '';
      feedback.textContent = ok ? `Esatto.${explain}` : `Non proprio.${explain}`;
      if (q.url) {
        const link = document.createElement('a');
        link.href = q.url;
        link.textContent = ' Approfondisci';
        feedback.appendChild(link);
      }
      window.setTimeout(() => {
        step++;
        renderQuestion();
      }, 1800);
    } else if (q.scores) {
      score += q.scores[idx] || 0;
      step++;
      renderQuestion();
    }
  }

  function showResult() {
    if (quiz.results) {
      const r = quiz.results.find((x) => score >= x.min && score <= x.max) || quiz.results[0];
      app.innerHTML = `
        <div class="tv-quiz__result">
          <h2>${escapeHtml(r.title)}</h2>
          <p>${escapeHtml(r.text)}</p>
          <div class="tv-quiz__result-actions">
            <a href="${escapeHtml(r.url)}" class="tv-btn tv-btn--filled">Scopri la scheda</a>
            <a href="#condividi" class="tv-btn tv-btn--outlined">Sfida un amico</a>
          </div>
        </div>`;
    } else {
      app.innerHTML = `
        <div class="tv-quiz__result">
          <h2>Completato!</h2>
          <p>Punteggio: ${score}/${quiz.questions.length}</p>
          <div class="tv-quiz__result-actions">
            <a href="#condividi" class="tv-btn tv-btn--outlined">Sfida un amico al quiz</a>
          </div>
        </div>`;
    }
    if (quiz.badge && window.TVBadges) window.TVBadges.unlockBadge(quiz.badge);
    document.getElementById('condividi')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  app.setAttribute('aria-busy', 'false');
  app.innerHTML = `
    <div class="tv-quiz__intro">
      <p>${escapeHtml(quiz.description)}</p>
      <button type="button" class="tv-btn tv-btn--filled" id="quiz-start">Inizia</button>
    </div>`;
  document.getElementById('quiz-start').addEventListener('click', () => {
    step = 0;
    score = 0;
    renderQuestion();
  });
});
