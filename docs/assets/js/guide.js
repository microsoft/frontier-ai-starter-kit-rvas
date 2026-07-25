(function () {
  'use strict';

  const GUIDES = {
    accelerator: { title: 'Accelerator guide', path: 'accelerator_path', summary: 'Deployable starter assets and reusable scripts.' },
  };

  async function init() {
    const scenarioId = FP.qp('scenario');
    const activityId = FP.qp('activity');
    const guideId = FP.qp('guide');
    if (!guideId) return showError('Select a guide.');
    if (/facilitator/i.test(guideId)) return showError('This guide no longer exists. Use the scenario lessons, activity guide, or solution path.');

    try {
      const data = await FP.loadData();
      if (activityId) return showError('This activity guide was not found. Use the activity page and solution path.');
      if (!scenarioId) return showError('Select a scenario and guide.');

      await renderScenarioGuide(data, scenarioId, guideId);
    } catch (error) {
      showError(error.message);
    }

  }

  async function renderScenarioGuide(data, scenarioId, guideId) {
    const scenario = (data.scenarios || []).find((item) => item.id === scenarioId);
    const guide = GUIDES[guideId];
    if (!scenario || !guide) return showError('This scenario guide was not found.');

    try {
      const sourcePath = scenario[guide.path];
      if (!sourcePath) return showError(`The ${guide.title.toLowerCase()} is not configured for this scenario.`);

      renderScenarioShell(scenario, guide);
      const response = await fetch(sourcePath, { cache: 'no-cache' });
      if (!response.ok) throw new Error(`Could not load guide (${response.status})`);
      const body = document.getElementById('guideBody');
      const content = await response.text();
      if (/\.md$/i.test(sourcePath)) {
        FP.renderMd(content, body);
        rewriteGuideLinks(body, scenario, sourcePath, data.activities || []);
        FP.initDiagramZoom(body);
      } else {
        renderCode(content, body);
      }
    } catch (error) {
      showError(error.message);
    }
  }

  function renderScenarioShell(scenario, guide) {
    document.title = `${guide.title} — ${scenario.name} — AI Starter Kit`;
    document.getElementById('guideTitle').textContent = guide.title;
    document.getElementById('guideEyebrow').textContent = scenario.name;
    document.getElementById('guideSummary').textContent = guide.summary;
    document.getElementById('guideBreadcrumbs').innerHTML = `
      <a href="index.html">Home</a>
      <span aria-hidden="true">/</span>
      <a href="index.html#outcomes">Scenarios</a>
      <span aria-hidden="true">/</span>
      <a href="scenario.html?id=${encodeURIComponent(scenario.id)}">${FP.esc(scenario.name)}</a>
      <span aria-hidden="true">/</span>
      <span>${FP.esc(guide.title)}</span>`;
    document.getElementById('guideActions').innerHTML = `
      <a id="scenarioBack" class="btn btn-ghost" href="scenario.html?id=${encodeURIComponent(scenario.id)}">Back to scenario</a>`;
  }

  function renderCode(content, target) {
    const pre = document.createElement('pre');
    pre.className = 'code-block';
    pre.textContent = content;
    target.innerHTML = '';
    target.appendChild(pre);
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
    const match = path.match(/(?:^|\/)(lesson|activity|scenario|slides|guide)\.html(\?.*)?$/i);
    return match ? `${match[1].toLowerCase()}.html${match[2] || ''}${hash ? `#${hash}` : ''}` : '';
  }

  function rewriteGuideLinks(container, scenario, sourcePath, activities) {
    const lessonRoutes = new Map((scenario.lessons || []).map((lesson) => [lesson.content_path, lesson.lesson_path]));
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

      const resolved = resolveRelative(sourcePath, path);
      if (lessonRoutes.has(resolved)) {
        link.href = lessonRoutes.get(resolved) + (hash ? `#${hash}` : '');
        return;
      }

      const activityMatch = resolved.match(/^assets\/data\/activities\/([^/]+)\/README\.md$/i);
      if (activityMatch && activityIds.has(activityMatch[1])) {
        link.href = FP.activityUrl(activityMatch[1]) + (hash ? `#${hash}` : '');
        return;
      }

      link.href = `${resolved}${hash ? `#${hash}` : ''}`;
    });
  }

  function showError(message) {
    FP.renderError('mainContent', message);
  }

  document.addEventListener('DOMContentLoaded', init);
})();
