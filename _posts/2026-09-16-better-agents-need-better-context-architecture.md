---
title: "Better agents need better context architecture"
date: 2026-09-16 09:00:00 +0530
categories: [AI]
tags: [ai-agents, context-engineering, knowledge-graphs, llm, architecture]
description: "Better agents aren't just a matter of better prompts or bigger context windows. Documents give agents information; graphs give them relationships, and relationships need provenance."
image:
  path: /assets/img/posts/context-architecture-cover.jpg
  alt: "Better agents need better context architecture."
---

The more I work with AI agents, the more convinced I am that the answer isn't just better prompts or bigger context windows. It's better context architecture.

Documents give agents information. Graphs give them relationships. Most of the questions that matter in engineering organizations are about relationships: who owns this, what calls it, why it was built this way, and what breaks if it changes.

![Better agents need better context architecture. Documents give agents information; connected graphs give them relationships such as author, references, related_to, contains, used_by and mentions. Fragmented knowledge becomes connected context and then navigable relationships. Graphify connects knowledge agents can navigate and reason over.](/assets/img/posts/context-architecture.jpg){: .infographic width="1122" height="1402" }

## Bigger windows aren't the whole answer

It is tempting to treat context as a capacity problem: if the agent got it wrong, give it more. The evidence says otherwise. The *Lost in the Middle* study ([Liu et al.](https://arxiv.org/abs/2307.03172)) found that language models use information at the beginning or end of a long input well, and significantly worse when it sits in the middle, even for models built for long contexts. Anthropic's guide to [context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) puts it directly: context is a critical but finite resource.

So the job is not to put more text in front of the agent. It is to put the *right* facts in front of it, connected in a way it can follow.

## Questions that cross document boundaries

Take a question like: *which teams should review a change to this service's authentication contract?* A good answer needs the service's owner, its current callers, the interface in question, the decision that shaped it, and the current review policy.

Those facts live in different places: a service catalogue, the code, an architecture decision record, a wiki page. A search for "authentication" returns documents that mention the word. It doesn't return the chain. The agent then has to infer how the pieces connect, and it can't tell a current caller from a historical example, or an authoritative policy from an abandoned proposal.

An explicit relationship such as *service A calls interface B* makes that navigation direct. That is what a knowledge graph adds: entities and the edges between them, which an agent can walk and reason over.

## Relationships need provenance

An edge is only as good as its source. For every relationship, an agent (and the person checking its answer) needs to know three things:

- **Where it came from.** Parsed from code, declared in a catalogue, or written by a person?
- **When it was last true.** A dependency observed yesterday is stronger evidence than one documented two years ago.
- **What kind of claim it is.** Observed behaviour, declared intent, or someone's interpretation.

A graph can encode a stale or wrong relationship just as easily as a document can hold an outdated instruction. Provenance is what lets an agent, or a reviewer, tell them apart.

## Graphify as one approach

My original post pointed to [Graphify](https://github.com/Graphify-Labs/graphify), which builds a queryable knowledge graph from a codebase and its surrounding material: docs, SQL schemas, configs and PDFs. Two of its design choices line up with the points above: it parses code deterministically rather than guessing, and it aims to explain every edge it creates.

It's one useful direction rather than proof that a graph improves every agent task. For a narrow question, plain document search can be entirely enough. Let the architecture follow the questions you need answered and the evidence you can keep current.

## Evaluate answers, not confidence

Start with a small set of real questions that need facts from several sources. For each, write down a good answer and the evidence it requires. Include questions where the right answer is "the ownership information is missing": an agent that admits a gap is more useful than one that fills it convincingly.

Then compare how the agent does with today's information and with the proposed structure. Look for unsupported relationships, stale sources and dependencies it missed. That tells you far more than whether the answer sounds confident.

Often the first improvement is unglamorous: clear ownership metadata, links from decisions to the interfaces they shaped, a date on every runbook. Context architecture includes those ordinary information habits. The same context is what makes AI useful in operations, as in [AI reasons over observability](/posts/ai-reasons-over-observability/).

Pick one question your agents keep getting wrong. Draw the chain of facts needed to answer it, and repair the weakest link.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">The more I work with AI agents, the more convinced I am that it isn’t just better prompts or bigger context windows.<br><br>It’s better context architecture.<br><br>Graphify helps turn fragmented knowledge into a connected graph that agents can navigate and reason over.<br><br>Documents give agents information.<br>Graphs give them relationships.<br><br><a href="https://t.co/BmMRR0ekWH">https://t.co/BmMRR0ekWH</a></p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2100052634178904557?ref_src=twsrc%5Etfw">September 16, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
