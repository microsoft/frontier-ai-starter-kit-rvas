---
title: Resources
nav_order: 5
---

<div class="hero-panel challenge-hero">
  <span class="hero-kicker">Reference shelf</span>
  <h1>Resources</h1>
  <p class="hero-tagline">A curated set of official docs, SDK guides, and community links for participants who want context fast. Use this page when you need the right reference without digging through search results mid-hackathon.</p>
</div>

## Microsoft Foundry

<div class="quick-grid">
  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/">Microsoft Foundry documentation</a></h3>
    <p>The official hub for concepts, how-to guides, and platform capabilities.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/how-to/create-projects">Create projects in Microsoft Foundry</a></h3>
    <p>Project setup guidance, prerequisites, and role requirements.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/how-to/deploy-models-openai">Deploy models in Microsoft Foundry</a></h3>
    <p>Deployment flow for taking a model from catalog to runnable endpoint.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/how-to/model-catalog-overview">Model catalog overview</a></h3>
    <p>How to explore providers, capabilities, and deployment options.</p>
  </div>

</div>

## Azure AI Projects & Foundry SDK *(primary)*

The SDK used throughout this hackathon. `azure-ai-projects` is the Foundry project client; `azure-ai-agents` drives agent creation, versioning, and tool attachment.

<div class="quick-grid">
  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme">Azure AI Projects SDK for Python</a></h3>
    <p>Package overview, <code>AIProjectClient</code> setup, connections, agents, and OpenAI client integration.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code">Get started with the Foundry SDK (Python)</a></h3>
    <p>Quickstart: create a project client, run a chat call, and connect to Azure AI Search.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/agents/quickstart">Agents quickstart</a></h3>
    <p>Create, version, and run a Foundry agent end-to-end with <code>PromptAgentDefinition</code>.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples">azure-ai-projects samples</a></h3>
    <p>Official SDK samples for agents, connections, evals, and search tool configuration.</p>
  </div>

</div>

## Azure AI Inference SDK *(secondary — direct model calls without the project client)*

Use this when calling a model endpoint directly, without a Foundry project. The challenges in this hackathon use `azure-ai-projects` + `get_openai_client()` by default; Azure AI Inference is an alternative for standalone model inference.

<div class="quick-grid">
  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/python/api/overview/azure/ai-inference-readme">Azure AI Inference SDK for Python</a></h3>
    <p>Package overview, supported endpoints, auth options, and core chat APIs.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://aka.ms/azsdk/azure-ai-inference/python/reference">API reference</a></h3>
    <p>Class-level reference for clients, models, and request parameters.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples">Azure SDK samples</a></h3>
    <p>Practical Python examples for chat completions, embeddings, and authentication.</p>
  </div>

</div>

## Prompt Engineering

<div class="quick-grid">
  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/ai-services/openai/concepts/prompt-engineering">Prompt engineering concepts</a></h3>
    <p>Azure AI guidance on structure, clarity, examples, and iteration for effective prompts.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/quickstarts/get-started-playground">Playgrounds in Microsoft Foundry</a></h3>
    <p>How to test prompts, compare behaviors, and iterate quickly in the portal.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://cookbook.openai.com/">OpenAI Cookbook</a></h3>
    <p>Helpful patterns and examples for prompt design, structured output, and application behaviors.</p>
  </div>

</div>

## RAG &amp; AI Search

<div class="quick-grid">
  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/concepts/retrieval-augmented-generation">RAG in Microsoft Foundry</a></h3>
    <p>Architecture overview for retrieval-backed generation with Azure services.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/search/vector-search-overview">Vector search overview</a></h3>
    <p>How embeddings and vector indexes improve semantic retrieval.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/how-to/index-add">Add data and build indexes in Microsoft Foundry</a></h3>
    <p>Connect data, build indexes, and create grounded chat experiences.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/en-us/azure/search/tutorial-rag-build-solution">Classic RAG tutorial</a></h3>
    <p>A step-by-step Azure AI Search tutorial that makes the retrieval flow concrete.</p>
  </div>

</div>

## Evaluation

<div class="quick-grid">
  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/concepts/evaluation-approach-gen-ai">Azure AI evaluation concepts</a></h3>
    <p>Official guidance for evaluators, datasets, and evaluation workflows.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/azure/foundry/how-to/evaluate-generative-ai-app">Evaluate with Microsoft Foundry</a></h3>
    <p>Practical how-to guide for running built-in evaluators on your application.</p>
  </div>

  <div class="quick-card">
    <h3><a href="https://learn.microsoft.com/en-us/training/paths/evaluate-generative-ai-apps/">Evaluate generative AI apps</a></h3>
    <p>Microsoft Learn training path on quality metrics, testing, and iteration.</p>
  </div>

</div>

## Community

<div class="quick-grid">
  <div class="quick-card">
    <h3><a href="https://microsoft.github.io/WhatTheHack/">What The Hack community</a></h3>
    <p>Explore the broader WTH format, community guidance, and related event resources.</p>
  </div>

</div>
