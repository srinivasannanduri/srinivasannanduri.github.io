---
title: "AI reasons over observability"
date: 2026-08-27 09:00:00 +0530
categories: [Observability]
tags: [observability, ai-agents, aiops, sre, incident-response]
description: "AI shouldn't replace the observability platform. It should reason over it: telemetry supplies the evidence, context connects it, reasoning interprets it, and agents act within limits you set."
image:
  path: /assets/img/posts/ai-and-observability-cover.jpg
  alt: "AI reasons over observability."
---

AI shouldn't replace the observability platform. It should reason over it.

Metrics, logs, traces and events provide the evidence. AI provides correlation and reasoning. Agents add action. The interesting future is a pipeline with four distinct stages: **telemetry → context → reasoning → action**. Each stage has a different job, fails in a different way, and deserves its own design.

![AI reasons over observability. Metrics, logs, traces and events feed four stages: telemetry, context, reasoning (correlation and interpretation) and action (agents act on the understanding). Observability supplies the evidence.](/assets/img/posts/ai-and-observability.jpg){: .infographic width="1122" height="1402" }

## Four stages, four different jobs

- **Telemetry** records what the system did. It is the evidence, and [OpenTelemetry](https://opentelemetry.io/docs/concepts/observability-primer/) gives it a common shape. An agent cannot reason its way past missing or wrong data.
- **Context** connects that evidence to the things people care about: which service, which dependency, which owner, which deployment, which user journey, which SLO. It is what an experienced on-call engineer carries in their head, and it is usually the weakest stage.
- **Reasoning** proposes explanations: these errors started after that change, on this path, for these tenants. Its output is a hypothesis, not a verdict.
- **Action** changes something, or asks a person to. Tool protocols such as the [Model Context Protocol](https://modelcontextprotocol.io/), an open standard for connecting AI applications to external systems, make it straightforward to give an agent both read and write access. That is exactly why the action stage needs the most deliberate design.

A product may present all four in one chat window. Design and evaluate them separately anyway, because a failure in one looks like a failure in all of them.

## Correlation is a hypothesis

An agent notices that error rates rose three minutes after a deployment. That timing is a good hypothesis. It is not a cause. Plenty of incidents start near a deployment for unrelated reasons, and the cost of a confident wrong answer during an incident is high: the team rolls back, the errors continue, and twenty minutes are gone.

A useful agent answer looks like a good incident note. It lists what was observed, with time ranges and sources. It states the current hypothesis. It names the evidence that would refute it, and what it couldn't see. I described that observed / believed / would-change-our-mind structure in [The product is understanding](/posts/the-product-is-understanding/). An agent should be held to the same standard as an engineer, not a looser one because its prose is fluent.

## Match authority to reversibility

Suggesting the right runbook and rolling back a production service are different kinds of help. Decide in advance which actions an agent may take, under what conditions, and how the result is checked:

1. **Investigate**, read-only: query telemetry, gather context, summarize.
2. **Recommend** with evidence, for a person to approve.
3. **Act** on pre-approved, easily reversed steps with a limited blast radius, such as scaling out, restarting one instance or turning off a feature flag, and report what it did.
4. **Never act alone** on hard-to-reverse changes: data deletion, schema changes, region failover.

The dividing line is the same one I use for engineering decisions in general: how expensive the action is to reverse, as in [Price the reversal](/posts/price-the-reversal/). Every agent also needs stopping conditions. Missing evidence, conflicting ownership, or an action outside its authority should end in an explicit handoff to a person, with the evidence attached.

## Context is the bottleneck

When AI-assisted investigation fails, the reasoning is rarely the first problem. The agent didn't know who owns the service, which dependencies it has, what changed in the last hour, or which SLO the symptom threatens. Better models don't fix missing context. Better context architecture does, which is the subject of [Better agents need better context architecture](/posts/better-agents-need-better-context-architecture/).

## Evaluate the whole path

A plausible summary is not evidence of operational value. Build an evaluation set from real past incidents, where you already know the answer, and replay them. For each, check whether the agent:

- found the evidence that mattered, and in reasonable time;
- avoided causal claims the evidence didn't support;
- proposed a next step an experienced engineer would agree with;
- stayed within its authority, and handed off when it should have.

Then look at the outcomes of the actions it took. Did user experience improve? Is there a clear record of what it did and why? Could an operator who wasn't there understand it afterwards?

Start with one operational question and one bounded action. Keep the evidence visible at every stage, so people can trust the reasoning, challenge it, and improve it as the system grows. Observability supplies the evidence; everything above it should show its work.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">AI shouldn’t replace the observability platform.<br><br>It should reason over it.<br><br>Metrics, logs, traces and events provide evidence.<br><br>AI provides correlation and reasoning.<br><br>Agents add action.<br><br>The interesting future is:<br><br>Telemetry → Context → Reasoning → Action.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2092817819138412707?ref_src=twsrc%5Etfw">August 27, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
