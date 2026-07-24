(function () {
  'use strict';

  async function init() {
    const id = FP.qp('id');
    if (!id) return showError('No scenario was selected.');
    try {
      const data = await FP.loadData();
      const scenario = (data.scenarios || []).find((item) => item.id === id);
      if (!scenario) return showError(`Scenario "${id}" was not found.`);
      renderScenario(scenario);
      const response = await fetch(scenario.readme_path, { cache: 'no-cache' });
      if (!response.ok) throw new Error(`Could not load playbook (${response.status})`);
      FP.renderMd(await response.text(), document.getElementById('scenarioBody'));
    } catch (error) {
      showError(error.message);
    }
  }

  function renderScenario(scenario) {
    document.title = `${scenario.name} — AI Starter Kit`;
    document.getElementById('title').textContent = scenario.name;
    document.getElementById('tagline').textContent = scenario.tagline;
    document.getElementById('scenarioMaturity').textContent = `${scenario.maturity} scenario playbook`;
    document.getElementById('customerOutcome').textContent = scenario.customer_outcome;
    document.getElementById('slidesLink').href = `slides.html?id=${encodeURIComponent(scenario.id)}`;
    document.getElementById('acceleratorLink').href = scenario.accelerator_path;
    document.getElementById('localDemoLink').href = scenario.local_demo_path;
    document.getElementById('facilitatorLink').href = scenario.facilitator_path;
    document.getElementById('validatorLink').href = scenario.validator_path;
    document.getElementById('decisionPrompts').innerHTML = (scenario.decision_prompts || [])
      .map((prompt) => `<li>${FP.esc(prompt)}</li>`).join('');
    document.getElementById('buildModuleList').innerHTML = (scenario.build_modules || [])
      .map((module) => `<li><strong>${module.sequence}. ${FP.esc(module.title)}</strong><span>${FP.esc(module.summary)}</span><small>Checkpoint: ${FP.esc(module.checkpoint)}</small>${module.activity_path ? `<a href="${FP.esc(module.activity_path)}">Open implementation activity</a>` : ''}</li>`).join('');
    document.getElementById('lessonList').innerHTML = (scenario.lessons || [])
      .map((lesson) => `<li><a href="${FP.esc(lesson.lesson_path)}">Lesson ${lesson.sequence}: ${FP.esc(lesson.title)}</a></li>`).join('');
  }

  function showError(message) {
    const target = document.getElementById('scenarioBody');
    if (target) target.innerHTML = `<p class="text-dim">${FP.esc(message)}</p>`;
  }

  document.addEventListener('DOMContentLoaded', init);
})();
