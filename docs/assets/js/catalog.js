/* Build AI apps — path catalog: choose one route, then filter chapters. */
(function () {
  'use strict';

  let _all = [];
  let _outcomes = [];
  let _activeOutcome = null;
  let _activeDiff = null;
  let _query = '';

  async function init() {
    let data;
    try { data = await FP.loadData(); }
    catch (e) { FP.renderError('grid', e.message); return; }

    _all = data.challenges || [];
    _outcomes = data.outcomes || [];

    buildOutcomeChips();
    buildDiffChips();
    initSearch();
    applyUrlState();
    render();
  }

  const DIFFS = ['beginner', 'intermediate', 'advanced'];

  /* Seed filter state from the URL query string (?outcome=&difficulty=&q=) and
     reflect it on the chips + search input before the first render. Invalid
     values are ignored rather than applied. */
  function applyUrlState() {
    const outcome = FP.qp('outcome');
    if (outcome && _outcomes.some((o) => o.id === outcome)) _activeOutcome = outcome;
    if (!_activeOutcome) _activeOutcome = defaultOutcomeId();

    const diff = FP.qp('difficulty');
    if (diff && DIFFS.indexOf(diff) !== -1) _activeDiff = diff;

    const q = (FP.qp('q') || '').trim();
    if (q) {
      _query = q.toLowerCase();
      const input = document.getElementById('searchInput');
      if (input) input.value = q;
    }

    syncChipState();
    syncUrl();
  }

  /* Reflect active filters onto the rendered chips. */
  function syncChipState() {
    document.querySelectorAll('#outcomeChips .chip').forEach((b) => {
      const on = b.dataset.outcome === _activeOutcome;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', String(on));
    });
    document.querySelectorAll('#diffChips .chip').forEach((b) => {
      const on = b.dataset.diff === _activeDiff;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', String(on));
    });
  }

  /* Keep the address bar in sync with the active filters so the view is
     shareable. replaceState avoids polluting back/forward history. */
  function syncUrl() {
    const q = new URLSearchParams();
    q.set('outcome', _activeOutcome || defaultOutcomeId());
    if (_activeDiff) q.set('difficulty', _activeDiff);
    if (_query) q.set('q', _query);
    const qs = q.toString();
    const url = window.location.pathname + (qs ? '?' + qs : '');
    window.history.replaceState(null, '', url);
  }

  function buildOutcomeChips() {
    const container = document.getElementById('outcomeChips');
    if (!container) return;
    container.innerHTML = _outcomes.map((o) =>
      `<button class="chip chip-outcome" data-outcome="${FP.esc(o.id)}"
         aria-pressed="false" type="button">
         ${FP.esc(o.name)}
       </button>`
    ).join('');

    container.querySelectorAll('.chip').forEach((btn) => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.outcome;
        _activeOutcome = id;
        syncChipState();
        syncUrl();
        render();
      });
    });
  }

  function buildDiffChips() {
    const container = document.getElementById('diffChips');
    if (!container) return;
    const diffs = ['beginner', 'intermediate', 'advanced'];
    container.innerHTML = diffs.map((d) =>
      `<button class="chip" data-diff="${d}" aria-pressed="false" type="button">${d}</button>`
    ).join('');

    container.querySelectorAll('.chip').forEach((btn) => {
      btn.addEventListener('click', () => {
        const d = btn.dataset.diff;
        _activeDiff = _activeDiff === d ? null : d;
        container.querySelectorAll('.chip').forEach((b) => {
          b.classList.toggle('active', b.dataset.diff === _activeDiff);
          b.setAttribute('aria-pressed', String(b.dataset.diff === _activeDiff));
        });
        syncUrl();
        render();
      });
    });
  }

  function initSearch() {
    const input = document.getElementById('searchInput');
    if (!input) return;
    input.addEventListener('input', () => {
      _query = input.value.trim().toLowerCase();
      syncUrl();
      render();
    });

    const clearBtn = document.getElementById('clearBtn');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        _query = '';
        input.value = '';
        _activeOutcome = defaultOutcomeId();
        _activeDiff = null;
        syncChipState();
        syncUrl();
        render();
      });
    }
  }

  function filtered() {
    return _all.filter((c) => {
      if (!_activeOutcome) return false;
      if (!(c.outcomes || []).includes(_activeOutcome)) return false;
      if (_activeDiff   && c.difficulty !== _activeDiff) return false;
      if (_query) {
        const outcomeNames = (c.outcomes || []).map((id) => FP.outcomeName(id, _outcomes));
        const hay = [c.title, c.description, ...(c.tags || []), ...outcomeNames, c.module, c.track]
          .join(' ').toLowerCase();
        if (!hay.includes(_query)) return false;
      }

      return true;
    });
  }

  function defaultOutcomeId() {
    return _outcomes.length ? _outcomes[0].id : '';
  }

  function render() {
    const grid = document.getElementById('grid');
    const countEl = document.getElementById('count');
    if (!grid) return;

    const items = filtered();

    if (countEl) countEl.textContent = items.length + ' challenge' + (items.length === 1 ? '' : 's');

    if (!items.length) {
      grid.innerHTML = '<div class="no-results">No challenges match those filters. <button class="btn btn-ghost btn-sm" id="inlineClrBtn" type="button">Clear filters</button></div>';
      const b = document.getElementById('inlineClrBtn');
      if (b) b.addEventListener('click', () => document.getElementById('clearBtn')?.click());
      return;
    }

    grid.innerHTML = `<div class="challenge-grid">${items.map((c) => challengeCard(c)).join('')}</div>`;
    FP.initReveal();
  }

  function challengeCard(c) {
    const color = FP.moduleColor(c.module);
    return `
      <a href="${challengeUrl(c)}" class="ch-card mod-${FP.esc(c.module)} reveal"
         style="--mod-color:${color}">
        <div class="ch-card-top">
          <span class="ch-mod-dot"></span>
          <span class="ch-module-label">${FP.esc(c.track || c.module)}</span>
        </div>
        <div class="ch-title">${FP.esc(c.title)}</div>
        <div class="ch-desc">${FP.esc(c.description)}</div>
        <div class="ch-footer">
          ${FP.diffBadge(c.difficulty)}
          ${FP.durBadge(c.duration_minutes)}
          <div class="ch-tags">${FP.tagBadges(c.tags, 3)}</div>
        </div>
      </a>`;
  }

  function challengeUrl(c) {
    const q = new URLSearchParams();
    q.set('id', c.id);
    q.set('outcome', _activeOutcome);
    return 'challenge.html?' + q.toString();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
