/* Microsoft Foundry — shared helpers: data loading, theme, nav, badges, scroll-reveal. */
(function () {
  'use strict';

  const FP = (window.FP = window.FP || {});

  /* ─────────────────────────── Data ─────────────────────────────── */
  FP.dataUrl = 'assets/data/platform.json';

  FP.loadData = async function () {
    if (FP._cache) return FP._cache;
    const res = await fetch(FP.dataUrl, { cache: 'no-cache' });
    if (!res.ok) throw new Error('Could not load platform data (' + res.status + ')');
    FP._cache = await res.json();
    return FP._cache;
  };

  /* Module accent CSS variable resolving */
  FP.moduleColor = function (moduleId) {
    const map = {
      foundry: 'var(--c-ghec)',
      ghec: 'var(--c-ghec)',
      ghas: 'var(--c-ghas)',
      ghaw: 'var(--c-ghaw)',
      'sre-agent': 'var(--c-agentic)',
      'agentic-devops': 'var(--c-agentic)',
    };
    return map[moduleId] || 'var(--c-gold)';
  };

  FP.moduleName = function (moduleId, modules) {
    const m = (modules || []).find((x) => x.id === moduleId);
    return m ? m.name : moduleId;
  };

  FP.applyModuleColor = function (el, moduleId) {
    el.style.setProperty('--mod-color', FP.moduleColor(moduleId));
    el.classList.add('mod-' + moduleId);
  };

  /* ─────────────────────────── Escape ───────────────────────────── */
  FP.esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, (c) =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])
    );
  };

  /* ─────────────────────────── Badges ───────────────────────────── */
  FP.diffBadge = function (diff) {
    diff = (diff || 'beginner').toLowerCase();
    return `<span class="badge badge-difficulty-${FP.esc(diff)}">${FP.esc(diff)}</span>`;
  };

  FP.durBadge = function (mins) {
    if (!mins) return '';
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    const label = h && m ? `${h}h ${m}m` : h ? `${h}h` : `${m}m`;
    return `<span class="badge badge-duration">${label}</span>`;
  };

  FP.levelBadge = function (level) {
    if (!level) return '';
    const normalized = String(level).toLowerCase();
    return `<span class="badge badge-level-${FP.esc(normalized)}">${FP.esc(formatLabel(normalized))}</span>`;
  };

  FP.tagBadges = function (tags, limit) {
    if (!Array.isArray(tags) || !tags.length) return '';
    const show = limit ? tags.slice(0, limit) : tags;
    return show.map((t) => `<span class="badge badge-tag">${FP.esc(t)}</span>`).join('');
  };

  function formatLabel(value) {
    return String(value || '').replace(/[-_]+/g, ' ');
  }

  /* ─────────────────────────── URL helpers ───────────────────────── */
  FP.activityUrl = function (id) {
    return 'activity.html?id=' + encodeURIComponent(id);
  };
  FP.referenceUrl = function (capability) {
    return capability ? 'reference.html?capability=' + encodeURIComponent(capability) : 'reference.html';
  };
  FP.outcomeName = function (outcomeId, outcomes) {
    const o = (outcomes || []).find((x) => x.id === outcomeId);
    return o ? o.name : outcomeId;
  };

  /* ─────────────────────────── Query params ─────────────────────── */
  FP.qp = function (name) {
    return new URLSearchParams(window.location.search).get(name);
  };

  /* ─────────────────────────── Theme ────────────────────────────── */
  const THEME_KEY = 'fp-theme';

  FP.initTheme = function () {
    /* RVAS brand: light theme only; toggle removed. */
    document.documentElement.setAttribute('data-theme', 'light');
  };

  function _sunIcon() {
    return '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M18.4 5.6L17 7M6.9 17.1L5.6 18.4"/></svg>';
  }
  function _moonIcon() {
    return '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  }

  /* ─────────────────────────── Nav ──────────────────────────────── */
  FP.initNav = function () {
    const toggle = document.querySelector('.nav-toggle');
    const links  = document.querySelector('.nav-links');
    if (toggle && links) {
      toggle.addEventListener('click', () => {
        const open = links.classList.toggle('open');
        toggle.setAttribute('aria-expanded', String(open));
      });
      // Close on Esc
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && links.classList.contains('open')) {
          links.classList.remove('open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    }
  };

  /* ─────────────────────────── Reveal ───────────────────────────── */
  FP.initReveal = function () {
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.reveal').forEach((el) => el.classList.add('visible'));
      return;
    }
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
        });
      },
      { threshold: 0.08 }
    );
    document.querySelectorAll('.reveal').forEach((el) => obs.observe(el));
  };

  /* ─────────────────────────── Error rendering ───────────────────── */
  FP.renderError = function (container, msg) {
    if (typeof container === 'string') container = document.getElementById(container);
    if (!container) return;
    container.innerHTML = `<div class="empty" role="alert"><strong>Could not load data.</strong><br>${FP.esc(msg)}</div>`;
  };

  /* ─────────────────────────── Markdown ─────────────────────────── */
  FP.renderMd = function (rawMd, targetEl) {
    if (!rawMd) { targetEl.innerHTML = '<p class="text-dim">No content.</p>'; return; }
    if (window.marked) {
      targetEl.innerHTML = window.marked.parse(rawMd, { breaks: false, gfm: true });
    } else {
      // Fallback: wrap in <pre> if marked not available
      const pre = document.createElement('pre');
      pre.textContent = rawMd;
      pre.style.whiteSpace = 'pre-wrap';
      targetEl.innerHTML = '';
      targetEl.appendChild(pre);
    }
  };

  /* ─────────────────────────── Diagram zoom ─────────────────────── */
  FP.initDiagramZoom = function (container) {
    if (!container) return;
    container.querySelectorAll('img[src]').forEach((image) => {
      if (image.dataset.diagramZoomReady === 'true') return;
      if (!isDiagramImage(image)) return;

      image.dataset.diagramZoomReady = 'true';
      image.classList.add('diagram-zoomable');
      image.setAttribute('role', 'button');
      image.setAttribute('tabindex', '0');
      image.setAttribute('aria-label', zoomLabel(image));
      if (!image.getAttribute('title')) image.setAttribute('title', 'Click to zoom');

      image.addEventListener('click', () => openDiagramZoom(image));
      image.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          openDiagramZoom(image);
        }
      });
    });
  };

  function isDiagramImage(image) {
    const src = `${image.getAttribute('src') || ''} ${image.currentSrc || ''} ${image.src || ''}`.toLowerCase();
    const text = `${image.getAttribute('alt') || ''} ${image.getAttribute('title') || ''}`.toLowerCase();
    return src.includes('/diagrams/') || src.includes('diagrams/') || /\bdiagram\b/.test(text);
  }

  function zoomLabel(image) {
    const alt = (image.getAttribute('alt') || '').trim();
    return alt ? `Zoom diagram: ${alt}` : 'Zoom diagram';
  }

  function openDiagramZoom(sourceImage) {
    const modal = ensureDiagramZoomModal();
    const image = modal.querySelector('[data-diagram-lightbox-image]');
    const caption = modal.querySelector('[data-diagram-lightbox-caption]');
    const close = modal.querySelector('[data-diagram-lightbox-close]');
    const alt = (sourceImage.getAttribute('alt') || '').trim();

    modal._returnFocus = sourceImage;
    image.src = sourceImage.currentSrc || sourceImage.src;
    image.alt = alt || 'Zoomed diagram';
    caption.textContent = alt || '';
    caption.hidden = !alt;

    modal.hidden = false;
    document.body.classList.add('diagram-lightbox-open');
    close.focus({ preventScroll: true });
  }

  function closeDiagramZoom() {
    const modal = document.querySelector('[data-diagram-lightbox]');
    if (!modal || modal.hidden) return;

    const image = modal.querySelector('[data-diagram-lightbox-image]');
    modal.hidden = true;
    document.body.classList.remove('diagram-lightbox-open');
    image.removeAttribute('src');

    if (modal._returnFocus && typeof modal._returnFocus.focus === 'function') {
      modal._returnFocus.focus({ preventScroll: true });
    }
    modal._returnFocus = null;
  }

  function ensureDiagramZoomModal() {
    let modal = document.querySelector('[data-diagram-lightbox]');
    if (modal) return modal;

    modal = document.createElement('div');
    modal.className = 'diagram-lightbox';
    modal.hidden = true;
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Diagram preview');
    modal.setAttribute('data-diagram-lightbox', '');
    modal.innerHTML = `
      <button class="diagram-lightbox__backdrop" type="button" aria-label="Close diagram preview" data-diagram-lightbox-backdrop></button>
      <figure class="diagram-lightbox__panel">
        <button class="diagram-lightbox__close" type="button" aria-label="Close diagram preview" data-diagram-lightbox-close>&times;</button>
        <img class="diagram-lightbox__image" alt="" data-diagram-lightbox-image>
        <figcaption class="diagram-lightbox__caption" data-diagram-lightbox-caption></figcaption>
      </figure>`;
    document.body.appendChild(modal);

    modal.querySelector('[data-diagram-lightbox-backdrop]').addEventListener('click', closeDiagramZoom);
    modal.querySelector('[data-diagram-lightbox-close]').addEventListener('click', closeDiagramZoom);
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeDiagramZoom();
    });
    return modal;
  }

  FP.renderInlineMd = function (rawMd) {
    if (rawMd == null || rawMd === '') return '';
    if (!window.marked || typeof window.marked.parseInline !== 'function') return FP.esc(rawMd);

    try {
      return _sanitizeInlineHtml(window.marked.parseInline(String(rawMd), { breaks: false, gfm: true }));
    } catch (e) {
      return FP.esc(rawMd);
    }
  };

  function _sanitizeInlineHtml(html) {
    const template = document.createElement('template');
    template.innerHTML = html;

    const out = document.createElement('span');
    Array.from(template.content.childNodes).forEach((node) => {
      out.appendChild(_sanitizeInlineNode(node));
    });
    return out.innerHTML;
  }

  function _sanitizeInlineNode(node) {
    if (node.nodeType === 3) return document.createTextNode(node.textContent || '');
    if (node.nodeType !== 1) return document.createTextNode('');

    const tag = node.tagName.toLowerCase();
    if (!['a', 'strong', 'em', 'code', 'del', 'br'].includes(tag)) {
      return _sanitizeInlineChildren(node);
    }

    if (tag === 'br') return document.createElement('br');

    if (tag === 'a') {
      const href = node.getAttribute('href') || '';
      if (!_isSafeInlineHref(href)) return _sanitizeInlineChildren(node);

      const a = document.createElement('a');
      a.setAttribute('href', href);
      const title = node.getAttribute('title');
      if (title) a.setAttribute('title', title);
      Array.from(node.childNodes).forEach((child) => a.appendChild(_sanitizeInlineNode(child)));
      return a;
    }

    const el = document.createElement(tag);
    Array.from(node.childNodes).forEach((child) => el.appendChild(_sanitizeInlineNode(child)));
    return el;
  }

  function _sanitizeInlineChildren(node) {
    const frag = document.createDocumentFragment();
    Array.from(node.childNodes).forEach((child) => frag.appendChild(_sanitizeInlineNode(child)));
    return frag;
  }

  function _isSafeInlineHref(href) {
    const trimmed = String(href || '').trim();
    if (!trimmed) return false;
    if (/[\u0000-\u001F\u007F]/.test(trimmed)) return false;
    if (!/^[a-z][a-z0-9+.-]*:/i.test(trimmed) && !trimmed.startsWith('//')) return true;
    try {
      return ['http:', 'https:', 'mailto:'].includes(new URL(trimmed, window.location.href).protocol);
    } catch (e) {
      return false;
    }
  }

  /* ─────────────────────────── Init ─────────────────────────────── */
  document.addEventListener('DOMContentLoaded', () => {
    FP.initTheme();
    FP.applyKiosk();
    FP.initReveal();
  });

})();
