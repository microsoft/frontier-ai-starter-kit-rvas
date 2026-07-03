/* Microsoft Foundry — home page */
(function () {
  'use strict';

  async function init() {
    let data;
    try { data = await FP.loadData(); }
    catch (e) { FP.renderError('outcomeGrid', e.message); return; }

    const { outcomes, challenges } = data;

    renderStats(outcomes || [], challenges);
    renderOutcomeCards(outcomes || [], challenges);
  }

  function renderStats(outcomes, challenges) {
    const totalChallenges = challenges.length;
    const totalPaths = outcomes.length;
    const totalTracks = new Set(challenges.map((c) => c.track).filter(Boolean)).size;
    const totalMins = challenges.reduce((s, c) => s + (c.duration_minutes || 0), 0);

    _setText('stat-challenges', totalChallenges);
    _setText('stat-modules', totalPaths);
    _setText('stat-tracks', totalTracks);
    const h = Math.round(totalMins / 60);
    _setText('stat-hours', h + 'h');
  }

  function renderOutcomeCards(outcomes, challenges) {
    const grid = document.getElementById('outcomeGrid');
    if (!grid) return;

    if (!outcomes.length) {
      grid.innerHTML = '<div class="empty">No outcome journeys configured.</div>';
      return;
    }

    grid.innerHTML = outcomes.map((o) => {
      const count = o.challenge_count || (o.challenge_ids || []).length || 0;
      const mins = o.duration_minutes || (o.challenge_ids || []).reduce((sum, id) => {
        const c = challenges.find((x) => x.id === id);
        return sum + (c && c.duration_minutes ? c.duration_minutes : 0);
      }, 0);
      const metrics = (o.success_metrics || []).slice(0, 2)
        .map((m) => `<li>${FP.esc(m)}</li>`)
        .join('');
      return `
        <a href="${FP.catalogOutcomeUrl(o.id)}" class="outcome-card reveal">
          <div class="outcome-card-top">
            <span class="outcome-id">${FP.esc(o.id)}</span>
            <span class="badge badge-duration">${count} challenges</span>
            ${FP.durBadge(mins)}
          </div>
          <h3>${FP.esc(o.name)}</h3>
          <p>${FP.esc(o.tagline || o.description || '')}</p>
          ${metrics ? `<ul class="outcome-metrics">${metrics}</ul>` : ''}
        </a>`;
    }).join('');
    FP.initReveal();
  }

  function _setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  }

  document.addEventListener('DOMContentLoaded', init);
})();
