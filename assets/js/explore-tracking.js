/**
 * Internal navigation analytics — explore_next and related_links clicks via GTM dataLayer.
 */
(function () {
  function pagePath() {
    return window.location.pathname || "/";
  }

  function pushEvent(params) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: "tv_internal_link" }, params));
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest("a[data-tv-track]");
    if (!link) {
      return;
    }
    pushEvent({
      tv_link_type: link.getAttribute("data-tv-track") || "",
      tv_link_url: link.getAttribute("data-tv-track-url") || link.getAttribute("href") || "",
      tv_link_label: link.getAttribute("data-tv-track-label") || link.textContent.trim(),
      tv_link_reason: link.getAttribute("data-tv-track-reason") || "",
      tv_link_pos: link.getAttribute("data-tv-track-pos") || "",
      tv_page_path: pagePath(),
    });
  });
})();
