---
title: "The product is understanding"
date: 2026-09-04 09:00:00 +0530
categories: [Observability]
tags: [observability, sre, debugging, incident-response, telemetry]
description: "Observability isn't about collecting more telemetry. It's about shortening the time between 'something is wrong' and 'we understand why', for questions nobody anticipated at deploy time."
image:
  path: /assets/img/posts/observability-and-debugging-cover.jpg
  alt: "The product is understanding."
---

Observability isn't about collecting more telemetry. It's about reducing the time between "something is wrong" and "we understand why".

Metrics, logs, traces and events are ingredients. The product is understanding. A team can store a great deal of data and still leave the engineer on call at 2 a.m. not knowing where to start, because the missing piece is rarely more data. It is a connection between signals, a dimension to slice by, or a question the evidence was never shaped to answer.

![The product is understanding. Metrics, logs, traces and events flow through a funnel from "something is wrong" to "we understand why": answer questions you did not anticipate, reduce noise, shorten the path to understanding. Debugging closes the gap between what we think and what is happening. A print statement can be an act of honesty.](/assets/img/posts/observability-and-debugging.webp){: .infographic width="1122" height="1402" }

## Measure the path, not the pile

Telemetry volume is easy to measure, so it gets measured. The number that matters is harder: how long it takes to go from the first symptom to an explanation you can test.

An investigation usually moves through the same stages. Something is detected. Then you establish the scope: all requests, one operation, one tenant, one region, one version? Then you form and test explanations, then act. In my experience, most of the time is lost in scoping and explaining, not in detection. So that is where to look when you judge whether your observability is any good. After an incident, ask how long it took to reach the first correct hypothesis, and what slowed it down.

## Design for questions you didn't anticipate

Adding more dashboards won't save a brittle architecture. A dashboard encodes the questions someone thought of last quarter. The incidents that hurt are the ones nobody predicted.

OpenTelemetry's [observability primer](https://opentelemetry.io/docs/concepts/observability-primer/) puts it plainly: observability lets you understand a system from the outside by asking questions about it *without knowing its inner workings*. That only works if the telemetry was designed for it:

- **Context on every signal.** Service version, operation, tenant, region, feature flag. These are the dimensions you will want to slice by, and they are exactly the ones teams drop first to save cost.
- **A thread through the request.** A shared trace identifier, propagated with the [W3C Trace Context](https://www.w3.org/TR/trace-context/) `traceparent` header, lets you move from a slow metric to the specific requests behind it, and from there to their logs.
- **Changes as events.** Deployments, configuration changes and feature-flag flips on the same timeline as the symptoms. "What changed?" is the first question in most investigations, and it should take seconds to answer.

Charity Majors, Liz Fong-Jones and George Miranda's *Observability Engineering* makes the same case at length: the goal is to explore unknown unknowns, not to pre-build an answer for each known failure.

## Fifty alerts is noise, not visibility

If it takes fifty alerts to detect one outage, you don't have visibility. You have noise. Fifty pages for one incident means fifty things to read before anyone starts understanding anything, and a high chance the one alert that mattered gets lost.

Google's SRE book draws the line in its chapter on [monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/): separate symptoms from causes, and make every page actionable. Page on the user-facing symptom. Keep the causes as evidence you can reach from that page. I wrote about treating alerts as a product, with owners, contracts and quality metrics, in [Alerts are a product, not a byproduct](/posts/alerts-are-a-product/).

## Debugging closes the gap between belief and reality

Debugging is narrowing the gap between what I *think* is happening and what is *actually* happening. Most of the difficulty is not finding the bug. It is noticing which of my beliefs I haven't checked.

That is why a print statement is honesty, not laziness. It replaces an assumption ("this branch runs", "this value is never null") with an observation. Brian Kernighan said it decades ago: the most effective debugging tool is still careful thought, coupled with judiciously placed print statements. In production the equivalent is a deliberate log line or span attribute, added with care for sensitive data and overhead, that answers one specific question.

The same discipline helps a team during an incident. "The database is slow" is a hypothesis. "These requests spent most of their time waiting on this query" is an observation. Keep a running note with three short sections: what we observed, what we currently believe, and what evidence would change our minds. It stops an early guess from narrowing the investigation too soon, and it lets the next person on shift pick up the evidence rather than inherit a conclusion.

## Improve the next investigation

After an incident is understood, look back at where the path got hard. Was there no identifier linking two signals? Was the change that caused it invisible? Did a flood of alerts hide the one journey users were failing? Fix the smallest missing connection that would have made the next investigation shorter.

Sometimes that means more telemetry, but each addition has a cost. Every label multiplies series count, as I described in [Scale tests every assumption](/posts/scale-tests-every-assumption/), and every field needs a purpose, an owner and a retention period. A field nobody can interpret, or is allowed to keep, adds work without adding understanding.

Pick a recent incident and write down the questions the on-call engineer couldn't answer quickly. Close one of those gaps. The test of observability is whether the next person can reason about a problem neither of you has seen before.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Debugging is just narrowing the gap between &quot;what I think is happening&quot; and &quot;what is actually happening.&quot; A print statement is honesty, not laziness.<br><br><a href="https://twitter.com/hashtag/EngineeringMusings?src=hash&amp;ref_src=twsrc%5Etfw">#EngineeringMusings</a></p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2095717565935059392?ref_src=twsrc%5Etfw">September 4, 2026</a></blockquote>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Adding more dashboards won&#39;t save a brittle architecture.<br><br>True observability isn&#39;t hoarding metrics, logs, and traces—it&#39;s having a system designed to answer questions you didn&#39;t anticipate at deploy time.<br><br>If you need 50 alerts to detect a single outage, you don&#39;t have visibility. You have noise.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2089732998329770249?ref_src=twsrc%5Etfw">August 18, 2026</a></blockquote>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Observability isn’t about collecting more telemetry.<br><br>It’s about reducing the time between “something is wrong” and “we understand why.”<br><br>Metrics, logs, traces and events are ingredients.<br><br>The real product is understanding.<a href="https://twitter.com/hashtag/Observability?src=hash&amp;ref_src=twsrc%5Etfw">#Observability</a> <a href="https://twitter.com/hashtag/SRE?src=hash&amp;ref_src=twsrc%5Etfw">#SRE</a></p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2086292000798847068?ref_src=twsrc%5Etfw">August 9, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
