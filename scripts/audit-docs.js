#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { TextDecoder } = require('util');

const ROOT = path.resolve(__dirname, '..');
const SCRIPT_EXTENSIONS = '(?:py|sh|js|mjs|cjs|ps1)';
const ROOT_SCRIPT_PREFIXES = ['activities/', 'docs/', 'resources/', 'scripts/', '.devcontainer/'];
const GENERATED_PREFIXES = ['docs/assets/data/activities/', 'docs/resources/'];
const SKIP_PREFIXES = ['docs/assets/data/', 'docs/resources/', 'docs/vendor/'];
const SITE_CHROME_DENY = /[▸◆▣›↗]/gu;
const MOJIBAKE = /(?:Ã[\u0080-\u00BF]|Â[\u0080-\u00BF]?|â(?:€|€™|€œ|€|€“|€”|†’|œ|š)|ðŸ|ï¸|ï¿½)/gu;
const LEARNER_CONTEXT = /\b(?:add|append|author|build|create|creates|creating|implement|save|scaffold|write|your)\b/i;

function relative(file) {
  return path.relative(ROOT, file).split(path.sep).join('/');
}

function walk(dir, predicate, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(abs, predicate, out);
    else if (predicate(abs)) out.push(abs);
  }
  return out;
}

function isSkipped(rel) {
  return SKIP_PREFIXES.some((prefix) => rel.startsWith(prefix));
}

function sourceDocs() {
  const files = [];
  for (const name of ['README.md', 'CONTRIBUTING.md']) {
    const file = path.join(ROOT, name);
    if (fs.existsSync(file)) files.push(file);
  }

  walk(path.join(ROOT, 'docs'), (file) => {
    const rel = relative(file);
    return file.endsWith('.md') && !isSkipped(rel);
  }, files);

  walk(path.join(ROOT, 'activities'), (file) => {
    const name = path.basename(file);
    return name === 'README.md' || name === 'solution.md';
  }, files);

  const backendReadme = path.join(ROOT, 'scripts/action-backend/README.md');
  if (fs.existsSync(backendReadme)) files.push(backendReadme);
  return [...new Set(files)].sort();
}

function generatedDocs() {
  const files = [];
  for (const prefix of GENERATED_PREFIXES) {
    walk(path.join(ROOT, prefix), (file) => file.endsWith('.md'), files);
  }
  return [...new Set(files)].sort();
}

function siteChromeFiles() {
  const files = walk(path.join(ROOT, 'docs'), (file) => {
    const rel = relative(file);
    if (isSkipped(rel) || rel === 'docs/assets/js/marked.min.js') return false;
    return ['.html', '.js', '.css'].includes(path.extname(file));
  });
  return files.sort();
}

function readUtf8(file, failures) {
  const buffer = fs.readFileSync(file);
  try {
    return new TextDecoder('utf-8', { fatal: true }).decode(buffer);
  } catch (error) {
    failures.push(`${relative(file)}: invalid UTF-8 (${error.message})`);
    return null;
  }
}

function lineNumber(text, index) {
  return text.slice(0, index).split('\n').length;
}

function findMatches(file, text, regex, label, failures) {
  regex.lastIndex = 0;
  for (const match of text.matchAll(regex)) {
    failures.push(`${relative(file)}:${lineNumber(text, match.index)}: ${label} ${JSON.stringify(match[0])}`);
  }
}

function auditCharacters(files, failures, { chrome = false } = {}) {
  for (const file of files) {
    const text = readUtf8(file, failures);
    if (text == null) continue;
    findMatches(file, text, /\uFFFD/gu, 'contains the Unicode replacement character', failures);
    findMatches(file, text, MOJIBAKE, 'contains likely mojibake', failures);
    findMatches(file, text, /\u25A1/gu, 'uses ambiguous WHITE SQUARE; use a Markdown task item', failures);
    if (chrome) {
      findMatches(file, text, SITE_CHROME_DENY, 'uses a fragile text glyph in site chrome', failures);
    }
  }
}

function cleanToken(token) {
  return token
    .replace(/^['"`(]+/, '')
    .replace(/['"`),.;:]+$/, '')
    .split('#', 1)[0];
}

function hasTemplateSyntax(token) {
  return /[<>{}*[\]$]/.test(token);
}

function resolveScript(doc, token, isMarkdownLink) {
  const cleaned = cleanToken(token);
  if (!cleaned || hasTemplateSyntax(cleaned) || /^(?:https?:)?\/\//i.test(cleaned)) return null;

  const candidates = [];
  if (isMarkdownLink || cleaned.startsWith('../')) {
    candidates.push(path.resolve(path.dirname(doc), cleaned));
  }
  if (cleaned.startsWith('./scripts/')) {
    candidates.push(path.resolve(ROOT, cleaned.slice(2)));
  } else if (cleaned.startsWith('./')) {
    candidates.push(path.resolve(path.dirname(doc), cleaned));
  } else if (ROOT_SCRIPT_PREFIXES.some((prefix) => cleaned.startsWith(prefix))) {
    candidates.push(path.resolve(ROOT, cleaned));
  } else if (!cleaned.includes('/')) {
    candidates.push(path.resolve(path.dirname(doc), cleaned));
  }

  return {
    token: cleaned,
    candidates: [...new Set(candidates)],
    existing: candidates.find((candidate) => fs.existsSync(candidate)) || null,
  };
}

function scriptReferences(file, text) {
  const refs = [];
  const linkPattern = new RegExp(
    `\\[[^\\]]*\\]\\(([^)\\s]+\\.${SCRIPT_EXTENSIONS})(?![A-Za-z0-9])(?:#[^)]*)?\\)`,
    'gu',
  );
  for (const match of text.matchAll(linkPattern)) {
    refs.push({ token: match[1], index: match.index, line: match[0], isMarkdownLink: true });
  }

  const commandPattern = new RegExp(
    `(?:python3?|bash|sh|node)\\s+([^\\s\\x60]+\\.${SCRIPT_EXTENSIONS})(?![A-Za-z0-9])([^\\n\\x60]*)|((?:\\.\\/)?(?:${ROOT_SCRIPT_PREFIXES.map((p) => p.replace(/[/.]/g, '\\$&')).join('|')})[^\\s\\x60]+\\.${SCRIPT_EXTENSIONS})(?![A-Za-z0-9])([^\\n\\x60]*)`,
    'gu',
  );
  for (const match of text.matchAll(commandPattern)) {
    refs.push({
      token: match[1] || match[3],
      args: match[2] || match[4] || '',
      index: match.index,
      line: match[0],
      isMarkdownLink: false,
    });
  }
  return refs;
}

function documentedFlags(args) {
  return [...String(args || '').matchAll(/(^|\s)(--[a-z][a-z0-9-]*)\b/gi)].map((match) => match[2]);
}

function recentWorkingDirectory(text, index) {
  const before = text.slice(Math.max(0, index - 1500), index);
  const matches = [...before.matchAll(/(?:^|[;&\n]\s*)cd\s+([^\s;&`]+)/g)];
  if (!matches.length) return null;
  const token = cleanToken(matches[matches.length - 1][1]);
  if (!token || hasTemplateSyntax(token)) return null;
  return path.resolve(ROOT, token);
}

function auditScriptReferences(files, failures) {
  let checked = 0;
  for (const file of files) {
    const text = readUtf8(file, failures);
    if (text == null) continue;
    const lines = text.split('\n');
    const repositoryRootContext = /\b(?:repository|repo) root\b/i.test(text);
    for (const ref of scriptReferences(file, text)) {
      const resolved = resolveScript(file, ref.token, ref.isMarkdownLink);
      if (!resolved) continue;
      if (
        !ref.isMarkdownLink &&
        !resolved.candidates.length &&
        resolved.token.includes('/') &&
        repositoryRootContext
      ) {
        resolved.candidates.push(path.resolve(ROOT, resolved.token));
        resolved.existing = resolved.candidates.find((candidate) => fs.existsSync(candidate)) || null;
      }
      if (!resolved.candidates.length) continue;
      if (
        !ref.isMarkdownLink &&
        ROOT_SCRIPT_PREFIXES.some((prefix) => resolved.token.replace(/^\.\//, '').startsWith(prefix)) &&
        !/\b(?:repository|repo) root\b/i.test(text)
      ) {
        failures.push(
          `${relative(file)}:${lineNumber(text, ref.index)}: root-relative script command lacks a ` +
          '`repository root` command-context note',
        );
      }
      if (!ref.isMarkdownLink && !resolved.existing) {
        const cwd = recentWorkingDirectory(text, ref.index);
        if (cwd) {
          const candidate = path.join(cwd, resolved.token);
          resolved.candidates.unshift(candidate);
          if (fs.existsSync(candidate)) resolved.existing = candidate;
        }
      }
      checked += 1;

      if (!resolved.existing) {
        const number = lineNumber(text, ref.index);
        const context = lines.slice(Math.max(0, number - 30), number + 1).join('\n');
        if (!ref.isMarkdownLink && resolved.token.includes('/') && repositoryRootContext) {
          const isRootPath = ROOT_SCRIPT_PREFIXES.some((prefix) => resolved.token.startsWith(prefix));
          if (isRootPath && LEARNER_CONTEXT.test(context)) continue;
          failures.push(
            `${relative(file)}:${number}: script ${JSON.stringify(resolved.token)} does not resolve ` +
            'from the documented repository-root command context',
          );
          continue;
        }
        const basename = path.basename(resolved.token);
        const mentionsBasename = context.toLowerCase().includes(basename.toLowerCase());
        const labelsAsFile = new RegExp(`(?:#|\\[)[^\\n]{0,120}${basename.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`, 'i');
        if ((LEARNER_CONTEXT.test(context) && mentionsBasename) || labelsAsFile.test(context)) continue;
        failures.push(
          `${relative(file)}:${number}: script ${JSON.stringify(resolved.token)} does not resolve ` +
          `(${resolved.candidates.map(relative).join(' or ')})`,
        );
        continue;
      }

      if (!ref.isMarkdownLink) {
        const implementation = readUtf8(resolved.existing, failures);
        if (implementation == null) continue;
        for (const flag of documentedFlags(ref.args)) {
          if (!implementation.includes(flag)) {
            failures.push(
              `${relative(file)}:${lineNumber(text, ref.index)}: documented flag ${flag} is not handled by ` +
              relative(resolved.existing),
            );
          }
        }
      }
    }
  }
  return checked;
}

function maskCode(markdown) {
  return markdown
    .replace(/```[\s\S]*?```/g, (block) => block.replace(/[^\n]/g, ' '))
    .replace(/`[^`\n]*`/g, (inline) => ' '.repeat(inline.length));
}

function renderedLinks(markdown) {
  const links = [];
  const visible = maskCode(markdown);
  const markdownLink = /!?\[[^\]]*\]\(([^)\s]+)(?:\s+["'][^"']*["'])?\)/gu;
  const htmlLink = /\b(?:href|src)=["']([^"']+)["']/giu;
  for (const regex of [markdownLink, htmlLink]) {
    for (const match of visible.matchAll(regex)) {
      links.push({ target: match[1], index: match.index });
    }
  }
  return links;
}

function auditGeneratedLinks(files, failures) {
  let checked = 0;
  const docsRoot = path.join(ROOT, 'docs');
  for (const file of files) {
    const text = readUtf8(file, failures);
    if (text == null) continue;
    for (const link of renderedLinks(text)) {
      const target = link.target.trim();
      if (
        !target ||
        target.startsWith('#') ||
        hasTemplateSyntax(target) ||
        /^(?:https?:|mailto:|tel:|data:|javascript:|\/\/)/i.test(target)
      ) {
        continue;
      }
      let pathname;
      try {
        pathname = decodeURIComponent(target.split(/[?#]/, 1)[0]);
      } catch {
        failures.push(
          `${relative(file)}:${lineNumber(text, link.index)}: link has invalid URL encoding ${JSON.stringify(target)}`,
        );
        continue;
      }
      if (!pathname) continue;
      const resolved = path.resolve(docsRoot, pathname.replace(/^\/+/, ''));
      checked += 1;
      if (!resolved.startsWith(`${docsRoot}${path.sep}`) || !fs.existsSync(resolved)) {
        failures.push(
          `${relative(file)}:${lineNumber(text, link.index)}: rendered link ${JSON.stringify(target)} ` +
          `does not resolve to a published file (${relative(resolved)})`,
        );
      }
    }
  }
  return checked;
}

const RETIRED_LESSON_HEADINGS = [
  /^#{1,6}\s+audience\b/gimu,
  /^#{1,6}\s+preparation\b/gimu,
  /^#{1,6}\s+timed (?:activity|exercise)\b/gimu,
  /^#{1,6}\s+artifact\b/gimu,
  /^#{1,6}\s+expected output\b/gimu,
  /^#{1,6}\s+debrief\b/gimu,
];

const REQUIRED_LESSON_HEADINGS = [
  'what you build',
  'choose your path',
  'implementation',
  'verify',
  'troubleshooting',
  'decision record',
  'next module',
];

function resolveRelativePath(basePath, href) {
  const segments = basePath.split('/').slice(0, -1);
  for (const part of href.split('/')) {
    if (!part || part === '.') continue;
    if (part === '..') segments.pop();
    else segments.push(part);
  }
  return segments.join('/');
}

function auditLessonRouting(scenario, lesson, activityIds, failures) {
  const source = path.join(ROOT, 'docs', lesson.content_path);
  if (!fs.existsSync(source)) {
    failures.push(`scenario ${scenario.id} lesson ${lesson.id}: generated lesson source is missing`);
    return;
  }

  const body = fs.readFileSync(source, 'utf8');
  const label = `scenario ${scenario.id} lesson ${lesson.id}`;

  for (const pattern of RETIRED_LESSON_HEADINGS) {
    pattern.lastIndex = 0;
    const match = pattern.exec(body);
    if (match) failures.push(`${label}: uses the retired workshop heading "${match[0].trim()}"`);
  }

  const headings = (body.match(/^#{1,6}\s+.*$/gmu) || []).map((line) =>
    line.replace(/^#{1,6}\s+/u, '').toLowerCase());
  for (const required of REQUIRED_LESSON_HEADINGS) {
    if (!headings.some((heading) => heading.includes(required))) {
      failures.push(`${label}: build-module contract is missing a "${required}" section`);
    }
  }

  const lessonPaths = new Set((scenario.lessons || []).map((item) => item.path));
  for (const match of body.matchAll(/\]\(([^)\s]+)\)/gu)) {
    const raw = match[1];
    if (!raw || raw.startsWith('#') || /^[a-z][a-z0-9+.-]*:/iu.test(raw)) continue;
    const [target] = raw.split('#');
    if (!/\.md$/iu.test(target)) continue;

    const resolved = resolveRelativePath(lesson.path, target);
    if (lessonPaths.has(resolved)) continue;

    const activityMatch = resolved.match(/^activities\/([^/]+)\/(?:README|FACILITATOR)\.md$/iu);
    if (activityMatch && activityIds.has(activityMatch[1])) continue;

    failures.push(`${label}: Markdown link "${raw}" does not resolve to an in-site course or activity route`);
  }
}

function auditBuildModules(scenario, activityIds, failures) {
  const modules = scenario.build_modules || [];
  if (!modules.length) {
    failures.push(`scenario ${scenario.id}: no build modules are published to the course roadmap`);
    return;
  }

  const seen = new Set();
  for (const module of modules) {
    const label = `scenario ${scenario.id} build module ${module.id || '<missing id>'}`;
    for (const field of ['id', 'title', 'summary', 'outcome', 'sequence']) {
      if (!module[field]) failures.push(`${label}: missing "${field}"`);
    }
    if (module.id && seen.has(module.id)) failures.push(`${label}: duplicate module id`);
    if (module.id) seen.add(module.id);
    if (module.activity_id && !activityIds.has(module.activity_id)) {
      failures.push(`${label}: references unknown activity "${module.activity_id}"`);
    }
  }
}

function auditScenarioCourseRoutes(failures) {
  const lessonPage = path.join(ROOT, 'docs', 'lesson.html');
  const lessonScript = path.join(ROOT, 'docs', 'assets', 'js', 'lesson.js');
  const guidePage = path.join(ROOT, 'docs', 'guide.html');
  const guideScript = path.join(ROOT, 'docs', 'assets', 'js', 'guide.js');
  const platformPath = path.join(ROOT, 'docs', 'assets', 'data', 'platform.json');

  if (!fs.existsSync(lessonPage)) failures.push('docs/lesson.html: customer lesson route is missing');
  if (!fs.existsSync(lessonScript)) failures.push('docs/assets/js/lesson.js: customer lesson renderer is missing');
  if (!fs.existsSync(guidePage)) failures.push('docs/guide.html: scenario guide route is missing');
  if (!fs.existsSync(guideScript)) failures.push('docs/assets/js/guide.js: scenario guide renderer is missing');
  if (!fs.existsSync(platformPath)) {
    failures.push('docs/assets/data/platform.json: generated course registry is missing; run npm run build');
    return;
  }

  let platform;
  try {
    platform = JSON.parse(fs.readFileSync(platformPath, 'utf8'));
  } catch (error) {
    failures.push(`docs/assets/data/platform.json: invalid JSON (${error.message})`);
    return;
  }

  const activityIds = new Set((platform.activities || []).map((activity) => activity.id));

  for (const scenario of platform.scenarios || []) {
    const readme = path.join(ROOT, 'docs', 'assets', 'data', 'scenarios', scenario.id, 'README.md');
    if (!fs.existsSync(readme)) {
      failures.push(`scenario ${scenario.id}: generated playbook is missing`);
      continue;
    }
    const playbook = fs.readFileSync(readme, 'utf8');
    if (/\]\(lessons\/[^)#]+\.md(?:#[^)]+)?\)/u.test(playbook)) {
      failures.push(`scenario ${scenario.id}: generated playbook links directly to a raw lesson Markdown file`);
    }
    if (/\]\(\.\.\/[^)]+\)/u.test(playbook)) {
      failures.push(`scenario ${scenario.id}: generated playbook contains parent-relative links that 404 from scenario.html`);
    }
    if (/\]\((?:\.\.\/)+(?:lesson|activity|scenario|slides)\.html/u.test(playbook)) {
      failures.push(`scenario ${scenario.id}: generated playbook must use root-relative app routes, not parent-relative app links`);
    }

    auditBuildModules(scenario, activityIds, failures);

    for (const lesson of scenario.lessons || []) {
      if (!lesson.lesson_path || !lesson.content_path) {
        failures.push(`scenario ${scenario.id} lesson ${lesson.id}: missing in-site lesson route metadata`);
        continue;
      }
      auditLessonRouting(scenario, lesson, activityIds, failures);
    }
  }
}

function main() {
  const args = new Set(process.argv.slice(2));
  const runSource = args.size === 0 || args.has('--source');
  const runGenerated = args.size === 0 || args.has('--generated');
  const failures = [];
  let referenceCount = 0;

  if (runSource) {
    const docs = sourceDocs();
    auditCharacters(docs, failures);
    auditCharacters(siteChromeFiles(), failures, { chrome: true });
    referenceCount += auditScriptReferences(docs, failures);
    console.log(`Audited ${docs.length} authoritative documentation files.`);
  }

  if (runGenerated) {
    const docs = generatedDocs();
    if (!docs.length) failures.push('No generated activity/resource Markdown found; run npm run build.');
    auditCharacters(docs, failures);
    referenceCount += auditScriptReferences(docs, failures);
    referenceCount += auditGeneratedLinks(docs, failures);
    auditScenarioCourseRoutes(failures);
    console.log(`Audited ${docs.length} generated documentation files.`);
  }

  if (failures.length) {
    console.error(`Documentation audit failed with ${failures.length} issue(s):`);
    failures.forEach((failure) => console.error(`  - ${failure}`));
    process.exit(1);
  }

  console.log(`Documentation audit passed (${referenceCount} documentation reference checks).`);
}

main();
