---
title: "Throughput is buyable. Latency isn't."
date: 2026-10-20 10:04:00 +0530
categories: [Architecture]
tags: [architecture, latency, distributed-systems, performance, sre]
description: "Money scales capacity; physics bounds delay. Add machines and you can do more work per second, but a single request still waits on distance, coordination and its slowest dependency. Design for latency early, because you can't buy it later."
---

Two systems can both be "too slow" and need opposite fixes. One can't keep up: queues grow, requests time out under load, and adding capacity brings it back. The other is slow even when it's idle: a single request takes 400 ms at three in the morning, and doubling the fleet changes nothing.

The first is a throughput problem. The second is a latency problem. The difference matters because only one of them responds to money.

## Money buys throughput

Throughput is how much work the system does per unit of time: requests per second, jobs per hour, gigabytes per minute. It scales with parallelism. If the work can be split, through sharding, partitioning or stateless replicas behind a load balancer, more machines do more of it. Commodity hardware is good at this, and the cloud made it a line item.

The gains are close to linear until coordination starts to dominate. Locks, shared counters, a single leader that every write passes through: past a certain point the machines spend more time agreeing with each other than doing the work. But up to that point, throughput is an engineering and budget problem. You can usually buy your way out.

## Physics bounds latency

Latency is how long one operation takes. Most of that time isn't computation. It's waiting: for a network round trip, for a lock, for a replica to acknowledge, for the slowest of several calls to return.

Some of that waiting has a hard floor. Light in optical fibre covers roughly 200 km per millisecond, so every 100 km between two machines costs at least a millisecond of round trip before any software runs. In practice:

| Path | Typical round trip |
|---|---|
| Within a data centre | under a millisecond |
| Across a continent | tens of milliseconds |
| Between continents | about 70–150 ms |

No budget moves those numbers. You can't make light faster, skip the acknowledgement that strong consistency requires, or parallelise distance. More servers in the same place don't shorten the trip between two places.

## Latency is the price of agreement

If nothing changes, latency doesn't matter. It matters when new information has to reach somewhere else before the system can answer: a write that must be durable on a quorum, a read that must see the latest value, a transaction that spans two services.

That's why replication cuts both ways. More replicas add read throughput and survive more failures. But if every write must be acknowledged by a majority, and that majority spans regions, every commit pays the slowest required round trip. Consensus doesn't just suffer from latency; it's built out of round trips.

This is the real trade-off behind consistency models. Strong consistency means coordination, and coordination means waiting. Systems that favour availability and accept weaker consistency exist largely to avoid that wait. The useful rule of thumb: **if latency matters more than freshness, reduce coordination.**

## The slowest machine decides

Fan-out makes this worse. Suppose a user request queries 100 servers and waits for all of them. Each server is fast 99% of the time and slow 1% of the time. The chance that at least one is slow on a given request is 1 − 0.99¹⁰⁰, about 63%. A rare problem on each machine becomes the normal experience for the user.

Jeff Dean and Luiz André Barroso described this in [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/): at enough fan-out, the service's latency is set by its tail, not its median. And adding servers to a fan-out widens it, so scaling out can make the user experience *worse*.

It also changes how you measure. An average hides the tail completely; look at p99 and p99.9, per dependency. If you aggregate across instances, use histograms rather than precomputed per-instance quantiles, because you can't average percentiles and get a percentile.

## Hide it, avoid it, or budget it

You can't eliminate latency, but you can choose what to do with it.

**Hide it.** Cache results that don't need to be fresh. Move work off the request path: acknowledge, then process asynchronously. Prefetch what the next step will need. Stream partial results so the user sees progress before the slowest part finishes.

**Avoid it.** Count the serial round trips on the critical path and remove the ones that aren't load-bearing. Keep calls in the same region as the data they need. Put strong consistency only where correctness demands it, and let everything else read slightly stale data. Batch chatty calls into one.

**Tolerate the tail.** Set timeouts from a latency budget, not a guess, so a slow dependency fails fast instead of holding the request. For idempotent reads, send a hedged request to a second replica if the first hasn't answered by around its p95. Dean and Barroso report large cuts in tail latency for a small increase in load. Make sure the extra requests can't overload the system when everything is slow at once.

**Budget it.** Give each hop a share of the end-to-end objective, the way you'd split an error budget. When a new dependency wants 30 ms, the question becomes which existing hop gives it up.

## Ask about latency in the design review

Throughput problems tend to show up gradually, under load, when there's still time to add capacity. Latency is set by topology: where the data lives, how many services sit on the critical path, which of them must agree before the user gets an answer. Once those decisions ship and others build on them, they're expensive to reverse, and no amount of spending will undo them.

So ask the latency questions while the design is still on the whiteboard:

- How many serial network round trips does the critical path make, and between which locations?
- Which steps need strong consistency, and which could tolerate stale reads?
- What's the fan-out, and what happens to the user's p99 when one backend has a bad minute?
- What's the end-to-end latency objective, and how is it split across hops?

Throughput is an engineering problem. Latency is a physics problem. Treat it as a design input from the start, because it's the one you can't buy later.
