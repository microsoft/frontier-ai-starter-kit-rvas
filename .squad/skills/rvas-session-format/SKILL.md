# SKILL: Session Format Design

## What This Skill Covers
Designing a "AI Starter Kit RVAS" () session-in-a-box content architecture — the pattern for structuring activities, guides, and supporting infrastructure.

## When to Use
- Creating any -format session regardless of technology focus
- Designing progressive activity sequences for hands-on learning events
- Structuring content for facilitator-facilitated, team-based technical workshops

## The Pattern

### Activity Design Formula

1. **Activity 00 is always Setup** — isolate environment issues from learning
2. **Linear progression** — each activity depends on the previous (unless audience is advanced)
3. **Time allocation follows difficulty** — Beginner: 30-45min, Intermediate: 1-1.5hr, Advanced: 1-1.5hr
4. **Total time ≈ event duration × 0.8** — leave 20% for breaks, transitions, intros
5. **5–7 activities is the sweet spot** — fewer feels shallow, more creates time pressure

### Each Activity Contains

**Student Guide (README.md):**
- Introduction (motivation/context)
- Description (what to accomplish)
- Success Criteria (checkboxes — unambiguous completion signal)
- Learning Resources (official docs, not full tutorials)
- Tips (progressive hints: vague → specific)
- Advanced Activities (stretch goals for fast teams)

**Facilitator Guide (solution.md):**
- Step-by-step solution walkthrough
- Common pitfalls and unblocking strategies
- Facilitation tips (questions to ask, not answers to give)
- Timing guidance (when to intervene)

### Difficulty Escalation Pattern

```
Setup (always first) → Basics (use the tool) → Design (make decisions) →
Orchestrate (combine pieces) → Real-World Scenario (complex integration) →
Quality/Safety (evaluate & improve) → Production (deploy & operationalize)
```

### Repo Structure Pattern

```
/
├── activities/activity-NN-slug/   ← Paired student + facilitator content
├── docs/                           ← GitHub Pages (student-facing only)
├── resources/                      ← Shared data, scripts, images
└── .devcontainer/                  ← Reproducible environment
```

### Key Principles
- Facilitator solutions NEVER go on the public site
- Devcontainer is mandatory for session reliability
- Provide sample data for any activity that needs external input
- Write success criteria as checkboxes — participants self-assess
- Evaluation/safety activities come BEFORE deployment activities
- Each activity folder is self-contained (no cross-folder imports)

## Anti-Patterns to Avoid
- Parallel activity tracks (too complex for facilitators to manage)
- Mixing setup with first learning activity (environment issues block learning)
- Publishing solutions publicly (defeats the session model)
- Leaving data sourcing to participants (creates divergent experiences)
- Putting deployment before evaluation (ships irresponsible AI)
