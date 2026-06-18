(function () {
  const FONTI = {
    rosen: 'Rosen',
    sommelier: 'Sommelier',
    pellegrino: 'Pellegrino',
    onuma: 'Onuma',
    hara: 'Hara',
  };

  function label(value) {
    return FONTI[value] || value.charAt(0).toUpperCase() + value.slice(1);
  }

  const form = document.getElementById('controversy-poll');
  const result = document.getElementById('poll-result');
  if (!form) return;
  const key = `tv-poll-${form.closest('[data-controversy]')?.dataset.controversy || 'default'}`;
  const saved = localStorage.getItem(key);

  function showResult(value) {
    if (!result) return;
    result.hidden = false;
    result.setAttribute('aria-live', 'polite');
    result.textContent = `Hai scelto la prospettiva ${label(value)}. Ora leggi le altre: è lì che nasce la comprensione.`;
    form.querySelectorAll('input, button').forEach((el) => {
      el.disabled = true;
    });
    form.classList.add('tv-poll__form--submitted');
  }

  if (saved) showResult(saved);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const choice = form.querySelector('input[name="poll"]:checked');
    if (!choice) {
      if (result) {
        result.hidden = false;
        result.textContent = 'Seleziona una prospettiva prima di inviare.';
      }
      const first = form.querySelector('input[name="poll"]');
      first?.focus();
      return;
    }
    localStorage.setItem(key, choice.value);
    showResult(choice.value);
  });
})();
