document.addEventListener('DOMContentLoaded', async () => {
  const app = document.getElementById('quiz-app');
  if (!app) return;
  const slug = app.dataset.quizSlug;
  let config;
  try {
    const res = await fetch('/assets/js/config/quizzes.json');
    config = await res.json();
  } catch {
    app.innerHTML = '<p>Quiz non disponibile.</p>';
    return;
  }
  const quiz = (config.quizzes || []).find((q) => q.slug === slug);
  if (!quiz) {
    app.innerHTML = '<p>Quiz non trovato.</p>';
    return;
  }

  let step = 0;
  let score = 0;

  function renderQuestion() {
    const q = quiz.questions[step];
    if (!q) return showResult();
    app.innerHTML = `
      <div class="tv-quiz__question">
        <p><strong>${step + 1}/${quiz.questions.length}</strong> ${q.q}</p>
        <div class="tv-quiz__options">
          ${q.options.map((opt, i) => `<button type="button" class="tv-btn tv-btn--outlined" data-idx="${i}">${opt}</button>`).join('')}
        </div>
        <p class="tv-quiz__feedback" hidden></p>
      </div>`;
    app.querySelectorAll('[data-idx]').forEach((btn) => {
      btn.addEventListener('click', () => answer(q, parseInt(btn.dataset.idx, 10), btn));
    });
  }

  function answer(q, idx, btn) {
    const feedback = app.querySelector('.tv-quiz__feedback');
    if (q.correct !== undefined) {
      const ok = idx === q.correct;
      if (ok) score++;
      feedback.hidden = false;
      feedback.textContent = ok
        ? `Esatto.${q.explain ? ' ' + q.explain : ''}`
        : `Non proprio.${q.explain ? ' ' + q.explain : ''}`;
      if (q.url) feedback.innerHTML += ` <a href="${q.url}">Approfondisci</a>`;
      setTimeout(() => { step++; renderQuestion(); }, 1500);
    } else if (q.scores) {
      score += q.scores[idx] || 0;
      step++;
      renderQuestion();
    }
  }

  function showResult() {
    if (quiz.results) {
      const r = quiz.results.find((x) => score >= x.min && score <= x.max) || quiz.results[0];
      app.innerHTML = `<h2>${r.title}</h2><p>${r.text}</p><a href="${r.url}" class="tv-btn tv-btn--filled">Scopri la scheda</a>`;
    } else {
      app.innerHTML = `<h2>Completato!</h2><p>Punteggio: ${score}/${quiz.questions.length}</p>`;
    }
    if (quiz.badge && window.TVBadges) window.TVBadges.unlockBadge(quiz.badge);
  }

  app.innerHTML = `<h2>${quiz.title}</h2><p>${quiz.description}</p><button type="button" class="tv-btn tv-btn--filled" id="quiz-start">Inizia</button>`;
  document.getElementById('quiz-start').addEventListener('click', () => {
    step = 0;
    score = 0;
    renderQuestion();
  });
});
