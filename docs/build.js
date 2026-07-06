#!/usr/bin/env node
/**
 * Microsoft Foundry session static-site build.
 *
 * This mirrors the frontier-agentic-devops-session structure: source Markdown
 * stays in the repo, this script emits browser-consumable JSON plus copied
 * participant/facilitator guides under docs/assets/data/.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OUT_DATA_DIR = path.join(__dirname, 'assets', 'data');
const OUT_GUIDES_DIR = path.join(OUT_DATA_DIR, 'activities');
const OUT_RESOURCES_DIR = path.join(__dirname, 'resources');

const CUSTOMER_CHAPTER_IDS = {
  foundations: 'customer-foundations',
  'advanced-action-tools': 'customer-action-tools',
  'advanced-evaluation-redteam': 'customer-evaluation-redteam',
  'advanced-tracing-observability': 'customer-tracing-observability',
  'advanced-deploy-hosted-agent': 'customer-deploy-hosted-agent',
  'extra-build-ui': 'customer-build-ui',
  'capstone-multi-agent': 'customer-capstone-multi-agent',
};

const MODULES = [
  {
    id: 'foundry',
    name: 'Path chapters',
    description: 'Guided capabilities for building, grounding, testing, deploying, and extending your AI app.',
    color: '#38bdf8',
    icon: 'icon-foundry.svg',
    tracks: [
      { id: 'define', name: 'Define', description: 'Shape the outcome, users, corpus, safety boundaries, and demo story.' },
      { id: 'foundations', name: 'Foundations', description: 'Provision Foundry, choose a model, create an agent, and ground it with knowledge.' },
      { id: 'actions', name: 'Action Tools', description: 'Attach governed tools and approval-gated workflows.' },
      { id: 'trust', name: 'Trust', description: 'Evaluate, red-team, trace, and debug agent behavior.' },
      { id: 'deploy', name: 'Deploy', description: 'Host the agent and expose a stakeholder-ready experience.' },
      { id: 'orchestrate', name: 'Orchestrate', description: 'Compose routers, specialists, and multi-agent workflows.' },
      { id: 'extras', name: 'Extras', description: 'Optional deepeners for UI, voice, Fabric IQ, long-running agents, and Copilot-assisted work.' },
    ],
  },
];

const OUTCOMES = [
  {
    id: 'customer-build',
    name: 'Bring your own customer outcome',
    tagline: 'Turn a real customer-safe scenario into a grounded, evaluated Foundry agent prototype.',
    description: 'Define the outcome, swap in your own corpus and persona, add one governed action, prove trust, and demo the result.',
    personas: ['builder', 'solution-architect', 'account-team', 'customer-engineer'],
    adoption_stage: ['define', 'build', 'prove', 'demo'],
    business_value: ['accelerate-prototyping', 'de-risk-ai-adoption', 'prove-customer-value'],
    activity_ids: [
      'customer-outcome',
      'customer-foundations',
      'customer-action-tools',
      'customer-evaluation-redteam',
      'customer-tracing-observability',
      'customer-deploy-hosted-agent',
      'customer-build-ui',
      'customer-capstone-multi-agent',
    ],
    success_metrics: [
      'The team can explain the target users, corpus, action, safety boundaries, and demo story.',
      'The prototype answers with citations, acts only through governed tools, and has a trust scorecard.',
    ],
  },
  {
    id: 'idea-forge',
    name: 'Need an idea first',
    tagline: 'Generate a ranked, buildable AI application idea before starting the customer build path.',
    description: 'Use Activity Forge to pick a right-sized idea with clear users, safe data, one action, and a believable demo.',
    personas: ['builder', 'facilitator', 'account-team'],
    adoption_stage: ['ideate', 'define'],
    business_value: ['find-buildable-use-cases', 'reduce-scope-risk'],
    activity_ids: ['idea-forge', 'customer-outcome'],
    success_metrics: [
      'A selected idea has an outcome, users, data sources, tier guidance, and risk notes.',
      'The chosen idea transfers cleanly into the Customer Build scenario pack.',
    ],
  },
  {
    id: 'upskill',
    name: 'Learn with Northfield',
    tagline: 'Practice the full Foundry path with the known-good Northfield University reference scenario.',
    description: 'Build the Northfield IQ Assistant, then reuse the same architecture for customer work later.',
    personas: ['participant', 'facilitator', 'developer'],
    adoption_stage: ['learn', 'practice', 'extend'],
    business_value: ['learn-foundry-patterns', 'create-repeatable-reference'],
    activity_ids: [
      'setup',
      'foundations',
      'advanced-action-tools',
      'advanced-evaluation-redteam',
      'advanced-tracing-observability',
      'advanced-deploy-hosted-agent',
      'extra-build-ui',
      'extra-voice-live',
      'extra-fabric-iq',
      'extra-copilot-assisted',
      'extra-magentic-workflows',
      'extra-hosted-longrunning',
      'capstone-multi-agent',
    ],
    success_metrics: [
      'The Northfield assistant is grounded, action-capable, evaluated, observable, and deployable.',
      'Participants can identify what to swap when moving from Northfield to a customer scenario.',
    ],
  },
];

const ACTIVITIES = [
  {
    id: 'setup',
    title: 'Getting Started',
    track: 'define',
    difficulty: 'beginner',
    duration_minutes: 30,
    description: 'Prepare Codespaces, Azure sign-in, and local tooling before running activity validators.',
    tags: ['setup', 'codespaces', 'azure'],
    outcomes: ['upskill'],
    participant: 'docs/setup.md',
  },
  {
    id: 'idea-forge',
    title: 'Idea Forge',
    track: 'define',
    difficulty: 'beginner',
    duration_minutes: 20,
    description: 'Generate and select a buildable customer AI application idea before starting Customer Build.',
    tags: ['ideation', 'customer', 'scenario'],
    outcomes: ['idea-forge'],
    participant: 'docs/idea-forge.md',
  },
  {
    id: 'customer-outcome',
    title: 'Define your outcome',
    track: 'define',
    difficulty: 'beginner',
    duration_minutes: 45,
    description: 'Create the scenario pack: users, outcome, corpus, safe action, success measures, and demo story.',
    tags: ['customer-build', 'scenario', 'planning'],
    outcomes: ['customer-build', 'idea-forge'],
    participant: 'docs/customer-outcome.md',
  },
  {
    id: 'customer-foundations',
    title: 'Ground your app',
    track: 'foundations',
    difficulty: 'beginner',
    duration_minutes: 210,
    description: 'Provision, choose a model, create your agent, and ground it in your own customer-safe data.',
    prerequisites: ['customer-outcome'],
    tags: ['customer-build', 'grounding', 'knowledge', 'citations'],
    outcomes: ['customer-build'],
    participant: 'docs/customer-build/foundations.md',
  },
  {
    id: 'customer-action-tools',
    title: 'Make it act',
    track: 'actions',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Add one governed action from your own workflow, with approval before any side effect.',
    prerequisites: ['customer-foundations'],
    tags: ['customer-build', 'tools', 'approval', 'workflow'],
    outcomes: ['customer-build'],
    participant: 'docs/customer-build/advanced-action-tools.md',
  },
  {
    id: 'customer-evaluation-redteam',
    title: "Prove it's safe",
    track: 'trust',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Create customer-scenario evals and red-team prompts that prove quality, safety, and groundedness.',
    prerequisites: ['customer-foundations'],
    tags: ['customer-build', 'evaluation', 'red-team', 'safety'],
    outcomes: ['customer-build'],
    participant: 'docs/customer-build/advanced-evaluation-redteam.md',
  },
  {
    id: 'customer-tracing-observability',
    title: 'See inside it',
    track: 'trust',
    difficulty: 'intermediate',
    duration_minutes: 75,
    description: 'Trace your customer scenario end-to-end so stakeholders can see retrieval, tools, latency, and failure paths.',
    prerequisites: ['customer-foundations'],
    tags: ['customer-build', 'observability', 'tracing'],
    outcomes: ['customer-build'],
    participant: 'docs/customer-build/advanced-tracing-observability.md',
  },
  {
    id: 'customer-deploy-hosted-agent',
    title: 'Ship it',
    track: 'deploy',
    difficulty: 'advanced',
    duration_minutes: 90,
    description: 'Package and host your customer agent behind a real endpoint for stakeholder testing.',
    prerequisites: ['customer-foundations'],
    tags: ['customer-build', 'deployment', 'hosted-agent'],
    outcomes: ['customer-build'],
    participant: 'docs/customer-build/advanced-deploy-hosted-agent.md',
  },
  {
    id: 'customer-build-ui',
    title: 'Demo UI: Build your app face',
    track: 'deploy',
    difficulty: 'intermediate',
    duration_minutes: 75,
    description: 'Create a stakeholder-facing UI for your customer scenario, including citations or approval state.',
    prerequisites: ['customer-foundations'],
    tags: ['customer-build', 'ui', 'demo'],
    outcomes: ['customer-build'],
    participant: 'docs/customer-build/extra-build-ui.md',
  },
  {
    id: 'customer-capstone-multi-agent',
    title: 'Grow it into a team',
    track: 'orchestrate',
    difficulty: 'advanced',
    duration_minutes: 120,
    description: 'Split your customer assistant into a router and specialist agents that match your demo journey.',
    prerequisites: ['customer-foundations'],
    tags: ['customer-build', 'multi-agent', 'capstone'],
    outcomes: ['customer-build'],
    participant: 'docs/customer-build/capstone-multi-agent.md',
  },
  {
    id: 'foundations',
    title: 'Ground: Foundations',
    track: 'foundations',
    difficulty: 'beginner',
    duration_minutes: 210,
    description: 'Provision Foundry, choose a model, create an agent, and ground it with the Northfield FAQ corpus.',
    tags: ['foundations', 'agent', 'knowledge', 'citations'],
    outcomes: ['upskill'],
    participant: 'activities/foundations/README.md',
    facilitator: 'docs/activities/foundations-facilitator.md',
  },
  {
    id: 'advanced-action-tools',
    title: 'Act: Action Tools',
    track: 'actions',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Attach governed tools and approval-gated actions to your Foundry agent.',
    prerequisites: ['foundations'],
    tags: ['tools', 'mcp', 'actions', 'approval'],
    outcomes: ['upskill'],
    participant: 'activities/advanced-action-tools/README.md',
    facilitator: 'docs/activities/advanced-action-tools-facilitator.md',
  },
  {
    id: 'advanced-evaluation-redteam',
    title: 'Prove: Evaluation & Red Teaming',
    track: 'trust',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Build quality and safety evals, run adversarial prompts, and gate the agent with a scorecard.',
    prerequisites: ['foundations'],
    tags: ['evaluation', 'red-team', 'safety', 'quality'],
    outcomes: ['upskill'],
    participant: 'activities/advanced-evaluation-redteam/README.md',
    facilitator: 'docs/activities/advanced-evaluation-redteam-facilitator.md',
  },
  {
    id: 'advanced-tracing-observability',
    title: 'Debug: Tracing & Observability',
    track: 'trust',
    difficulty: 'intermediate',
    duration_minutes: 75,
    description: 'Trace model calls, retrieval, tool use, and failures in Application Insights.',
    prerequisites: ['foundations'],
    tags: ['observability', 'tracing', 'app-insights', 'debugging'],
    outcomes: ['upskill'],
    participant: 'activities/advanced-tracing-observability/README.md',
    facilitator: 'docs/activities/advanced-tracing-observability-facilitator.md',
  },
  {
    id: 'advanced-deploy-hosted-agent',
    title: 'Deploy: Hosted Agent',
    track: 'deploy',
    difficulty: 'advanced',
    duration_minutes: 90,
    description: 'Package and deploy your agent as a hosted endpoint with the agent.yaml contract.',
    prerequisites: ['foundations'],
    tags: ['deployment', 'hosted-agent', 'container'],
    outcomes: ['upskill'],
    participant: 'activities/advanced-deploy-hosted-agent/README.md',
    facilitator: 'docs/activities/advanced-deploy-hosted-agent-facilitator.md',
  },
  {
    id: 'extra-build-ui',
    title: 'Demo UI: Build a UI',
    track: 'deploy',
    difficulty: 'intermediate',
    duration_minutes: 75,
    description: 'Create a stakeholder-facing chat or demo UI for the Foundry agent.',
    prerequisites: ['foundations'],
    tags: ['ui', 'demo', 'frontend'],
    outcomes: ['upskill'],
    participant: 'activities/extra-build-ui/README.md',
    facilitator: 'docs/activities/extra-build-ui-facilitator.md',
  },
  {
    id: 'extra-voice-live',
    title: 'Interface: Voice Live',
    track: 'extras',
    difficulty: 'advanced',
    duration_minutes: 75,
    description: 'Add a spoken interaction path for contact-center, accessibility, or demo scenarios.',
    prerequisites: ['foundations'],
    tags: ['voice', 'realtime', 'interface'],
    outcomes: ['upskill'],
    participant: 'activities/extra-voice-live/README.md',
    facilitator: 'docs/activities/extra-voice-live-facilitator.md',
  },
  {
    id: 'extra-fabric-iq',
    title: 'Deepen: Fabric IQ',
    track: 'extras',
    difficulty: 'advanced',
    duration_minutes: 75,
    description: 'Ground answers in operational or analytical data when static documents are not enough.',
    prerequisites: ['foundations'],
    tags: ['fabric', 'knowledge', 'data'],
    outcomes: ['upskill'],
    participant: 'activities/extra-fabric-iq/README.md',
    facilitator: 'docs/activities/extra-fabric-iq-facilitator.md',
  },
  {
    id: 'extra-copilot-assisted',
    title: 'Accelerate: Copilot-Assisted Build',
    track: 'extras',
    difficulty: 'intermediate',
    duration_minutes: 45,
    description: 'Use skills and MCP deliberately instead of guessing fast-moving Foundry APIs.',
    tags: ['copilot', 'skills', 'mcp'],
    outcomes: ['upskill'],
    participant: 'activities/extra-copilot-assisted/README.md',
    facilitator: 'docs/activities/extra-copilot-assisted-facilitator.md',
  },
  {
    id: 'extra-magentic-workflows',
    title: 'Orchestrate: Magentic Workflows',
    track: 'orchestrate',
    difficulty: 'advanced',
    duration_minutes: 90,
    description: 'Explore manager/planner orchestration with Microsoft Agent Framework patterns.',
    prerequisites: ['foundations'],
    tags: ['multi-agent', 'orchestration', 'magentic'],
    outcomes: ['upskill'],
    participant: 'activities/extra-magentic-workflows/README.md',
    facilitator: 'docs/activities/extra-magentic-workflows-facilitator.md',
  },
  {
    id: 'extra-hosted-longrunning',
    title: 'Deploy: Long-Running Agents',
    track: 'deploy',
    difficulty: 'advanced',
    duration_minutes: 75,
    description: 'Use background run patterns for workflows that outlive a browser session.',
    prerequisites: ['foundations'],
    tags: ['hosted-agent', 'long-running', 'workflow'],
    outcomes: ['upskill'],
    participant: 'activities/extra-hosted-longrunning/README.md',
    facilitator: 'docs/activities/extra-hosted-longrunning-facilitator.md',
  },
  {
    id: 'capstone-multi-agent',
    title: 'Orchestrate: Multi-Agent Capstone',
    track: 'orchestrate',
    difficulty: 'advanced',
    duration_minutes: 120,
    description: 'Split the assistant into a router and specialist agents for a realistic customer journey.',
    prerequisites: ['foundations'],
    tags: ['capstone', 'multi-agent', 'router'],
    outcomes: ['upskill'],
    participant: 'activities/capstone-multi-agent/README.md',
    facilitator: 'docs/activities/capstone-multi-agent-facilitator.md',
  },
];

function readIfExists(relPath) {
  const abs = path.join(ROOT, relPath);
  return fs.existsSync(abs) ? fs.readFileSync(abs, 'utf8') : null;
}

function stripFrontMatter(markdown) {
  return markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
}

function sourceDirFor(activity) {
  if (!activity.participant) return '';
  return path.posix.dirname(activity.participant.replace(/\\/g, '/'));
}

function repoBlob(pathPart) {
  return `https://github.com/microsoft/frontier-ai-starter-kit-rvas/blob/main/${pathPart}`;
}

function customerChapterId(slug) {
  return CUSTOMER_CHAPTER_IDS[slug] || slug;
}

function activityUrl(id, hash = '') {
  return `activity.html?id=${id}${hash || ''}`;
}

function transformMarkdown(markdown, activity) {
  const activityAssetBase = `assets/data/activities/${activity.id}/assets/`;
  const sourceDir = sourceDirFor(activity);
  const isCustomerChapter = sourceDir === 'docs/customer-build';

  return stripFrontMatter(markdown)
    .replace(/\{% include journey-status\.html[^%]*%\}/g, '')
    .replace(/\{% include module-lens\.html[^%]*%\}/g, '')
    .replace(/\{%[^%]*%\}/g, '')
    .replace(/\{\{\s*'\/customer-build'\s*\|\s*relative_url\s*\}\}/g, 'catalog.html?outcome=customer-build')
    .replace(/\{\{\s*'\/customer-outcome'\s*\|\s*relative_url\s*\}\}/g, 'activity.html?id=customer-outcome')
    .replace(/\{\{\s*'\/idea-forge'\s*\|\s*relative_url\s*\}\}/g, 'activity.html?id=idea-forge')
    .replace(/\{\{\s*'\/upskill'\s*\|\s*relative_url\s*\}\}/g, 'catalog.html?outcome=upskill')
    .replace(/\{\{\s*'\/setup'\s*\|\s*relative_url\s*\}\}/g, 'activity.html?id=setup')
    .replace(/\{\{\s*'\/activities\/([^'#]+)(#[^']*)?'\s*\|\s*relative_url\s*\}\}/g, (_m, slug, hash = '') => activityUrl(slug, hash))
    .replace(/\{\{\s*'\/customer-build\/([^'#]+)(#[^']*)?'\s*\|\s*relative_url\s*\}\}/g, (_m, slug, hash = '') => activityUrl(customerChapterId(slug), hash))
    .replace(/\]\(\.\.\/\.\.\/docs\/customer-build\.md\)/g, '](catalog.html?outcome=customer-build)')
    .replace(/\]\(\.\.\/\.\.\/docs\/customer-build\/([^).#]+)\.md(#[^)]+)?\)/g, (_m, slug, hash = '') => `](${activityUrl(customerChapterId(slug), hash)})`)
    .replace(/\]\(\.\.\/\.\.\/docs\/customer-outcome\.md\)/g, '](activity.html?id=customer-outcome)')
    .replace(/\]\(\.\.\/activities\/([^)#]+)(#[^)]+)?\)/g, (_m, slug, hash = '') => `](${activityUrl(slug, hash)})`)
    .replace(/\]\(\.\.\/customer-outcome(#[^)]+)?\)/g, (_m, hash = '') => `](${activityUrl('customer-outcome', hash)})`)
    .replace(/\]\(\.\.\/idea-forge(#[^)]+)?\)/g, (_m, hash = '') => `](${activityUrl('idea-forge', hash)})`)
    .replace(/\]\(\.\.\/\.\.\/resources\//g, '](resources/')
    .replace(/\]\(\.\.\/\.\.\/docs\/activities\/([^)]+)\.md\)/g, (_m, slug) => `](activity.html?id=${slug})`)
    .replace(/\]\((?:\.\.\/)*customer-build\.md\)/g, '](catalog.html?outcome=customer-build)')
    .replace(/\]\((?:\.\.\/)*customer-outcome\.md\)/g, '](activity.html?id=customer-outcome)')
    .replace(/\]\(\.\.\/([a-z0-9-]+)\/README\.md\)/g, (_m, slug) => `](activity.html?id=${slug})`)
    .replace(/\]\((foundations|advanced-action-tools|advanced-evaluation-redteam|advanced-tracing-observability|advanced-deploy-hosted-agent|extra-build-ui|capstone-multi-agent)(#[^)]+)?\)/g,
      (_m, slug, hash = '') => isCustomerChapter ? `](${activityUrl(customerChapterId(slug), hash)})` : _m)
    .replace(/\]\(assets\//g, `](${activityAssetBase}`)
    .replace(/\]\(solution\.md\)/g, sourceDir ? `](${repoBlob(`${sourceDir}/solution.md`)})` : '](#)')
    .replace(/\]\(evaluate\.py\)/g, sourceDir ? `](${repoBlob(`${sourceDir}/evaluate.py`)})` : '](#)')
    .replace(/\]\(validate\.py\)/g, sourceDir ? `](${repoBlob(`${sourceDir}/validate.py`)})` : '](#)')
    .replace(/\]\(\.\.\/\.\.\/\.env\.sample\)/g, `](${repoBlob('.env.sample')})`)
    .replace(/\]\(\.\.\/\.\.\/\.github\//g, `](${repoBlob('.github/')}`)
    .replace(/\]\(\.\.\/\.\.\/scripts\//g, `](${repoBlob('scripts/')}`)
    .replace(/\]\(\.\.\/\.\.\/docs\//g, `](${repoBlob('docs/')}`);
}

function writeGuide(activity, kind) {
  const guideDir = path.join(OUT_GUIDES_DIR, activity.id);
  fs.mkdirSync(guideDir, { recursive: true });

  const outName = kind === 'facilitator' ? 'FACILITATOR.md' : 'README.md';
  const configured = kind === 'facilitator' ? activity.facilitator : activity.participant;
  const fallback = kind === 'facilitator'
    ? `# Facilitator guide\n\nFacilitator-specific notes are not available for this item. Use the participant guide and the success criteria in the sidebar.`
    : `# ${activity.title}\n\nGuide content is not available yet.`;

  const raw = configured ? readIfExists(configured) : null;
  fs.writeFileSync(path.join(guideDir, outName), transformMarkdown(raw || fallback, activity));

  if (kind === 'participant' && activity.participant && activity.participant.startsWith('activities/')) {
    const srcDir = path.join(ROOT, path.dirname(activity.participant));
    const srcAssets = path.join(srcDir, 'assets');
    if (fs.existsSync(srcAssets)) {
      fs.cpSync(srcAssets, path.join(guideDir, 'assets'), { recursive: true });
    }
  }
}

function copyResources() {
  fs.rmSync(OUT_RESOURCES_DIR, { recursive: true, force: true });
  const src = path.join(ROOT, 'resources');
  if (fs.existsSync(src)) {
    fs.cpSync(src, OUT_RESOURCES_DIR, { recursive: true });
  }
}

function activityOutput(activity) {
  return {
    id: activity.id,
    title: activity.title,
    module: 'foundry',
    track: activity.track,
    difficulty: activity.difficulty,
    duration_minutes: activity.duration_minutes,
    description: activity.description,
    prerequisites: activity.prerequisites || [],
    prerequisite_capabilities: activity.prerequisite_capabilities || [],
    success_criteria: activity.success_criteria || [],
    tags: activity.tags || [],
    outcomes: activity.outcomes || [],
    personas: activity.personas || [],
    business_value: activity.business_value || [],
    adoption_stage: activity.adoption_stage || '',
    app_dependency: 'none',
    emu_compatible: true,
    tier: activity.track === 'extras' ? 'extra' : 'core',
    references: activity.references || [],
    source_repo: 'microsoft/frontier-ai-starter-kit-rvas',
    source_path: activity.participant || '',
    license: 'MIT',
    participant_path: `assets/data/activities/${activity.id}/README.md`,
    facilitator_path: `assets/data/activities/${activity.id}/FACILITATOR.md`,
  };
}

function detectMissingReferences(activities, outcomes) {
  const ids = new Set(activities.map((c) => c.id));
  const missing = [];
  for (const activity of activities) {
    for (const prereq of activity.prerequisites || []) {
      if (!ids.has(prereq)) missing.push(`${activity.id} prerequisite ${prereq}`);
    }
  }
  for (const outcome of outcomes) {
    for (const id of outcome.activity_ids || []) {
      if (!ids.has(id)) missing.push(`${outcome.id} outcome activity ${id}`);
    }
  }
  return missing;
}

function main() {
  const missing = detectMissingReferences(ACTIVITIES, OUTCOMES);
  if (missing.length) {
    console.error('Build failed: missing references');
    missing.forEach((m) => console.error(`  - ${m}`));
    process.exit(1);
  }

  fs.rmSync(OUT_GUIDES_DIR, { recursive: true, force: true });
  fs.mkdirSync(OUT_DATA_DIR, { recursive: true });
  copyResources();

  for (const activity of ACTIVITIES) {
    writeGuide(activity, 'participant');
    writeGuide(activity, 'facilitator');
  }

  const outputActivities = ACTIVITIES.map(activityOutput);
  const activityById = new Map(outputActivities.map((c) => [c.id, c]));

  const modules = MODULES.map((mod) => {
    const moduleActivities = outputActivities.filter((c) => c.module === mod.id);
    const tracks = mod.tracks.map((track) => ({
      ...track,
      activity_count: moduleActivities.filter((c) => c.track === track.id).length,
    }));
    return {
      ...mod,
      activity_count: moduleActivities.length,
      tracks,
    };
  });

  const outcomes = OUTCOMES.map((outcome) => {
    const duration = (outcome.activity_ids || []).reduce((total, id) => {
      const activity = activityById.get(id);
      return total + (activity ? activity.duration_minutes || 0 : 0);
    }, 0);
    return {
      ...outcome,
      activity_count: (outcome.activity_ids || []).length,
      duration_minutes: duration,
    };
  });

  const graph = {
    nodes: outputActivities.map((c) => ({ id: c.id, title: c.title, module: c.module, track: c.track, tier: c.tier })),
    edges: outputActivities.flatMap((c) => (c.prerequisites || []).map((from) => ({ from, to: c.id }))),
  };

  fs.writeFileSync(
    path.join(OUT_DATA_DIR, 'platform.json'),
    JSON.stringify({ generated_at: new Date().toISOString(), modules, outcomes, activities: outputActivities }, null, 2),
  );
  fs.writeFileSync(path.join(OUT_DATA_DIR, 'dependency-graph.json'), JSON.stringify(graph, null, 2));

  console.log(`✓ built platform.json (modules: ${modules.length}, outcomes: ${outcomes.length}, activities: ${outputActivities.length})`);
  console.log(`✓ copied guides → ${path.relative(ROOT, OUT_GUIDES_DIR)}`);
}

main();
