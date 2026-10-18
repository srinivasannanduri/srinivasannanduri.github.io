---
title: "Let risk choose the review"
date: 2026-10-10 09:00:00 +0530
categories: [Leadership]
tags: [design-review, architecture, leadership, decision-making, engineering-judgment]
description: "As teams scale, principal engineers can't review everything without becoming bottlenecks, and stepping away invites drift. The answer isn't reviewing faster. It's routing each decision by its risk."
image:
  path: /assets/img/posts/reviews-that-scale-cover.jpg
  alt: "Let risk choose the review."
---

As teams scale, code and design reviews multiply. Principal engineers can't review everything without becoming bottlenecks. But stepping away entirely risks architectural drift.

The answer isn't reviewing faster. It's redesigning how reviews work, so that the consequences of a decision, not its size or its author, decide how much scrutiny it gets.

![Let risk choose the review. Local, reversible decisions go to the team; cross-team contracts go to domain review; high-impact, hard-to-reverse decisions go to senior review. A review-ready proposal shows the decision, alternatives, changed boundaries and blast radius. Show the delta and record why, automate checks, delegate review while keeping accountability, and invest in better contracts, guardrails and escalation paths. Measure safer decisions and fewer late reversals.](/assets/img/posts/reviews-that-scale.jpg){: .infographic width="1122" height="1402" }

## Route the decision, not the change

When every proposal goes through the same meeting with the same people, a local refactor and a shared data contract compete for the same attention. The queue grows, and the decisions that most need careful judgment get the least time.

Route by consequence instead:

- **Local and reversible** decisions stay with the team. A clear owner and an easy way back are enough.
- **Cross-team contracts** go to a domain review with the teams that depend on them.
- **High-impact, hard-to-reverse** decisions get senior review and broader accountability.

Jeff Bezos's 2015 shareholder letter made the same distinction between one-way and two-way doors: most decisions can be reversed cheaply and should be made quickly by small groups; a few cannot, and deserve slow, careful deliberation. Reversibility is the single most useful routing signal I know, for the reasons in [Price the reversal](/posts/price-the-reversal/).

These are routing principles, not org-chart levels. A small, security-sensitive change can need a specialist despite touching three lines. Agree a short list of escalation triggers with the teams who use the process, such as contract changes, data migrations, unclear ownership, changes to failure isolation, and security boundaries, and keep a path for any engineer to ask for help when they're unsure.

## Make the proposal review-ready

A reviewer should be able to judge a decision in minutes, not rediscover the system. A short decision brief does that: what is changing and why now, the alternatives considered, the boundaries affected, the likely blast radius, the reversal path, and the evidence behind the key assumptions.

When a design already exists, show the delta. A new dependency or a change of ownership should stand out, not be buried in a full re-presentation.

Then record the decision and why it was made. Michael Nygard's [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) introduced the lightweight architecture decision record for exactly this. A record lets future teams tell a deliberate trade-off from an accident, and gives reviewers something to revisit when conditions change.

## Automate what you can, and delegate the rest with support

Anything you can check reliably should be checked by a machine: required fields in the brief, API and schema linting, policy-as-code rules for security and data handling. Automation makes a review cheaper to prepare. It doesn't settle the design; passing a checklist is not approval.

Human attention is for what machines can't judge: ambiguous consequences, real alternatives, trade-offs between teams. Delegating that judgment only works if people have what they need to exercise it: clear contracts, guardrails, worked examples of good decisions, and escalation paths that people actually use. Otherwise you have transferred responsibility without the context to carry it.

The accountable owner stays explicit, even when many people advise. For a principal engineer, the job shifts from reviewing every decision to designing the review system: setting the guardrails, sampling decisions made without you, and coaching where judgment is still developing.

## Measure whether it helps

Meeting counts and approval times give an incomplete picture. Better signals are late reversals, dependencies discovered after launch, escalations that turned out to be unnecessary, and how long good decisions waited for a review slot. Ask authors and reviewers where the process clarified a risk and where it only created waiting.

Try it with your next few proposals: name the decision, route it by its consequences, and capture a short rationale. Review the results together before you scale the process up. A good review system doesn't just examine individual designs; it grows the organization's judgment.

## Where this started

This post grew out of a seven-part thread on X. Here is how it opened; the rest of the thread is [on X](https://x.com/snanduri_/status/2108796948631478305).

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">As teams scale, code and design reviews multiply. Principal Engineers can&#39;t review everything without becoming bottlenecks.<br><br>But stepping away entirely risks architectural drift.<br><br>The answer isn&#39;t reviewing faster. It&#39;s redesigning how reviews work. (1/7)</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2108796948631478305?ref_src=twsrc%5Etfw">October 10, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
