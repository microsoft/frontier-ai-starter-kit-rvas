/* AI Starter Kit — dedicated Idea Forge page. */
(function () {
  'use strict';

  async function init() {
    const target = document.getElementById('ideaForgeBody');
    if (!target) return;

    try {
      const response = await fetch('assets/data/activities/idea-forge/README.md', { cache: 'no-cache' });
      if (!response.ok) throw new Error(`Could not load Idea Forge (${response.status})`);
      FP.renderMd(await response.text(), target);
      rewriteLinks(target);
    } catch (error) {
      target.innerHTML = `<p class="text-dim">${FP.esc(error.message)}</p>`;
    }
  }

  function rewriteLinks(container) {
    container.querySelectorAll('a[href]').forEach((link) => {
      const raw = link.getAttribute('href') || '';
      if (!raw || raw.startsWith('#') || /^[a-z][a-z0-9+.-]*:/i.test(raw)) return;
      if (raw.indexOf('scenario.html') !== -1 || raw.indexOf('activity.html') !== -1) {
        link.href = raw.replace(/^\.\//, '');
        return;
      }
      if (raw === '/#outcomes' || raw === '#outcomes') {
        link.href = 'index.html#outcomes';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
