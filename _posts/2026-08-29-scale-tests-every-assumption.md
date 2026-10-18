---
title: "Scale tests every assumption"
date: 2026-08-29 09:00:00 +0530
categories: [Architecture]
tags: [architecture, scalability, distributed-systems, simplicity, design-review]
description: "At small scale almost any architecture works. Growth multiplies the costs a design quietly assumed away. A mature design stays simple under scale, failure, change and time, and so does the conversation about it."
image:
  path: /assets/img/posts/architecture-at-scale-cover.jpg
  alt: "Scale tests every assumption."
---

At small scale, almost any architecture works. That isn't because the design is good. It's because none of its assumptions have been tested yet.

Every query touches a few records. Every tenant behaves roughly the same. Someone on the team can repair the odd failure by hand. Growth doesn't just raise the numbers on those assumptions. It changes whether they are true, and when enough of them stop being true, the architecture has to change with them.

![Scale tests every assumption: replication, cardinality, retention, read paths, failure domains and cost. A design passes through four gates: scale, failure, change and time. A mature design stays simple under all four by choosing trade-offs, making complexity visible and aligning people. Good architecture simplifies the system and the conversation.](/assets/img/posts/architecture-at-scale.webp){: .infographic width="1122" height="1402" }

## Scale multiplies, it doesn't add

Take a telemetry service that ingests measurements and answers interactive queries. On a whiteboard, "10× more traffic" sounds like 10× more of everything. In practice the cost drivers multiply each other:

- **Storage and write work** grow with ingest rate × replication factor × retention. Doubling retention for a compliance request has the same effect on storage as doubling traffic.
- **Series count** grows with the product of label cardinalities. One new label with a few hundred values, added to one popular metric, can multiply that metric's series count by a few hundred.
- **Read cost** grows with the series a query touches × the time range it covers. A dashboard that was cheap over the last hour can be the most expensive query in the system over the last 90 days.

Those terms also interact. A design that comfortably serves one tenant's short queries can fall over when several tenants run long-range queries at the same moment, and an average request rate will never show you that. Cost is usually the assumption that breaks last and hurts most, because it fails quietly and on a monthly bill rather than a pager.

So I start scale reviews with a workload sketch instead of a component diagram: who sends what, at what rate, kept for how long, and read by which queries. Ranges, not single numbers, and the uncertainty written down. That turns "it needs to scale" into something the room can actually challenge.

## Failure: draw the blast radius, not just the boxes

A capacity plan needs a failure story beside it. If one storage partition slows down, which requests wait? If one tenant sends ten times its usual traffic, who else feels it? If a region goes away, what did we actually promise?

Those questions turn topology into user experience. They also expose designs that haven't removed complexity, only moved it into recovery runbooks and on-call judgement. Isolation is a design choice, not an outcome: cells, per-tenant limits, and techniques such as [shuffle sharding](https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/) exist to keep one bad actor from becoming everyone's incident.

A manual procedure can be the right call early on. Write down when it stops being acceptable, who owns it, and what signal says it's time to automate. An operational assumption nobody wrote down is one nobody budgets for.

## Change and time are tests too

The other two tests arrive later and get less attention. *Change*: a new label, a new query pattern, a longer retention tier, a second region. *Time*: the people who designed the system move on, and someone else has to run it at 3 a.m. with only the runbook.

A design that only its authors can operate has already failed the time test; it just hasn't been graded yet. This is also where reversal cost shows up. The decisions that leaked into contracts and stored data are the ones that make change expensive, which I wrote about in [Price the reversal](/posts/price-the-reversal/).

## Resist the urge to add complexity

The hardest problem in distributed systems isn't caching or naming things. It's resisting complexity when a simple, well-understood abstraction would cover 95% of the problem.

Every new system has a running cost that never shows up in the design doc: on-call, upgrades, security patches, capacity planning, and the expertise to debug it. Dan McKinley's [Choose Boring Technology](https://mcfunley.com/choose-boring-technology) puts it well: a team gets about three innovation tokens, so spend them where they buy something that matters. A partitioned table, a queue and a cache with a sensible expiry policy are boring precisely because thousands of teams have already found their failure modes for you.

Architecture maturity is knowing the best solution is rarely the cleverest one. It's the one that stays simple under scale, failure, change and time. Often the most valuable thing an architect says in a review is "no, we don't need another system for that".

## Good architecture simplifies the conversation too

The hardest architecture problems are rarely technology problems. They're about choosing the trade-offs, making complexity visible, saying no to systems we don't need, and getting people aligned behind a decision.

A good review leaves the team with a short list of explicit trade-offs rather than a longer diagram. Which read paths do we support, and which do we refuse? Where is isolation enforced? What does each extra day of retention cost? Which choices will be expensive to reverse? When those answers are written down, people can disagree with something specific, and then commit to it.

Before your next scaling discussion, replace the word "large" with three workload ranges and one failure scenario. The conversation that follows will tell you more than any early debate about which technology to use.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">At small scale, almost any architecture works.<br><br>At large scale, every assumption gets tested:<br>replication, cardinality, retention, query / read paths, failure domains — and especially cost.<br><br>Scale doesn’t just change the numbers. It changes the architecture.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2093556599281631583?ref_src=twsrc%5Etfw">August 29, 2026</a></blockquote>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">The hardest problem in distributed systems isn&#39;t caching or naming things.<br><br>It&#39;s resisting the urge to add complexity when a simple, well-understood abstraction would have solved 95% of the problem.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2091539217533006218?ref_src=twsrc%5Etfw">August 23, 2026</a></blockquote>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Architecture maturity is knowing that the best solution isn’t the cleverest design.<br><br>It’s the one that stays simple under scale, failure, change, and time.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2087760159997394958?ref_src=twsrc%5Etfw">August 13, 2026</a></blockquote>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">The hardest architecture problems are rarely technology problems.<br><br>They’re usually about:<br>• choosing the right trade-offs<br>• making complexity visible<br>• saying “no” to unnecessary systems<br>• and aligning people around a decision<br><br>Good architecture simplifies both the system and the conversation.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2087121698844033308?ref_src=twsrc%5Etfw">August 11, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
