/**
 * Navigation prefetch — warm cache for likely next pages (explore_next, path nav, hubs).
 * Uses link[rel=prefetch] on intent (hover/touch) and for high-priority anchors.
 */
(function () {
  'use strict';

  var prefetched = new Set();
  var hoverTimer = null;

  var INTENT_SELECTORS = [
    'a[data-tv-prefetch]',
    '.tv-explore-next a[href]',
    '.tv-breadcrumb a[href]',
    '.tv-path-nav a[href]',
    '.tv-bottom-nav a[href]',
    '.tv-header__nav a[href]',
    '.tv-mininav a[href]',
    '.tv-footer__nav a[href]',
  ].join(',');

  function normalizePath(href) {
    if (!href || href.charAt(0) === '#') return null;
    try {
      var url = new URL(href, window.location.href);
      if (url.origin !== window.location.origin) return null;
      if (url.pathname.replace(/\/$/, '') === window.location.pathname.replace(/\/$/, '')) {
        return null;
      }
      return url.pathname + url.search;
    } catch (_err) {
      return null;
    }
  }

  function shouldSkip(path) {
    if (!path) return true;
    if (path.indexOf('/diario/nuova') !== -1) return true;
    if (path.indexOf('/cerca') === 0) return true;
    return false;
  }

  function prefetchPath(path) {
    if (shouldSkip(path) || prefetched.has(path)) return;
    prefetched.add(path);
    var link = document.createElement('link');
    link.rel = 'prefetch';
    link.as = 'document';
    link.href = path;
    document.head.appendChild(link);
  }

  function isHighPriority(link) {
    return link.getAttribute('data-tv-prefetch') === 'high';
  }

  function scheduleIntent(link) {
    var path = normalizePath(link.getAttribute('href'));
    if (!path) return;

    clearTimeout(hoverTimer);
    if (isHighPriority(link)) {
      prefetchPath(path);
      return;
    }

    hoverTimer = window.setTimeout(function () {
      prefetchPath(path);
    }, 65);
  }

  function bindIntent(link) {
    if (link.dataset.tvPrefetchBound === '1') return;
    link.dataset.tvPrefetchBound = '1';

    link.addEventListener(
      'mouseenter',
      function () {
        scheduleIntent(link);
      },
      { passive: true }
    );
    link.addEventListener(
      'mouseleave',
      function () {
        clearTimeout(hoverTimer);
      },
      { passive: true }
    );
    link.addEventListener(
      'focus',
      function () {
        scheduleIntent(link);
      },
      { passive: true }
    );
    link.addEventListener(
      'touchstart',
      function () {
        prefetchPath(normalizePath(link.getAttribute('href')));
      },
      { passive: true }
    );
  }

  function bindIntentLinks(root) {
    var scope = root || document;
    scope.querySelectorAll(INTENT_SELECTORS).forEach(bindIntent);
  }

  function prefetchHighPriority() {
    document.querySelectorAll('a[data-tv-prefetch="high"][href]').forEach(function (link) {
      prefetchPath(normalizePath(link.getAttribute('href')));
    });
  }

  function prefetchIdleHubs() {
    if (window.location.pathname.indexOf('/cerca') === 0) return;
    ['/varieta/', '/italia/', '/impara/', '/guide/'].forEach(function (path) {
      prefetchPath(path);
    });
  }

  function onCatalogHover(event) {
    var link = event.target.closest('.tv-catalog-results a[href]');
    if (!link) return;
    scheduleIntent(link);
  }

  function init() {
    bindIntentLinks();
    prefetchHighPriority();

    var catalog = document.querySelector('.tv-catalog-results');
    if (catalog) {
      catalog.addEventListener('mouseover', onCatalogHover, { passive: true });
    }

    var idle = window.requestIdleCallback || function (cb) {
      window.setTimeout(cb, 1200);
    };
    idle(function () {
      prefetchIdleHubs();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
