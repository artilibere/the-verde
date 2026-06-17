(function () {
  const form = document.getElementById('controversy-poll');
  const result = document.getElementById('poll-result');
  if (!form) return;
  const key = `tv-poll-${form.closest('[data-controversy]')?.dataset.controversy || 'default'}`;
  const saved = localStorage.getItem(key);
  if (saved && result) {
    result.hidden = false;
    result.textContent = `Hai riflettuto con la prospettiva ${saved}. Esplora le altre voci sopra.`;
  }
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const choice = form.querySelector('input[name="poll"]:checked');
    if (!choice || !result) return;
    localStorage.setItem(key, choice.value);
    result.hidden = false;
    result.textContent = `Hai scelto la prospettiva ${choice.value}. Ora leggi le altre: è lì che nasce la comprensione.`;
  });
})();
