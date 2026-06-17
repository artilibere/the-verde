// Giscus: sostituire repo-id e category-id con valori reali del repository GitHub
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('giscus-container');
  if (!container || container.dataset.loaded) return;
  const script = document.createElement('script');
  script.src = 'https://giscus.app/client.js';
  script.setAttribute('data-repo', 'YOUR_ORG/the-verde.it');
  script.setAttribute('data-repo-id', 'GISCUS_REPO_ID');
  script.setAttribute('data-category', 'Community');
  script.setAttribute('data-category-id', 'GISCUS_CATEGORY_ID');
  script.setAttribute('data-mapping', 'pathname');
  script.setAttribute('data-theme', 'light');
  script.setAttribute('data-lang', 'it');
  script.crossOrigin = 'anonymous';
  script.async = true;
  container.appendChild(script);
  container.dataset.loaded = 'true';
});
