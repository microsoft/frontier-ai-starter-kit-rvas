/* Microsoft Foundry — activity detail page (?id=<activityId>) */
(function () {
  'use strict';

  let _route = null;

  function cUrl(id) {
    const q = new URLSearchParams();
    q.set('id', id);
    if (_route) q.set('outcome', _route);
    return 'activity.html?' + q.toString();
  }

  async function init() {
    const requestedId = FP.qp('id');
    if (!requestedId) { showError('No activity ID specified.'); return; }

    let data;
    try { data = await FP.loadData(); }
    catch (e) { showError(e.message); return; }

    const alias = (data.aliases || {})[requestedId];
    const activityId = alias ? alias.id : requestedId;
    const activity = (data.activities || []).find((c) => c.id === activityId);
    if (!activity) { showError('Activity "' + requestedId + '" not found.'); return; }

    const mod = (data.modules || []).find((m) => m.id === activity.module);
    const allActivities = data.activities || [];
    _route = resolveRoute(activity);

    document.title = activity.title + ' — AI Starter Kit';

    // A render error used to reject silently and leave the page frozen on its
    // placeholders, which reads as a slow network rather than a bug. Surface it.
    try {
      applyModuleColor(activity.module);
      renderHero(activity, mod);
      renderFacts(activity, mod, allActivities, data.outcomes || []);
      renderRelated(activity, allActivities);
    } catch (e) {
      console.error('activity page render failed', e);
      showError('This page failed to render: ' + e.message);
      return;
    }

    loadGuide(activity, allActivities);
  }

  function applyModuleColor(moduleId) {
    const color = FP.moduleColor(moduleId);
    document.documentElement.style.setProperty('--mod-color', color);
    document.querySelectorAll('[data-mod-color]').forEach((el) => {
      el.style.color = color;
    });
  }

  function renderHero(c, mod) {
    const color = FP.moduleColor(c.module);

    // Breadcrumbs
    const crumbs = document.getElementById('breadcrumbs');
    if (crumbs) {
      crumbs.innerHTML = `
        <a href="index.html">Home</a>
        <span aria-hidden="true">/</span>
        <a href="reference.html">Reference Library</a>
        <span aria-hidden="true">/</span>
        <span style="color:${color}">${FP.esc(c.track || c.module)}</span>
        <span aria-hidden="true">/</span>
        <span>${FP.esc(c.id)}</span>`;
    }

    _setText('activityTitle', c.title);
    _setText('activityId', c.id);
    _setText('activityEyebrow', `Reference activity · ${c.track || c.module || 'Reusable capability'}`);
    _setText(
      'activitySummary',
      c.description || 'Use this reusable build activity to prove a specific capability before adapting it to your scenario.'
    );

    const meta = document.getElementById('activityMeta');
    if (meta) {
      meta.innerHTML = `
        ${FP.diffBadge(c.difficulty)}
        ${FP.durBadge(c.duration_minutes)}
        ${c.tier && c.tier !== 'core' ? `<span class="badge badge-app">${FP.esc(c.tier)}</span>` : ''}
        ${c.app_dependency && c.app_dependency !== 'none' ? `<span class="badge badge-app">App: ${FP.esc(c.app_dependency)}</span>` : ''}
        <span class="badge-tag badge" style="color:${color}">${FP.esc(c.module)} · ${FP.esc(c.track || '')}</span>`;
    }

  }

  function renderFacts(c, mod, allActivities, outcomes) {
    // Prerequisites
    const prereqPanel = document.getElementById('prereqPanel');
    const prereqList  = document.getElementById('prereqList');
    if (prereqPanel && prereqList) {
      if (!c.prerequisites || !c.prerequisites.length) {
        prereqPanel.style.display = 'none';
      } else {
        prereqList.innerHTML = c.prerequisites.map((pid) => {
          const prereq = allActivities.find((x) => x.id === pid);
          return `<li class="prereq-item">
            ${prereq
              ? `<a href="${cUrl(pid)}" style="color:${FP.moduleColor(prereq.module)}">${FP.esc(prereq.title)}</a>`
              : `<span class="mono">${FP.esc(pid)}</span>`}
          </li>`;
        }).join('');
      }
    }

    // Prerequisite capabilities
    const capPanel = document.getElementById('capPanel');
    const capList  = document.getElementById('capList');
    if (capPanel && capList) {
      if (!c.prerequisite_capabilities || !c.prerequisite_capabilities.length) {
        capPanel.style.display = 'none';
      } else {
        capList.innerHTML = c.prerequisite_capabilities
          .map((cap) => `<li class="cap-item">${FP.esc(cap)}</li>`)
          .join('');
      }
    }

    // Success criteria
    const criteriaList = document.getElementById('criteriaList');
    if (criteriaList) {
      criteriaList.innerHTML = successCriteriaFor(c)
        .map((s) => `<li class="criteria-item"><span>${FP.renderInlineMd(s)}</span></li>`)
        .join('');
    }

    // References
    const refPanel = document.getElementById('refPanel');
    const refList  = document.getElementById('refList');
    if (refPanel && refList) {
      if (!c.references || !c.references.length) {
        refPanel.style.display = 'none';
      } else {
        refList.innerHTML = c.references.map((r) =>
          `<a href="${FP.esc(r)}" target="_blank" rel="noopener" class="attribution" style="display:block;margin-bottom:5px">${FP.esc(r.replace('https://', ''))}</a>`
        ).join('');
      }
    }
  }

  function successCriteriaFor(c) {
    if (c.success_criteria && c.success_criteria.length) return c.success_criteria;

    const criteria = [];
    if (c.description) criteria.push(c.description);

    if (c.id === 'setup') {
      criteria.push('Your local or cloud workspace can authenticate to Azure and run the repository validation commands.');
    } else if (c.id === 'cleanup') {
      criteria.push('You can identify the resources created for the session and remove or stop them safely.');
    } else if (c.track === 'define') {
      criteria.push('You leave with a scenario decision or handoff artifact that a customer team can review.');
    } else if (c.track === 'foundations') {
      criteria.push('The resulting agent or project can answer a test question using the approved sample grounding path.');
    } else if (c.track === 'actions') {
      criteria.push('A governed action path proves the agent can call a tool without bypassing approval or safety boundaries.');
    } else if (c.track === 'trust') {
      criteria.push('The activity produces evidence a facilitator can use to accept, reject, or improve the agent behavior.');
    } else if (c.track === 'deploy') {
      criteria.push('The result can be invoked outside the notebook or local script through the intended deployment surface.');
    } else {
      criteria.push('The reusable artifact is ready to adapt inside a customer scenario without changing the scenario journey.');
    }

    return [...new Set(criteria)];
  }

  function renderRelated(c, allActivities) {
    const relPanel = document.getElementById('relatedPanel');
    const relGrid  = document.getElementById('relatedGrid');
    if (!relPanel || !relGrid) return;

    const myTags = new Set(c.tags || []);
    const related = allActivities
      .filter((x) => x.id !== c.id && (x.tags || []).some((t) => myTags.has(t)))
      .sort((a, b) => {
        const aMatch = (a.tags || []).filter((t) => myTags.has(t)).length;
        const bMatch = (b.tags || []).filter((t) => myTags.has(t)).length;
        return bMatch - aMatch;
      })
      .slice(0, 5);

    if (!related.length) { relPanel.style.display = 'none'; return; }

    relGrid.innerHTML = related.map((r) => {
      const color = FP.moduleColor(r.module);
      return `
        <a href="${cUrl(r.id)}" class="related-item">
          <span class="related-dot" style="background:${color}"></span>
          <span style="flex:1;min-width:0;font-size:0.8rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${FP.esc(r.title)}</span>
          <span class="badge badge-tag" style="color:${color};flex-shrink:0">${FP.esc(r.module)}</span>
        </a>`;
    }).join('');
  }

  async function loadGuide(c, allActivities) {
    const body = document.getElementById('guideBody');
    if (!body) return;

    const path = c.participant_path;
    if (!path) {
      body.innerHTML = `<p class="text-dim" style="font-size:.875rem">Guide not available for this view.</p>`;
      return;
    }

    body.innerHTML = '<p class="text-dim" style="font-size:.875rem;font-family:var(--font-mono)">Loading guide…</p>';

    try {
      const res = await fetch(path, { cache: 'no-cache' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const md = stripRedundantActivityMetadata(await res.text());
      FP.renderMd(md, body);
      ensureGuideAnchors(body);
      removeDuplicateGuideTitle(body, c);
      body.querySelectorAll('.next-panel').forEach((el) => el.remove());
      renderActivityPager(body, c, allActivities);
      scrollToGuideAnchor(body);
      FP.initDiagramZoom(body);
    } catch (e) {
      body.innerHTML = `<p class="text-dim" style="font-size:.875rem">Could not load guide: ${FP.esc(e.message)}</p>`;
      renderActivityPager(body, c, allActivities);
    }

    function stripRedundantActivityMetadata(markdown) {
      const lines = String(markdown || '').split(/\r?\n/);
      const output = [];
      for (let index = 0; index < lines.length;) {
        if (!lines[index].startsWith('>')) {
          output.push(lines[index]);
          index += 1;
          continue;
        }

        const block = [];
        while (index < lines.length && lines[index].startsWith('>')) {
          block.push(lines[index]);
          index += 1;
        }

        const text = block
          .map((line) => line.replace(/^>\s?/, '').trim())
          .join(' ');
        const isRepeatedMetadata =
          /(?:Guided|Build-from-scratch|Prereqs?:|⭐|⏱|🛠)/u.test(text) ||
          /^Tier\s+\d+\s*[·-]/i.test(text);

        if (!isRepeatedMetadata) output.push(...block);
      }
      return output.join('\n');
    }

    function ensureGuideAnchors(container) {
      container.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach((heading) => {
        if (!heading.id) heading.id = guideHeadingId(heading.textContent || '');
      });
    }

    function guideHeadingId(value) {
      return String(value || '')
        .trim()
        .toLowerCase()
        .replace(/[^\w\s-]/gu, '')
        .replace(/\s+/gu, '-');
    }

    function scrollToGuideAnchor(container) {
      const id = decodeURIComponent(window.location.hash.slice(1));
      if (!id) return;
      const target = container.querySelector('#' + CSS.escape(id));
      if (target) requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
    }
  }

  function removeDuplicateGuideTitle(container, activity) {
    const title = container.querySelector('h1');
    if (!title || !activity || !activity.title) return;

    const guideTitle = normalizeTitle(title.textContent);
    const activityTitle = normalizeTitle(activity.title);

    if (guideTitle === activityTitle || guideTitle.endsWith(' · ' + activityTitle)) {
      title.remove();
    }
  }

  function normalizeTitle(value) {
    return String(value || '')
      .replace(/[‘’]/g, "'")
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();
  }

  function renderActivityPager(container, current, allActivities) {
    if (!container || !Array.isArray(allActivities) || !allActivities.length) return;

    const sequence = activitySequence(allActivities, current);
    const index = sequence.findIndex((c) => c.id === current.id);
    if (index === -1) return;

    const prev = sequence[index - 1] || null;
    const next = sequence[index + 1] || null;

    const nav = document.createElement('nav');
    nav.className = 'activity-pager';
    nav.setAttribute('aria-label', 'Activity navigation');
    nav.innerHTML = `
      ${pagerItem(prev, 'prev', '← Previous')}
      ${pagerItem(next, 'next', 'Next →')}
    `;
    container.appendChild(nav);
  }

  function activitySequence(allActivities, current) {
    const route = _route || (current.outcomes || [])[0];
    if (!route) return allActivities;
    return allActivities.filter((c) => (c.outcomes || []).includes(route));
  }

  function resolveRoute(activity) {
    const routes = activity.outcomes || [];
    const requested = FP.qp('outcome');
    if (requested && routes.includes(requested)) return requested;
    return routes[0] || null;
  }

  function pagerItem(activity, direction, label) {
    if (!activity) {
      return `
        <span class="activity-pager-link ${direction} is-disabled" aria-disabled="true">
          <span>${label}</span>
          <strong>No ${direction === 'prev' ? 'previous' : 'next'} activity</strong>
        </span>`;
    }

    return `
      <a class="activity-pager-link ${direction}" href="${cUrl(activity.id)}">
        <span>${label}</span>
        <strong>${FP.esc(activity.title)}</strong>
      </a>`;
  }

  function showError(msg) {
    const main = document.getElementById('mainContent');
    if (main) main.innerHTML = `<div class="wrap section"><div class="empty">${FP.esc(msg)}</div></div>`;
  }

  function _setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  }

  document.addEventListener('DOMContentLoaded', () => {
    init().catch((e) => {
      console.error('activity page failed to initialise', e);
      showError('This page failed to load: ' + e.message);
    });
  });
})();
