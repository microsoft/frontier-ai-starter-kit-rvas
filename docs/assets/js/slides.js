(function () {
  'use strict';

  async function init() {
    const id = FP.qp('id');
    const deck = document.getElementById('slideDeck');
    if (!id) return showError('No scenario was selected.');

    try {
      const data = await FP.loadData();
      const scenario = (data.scenarios || []).find((item) => item.id === id);
      if (!scenario) return showError(`Scenario "${id}" was not found.`);

      document.title = `${scenario.name} — Customer Slides`;
      document.getElementById('deckTitle').textContent = scenario.name;
      const response = await fetch(scenario.slides_path, { cache: 'no-cache' });
      if (!response.ok) throw new Error(`Could not load slides (${response.status})`);
      renderDeck(await response.text(), deck);
    } catch (error) {
      showError(error.message);
    }
  }

  function renderDeck(source, deck) {
    const content = source.replace(/^---\s*\n[\s\S]*?\n---\s*\n/mu, '').trim();
    const slides = content.split(/\n---\s*\n/gu).filter(Boolean);
    deck.innerHTML = slides.map((slide, index) => {
      const { id, markdown } = parseSlide(slide, index);
      return `
      <article class="customer-slide" id="${FP.esc(id)}" tabindex="-1">
        <span class="slide-number">${String(index + 1).padStart(2, '0')}</span>
        <div class="slide-content">${window.marked.parse(markdown, { breaks: false, gfm: true })}</div>
      </article>`;
    }).join('');
    FP.initDiagramZoom(deck);
    focusRequestedSlide(deck);
  }

  function parseSlide(slide, index) {
    const match = slide.match(/^\s*<!--\s*slide:id=([a-z0-9-]+)\s*-->\s*/i);
    if (!match) return { id: `slide-${index + 1}`, markdown: slide };
    return {
      id: match[1].toLowerCase(),
      markdown: slide.slice(match[0].length).trimStart(),
    };
  }

  function focusRequestedSlide(deck) {
    const requested = decodeURIComponent((window.location.hash || '').replace(/^#/, '')).toLowerCase();
    if (!requested) return;

    const exact = document.getElementById(requested);
    const target = exact || Array.from(deck.querySelectorAll('.customer-slide'))
      .find((slide) => slide.id.startsWith(`${requested}-`));
    if (!target) return;

    target.scrollIntoView({ block: 'start' });
    target.focus({ preventScroll: true });
  }

  function showError(message) {
    document.getElementById('slideDeck').innerHTML = `<p>${FP.esc(message)}</p>`;
  }

  document.getElementById('printSlides').addEventListener('click', () => window.print());
  document.addEventListener('DOMContentLoaded', init);
})();
