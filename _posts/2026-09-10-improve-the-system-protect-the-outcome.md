---
title: "Improve the system. Protect the outcome."
date: 2026-09-10 09:00:00 +0530
categories: [Reliability]
tags: [systems-thinking, sre, slo, metrics, observability]
description: "Tuning parameters is the weakest way to change a system, and turning a metric into the goal is the fastest way to lose what it measured. Fix the loop, and anchor every target in a user outcome."
image:
  path: /assets/img/posts/systems-and-metrics-cover.jpg
  alt: "Improve the system. Protect the outcome."
---

Engineering teams make two mistakes with systems that look unrelated but come from the same place.

The first is reaching for parameters: more memory, a longer timeout, a few more instances. The second is making a metric the goal: deployments per week, tickets closed, an uptime percentage. Both treat the number as the system. Both can improve the number while the thing users care about stays the same, or gets worse.

![Improve the system, protect the outcome. Look beyond parameters to information flows, feedback loops and system goals. Keep metrics anchored in user outcomes: deployments are not value, tickets are not progress, uptime numbers are not reliability. Good SLOs connect targets to user experience. Ideas from Donella Meadows and Goodhart's Law.](/assets/img/posts/systems-and-metrics.webp){: .infographic width="1122" height="1402" }

## Parameters are the weakest lever

Donella Meadows' essay [Leverage Points: Places to Intervene in a System](https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/) ranks twelve places to change a system, from least to most effective. Constants, parameters and numbers come last, at number twelve. Feedback loops, the structure of information flows and the goals of the system all rank far higher.

That ranking maps closely onto how production incidents actually behave. Take a service with recurring latency spikes. The usual fixes are parameters: raise the client timeout, add instances, enlarge the queue. Sometimes they help for a week. But the spikes are often driven by a loop. Requests time out, clients retry, the retries add load, more requests time out. If three layers each retry three times, one user request can become dozens of attempts at the bottom of the stack. Google's SRE book describes this in its chapter on [cascading failures](https://sre.google/sre-book/addressing-cascading-failures/): retries amplify overload.

The queue depth is the stock. The retry loop is what keeps filling it. Fixing the loop means retry budgets and jittered backoff, shedding load before the queue grows, and telling callers early that the service is saturated. That last one is an information flow, two levels above any timeout setting. Fix the loop, not just the stock.

## When the number becomes the goal

Charles Goodhart made his observation about monetary policy in 1975. The version most engineers quote is anthropologist Marilyn Strathern's: *when a measure becomes a target, it ceases to be a good measure.*

It applies directly to engineering:

- If **deployment frequency** becomes the goal, teams optimize deployments: smaller, more frequent, not necessarily more valuable.
- If **ticket closure** becomes the goal, teams optimize tickets: a hard case gets a workaround, closes, and comes back under a new number.
- If **uptime** becomes the goal, teams may optimize the number instead of reliability: a health check that stays green while users cannot finish the one task the service exists for.

None of this means targets are bad. A metric is a proxy, and pressure to improve the proxy widens the gap between it and the outcome. The defence is to keep the outcome in view and design the system around the metric so that gaming it is harder than improving the real thing.

## Anchor targets in user outcomes

Good SLOs are targets anchored in user outcomes. Google's [SRE chapter on service level objectives](https://sre.google/sre-book/service-level-objectives/) separates an SLI, a carefully defined measure of the service, from an SLO, a target for that measure. Most of the value is in the word "carefully".

For a report service, a useful SLI is not "the process is up". It is closer to: *the share of valid report requests that complete successfully within an agreed time*. Then every word needs a definition. Which requests are valid? What counts as success: a 200, or a report with the right data in it? Over what window? And does the aggregate hide a pattern, such as one large customer whose reports fail every morning while everyone else's succeed?

An SLO also needs a consequence, or it becomes a reporting ritual. That is the job of an [error budget policy](https://sre.google/workbook/error-budget-policy/): when the budget is spent, reliability work takes priority over features; when it is healthy, the team ships with confidence. The number exists to drive that decision.

## Pair every target with a counter-signal

Each target should come with a check that exposes the most likely way to game it:

- **Deployment frequency** alongside change failure rate. [DORA](https://dora.dev/guides/dora-metrics-four-keys/) measures throughput and instability together for exactly this reason.
- **Tickets closed** alongside reopen rate and repeat contacts.
- **SLO attainment** alongside the worst-served customers and the most important user journeys, not only the average.

The aim is not more dashboards. Add a measure only when it answers a question someone will act on.

## Try this with your team

Pick one number your team celebrates. Write the user outcome next to it. Then describe one way the number could improve while that outcome gets worse.

If that is easy to describe, you have found your next change, and it is probably to a loop, an information flow or a goal rather than another target.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Goodhart’s Law is especially relevant in engineering:<br><br>If deployment frequency becomes the goal, teams optimize deployments.<br>If ticket closure becomes the goal, teams optimize tickets.<br>If uptime becomes the goal, teams may optimize the number instead of reliability.<br><br>This doesn’t mean targets are bad.<br><br>Good SLOs are targets anchored in user outcomes. Goodhart’s Law is the warning not to let the metric become more important than the outcome it represents.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2097853978709233801?ref_src=twsrc%5Etfw">September 10, 2026</a></blockquote>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Most engineering teams try to fix system bottlenecks by tweaking parameters (adding more RAM, tweaking timeouts, scaling instances).<br><br>But according to Donella Meadows, the highest leverage points aren&#39;t numbers—they are information flows, feedback loops, and system goals.<br><br>Fix the loop, not just the stock.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2090705998885560572?ref_src=twsrc%5Etfw">August 21, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
