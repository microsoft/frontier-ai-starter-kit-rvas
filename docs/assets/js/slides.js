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
    deck.innerHTML = slides.map((slide, index) => `
      <article class="customer-slide">
        <span class="slide-number">${String(index + 1).padStart(2, '0')}</span>
        <div class="slide-content">${window.marked.parse(slide, { breaks: false, gfm: true })}</div>
      </article>`).join('');
  }

  function showError(message) {
    document.getElementById('slideDeck').innerHTML = `<p>${FP.esc(message)}</p>`;
  }

  document.getElementById('printSlides').addEventListener('click', () => window.print());
  document.addEventListener('DOMContentLoaded', init);
})();
