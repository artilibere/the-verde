(function () {
  const bars = document.querySelectorAll('.tv-share');
  if (!bars.length) return;

  const INVITE_TITLES = {
    variety: (title) => `Ho trovato una scheda chiara su ${title} — tè verde senza hype detox. Ti interessa?`,
    controversy: (title) =>
      `Questo pezzo mette ordine su «${title}», senza miracoli. Vale una lettura con calma:`,
    glossary: (title) => `Termine spiegato bene: ${title}. Per chi inizia col tè verde (solo Camellia sinensis):`,
    quiz: (title) => `Fai questo quiz sul tè verde e dimmi che varietà ti esce — poi confrontiamo:`,
    home: () =>
      'Scopri il tè verde con cultura e gusto, radicato in Italia — niente detox, solo Camellia sinensis:',
    catalog: () => 'Catalogo chiaro di varietà di tè verde — esploriamolo insieme?',
    hub: (title) => `Tema utile sul tè verde: ${title}.`,
    article: (title) => `Guide sul tè verde in Italia: ${title}.`,
    default: (title) => `${title} — The Verde`,
  };

  function pageContext(bar) {
    return bar.dataset.shareContext || 'default';
  }

  function pageTitle() {
    return (
      document.querySelector('meta[property="og:title"]')?.content ||
      document.querySelector('h1')?.textContent?.trim() ||
      document.title.split('|')[0].trim()
    );
  }

  function inviteMessage(context, title, url) {
    const hook = (INVITE_TITLES[context] || INVITE_TITLES.default)(title);
    return `${hook}\n\n${url}`;
  }

  function showFeedback(bar, message) {
    const feedback = bar.querySelector('.tv-share__feedback');
    if (!feedback) return;
    feedback.textContent = message;
    feedback.hidden = false;
    window.setTimeout(() => {
      feedback.hidden = true;
    }, 2800);
  }

  function showPreview(bar, message) {
    const preview = bar.querySelector('[data-share-preview]');
    if (!preview) return;
    preview.textContent = message;
    preview.hidden = false;
  }

  bars.forEach((bar) => {
    const context = pageContext(bar);
    const url = window.location.href;
    const title = pageTitle();
    const message = inviteMessage(context, title, url);

    const whatsapp = bar.querySelector('[data-share="whatsapp"]');
    const telegram = bar.querySelector('[data-share="telegram"]');
    const email = bar.querySelector('[data-share="email"]');
    const nativeBtn = bar.querySelector('[data-share="native"]');
    const copyMessageBtn = bar.querySelector('[data-share="copy-message"]');
    const copyLinkBtn = bar.querySelector('[data-share="copy-link"]');

    if (whatsapp) {
      whatsapp.href = `https://wa.me/?text=${encodeURIComponent(message)}`;
    }
    if (telegram) {
      const shareUrl = new URL('https://t.me/share/url');
      shareUrl.searchParams.set('url', url);
      shareUrl.searchParams.set('text', message.replace(`\n\n${url}`, ''));
      telegram.href = shareUrl.toString();
    }
    if (email) {
      const subject = encodeURIComponent(`The Verde — ${title}`);
      const body = encodeURIComponent(message);
      email.href = `mailto:?subject=${subject}&body=${body}`;
    }

    if (navigator.share && nativeBtn) {
      nativeBtn.hidden = false;
      nativeBtn.addEventListener('click', () => {
        navigator.share({ title, text: message }).catch(() => {});
      });
    }

    copyMessageBtn?.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(message);
        showFeedback(bar, 'Messaggio copiato — incollalo dove vuoi invitarlo');
        showPreview(bar, message);
      } catch {
        window.prompt('Copia il messaggio:', message);
      }
    });

    copyLinkBtn?.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(url);
        showFeedback(bar, 'Link copiato negli appunti');
      } catch {
        window.prompt('Copia il link:', url);
      }
    });
  });

  window.TVShare = {
    messageFor(context, title, url) {
      return inviteMessage(context, title, url);
    },
    scrollToInvite() {
      document.getElementById('condividi')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    },
  };
})();
