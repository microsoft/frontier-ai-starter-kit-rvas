(function () {
  'use strict';

  let scenarios = [];
  let lastRecommendation = null;

  const scenarioByOutcome = {
    grounding: 'ai-grounding',
    content: 'content-understanding-document-workflow',
    avatar: 'avatar-enabled-onboarding',
  };

  async function init() {
    try {
      const data = await FP.loadData();
      scenarios = data.scenarios || [];
      bindForm();
      recommend();
    } catch (error) {
      FP.renderError('decisionCards', error.message);
    }
  }

  function bindForm() {
    const form = document.getElementById('explorerForm');
    form.addEventListener('change', recommend);
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      recommend();
      document.querySelector('.explorer-result').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    document.getElementById('resetExplorer').addEventListener('click', () => {
      form.reset();
      recommend();
    });
    document.getElementById('copyDecision').addEventListener('click', copySummary);
  }

  function values() {
    const form = new FormData(document.getElementById('explorerForm'));
    return Object.fromEntries(form.entries());
  }

  function recommend() {
    const input = values();
    const id = scenarioByOutcome[input.outcome];
    const scenario = scenarios.find((item) => item.id === id);
    if (!scenario) return;

    const cards = decisionCards(input);
    lastRecommendation = { scenario, input, cards };
    document.getElementById('scenarioName').textContent = scenario.name;
    document.getElementById('scenarioWhy').textContent = why(scenario, input);
    const link = document.getElementById('scenarioLink');
    link.href = `scenario.html?id=${encodeURIComponent(scenario.id)}`;
    link.textContent = `Open ${scenario.name} playbook`;
    document.getElementById('decisionCards').innerHTML = cards.map(cardTemplate).join('');
  }

  function why(scenario, input) {
    if (input.outcome === 'grounding' && input.data === 'structured') {
      return 'The outcome is trusted answers, but operational data is central. Start with the data owner, access model, and the IQ pattern that can preserve provenance.';
    }
    if (input.outcome === 'content') {
      return 'The outcome is an AI-ready content workflow. Start with the SME’s extraction understanding, safe handoff, and a reviewable downstream decision.';
    }
    if (input.outcome === 'avatar') {
      return 'The outcome is consistent learning communication. Start with approved content, disclosure, accessibility, and the human approvals that make an avatar safe to operate.';
    }
    return scenario.tagline;
  }

  function decisionCards(input) {
    const cards = [];
    cards.push(platformCard(input));
    cards.push(sourceCard(input));
    cards.push(environmentCard(input));
    cards.push(evidenceCard(input));
    return cards;
  }

  function platformCard(input) {
    const copilotFirst = input.environment === 'm365' && input.ownership !== 'engineering';
    return {
      label: 'Platform discussion',
      title: copilotFirst ? 'Start by evaluating Copilot Studio alongside Foundry' : 'Start with a Foundry-led design discussion',
      body: copilotFirst
        ? 'The customer already works in Microsoft 365 and business ownership is important. Explore Copilot Studio’s maker and channel fit, then test whether the required grounding, tools, evaluation, and operating controls remain sufficient.'
        : 'The outcome needs explicit engineering control, reusable integrations, or a tailored evidence loop. Explore Foundry first, while keeping Copilot Studio as a channel or maker-surface discussion where Microsoft 365 is central.',
    };
  }

  function sourceCard(input) {
    if (input.data === 'sharepoint') {
      return {
        label: 'Knowledge and data',
        title: 'Begin with SharePoint ownership and access—not ingestion volume',
        body: 'Identify approved sites, content owners, change/withdrawal rules, audience permissions, and the safe representative sample. Then decide whether the selected IQ pattern can preserve those boundaries.',
      };
    }
    if (input.data === 'structured') {
      return {
        label: 'Knowledge and data',
        title: 'Begin with the governed data product',
        body: 'Ask for the data owner, semantic contract, allowed fields, freshness expectation, and platform-enforced access. Fabric IQ may be relevant, but only after the governed source and evidence requirements are clear.',
      };
    }
    return {
      label: 'Knowledge and data',
      title: 'Separate the content problem from the data-readiness problem',
      body: 'Map the source types and owners first. Content Understanding can prepare documents; Foundry, Fabric, Work, or Web IQ can ground a later experience. Do not collapse those decisions into one “RAG” choice.',
    };
  }

  function environmentCard(input) {
    if (input.environment === 'greenfield') {
      return {
        label: 'Starting point',
        title: 'Use the minimum demo accelerator',
        body: 'Provision only the scenario’s safe demonstration resources and samples. Keep names, source bindings, and model choices parameterized so the customer can replace them after the conversation.',
      };
    }
    return {
      label: 'Starting point',
      title: 'Bind to the environment that already exists',
      body: 'Inventory the existing landing zone, project, data platform, and identity model. Use the bring-your-own-environment path; do not redeploy enterprise infrastructure to demonstrate one scenario.',
    };
  }

  function evidenceCard(input) {
    const owner = input.ownership === 'business' ? 'business owner and technical owner' : input.ownership === 'shared' ? 'business/technical handoff' : 'engineering owner';
    return {
      label: 'Evidence from day one',
      title: `Define the golden dataset and ${owner}`,
      body: 'Capture representative good, edge, and refusal cases before implementation. Decide what quality, groundedness, reviewer correction, latency, and access failures would block the next customer decision.',
    };
  }

  function cardTemplate(card) {
    return `<article class="decision-card"><span>${FP.esc(card.label)}</span><h3>${FP.esc(card.title)}</h3><p>${FP.esc(card.body)}</p></article>`;
  }

  async function copySummary() {
    if (!lastRecommendation) return;
    const { scenario, input, cards } = lastRecommendation;
    const text = [
      `AI Starter Kit decision summary`,
      `Scenario: ${scenario.name}`,
      `Outcome: ${input.outcome}; data: ${input.data}; environment: ${input.environment}; ownership: ${input.ownership}.`,
      ...cards.map((card) => `${card.label}: ${card.title}. ${card.body}`),
      'Assumptions must be confirmed with the customer before implementation.',
    ].join('\n\n');
    try {
      await navigator.clipboard.writeText(text);
      document.getElementById('copyDecision').textContent = 'Copied';
      setTimeout(() => { document.getElementById('copyDecision').textContent = 'Copy conversation summary'; }, 1800);
    } catch (error) {
      window.prompt('Copy this decision summary:', text);
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
