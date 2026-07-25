#!/usr/bin/env node
/**
 * Microsoft Foundry session static-site build.
 *
 * This mirrors the frontier-agentic-devops-session structure: source Markdown
 * stays in the repo, this script emits browser-consumable JSON plus copied
 * participant guides under docs/assets/data/.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SCENARIOS_DIR = path.join(ROOT, 'scenarios');
const OUT_DATA_DIR = path.join(__dirname, 'assets', 'data');
const OUT_GUIDES_DIR = path.join(OUT_DATA_DIR, 'activities');
const OUT_RESOURCES_DIR = path.join(__dirname, 'resources');

const LEGACY_ACTIVITY_ALIASES = {};

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
      { id: 'orchestrate', name: 'Orchestrate', description: 'Coordinate multiple agents with manager, planner, and router patterns.' },
      { id: 'extras', name: 'Extras', description: 'Optional deepeners for UI, voice, Fabric IQ, and long-running agents.' },
    ],
  },
];

const OUTCOMES = [
  {
    id: 'idea-forge',
    name: 'Need an idea first',
    tagline: 'Generate a ranked, buildable AI application idea before starting the customer build path.',
    description: 'Use Activity Forge to pick a right-sized idea with clear users, safe data, one action, and a believable demo.',
    personas: ['builder', 'facilitator', 'account-team'],
    adoption_stage: ['ideate', 'define'],
    business_value: ['find-buildable-use-cases', 'reduce-scope-risk'],
    activity_ids: ['idea-forge'],
    success_metrics: [
      'A selected idea has an outcome, users, data sources, tier guidance, and risk notes.',
      'The chosen idea transfers cleanly into the Customer Build scenario pack.',
    ],
  },
  {
    id: 'reference',
    name: 'Reference Library',
    tagline: 'Reusable implementation building blocks for scenario playbooks.',
    description: 'Open these activities only when a scenario calls for the specific capability.',
    personas: ['builder', 'facilitator', 'developer'],
    adoption_stage: ['build', 'prove', 'demo'],
    business_value: ['reuse-building-blocks', 'reduce-implementation-risk'],
    activity_ids: [
      'foundations',
      'advanced-action-tools',
      'advanced-evaluation-redteam',
      'advanced-tracing-observability',
      'advanced-deploy-hosted-agent',
      'extra-build-ui',
      'extra-voice-live',
      'extra-fabric-iq',
      'extra-document-workflow',
      'extra-visual-multimodal',
      'extra-governed-data-copilot',
      'extra-magentic-workflows',
      'extra-hosted-longrunning',
    ],
    success_metrics: [
      'Teams can find the implementation mechanics that support a chosen scenario.',
      'Reference activities stay reusable and do not become a separate customer journey.',
    ],
  },
];

const ACTIVITIES = [
  {
    id: 'idea-forge',
    title: 'Idea Forge',
    track: 'define',
    difficulty: 'beginner',
    duration_minutes: 20,
    description: 'Generate and select a buildable customer AI application idea before starting Customer Build.',
    outcomes: ['idea-forge'],
    participant: 'docs/idea-forge.md',
  },
  {
    id: 'foundations',
    title: 'Ground: Foundations',
    track: 'foundations',
    difficulty: 'beginner',
    duration_minutes: 210,
    description: 'Provision Foundry, choose a model, create an agent, and ground it with an approved sample corpus.',
    outcomes: ['reference'],
    participant: 'activities/foundations/README.md',
  },
  {
    id: 'advanced-action-tools',
    title: 'Act: Action Tools',
    track: 'actions',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Attach governed tools and approval-gated actions to your Foundry agent.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/advanced-action-tools/README.md',
  },
  {
    id: 'advanced-evaluation-redteam',
    title: 'Prove: Evaluation & Red Teaming',
    track: 'trust',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Build quality and safety evals, run adversarial prompts, and gate the agent with a scorecard.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/advanced-evaluation-redteam/README.md',
  },
  {
    id: 'advanced-tracing-observability',
    title: 'Debug: Tracing & Observability',
    track: 'trust',
    difficulty: 'intermediate',
    duration_minutes: 75,
    description: 'Trace model calls, retrieval, tool use, and failures in Application Insights.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/advanced-tracing-observability/README.md',
  },
  {
    id: 'advanced-deploy-hosted-agent',
    title: 'Deploy: Hosted Agent',
    track: 'deploy',
    difficulty: 'advanced',
    duration_minutes: 90,
    description: 'Package and deploy your agent as a hosted endpoint with the unified azure.yaml contract.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/advanced-deploy-hosted-agent/README.md',
  },
  {
    id: 'extra-build-ui',
    title: 'Demo UI: Build a UI',
    track: 'deploy',
    difficulty: 'intermediate',
    duration_minutes: 75,
    description: 'Create a stakeholder-facing chat or demo UI for the Foundry agent.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/extra-build-ui/README.md',
  },
  {
    id: 'extra-voice-live',
    title: 'Interface: Voice Live',
    track: 'extras',
    difficulty: 'advanced',
    duration_minutes: 75,
    description: 'Add a spoken interaction path for contact-center, accessibility, or demo scenarios.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/extra-voice-live/README.md',
  },
  {
    id: 'extra-fabric-iq',
    title: 'Deepen: Fabric IQ',
    track: 'extras',
    difficulty: 'advanced',
    duration_minutes: 75,
    description: 'Ground answers in operational or analytical data when static documents are not enough.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/extra-fabric-iq/README.md',
  },
  {
    id: 'extra-document-workflow',
    title: 'Build: Document Workflow',
    track: 'extras',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Extract, validate, review, and route document data with a keyless, human-governed workflow.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/extra-document-workflow/README.md',
  },
  {
    id: 'extra-visual-multimodal',
    title: 'Build: Visual Multimodal',
    track: 'extras',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Analyze safe image inputs with structured results, uncertainty handling, and human review boundaries.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/extra-visual-multimodal/README.md',
  },
  {
    id: 'extra-governed-data-copilot',
    title: 'Build: Governed Data Copilot',
    track: 'extras',
    difficulty: 'advanced',
    duration_minutes: 90,
    description: 'Query approved structured data through explicit access, field, and result-provenance controls.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/extra-governed-data-copilot/README.md',
  },
  {
    id: 'extra-magentic-workflows',
    title: 'Orchestrate: Magentic Workflows',
    track: 'orchestrate',
    difficulty: 'advanced',
    duration_minutes: 90,
    description: 'Explore manager/planner orchestration with Microsoft Agent Framework patterns.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/extra-magentic-workflows/README.md',
  },
  {
    id: 'extra-hosted-longrunning',
    title: 'Deploy: Long-Running Agents',
    track: 'deploy',
    difficulty: 'advanced',
    duration_minutes: 75,
    description: 'Use background run patterns for workflows that outlive a browser session.',
    prerequisites: ['foundations'],
    outcomes: ['reference'],
    participant: 'activities/extra-hosted-longrunning/README.md',
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

function activityUrl(id, hash = '') {
  return `activity.html?id=${id}${hash || ''}`;
}

function transformMarkdown(markdown, activity) {
  const activityAssetBase = `assets/data/activities/${activity.id}/assets/`;
  const sourceDir = sourceDirFor(activity);

  return stripFrontMatter(markdown)
    .replace(/\{% include journey-status\.html[^%]*%\}/g, '')
    .replace(/\{% include module-lens\.html[^%]*%\}/g, '')
    .replace(/\{%[^%]*%\}/g, '')
    .replace(/\{\{\s*'\/idea-forge'\s*\|\s*relative_url\s*\}\}/g, 'idea-forge.html')
    .replace(/\{\{\s*'\/activities\/([^'#]+)(#[^']*)?'\s*\|\s*relative_url\s*\}\}/g, (_m, slug, hash = '') => activityUrl(slug, hash))
    .replace(/\]\(\.\.\/activities\/([^)#]+)(#[^)]+)?\)/g, (_m, slug, hash = '') => `](${activityUrl(slug, hash)})`)
    .replace(/\]\(\.\.\/idea-forge(#[^)]+)?\)/g, (_m, hash = '') => `](${activityUrl('idea-forge', hash)})`)
    .replace(/\]\(\.\.\/\.\.\/resources\//g, '](resources/')
    .replace(/\]\(\.\.\/\.\.\/docs\/activities\/([^)]+)\.md\)/g, (_m, slug) => `](activity.html?id=${slug})`)
    .replace(/\]\(\.\.\/([a-z0-9-]+)\/README\.md\)/g, (_m, slug) => `](activity.html?id=${slug})`)
    .replace(/\]\(assets\//g, `](${activityAssetBase}`)
    .replace(/\]\(([^):?#]+\.(?:py|sh|js|mjs|cjs|ps1))(#[^)]+)?\)/g, (_m, target, hash = '') => {
      if (!sourceDir) return _m;
      const candidate = path.resolve(ROOT, sourceDir, target);
      if (!candidate.startsWith(`${ROOT}${path.sep}`) || !fs.existsSync(candidate)) return _m;
      return `](${repoBlob(path.relative(ROOT, candidate).split(path.sep).join('/'))}${hash})`;
    })
    .replace(/\]\(solution\.md\)/g, sourceDir ? `](${repoBlob(`${sourceDir}/solution.md`)})` : '](#)')
    .replace(/\]\(evaluate\.py\)/g, sourceDir ? `](${repoBlob(`${sourceDir}/evaluate.py`)})` : '](#)')
    .replace(/\]\(validate\.py\)/g, sourceDir ? `](${repoBlob(`${sourceDir}/validate.py`)})` : '](#)')
    .replace(/\]\(\.\.\/\.\.\/\.env\.sample\)/g, `](${repoBlob('.env.sample')})`)
    .replace(/\]\(\.\.\/\.\.\/\.vscode\//g, `](${repoBlob('.vscode/')}`)
    .replace(/\]\(\.\.\/\.\.\/\.github\//g, `](${repoBlob('.github/')}`)
    .replace(/\]\(\.\.\/\.\.\/scripts\//g, `](${repoBlob('scripts/')}`)
    .replace(/\]\(\.\.\/\.\.\/docs\//g, `](${repoBlob('docs/')}`);
}

function writeGuide(activity) {
  const guideDir = path.join(OUT_GUIDES_DIR, activity.id);
  fs.mkdirSync(guideDir, { recursive: true });

  const configured = activity.participant;
  const fallback = `# ${activity.title}\n\nGuide content is not available yet.`;

  const raw = configured ? readIfExists(configured) : null;
  fs.writeFileSync(path.join(guideDir, 'README.md'), transformMarkdown(raw || fallback, activity));

  if (activity.participant && activity.participant.startsWith('activities/')) {
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

function loadScenarioRegistry() {
    if (!fs.existsSync(SCENARIOS_DIR)) return [];

    return fs.readdirSync(SCENARIOS_DIR, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => {
        const root = path.join(SCENARIOS_DIR, entry.name);
        const manifestPath = path.join(root, 'manifest.json');
        if (!fs.existsSync(manifestPath)) {
          throw new Error(`scenario ${entry.name} is missing manifest.json`);
        }
        try {
          return { root, ...JSON.parse(fs.readFileSync(manifestPath, 'utf8')) };
        } catch (error) {
          throw new Error(`scenario ${entry.name} has invalid manifest.json: ${error.message}`);
        }
      })
      .sort((left, right) => {
        const leftOrder = Number.isFinite(left.order) ? left.order : Number.MAX_SAFE_INTEGER;
        const rightOrder = Number.isFinite(right.order) ? right.order : Number.MAX_SAFE_INTEGER;
        if (leftOrder !== rightOrder) return leftOrder - rightOrder;
        return left.name.localeCompare(right.name);
      });
}

function scenarioPathExists(scenario, relativePath) {
    if (!relativePath || typeof relativePath !== 'string') return false;
    const target = path.resolve(scenario.root, relativePath);
    return target.startsWith(`${scenario.root}${path.sep}`) && fs.existsSync(target);
}

function detectScenarioProblems(scenarios) {
    const problems = [];
    const ids = new Set();
    for (const scenario of scenarios) {
      if (!scenario.id || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/u.test(scenario.id)) {
        problems.push(`${path.basename(scenario.root)} scenario needs a kebab-case id`);
      }
      if (!scenario.name || !scenario.tagline || !scenario.customer_outcome || !scenario.owner || !scenario.maturity) {
        problems.push(`${scenario.id || path.basename(scenario.root)} scenario manifest needs name, tagline, customer_outcome, owner, and maturity`);
      }
      if (!Array.isArray(scenario.decision_prompts) || !scenario.decision_prompts.length) {
        problems.push(`${scenario.id} scenario needs at least one decision prompt`);
      }
      if (ids.has(scenario.id)) problems.push(`duplicate scenario id ${scenario.id}`);
      ids.add(scenario.id);
      if (!scenarioPathExists(scenario, 'README.md')) problems.push(`${scenario.id} scenario is missing README.md`);
      if (!scenarioPathExists(scenario, scenario.slides)) problems.push(`${scenario.id} scenario slides ${scenario.slides} missing`);
      if (!scenarioPathExists(scenario, scenario.accelerator)) problems.push(`${scenario.id} scenario accelerator ${scenario.accelerator} missing`);
      if (!Array.isArray(scenario.lessons) || !scenario.lessons.length) {
        problems.push(`${scenario.id} scenario needs at least one lesson`);
        continue;
      }
      if (!Array.isArray(scenario.build_modules) || !scenario.build_modules.length) {
        problems.push(`${scenario.id} scenario needs at least one build module`);
      }
      const moduleIds = new Set();
      for (const module of scenario.build_modules || []) {
        if (!module.id || !module.title || !module.summary || !module.outcome) {
          problems.push(`${scenario.id} build module needs id, title, summary, and outcome`);
        }
        if (moduleIds.has(module.id)) problems.push(`${scenario.id} duplicate build module id ${module.id}`);
        moduleIds.add(module.id);
        if (module.activity_id && !ACTIVITIES.some((activity) => activity.id === module.activity_id)) {
          problems.push(`${scenario.id} build module ${module.id} references unknown activity ${module.activity_id}`);
        }
        for (const implementationPath of module.implementation_paths || []) {
          if (!scenarioPathExists(scenario, implementationPath)) {
            problems.push(`${scenario.id} build module ${module.id} implementation path ${implementationPath} missing`);
          }
        }
      }
      const lessonIds = new Set();
      for (const lesson of scenario.lessons) {
        if (!lesson.id || !lesson.title || !scenarioPathExists(scenario, lesson.path)) {
          problems.push(`${scenario.id} lesson needs id, title, and an existing path`);
        }
        if (lessonIds.has(lesson.id)) problems.push(`${scenario.id} duplicate lesson id ${lesson.id}`);
        lessonIds.add(lesson.id);
      }
    }
    return problems;
}

function copyScenarioAssets(scenarios) {
    const outputRoot = path.join(OUT_DATA_DIR, 'scenarios');
    fs.rmSync(outputRoot, { recursive: true, force: true });
    for (const scenario of scenarios) {
      fs.cpSync(scenario.root, path.join(outputRoot, scenario.id), { recursive: true });
      const readmePath = path.join(outputRoot, scenario.id, 'README.md');
      if (fs.existsSync(readmePath)) {
        const lessonByPath = new Map((scenario.lessons || []).map((lesson) => [lesson.path, lesson]));
        let rewritten = fs.readFileSync(readmePath, 'utf8').replace(
          /\]\((lessons\/[^)#]+\.md)(#[^)]+)?\)/g,
          (match, lessonPath, hash = '') => {
            const lesson = lessonByPath.get(lessonPath);
            return lesson
              ? `](lesson.html?scenario=${encodeURIComponent(scenario.id)}&lesson=${encodeURIComponent(lesson.id)}${hash})`
              : match;
          },
        );
        rewritten = rewritten.replace(
          /\]\(\.\.\/\.\.\/activities\/([^/)#]+)\/(?:README|FACILITATOR)\.md(#[^)]+)?\)/g,
          (_match, activityId, hash = '') => `](activity.html?id=${encodeURIComponent(activityId)}${hash})`,
        );
        fs.writeFileSync(readmePath, rewritten);
      }
    }
}

function scenarioOutput(scenario) {
    const assetBase = `assets/data/scenarios/${scenario.id}/`;
    return {
      id: scenario.id,
      name: scenario.name,
      tagline: scenario.tagline,
      order: Number.isFinite(scenario.order) ? scenario.order : null,
      customer_outcome: scenario.customer_outcome,
      maturity: scenario.maturity || 'initial',
      level: scenario.level || 'guided',
      duration_minutes: scenario.duration_minutes || 0,
      stage: scenario.stage || '',
      owner: scenario.owner || 'Unassigned',
      decision_prompts: scenario.decision_prompts || [],
      lessons: (scenario.lessons || []).map((lesson, index) => ({
        ...lesson,
        sequence: index + 1,
        content_path: `${assetBase}${lesson.path}`,
        lesson_path: `lesson.html?scenario=${encodeURIComponent(scenario.id)}&lesson=${encodeURIComponent(lesson.id)}`,
      })),
      build_modules: (scenario.build_modules || []).map((module, index) => ({
        ...module,
        sequence: index + 1,
        activity_path: module.activity_id ? activityUrl(module.activity_id) : '',
      })),
      asset_base: assetBase,
      readme_path: `${assetBase}README.md`,
      slides_path: `${assetBase}${scenario.slides}`,
      accelerator_path: `${assetBase}${scenario.accelerator}`,
    };
}

function activityOutput(activity, outcomeIds) {
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
    outcomes: [...new Set([...(activity.outcomes || []), ...outcomeIds])],
    personas: activity.personas || [],
    business_value: activity.business_value || [],
    adoption_stage: activity.adoption_stage || '',
    app_dependency: 'none',
    tier: activity.track === 'extras' ? 'extra' : 'core',
    references: activity.references || [],
    source_repo: 'microsoft/frontier-ai-starter-kit-rvas',
    source_path: activity.participant || '',
    license: 'MIT',
    participant_path: `assets/data/activities/${activity.id}/README.md`,
  };
}

function detectMissingReferences(activities, outcomes, aliases, scenarios) {
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
  for (const [legacyId, target] of Object.entries(aliases)) {
    if (!ids.has(target.id)) missing.push(`${legacyId} alias target ${target.id}`);
  }
  missing.push(...detectScenarioProblems(scenarios));
  return missing;
}

function main() {
  const scenarios = loadScenarioRegistry();
  const missing = detectMissingReferences(ACTIVITIES, OUTCOMES, LEGACY_ACTIVITY_ALIASES, scenarios);
  if (missing.length) {
    console.error('Build failed: missing references');
    missing.forEach((m) => console.error(`  - ${m}`));
    process.exit(1);
  }

  fs.rmSync(OUT_GUIDES_DIR, { recursive: true, force: true });
  fs.mkdirSync(OUT_DATA_DIR, { recursive: true });
  copyResources();
  copyScenarioAssets(scenarios);

  for (const activity of ACTIVITIES) {
    writeGuide(activity);
  }

  const outputActivities = ACTIVITIES.map((activity) => {
    const outcomeIds = OUTCOMES
      .filter((outcome) => (outcome.activity_ids || []).includes(activity.id))
      .map((outcome) => outcome.id);
    return activityOutput(activity, outcomeIds);
  });
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
    JSON.stringify({
      modules,
      outcomes,
      scenarios: scenarios.map(scenarioOutput),
      aliases: LEGACY_ACTIVITY_ALIASES,
      activities: outputActivities,
    }, null, 2),
  );
  fs.writeFileSync(path.join(OUT_DATA_DIR, 'dependency-graph.json'), JSON.stringify(graph, null, 2));

  console.log(`✓ built platform.json (modules: ${modules.length}, outcomes: ${outcomes.length}, scenarios: ${scenarios.length}, activities: ${outputActivities.length})`);
  console.log(`✓ copied guides → ${path.relative(ROOT, OUT_GUIDES_DIR)}`);
}

main();
