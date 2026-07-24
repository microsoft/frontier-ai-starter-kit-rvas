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
      const body = document.getElementById('scenarioBody');
      FP.renderMd(await response.text(), body);
      rewriteScenarioLinks(body, scenario, data.activities || []);
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

  function resolveRelative(basePath, href) {
    const segments = basePath.split('/').slice(0, -1);
    href.split('/').forEach((part) => {
      if (!part || part === '.') return;
      if (part === '..') segments.pop();
      else segments.push(part);
    });
    return segments.join('/');
  }

  function routeAppPage(path, hash) {
    const match = path.match(/(?:^|\/)(lesson|activity|scenario|slides)\.html(\?.*)?$/i);
    return match ? `${match[1].toLowerCase()}.html${match[2] || ''}${hash ? `#${hash}` : ''}` : '';
  }

  function rewriteScenarioLinks(container, scenario, activities) {
    const lessonRoutes = new Map((scenario.lessons || []).map((lesson) => [lesson.path, lesson.lesson_path]));
    const activityIds = new Set((activities || []).map((activity) => activity.id));

    container.querySelectorAll('a[href]').forEach((link) => {
      const raw = link.getAttribute('href') || '';
      if (!raw || raw.startsWith('#') || /^[a-z][a-z0-9+.-]*:/i.test(raw)) return;

      const [path, hash] = raw.split('#');
      const appRoute = routeAppPage(path, hash);
      if (appRoute) {
        link.href = appRoute;
        return;
      }

      const resolved = resolveRelative('README.md', path);
      if (lessonRoutes.has(resolved)) {
        link.href = lessonRoutes.get(resolved) + (hash ? `#${hash}` : '');
        return;
      }

      const activityMatch = resolved.match(/^activities\/([^/]+)\/(?:README|FACILITATOR)\.md$/i);
      if (activityMatch && activityIds.has(activityMatch[1])) {
        link.href = FP.activityUrl(activityMatch[1]) + (hash ? `#${hash}` : '');
        return;
      }

      link.href = `${scenario.asset_base}${resolved}${hash ? `#${hash}` : ''}`;
    });
  }

  function showError(message) {
    const target = document.getElementById('scenarioBody');
    if (target) target.innerHTML = `<p class="text-dim">${FP.esc(message)}</p>`;
  }

  document.addEventListener('DOMContentLoaded', init);
})();
