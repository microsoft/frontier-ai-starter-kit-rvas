---
name: "rvas-activity-writing"
description: "Write student and facilitator activity content for AI Starter Kit RVAS repositories in a beginner-friendly, guided format."
domain: "instructional-design"
confidence: "high"
source: "earned"
tools:
  - name: "view"
    description: "Read plan files, templates, and prior decisions before drafting activity content."
    when: "At the start of any new activity-writing task"
---

## Context
Use this skill when creating or revising activity content for a AI Starter Kit RVAS repository. It applies best when the audience is hands-on learners who need enough structure to make progress without turning the experience into a tutorial. The goal is to create student materials that drive action and facilitator materials that support facilitation.

## Patterns
- Start from the repo blueprint first: read the plan, activity descriptions, existing decisions, and audience constraints.
- Follow the paired-file pattern: `README.md` for students, `solution.md` for facilitators.
- Student guides should answer six questions in order: why this matters, what we are building, what to do next, how to know we are done, where to learn more, and what to try if we finish early.
- Facilitator guides should include walkthrough, common blockers, timing expectations, and diagnostic questions that preserve discovery.
- Scaffold platform concepts before asking learners to make design choices. Define unfamiliar terms where they first appear.
- Reuse a single scenario across multiple activities when later work depends on shared context, such as a RAG corpus or evaluation task.
- Write success criteria as observable checkboxes, not vague goals.
- Prefer official Microsoft documentation in learning resources.

## Examples
- Activity 00: orient students around Azure AI Foundry hubs, projects, and connected resources before any model work begins.
- Activity 01: connect portal actions to SDK actions so learners see that a deployment becomes an endpoint their code can call.
- Activity 02: frame prompt engineering as system behavior design, then test with edge cases before saving the final prompt.
- RAG corpus pattern: create realistic, queryable documents with concrete deadlines, office hours, policies, and support contacts.

## Anti-Patterns
- Assuming students already know Azure vocabulary
- Publishing facilitator-only solution detail in student guides
- Writing activities as passive reading instead of action steps
- Using generic sample data that cannot answer precise retrieval questions
- Giving hints that solve the task immediately instead of narrowing the search space
