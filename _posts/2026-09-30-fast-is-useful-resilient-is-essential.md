---
title: "Fast is useful. Resilient is essential."
date: 2026-09-30 09:00:00 +0530
categories: [Reliability]
tags: [resilience, distributed-systems, failure-isolation, sre, architecture]
description: "If your system can't degrade gracefully when a dependency stalls, you've built an expensive domino chain. Design failure isolation before you optimize for scale."
image:
  path: /assets/img/posts/resilience-cover.jpg
  alt: "Fast is useful. Resilient is essential."
---

If your system cannot degrade gracefully when a third-party dependency stalls, you haven't built a resilient distributed system. You've built an expensive domino chain.

That is why I'd design failure isolation before optimizing for scale. Optimization makes the healthy path faster. Resilience decides what happens on the day the healthy path isn't available, and that day comes for every system.

![Fast is useful, resilient is essential. When a dependency stalls, contain the failure and degrade gracefully: design failure isolation before optimizing scale. A line of falling dominoes contrasts with islands joined by bridges. Optimization helps us move faster; resilience helps us survive the unexpected. We need both.](/assets/img/posts/resilience.webp){: .infographic width="1122" height="1402" }

## A stalled dependency is worse than a dead one

A dependency that fails cleanly is easy to deal with. Connections are refused, errors come back in milliseconds, and callers move on. The dangerous case is the one that stays half alive. It accepts connections, then holds them. Microsoft researchers called this [gray failure](https://www.microsoft.com/en-us/research/publication/gray-failure-achilles-heel-cloud-scale-systems/), as opposed to clean fail-stop failure, and found that the major availability breakdowns they saw in cloud environments tended to come from it.

Little's Law shows why. The number of requests in flight equals the arrival rate times how long each one takes. At 1,000 requests a second and 100 milliseconds each, you have about 100 in flight. If the dependency stalls and each call now waits 30 seconds for a timeout, you have 30,000. Threads, connection pools and memory sized for 100 are gone within seconds, and requests that never touched the slow dependency start failing too. That is the domino chain: one stalled supplier, many callers waiting, and, as Martin Fowler puts it in his note on [circuit breakers](https://martinfowler.com/bliki/CircuitBreaker.html), critical resources running out and cascading failures across multiple systems.

## Decide what degrades, operation by operation

"Degrade gracefully" is meaningless until you say what it means for each operation. Take a dashboard that shows a critical account summary and an optional recommendations panel. If the recommendation service stalls, the summary should still load and the panel should be left out with a short message. If the authorization check stalls, the right answer is to stop, not to guess.

Some operations can fall back to cached or stale data, as long as they say so. Some can be queued and finished later. Some must fail. The one thing that is never graceful is returning a wrong answer quickly. Write down, for each important operation, which work continues, which work stops, and how the user finds out. Every mechanism that follows exists to enforce those decisions.

## Bound what a failure can consume

Once you know what must survive, protect it:

- **Timeouts from the user's budget.** If the page has to render in two seconds, the optional panel gets a few hundred milliseconds, not the library default of thirty seconds. Propagate the remaining time as a deadline, which [gRPC supports directly](https://grpc.io/docs/guides/deadlines/), so downstream services stop working on requests the caller has already abandoned.
- **Bulkheads.** Give each dependency its own concurrency limit or pool, so a stall in one can only exhaust its own share.
- **Circuit breakers.** After repeated failures, stop calling the dependency for a while and fail fast, which frees resources and gives the dependency room to recover.
- **Retry budgets.** Retries are, in the words of AWS's [guide to timeouts, retries and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), "selfish". Cap them, add jitter, and only retry operations that are safe to repeat. I wrote about how retries turn a slowdown into a storm in [Improve the system. Protect the outcome.](/posts/improve-the-system-protect-the-outcome/)

## Recovery is a failure mode too

The moment a dependency comes back is often the second outage. Every client retries at once, queues drain in a burst, and the recovering service falls over again. Work that waited in a queue during the outage may no longer be worth doing: the user who asked has long since given up.

Plan the return to normal as carefully as the failure. Drop queued work whose deadline has passed instead of processing it. Bring traffic back gradually, not all at once. AWS's article on [load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) makes the useful distinction between throughput and *goodput*: work completed that someone is still waiting for. Recovery is done when goodput is back, not when the process restarts.

## Efficient and brittle

Optimization and resilience pull in different directions. Optimization removes slack: fewer instances, higher utilization, tighter timeouts, less redundancy. Resilience *is* slack, and you pay for it every day it isn't used.

Queueing theory makes the cost of removing slack concrete. In a simple queue, average waiting time grows with utilization ÷ (1 − utilization). At 50% utilization a request waits about one service time; at 90%, about nine; at 95%, about nineteen. A system tuned to run hot has no room left to absorb a stall, a burst or a slow recovery.

The same is true well beyond software. A society obsessed with productivity but indifferent to resilience can become extraordinarily efficient, and dangerously brittle. Optimization helps us move faster. Resilience helps us survive what we didn't predict. We need both, in that order of design: bound the unhealthy path first, then make the healthy path fast.

## Rehearse it

None of this is real until you've watched it happen. Pick one dependency and, in an agreed scope, make it slow rather than dead. Watch the user journeys that depend on it, the shared resources around it, and the transition back to normal.

Then describe the three states, slow, failed and recovering, and how each one affects users and shared capacity. If your team can explain all three, you have a design. If you can only list the mechanisms, you have a set of hopes.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">A society obsessed with productivity, but indifferent to resilience, may become extraordinarily efficient — and dangerously brittle.<br><br>Optimization helps us move faster.<br>Resilience helps us survive what we didn’t predict.<br><br>We need both.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2105121205393265041?ref_src=twsrc%5Etfw">September 30, 2026</a></blockquote>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Modern cloud architecture rule: <br><br>If your system cannot degrade gracefully when a third-party dependency stalls, you haven&#39;t built a resilient distributed system—you&#39;ve built an expensive domino chain.<br><br>Design for failure isolation before optimizing for scale.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2088672284836036715?ref_src=twsrc%5Etfw">August 15, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
