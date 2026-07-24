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
      await renderLesson(scenario, lesson);
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

  async function renderLesson(scenario, lesson) {
    const target = document.getElementById('lessonBody');
    const response = await fetch(lesson.content_path, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`Could not load lesson (${response.status})`);
    FP.renderMd(await response.text(), target);
    rewriteLessonLinks(target, scenario);
  }

  function rewriteLessonLinks(container, scenario) {
    const byPath = new Map((scenario.lessons || []).map((lesson) => [lesson.path, lesson.lesson_path]));
    container.querySelectorAll('a[href]').forEach((link) => {
      const raw = link.getAttribute('href') || '';
      const normalized = raw.replace(/^\.\//, '');
      if (byPath.has(normalized)) link.href = byPath.get(normalized);
    });
  }

  function showError(message) {
    FP.renderError('mainContent', message);
  }

  document.addEventListener('DOMContentLoaded', init);
})();
