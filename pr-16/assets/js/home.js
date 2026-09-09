/* Microsoft Foundry — home page */
(function () {
  'use strict';

  async function init() {
    let data;
    try { data = await FP.loadData(); }
    catch (e) { FP.renderError('outcomeGrid', e.message); return; }

    const { scenarios, activities } = data;

    renderStats(scenarios || [], activities);
    renderScenarioCards(scenarios || []);
  }

  function renderStats(scenarios, activities) {
    const totalActivities = activities.length;
    const totalPaths = scenarios.length;
    const totalLessons = scenarios.reduce((sum, scenario) => sum + (scenario.lessons || []).length, 0);
    const totalPrompts = scenarios.reduce((sum, scenario) => sum + (scenario.decision_prompts || []).length, 0);

    _setText('stat-activities', totalActivities);
    _setText('stat-modules', totalPaths);
    _setText('stat-tracks', totalLessons);
    _setText('stat-hours', totalPrompts);
  }

  function renderScenarioCards(scenarios) {
    const grid = document.getElementById('outcomeGrid');
    if (!grid) return;

    if (!scenarios.length) {
      grid.innerHTML = '<div class="empty">No scenario playbooks configured.</div>';
      return;
    }

    grid.innerHTML = scenarios.map((scenario) => {
      const lessons = scenario.lessons || [];
      const prompts = (scenario.decision_prompts || []).slice(0, 2)
        .map((prompt) => `<li>${FP.esc(prompt)}</li>`)
        .join('');
      return `
        <a href="scenario.html?id=${encodeURIComponent(scenario.id)}" class="outcome-card reveal">
          <div class="outcome-card-top">
            <span class="outcome-id">${FP.esc(scenario.maturity || 'initial')}</span>
            <span class="badge badge-duration">${lessons.length} lessons</span>
          </div>
          <h3>${FP.esc(scenario.name)}</h3>
          <p>${FP.esc(scenario.tagline || '')}</p>
          ${prompts ? `<ul class="outcome-metrics">${prompts}</ul>` : ''}
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
