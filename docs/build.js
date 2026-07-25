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
const SCENARIOS_DIR = path.join(ROOT, 'scenarios');
const OUT_DATA_DIR = path.join(__dirname, 'assets', 'data');
const OUT_GUIDES_DIR = path.join(OUT_DATA_DIR, 'activities');
const OUT_RESOURCES_DIR = path.join(__dirname, 'resources');

const CUSTOMER_CHAPTER_IDS = {
  foundations: 'foundations',
  'advanced-action-tools': 'advanced-action-tools',
  'advanced-evaluation-redteam': 'advanced-evaluation-redteam',
  'advanced-tracing-observability': 'advanced-tracing-observability',
  'advanced-deploy-hosted-agent': 'advanced-deploy-hosted-agent',
  'extra-build-ui': 'extra-build-ui',
  'extra-fabric-iq': 'extra-fabric-iq',
  'extra-voice-live': 'extra-voice-live',
  'extra-magentic-workflows': 'extra-magentic-workflows',
  'extra-hosted-longrunning': 'extra-hosted-longrunning',
  'extra-document-workflow': 'extra-document-workflow',
  'extra-visual-multimodal': 'extra-visual-multimodal',
  'extra-governed-data-copilot': 'extra-governed-data-copilot',
  'capstone-multi-agent': 'capstone-multi-agent',
};

const LEGACY_ACTIVITY_ALIASES = {
  'customer-foundations': { id: 'foundations', path: 'knowledge-assistant' },
  'customer-action-tools': { id: 'advanced-action-tools', path: 'governed-workflow-agent' },
  'customer-evaluation-redteam': { id: 'advanced-evaluation-redteam' },
  'customer-tracing-observability': { id: 'advanced-tracing-observability' },
  'customer-deploy-hosted-agent': { id: 'advanced-deploy-hosted-agent' },
  'customer-build-ui': { id: 'extra-build-ui' },
  'customer-capstone-multi-agent': { id: 'capstone-multi-agent', path: 'orchestrated-workflow' },
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
      { id: 'orchestrate', name: 'Orchestrate', description: 'Coordinate multiple agents with manager, planner, and router patterns.' },
      { id: 'extras', name: 'Extras', description: 'Optional deepeners for UI, voice, Fabric IQ, long-running agents, and Copilot-assisted work.' },
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
      'extra-document-workflow',
      'extra-visual-multimodal',
      'extra-governed-data-copilot',
      'extra-copilot-assisted',
      'extra-magentic-workflows',
      'extra-hosted-longrunning',
      'capstone-multi-agent',
      'cleanup',
    ],
    success_metrics: [
      'The Northfield assistant is grounded, action-capable, evaluated, observable, and deployable.',
      'Participants can identify what to swap when moving from Northfield to a customer scenario.',
    ],
  },
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
      'setup',
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
      'capstone-multi-agent',
      'cleanup',
    ],
    success_metrics: [
      'The team can explain the target users, corpus, action, safety boundaries, and demo story.',
      'The prototype answers with citations, acts only through governed tools, and has a trust scorecard.',
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
    id: 'cleanup',
    title: 'Cleanup and cost hygiene',
    track: 'extras',
    difficulty: 'beginner',
    duration_minutes: 10,
    description: 'Review teardown targets, stop local processes, and remove event resources safely.',
    tags: ['cleanup', 'cost', 'azure'],
    outcomes: ['customer-build', 'upskill'],
    participant: 'docs/activities/cleanup.md',
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
    description: 'Package and deploy your agent as a hosted endpoint with the unified azure.yaml contract.',
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
    id: 'extra-document-workflow',
    title: 'Build: Document Workflow',
    track: 'extras',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Extract, validate, review, and route document data with a keyless, human-governed workflow.',
    prerequisites: ['foundations'],
    tags: ['documents', 'document-intelligence', 'human-review', 'workflow'],
    outcomes: ['upskill'],
    participant: 'activities/extra-document-workflow/README.md',
    facilitator: 'docs/activities/extra-document-workflow-facilitator.md',
  },
  {
    id: 'extra-visual-multimodal',
    title: 'Build: Visual Multimodal',
    track: 'extras',
    difficulty: 'intermediate',
    duration_minutes: 90,
    description: 'Analyze safe image inputs with structured results, uncertainty handling, and human review boundaries.',
    prerequisites: ['foundations'],
    tags: ['vision', 'multimodal', 'structured-output', 'human-review'],
    outcomes: ['upskill'],
    participant: 'activities/extra-visual-multimodal/README.md',
    facilitator: 'docs/activities/extra-visual-multimodal-facilitator.md',
  },
  {
    id: 'extra-governed-data-copilot',
    title: 'Build: Governed Data Copilot',
    track: 'extras',
    difficulty: 'advanced',
    duration_minutes: 90,
    description: 'Query approved structured data through explicit access, field, and result-provenance controls.',
    prerequisites: ['foundations'],
    tags: ['data', 'governance', 'structured-data', 'provenance'],
    outcomes: ['upskill'],
    participant: 'activities/extra-governed-data-copilot/README.md',
    facilitator: 'docs/activities/extra-governed-data-copilot-facilitator.md',
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

const APP_PATHS = [
  {
    id: 'knowledge-assistant',
    name: 'Knowledge and policy assistant',
    tagline: 'Answer from trusted, approved sources with clear citations and abstention.',
    description: 'Choose this path when the primary customer value is reliable answers about policies, manuals, FAQs, or other governed knowledge.',
    sessions: [
      { activity_id: 'customer-outcome', status: 'required', note: 'Define users, approved sources, access assumptions, and abstention boundaries.' },
      { activity_id: 'foundations', status: 'required', label: 'Build the agent and knowledge base', note: 'Complete Steps 1-4, including Foundry IQ grounding.', anchor: '#step-1-setup-provisioning-foundry-ai-search' },
      { activity_id: 'advanced-evaluation-redteam', status: 'required', note: 'Test cited answers, abstention, and domain-specific safety.' },
      { activity_id: 'advanced-tracing-observability', status: 'recommended', note: 'Show retrieval, latency, and failure paths.' },
      { activity_id: 'advanced-deploy-hosted-agent', status: 'recommended', note: 'Expose a controlled endpoint for stakeholder testing.' },
      { activity_id: 'extra-build-ui', status: 'optional', note: 'Use only when a visible citations experience strengthens the demo.' },
      { activity_id: 'advanced-action-tools', status: 'optional', note: 'Add only a clearly governed side effect; knowledge alone is enough for this path.' },
    ],
  },
  {
    id: 'governed-workflow-agent',
    name: 'Governed action and workflow agent',
    tagline: 'Turn an approved request into one safe, reviewable workflow action.',
    description: 'Choose this path when value comes from creating, changing, routing, or escalating work rather than answering from a document corpus.',
    sessions: [
      { activity_id: 'customer-outcome', status: 'required', note: 'Define the side effect, requester, approver, escalation, and evidence.' },
      { activity_id: 'foundations', status: 'required', label: 'Provision and define the agent', note: 'Complete Steps 1-3. Knowledge-base Step 4 is optional unless the action needs policy context.', anchor: '#step-1-setup-provisioning-foundry-ai-search' },
      { activity_id: 'advanced-action-tools', status: 'required', note: 'Implement one small approval-gated action or safe draft/queue equivalent.' },
      { activity_id: 'advanced-evaluation-redteam', status: 'required', note: 'Evaluate call, deny, escalate, and refusal behavior.' },
      { activity_id: 'advanced-tracing-observability', status: 'required', note: 'Trace tool calls and approval decisions end to end.' },
      { activity_id: 'advanced-deploy-hosted-agent', status: 'recommended', note: 'Host the controlled workflow for stakeholder testing.' },
      { activity_id: 'extra-build-ui', status: 'optional', note: 'Add when users need an approval card or workflow status surface.' },
      { activity_id: 'extra-hosted-longrunning', status: 'optional', note: 'Use for work that must survive the request or browser session.' },
    ],
  },
  {
    id: 'document-workflow',
    name: 'Document workflow',
    tagline: 'Extract, validate, review, and route structured work from documents.',
    description: 'Choose this path when documents begin a business process and a human must be able to see, correct, and approve the extracted result.',
    sessions: [
      { activity_id: 'customer-outcome', status: 'required', note: 'Define approved document types, retention, reviewers, unacceptable extraction errors, and the route after review.' },
      { activity_id: 'foundations', status: 'required', label: 'Provision and define the agent', note: 'Complete Steps 1-3. A knowledge base is optional unless the workflow needs policy context.', anchor: '#step-1-setup-provisioning-foundry-ai-search' },
      { activity_id: 'extra-document-workflow', status: 'required', note: 'Build extraction, confidence validation, review, and structured handoff for one safe document type.' },
      { activity_id: 'advanced-evaluation-redteam', status: 'required', note: 'Test extraction quality, low-confidence handling, prompt injection in documents, and review routing.' },
      { activity_id: 'advanced-tracing-observability', status: 'required', note: 'Trace document processing, validation, and reviewer decisions.' },
      { activity_id: 'advanced-deploy-hosted-agent', status: 'recommended', note: 'Host the controlled workflow only after document and reviewer access are understood.' },
      { activity_id: 'extra-build-ui', status: 'optional', note: 'Add a review surface only when it makes correction and approval clearer.' },
    ],
  },
  {
    id: 'live-data-copilot',
    name: 'Live data and insights copilot',
    tagline: 'Answer right-now operational questions from a governed live data source.',
    description: 'Choose this path when the customer needs current state, capacity, inventory, queue, SLA, or metric insight rather than static policy retrieval.',
    sessions: [
      { activity_id: 'customer-outcome', status: 'required', note: 'Define the source of truth, allowed fields, freshness expectation, and access boundary.' },
      { activity_id: 'foundations', status: 'required', label: 'Provision and define the agent', note: 'Complete Steps 1-3. Add a static knowledge base only when policy context is also needed.', anchor: '#step-1-setup-provisioning-foundry-ai-search' },
      { activity_id: 'extra-fabric-iq', status: 'required', note: 'Connect the approved operational data path and prove source routing.' },
      { activity_id: 'advanced-evaluation-redteam', status: 'required', note: 'Test factuality, access boundaries, and safe handling of missing or stale data.' },
      { activity_id: 'advanced-tracing-observability', status: 'required', note: 'Trace live-data tool selection and latency.' },
      { activity_id: 'advanced-deploy-hosted-agent', status: 'recommended', note: 'Host the copilot for a controlled user trial.' },
      { activity_id: 'extra-build-ui', status: 'optional', note: 'Use when a data-oriented stakeholder experience improves the proof point.' },
    ],
  },
  {
    id: 'voice-multimodal-assistant',
    name: 'Voice assistant',
    tagline: 'Deliver a low-friction spoken interaction without weakening the agent contract.',
    description: 'Choose this path when voice, accessibility, hands-free use, or a live conversational experience is central to the customer outcome.',
    sessions: [
      { activity_id: 'customer-outcome', status: 'required', note: 'Define audience, language, accessibility needs, handoff behavior, and the safe spoken demo.' },
      { activity_id: 'foundations', status: 'required', label: 'Provision and define the agent', note: 'Complete Steps 1-3. Grounding is optional unless spoken answers need trusted source citations.', anchor: '#step-1-setup-provisioning-foundry-ai-search' },
      { activity_id: 'extra-voice-live', status: 'required', note: 'Bind Voice Live to the scenario agent and tune turn-taking.' },
      { activity_id: 'advanced-evaluation-redteam', status: 'required', note: 'Test safety, refusal, and task completion in the spoken experience.' },
      { activity_id: 'advanced-tracing-observability', status: 'recommended', note: 'Make latency and failed interaction paths visible.' },
      { activity_id: 'advanced-deploy-hosted-agent', status: 'recommended', note: 'Host the agent for a repeatable voice demo.' },
      { activity_id: 'extra-build-ui', status: 'optional', note: 'Add a companion transcript or handoff surface when it helps the user journey.' },
    ],
  },
  {
    id: 'visual-multimodal-assistant',
    name: 'Visual multimodal assistant',
    tagline: 'Turn safe image inputs into structured, reviewable assistance.',
    description: 'Choose this path when a user needs help understanding an image and the outcome can be bounded with explicit uncertainty and review behavior.',
    sessions: [
      { activity_id: 'customer-outcome', status: 'required', note: 'Define allowed image classes, privacy boundaries, unsupported cases, reviewers, and the safe proof scenario.' },
      { activity_id: 'foundations', status: 'required', label: 'Provision and define the agent', note: 'Complete Steps 1-3; add document grounding only if the image result needs policy context.', anchor: '#step-1-setup-provisioning-foundry-ai-search' },
      { activity_id: 'extra-visual-multimodal', status: 'required', note: 'Build structured image analysis with uncertainty and human-review boundaries.' },
      { activity_id: 'advanced-evaluation-redteam', status: 'required', note: 'Test correct interpretation, uncertainty, unsafe inputs, and escalation.' },
      { activity_id: 'advanced-tracing-observability', status: 'recommended', note: 'Trace image processing and failure paths without exposing unsafe content.' },
      { activity_id: 'advanced-deploy-hosted-agent', status: 'recommended', note: 'Host only the approved, access-controlled experience.' },
      { activity_id: 'extra-build-ui', status: 'optional', note: 'Use when the result needs a clear, reviewable visual interface.' },
    ],
  },
  {
    id: 'governed-data-copilot',
    name: 'Governed data copilot',
    tagline: 'Answer structured-data questions through explicit access, field, and provenance controls.',
    description: 'Choose this path when operational insight needs more governance than a generic live-data lookup: approved fields, query rules, access assumptions, and explainable results.',
    sessions: [
      { activity_id: 'customer-outcome', status: 'required', note: 'Define the data owner, approved fields, requester access, unacceptable disclosures, and a trustworthy result proof.' },
      { activity_id: 'foundations', status: 'required', label: 'Provision and define the agent', note: 'Complete Steps 1-3. Static knowledge is optional and may supply policy context.', anchor: '#step-1-setup-provisioning-foundry-ai-search' },
      { activity_id: 'extra-governed-data-copilot', status: 'required', note: 'Implement allowlisted structured-data access, query validation, provenance, and sensitive-result review.' },
      { activity_id: 'advanced-evaluation-redteam', status: 'required', note: 'Test access denial, unsafe query attempts, unsupported questions, and result correctness.' },
      { activity_id: 'advanced-tracing-observability', status: 'required', note: 'Trace the governed query path and inspect denied or escalated requests.' },
      { activity_id: 'advanced-deploy-hosted-agent', status: 'recommended', note: 'Expose only after caller identity and data-platform permissions are decided.' },
      { activity_id: 'extra-build-ui', status: 'optional', note: 'Use when results need a visible provenance and approval surface.' },
      { activity_id: 'extra-fabric-iq', status: 'optional', note: 'Use Fabric IQ when the governed source is a supported Fabric/OneLake workload.' },
    ],
  },
  {
    id: 'orchestrated-workflow',
    name: 'Orchestrated or long-running workflow',
    tagline: 'Coordinate specialist work when a single agent or one chat turn is not enough.',
    description: 'Choose this path when the outcome has real handoffs, specialist roles, durable jobs, or an auditable multi-step process.',
    sessions: [
      { activity_id: 'customer-outcome', status: 'required', note: 'Define role boundaries, handoffs, ownership, and the smallest valuable end-to-end process.' },
      { activity_id: 'foundations', status: 'required', label: 'Provision and define the agent', note: 'Complete Steps 1-3. Add grounding only to specialists that need trusted documents.', anchor: '#step-1-setup-provisioning-foundry-ai-search' },
      { activity_id: 'extra-magentic-workflows', status: 'required', note: 'Model the manager/planner workflow before adding concurrency.' },
      { activity_id: 'capstone-multi-agent', status: 'required', note: 'Build the smallest router and specialist team that proves the outcome.' },
      { activity_id: 'advanced-evaluation-redteam', status: 'required', note: 'Evaluate routing, handoffs, refusals, and final task completion.' },
      { activity_id: 'advanced-tracing-observability', status: 'required', note: 'Trace handoffs and investigate failed paths.' },
      { activity_id: 'advanced-action-tools', status: 'recommended', note: 'Add only if a specialist must safely change a downstream system.' },
      { activity_id: 'extra-hosted-longrunning', status: 'optional', note: 'Use when the workflow must continue after the initiating request ends.' },
      { activity_id: 'advanced-deploy-hosted-agent', status: 'recommended', note: 'Host the workflow behind a controlled endpoint.' },
    ],
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
    .replace(/\]\(\.\.\/customer-build\)/g, '](catalog.html?outcome=customer-build)')
    .replace(/\]\(\.\.\/\.\.\/resources\//g, '](resources/')
    .replace(/\]\(\.\.\/\.\.\/docs\/activities\/([^)]+)\.md\)/g, (_m, slug) => `](activity.html?id=${slug})`)
    .replace(/\]\((?:\.\.\/)*customer-build\.md\)/g, '](catalog.html?outcome=customer-build)')
    .replace(/\]\((?:\.\.\/)*customer-outcome\.md\)/g, '](activity.html?id=customer-outcome)')
    .replace(/\]\(\.\.\/([a-z0-9-]+)\/README\.md\)/g, (_m, slug) => `](activity.html?id=${slug})`)
    .replace(/\]\((foundations|advanced-action-tools|advanced-evaluation-redteam|advanced-tracing-observability|advanced-deploy-hosted-agent|extra-build-ui|capstone-multi-agent)(#[^)]+)?\)/g,
      (_m, slug, hash = '') => isCustomerChapter ? `](${activityUrl(customerChapterId(slug), hash)})` : _m)
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
      .sort((left, right) => left.name.localeCompare(right.name));
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
      if (!scenarioPathExists(scenario, scenario.facilitator)) problems.push(`${scenario.id} scenario facilitator guide missing`);
      if (!scenarioPathExists(scenario, scenario.local_demo)) problems.push(`${scenario.id} scenario local demo guide missing`);
      if (!scenarioPathExists(scenario, scenario.validator)) problems.push(`${scenario.id} scenario validator missing`);
      if (!Array.isArray(scenario.lessons) || !scenario.lessons.length) {
        problems.push(`${scenario.id} scenario needs at least one lesson`);
        continue;
      }
      if (!Array.isArray(scenario.build_modules) || !scenario.build_modules.length) {
        problems.push(`${scenario.id} scenario needs at least one build module`);
      }
      const moduleIds = new Set();
      for (const module of scenario.build_modules || []) {
        if (!module.id || !module.title || !module.summary || !module.checkpoint) {
          problems.push(`${scenario.id} build module needs id, title, summary, and checkpoint`);
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
      customer_outcome: scenario.customer_outcome,
      maturity: scenario.maturity || 'initial',
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
      facilitator_path: `${assetBase}${scenario.facilitator}`,
      local_demo_path: `${assetBase}${scenario.local_demo}`,
      validator_path: `${assetBase}${scenario.validator}`,
    };
}

function activityOutput(activity, pathIds, outcomeIds) {
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
    outcomes: [...new Set([...(activity.outcomes || []), ...outcomeIds])],
    paths: pathIds,
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
    facilitator_path: `assets/data/activities/${activity.id}/FACILITATOR.md`,
  };
}

function markdownHeadingId(heading) {
  return heading
    .trim()
    .toLowerCase()
    .replace(/[^\w\s-]/gu, '')
    .replace(/\s+/gu, '-');
}

function detectMissingReferences(activities, outcomes, paths, aliases, scenarios) {
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
  for (const path of paths) {
    for (const session of path.sessions || []) {
      const activity = activities.find((candidate) => candidate.id === session.activity_id);
      if (!activity) {
        missing.push(`${path.id} path session ${session.activity_id}`);
        continue;
      }
      if (session.anchor) {
        const source = readIfExists(activity.participant);
        const anchors = source
          ? [...source.matchAll(/^#{1,6}\s+(.+)$/gmu)].map((match) => markdownHeadingId(match[1]))
          : [];
        if (!anchors.includes(session.anchor.slice(1))) {
          missing.push(`${path.id} path anchor ${session.anchor} for ${session.activity_id}`);
        }
      }
    }
  }
  for (const [legacyId, target] of Object.entries(aliases)) {
    if (!ids.has(target.id)) missing.push(`${legacyId} alias target ${target.id}`);
    if (target.path && !paths.some((path) => path.id === target.path)) {
      missing.push(`${legacyId} alias path ${target.path}`);
    }
  }
  missing.push(...detectScenarioProblems(scenarios));
  return missing;
}

function main() {
  const scenarios = loadScenarioRegistry();
  const missing = detectMissingReferences(ACTIVITIES, OUTCOMES, APP_PATHS, LEGACY_ACTIVITY_ALIASES, scenarios);
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
    writeGuide(activity, 'participant');
    writeGuide(activity, 'facilitator');
  }

  const pathIdsByActivity = new Map();
  for (const path of APP_PATHS) {
    for (const session of path.sessions) {
      const ids = pathIdsByActivity.get(session.activity_id) || [];
      ids.push(path.id);
      pathIdsByActivity.set(session.activity_id, ids);
    }
  }

  const outputActivities = ACTIVITIES.map((activity) => {
    const outcomeIds = OUTCOMES
      .filter((outcome) => (outcome.activity_ids || []).includes(activity.id))
      .map((outcome) => outcome.id);
    return activityOutput(activity, pathIdsByActivity.get(activity.id) || [], outcomeIds);
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

  const paths = APP_PATHS.map((path) => ({
    ...path,
    sessions: path.sessions.map((session) => {
      const activity = activityById.get(session.activity_id);
      return {
        ...session,
        title: activity.title,
        description: activity.description,
        duration_minutes: activity.duration_minutes,
      };
    }),
  }));

  const graph = {
    nodes: outputActivities.map((c) => ({ id: c.id, title: c.title, module: c.module, track: c.track, tier: c.tier })),
    edges: outputActivities.flatMap((c) => (c.prerequisites || []).map((from) => ({ from, to: c.id }))),
  };

  fs.writeFileSync(
    path.join(OUT_DATA_DIR, 'platform.json'),
    JSON.stringify({
      modules,
      outcomes,
      paths,
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
