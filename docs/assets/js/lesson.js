(function () {
  'use strict';

  async function init() {
    const scenarioId = FP.qp('scenario');
    const lessonId = FP.qp('lesson');
    if (!scenarioId || !lessonId) return showError('Select a scenario and lesson to begin.');

    try {
      const data = await FP.loadData();
      const scenario = (data.scenarios || []).find((item) => item.id === scenarioId);
      const lesson = scenario && (scenario.lessons || []).find((item) => item.id === lessonId);
      if (!scenario || !lesson) return showError('This lesson was not found in the scenario course.');
      renderCourse(scenario, lesson);
      await renderLesson(scenario, lesson, data.activities || []);
    } catch (error) {
      showError(error.message);
    }
  }

  function renderCourse(scenario, lesson) {
    const playbookUrl = `scenario.html?id=${encodeURIComponent(scenario.id)}`;
    const lessons = scenario.lessons || [];
    const index = lessons.findIndex((item) => item.id === lesson.id);
    const previous = lessons[index - 1];
    const next = lessons[index + 1];

    document.title = `${lesson.title} — ${scenario.name} — AI Starter Kit`;
    document.getElementById('lessonTitle').textContent = lesson.title;
    document.getElementById('lessonEyebrow').textContent = `${scenario.name} · lesson ${lesson.sequence}`;
    document.getElementById('lessonSummary').textContent =
      'Make one customer decision, capture the evidence, and use the result to decide the next engagement move.';
    document.getElementById('lessonOutcome').textContent = scenario.customer_outcome;
    ['playbookBack', 'playbookNav'].forEach((id) => { document.getElementById(id).href = playbookUrl; });
    document.getElementById('lessonBuildModules').innerHTML = (scenario.build_modules || []).map((module) => `
      <li>
        <strong>${module.sequence}. ${FP.esc(module.title)}</strong>
        <span>${FP.esc(module.summary)}</span>
        <small>Checkpoint: ${FP.esc(module.checkpoint)}</small>
        ${module.activity_path ? `<a href="${FP.esc(module.activity_path)}">Open implementation activity</a>` : ''}
      </li>`).join('');

    document.getElementById('lessonProgress').innerHTML = lessons.map((item) => `
      <li class="${item.id === lesson.id ? 'is-current' : ''}">
        <a href="${FP.esc(item.lesson_path)}" ${item.id === lesson.id ? 'aria-current="step"' : ''}>
          <span>${item.sequence}</span>${FP.esc(item.title)}
        </a>
      </li>`).join('');

    document.getElementById('lessonPager').innerHTML = `
      ${previous ? `<a class="btn btn-ghost" href="${FP.esc(previous.lesson_path)}">Previous: ${FP.esc(previous.title)}</a>` : ''}
      ${next ? `<a class="btn btn-primary" href="${FP.esc(next.lesson_path)}">Next: ${FP.esc(next.title)}</a>` : ''}
      ${!next ? `<a class="btn btn-primary" href="${playbookUrl}">Return to playbook</a>` : ''}
    `;
  }

  async function renderLesson(scenario, lesson, activities) {
    const target = document.getElementById('lessonBody');
    const response = await fetch(lesson.content_path, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`Could not load lesson (${response.status})`);
    FP.renderMd(await response.text(), target);
    rewriteLessonLinks(target, scenario, lesson, activities);
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

  function rewriteLessonLinks(container, scenario, lesson, activities) {
    const lessonRoutes = new Map((scenario.lessons || []).map((item) => [item.path, item.lesson_path]));
    const activityIds = new Set((activities || []).map((item) => item.id));

    container.querySelectorAll('a[href]').forEach((link) => {
      const raw = link.getAttribute('href') || '';
      if (!raw || raw.startsWith('#') || /^[a-z][a-z0-9+.-]*:/i.test(raw)) return;

      const [path, hash] = raw.split('#');
      const resolved = resolveRelative(lesson.path, path);

      if (lessonRoutes.has(resolved)) {
        link.href = lessonRoutes.get(resolved);
        return;
      }

      const activityMatch = resolved.match(/^activities\/([^/]+)\/(README|FACILITATOR)\.md$/i);
      if (activityMatch && activityIds.has(activityMatch[1])) {
        link.href = FP.activityUrl(activityMatch[1]) + (hash ? `#${hash}` : '');
        link.dataset.route = 'activity';
        return;
      }

      if (/\.md$/i.test(path)) link.classList.add('is-source-link');
    });
  }

  function showError(message) {
    FP.renderError('mainContent', message);
  }

  document.addEventListener('DOMContentLoaded', init);
})();
