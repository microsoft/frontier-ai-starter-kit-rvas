(function () {
  'use strict';

  const GUIDES = {
    accelerator: { title: 'Accelerator guide', path: 'accelerator_path', summary: 'Deployable starter assets and module checkpoints.' },
    demo: { title: 'Local demo', path: 'local_demo_path', summary: 'Offline demo and validation flow for this scenario.' },
    facilitator: { title: 'Facilitator guide', path: 'facilitator_path', summary: 'Delivery notes, pacing, prompts, and facilitation guardrails.' },
    validator: { title: 'Local validator', path: 'validator_path', summary: 'Validator source and the checks it runs.' },
  };

  const STATIC_GUIDES = {
    'facilitator-hub': {
      title: 'Facilitator Hub',
      path: 'facilitator-hub.md',
      summary: 'Facilitation, pacing, unblock strategy, and customer-delivery guidance.',
    },
  };

  async function init() {
    const scenarioId = FP.qp('scenario');
    const activityId = FP.qp('activity');
    const guideId = FP.qp('guide');
    if (!guideId) return showError('Select a guide.');

    try {
      const data = await FP.loadData();
      if (activityId) {
        await renderActivityGuide(data, activityId, guideId);
        return;
      }
      if (!scenarioId && STATIC_GUIDES[guideId]) {
        await renderStaticGuide(STATIC_GUIDES[guideId]);
        return;
      }
      if (!scenarioId) return showError('Select a scenario and guide.');

      await renderScenarioGuide(data, scenarioId, guideId);
    } catch (error) {
      showError(error.message);
    }

    async function renderStaticGuide(guide) {
      try {
        renderStaticShell(guide);
        const response = await fetch(guide.path, { cache: 'no-cache' });
        if (!response.ok) throw new Error(`Could not load guide (${response.status})`);
        const body = document.getElementById('guideBody');
        const content = (await response.text())
          .replace(/^---\s*\n[\s\S]*?\n---\s*\n/mu, '')
          .replace(/\{\{\s*'\/customer-outcome'\s*\|\s*relative_url\s*\}\}/g, FP.activityUrl('customer-outcome'))
          .replace(/\{\{\s*'\/reference\.html'\s*\|\s*relative_url\s*\}\}/g, 'reference.html');
        FP.renderMd(content, body);
        FP.initDiagramZoom(body);
      } catch (error) {
        showError(error.message);
      }
    }

    function renderStaticShell(guide) {
      document.title = `${guide.title} — AI Starter Kit`;
      document.getElementById('guideTitle').textContent = guide.title;
      document.getElementById('guideEyebrow').textContent = 'Facilitator resource';
      document.getElementById('guideSummary').textContent = guide.summary;
      document.getElementById('guideBreadcrumbs').innerHTML = `
        <a href="index.html">Home</a>
        <span aria-hidden="true">/</span>
        <span>${FP.esc(guide.title)}</span>`;
      document.getElementById('guideActions').innerHTML = `
        <a class="btn btn-ghost" href="index.html#outcomes">See scenarios</a>
        <a class="btn btn-ghost" href="reference.html">Reference Library</a>`;
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

  async function renderActivityGuide(data, activityId, guideId) {
    if (guideId !== 'facilitator') return showError('This activity guide was not found.');

    const activity = (data.activities || []).find((item) => item.id === activityId);
    if (!activity || !activity.has_facilitator_guide) return showError('This activity does not have facilitator notes.');

    try {
      renderActivityShell(activity);
      const response = await fetch(activity.facilitator_path, { cache: 'no-cache' });
      if (!response.ok) throw new Error(`Could not load guide (${response.status})`);
      const body = document.getElementById('guideBody');
      FP.renderMd(await response.text(), body);
      rewriteActivityGuideLinks(body, activity);
      FP.initDiagramZoom(body);
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

  function renderActivityShell(activity) {
    document.title = `Facilitator notes — ${activity.title} — AI Starter Kit`;
    document.getElementById('guideTitle').textContent = 'Facilitator notes';
    document.getElementById('guideEyebrow').textContent = activity.title;
    document.getElementById('guideSummary').textContent =
      'Delivery notes, pitfalls, timing, and verification guidance for facilitators.';
    document.getElementById('guideBreadcrumbs').innerHTML = `
      <a href="index.html">Home</a>
      <span aria-hidden="true">/</span>
      <a href="reference.html">Reference Library</a>
      <span aria-hidden="true">/</span>
      <a href="activity.html?id=${encodeURIComponent(activity.id)}">${FP.esc(activity.title)}</a>
      <span aria-hidden="true">/</span>
      <span>Facilitator notes</span>`;
    document.getElementById('guideActions').innerHTML = `
      <a class="btn btn-ghost" href="activity.html?id=${encodeURIComponent(activity.id)}">Back to activity</a>`;
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

      const activityMatch = resolved.match(/^assets\/data\/activities\/([^/]+)\/(?:README|FACILITATOR)\.md$/i);
      if (activityMatch && activityIds.has(activityMatch[1])) {
        link.href = FP.activityUrl(activityMatch[1]) + (hash ? `#${hash}` : '');
        return;
      }

      link.href = `${resolved}${hash ? `#${hash}` : ''}`;
    });
  }

  function rewriteActivityGuideLinks(container, activity) {
    container.querySelectorAll('a[href]').forEach((link) => {
      const raw = link.getAttribute('href') || '';
      if (!raw || raw.startsWith('#') || /^[a-z][a-z0-9+.-]*:/i.test(raw)) return;

      const [path, hash] = raw.split('#');
      if (path === 'README.md') {
        link.href = `activity.html?id=${encodeURIComponent(activity.id)}${hash ? `#${hash}` : ''}`;
      }
    });
  }

  function showError(message) {
    FP.renderError('mainContent', message);
  }

  document.addEventListener('DOMContentLoaded', init);
})();
