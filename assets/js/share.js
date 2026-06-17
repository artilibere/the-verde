(function () {
  const bar = document.querySelector('.tv-share');
  if (!bar) return;

  const feedback = bar.querySelector('.tv-share__feedback');
  const nativeBtn = bar.querySelector('[data-share="native"]');
  const whatsapp = bar.querySelector('[data-share="whatsapp"]');
  const copyBtn = bar.querySelector('[data-share="copy"]');
  const url = window.location.href;
  const title = document.querySelector('meta[property="og:title"]')?.content || document.title;

  function showFeedback(message) {
    if (!feedback) return;
    feedback.textContent = message;
    feedback.hidden = false;
    window.setTimeout(() => {
      feedback.hidden = true;
    }, 2500);
  }

  if (whatsapp) {
    whatsapp.href = `https://wa.me/?text=${encodeURIComponent(`${title} — ${url}`)}`;
  }

  if (navigator.share && nativeBtn) {
    nativeBtn.hidden = false;
    nativeBtn.addEventListener('click', () => {
      navigator.share({ title, url }).catch(() => {});
    });
  }

  copyBtn?.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(url);
      showFeedback('Link copiato negli appunti');
    } catch {
      window.prompt('Copia il link:', url);
    }
  });
})();
