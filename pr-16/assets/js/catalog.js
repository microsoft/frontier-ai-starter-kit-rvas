/* AI Starter Kit — reference library: reusable implementation building blocks. */
(function () {
  'use strict';

  let _all = [];
  let _capabilities = [];
  let _activeCapability = null;
  let _activeDiff = null;
  let _query = '';

  async function init() {
    let data;
    try { data = await FP.loadData(); }
    catch (e) { FP.renderError('grid', e.message); return; }

    _all = data.activities || [];
    _capabilities = capabilityList(data.modules || []);

    buildCapabilityChips();
    buildDiffChips();
    initSearch();
    applyUrlState();
    render();
  }

  const DIFFS = ['beginner', 'intermediate', 'advanced'];

  /* Seed filter state from the URL query string (?capability=&difficulty=&q=) and
     reflect it on the chips + search input before the first render. Invalid
     values are ignored rather than applied. */
  function applyUrlState() {
    const capability = FP.qp('capability');
    if (capability && _capabilities.some((c) => c.id === capability)) _activeCapability = capability;

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
    document.querySelectorAll('#capabilityChips .chip').forEach((b) => {
      const on = b.dataset.capability === _activeCapability;
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
    if (_activeCapability) q.set('capability', _activeCapability);
    if (_activeDiff) q.set('difficulty', _activeDiff);
    if (_query) q.set('q', _query);
    const qs = q.toString();
    const url = window.location.pathname + (qs ? '?' + qs : '');
    window.history.replaceState(null, '', url);
  }

  function buildCapabilityChips() {
    const container = document.getElementById('capabilityChips');
    if (!container) return;
    container.innerHTML = _capabilities.map((c) =>
      `<button class="chip" data-capability="${FP.esc(c.id)}"
         aria-pressed="false" type="button" title="${FP.esc(c.description || '')}">
         ${FP.esc(c.name)}
       </button>`
    ).join('');

    container.querySelectorAll('.chip').forEach((btn) => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.capability;
        _activeCapability = _activeCapability === id ? null : id;
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
        _activeCapability = null;
        _activeDiff = null;
        syncChipState();
        syncUrl();
        render();
      });
    }
  }

  function filtered() {
    return _all.filter(matchesFilters);
  }

  function matchesFilters(c) {
    if (c.id === 'idea-forge') return false;
    if (_activeCapability && c.track !== _activeCapability) return false;
    if (_activeDiff && c.difficulty !== _activeDiff) return false;
    if (!_query) return true;
    const capability = _capabilities.find((candidate) => candidate.id === c.track);
    const hay = [c.title, c.description, capability?.name || '', c.module, c.track]
      .join(' ').toLowerCase();
    return hay.includes(_query);
  }

  function capabilityList(modules) {
    const tracks = modules.flatMap((mod) => mod.tracks || []);
    const seen = new Set();
    return tracks.filter((track) => {
      if (seen.has(track.id)) return false;
      seen.add(track.id);
      return true;
    });
  }

  function render() {
    const grid = document.getElementById('grid');
    const countEl = document.getElementById('count');
    if (!grid) return;

    const items = filtered();

    if (countEl) countEl.textContent = items.length + ' building block' + (items.length === 1 ? '' : 's');

    if (!items.length) {
      grid.innerHTML = '<div class="no-results">No building blocks match those filters. <button class="btn btn-ghost btn-sm" id="inlineClrBtn" type="button">Clear filters</button></div>';
      const b = document.getElementById('inlineClrBtn');
      if (b) b.addEventListener('click', () => document.getElementById('clearBtn')?.click());
      return;
    }

    const groups = groupedByCapability(items);
    grid.innerHTML = groups.map((group) => `
      <section class="reference-group reveal" aria-labelledby="ref-${FP.esc(group.id)}">
        <div class="shead" style="margin-bottom:16px">
          <div>
            <span class="eyebrow">Capability</span>
            <h2 id="ref-${FP.esc(group.id)}" style="margin-top:10px">${FP.esc(group.name)}</h2>
            <p>${FP.esc(group.description || '')}</p>
          </div>
        </div>
        <div class="activity-grid">${group.items.map((c) => activityCard(c)).join('')}</div>
      </section>
    `).join('');
    FP.initReveal();
  }

  function groupedByCapability(items) {
    const order = new Map(_capabilities.map((cap, index) => [cap.id, index]));
    const byTrack = new Map();
    items.forEach((item) => {
      const key = item.track || 'extras';
      if (!byTrack.has(key)) byTrack.set(key, []);
      byTrack.get(key).push(item);
    });
    return [...byTrack.entries()]
      .sort(([a], [b]) => (order.get(a) ?? 999) - (order.get(b) ?? 999))
      .map(([track, groupItems]) => {
        const cap = _capabilities.find((candidate) => candidate.id === track) || { id: track, name: track };
        return { ...cap, items: groupItems };
      });
  }

  function activityCard(c) {
    const color = FP.moduleColor(c.module);
    return `
      <a href="${activityUrl(c)}" class="ch-card mod-${FP.esc(c.module)} reveal"
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
        </div>
      </a>`;
  }

  function activityUrl(c) {
    const q = new URLSearchParams();
    q.set('id', c.id);
    return 'activity.html?' + q.toString();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
