---
title: "Hide the right complexity"
date: 2026-08-25 09:00:00 +0530
categories: [Platform]
tags: [platform-engineering, developer-experience, abstractions, api-design, architecture]
description: "Platform engineering isn't about exposing infrastructure. It's about hiding the right complexity behind reliable contracts, and being honest about the consequences you can't hide."
image:
  path: /assets/img/posts/platform-engineering-cover.jpg
  alt: "Hide the right complexity."
---

The best platforms make complexity disappear. Users shouldn't need to understand your topology, storage model, failure domains or scaling strategy to ship a service.

But complexity that disappears from the user's view hasn't gone anywhere. Someone still has to understand it, operate it and be paged for it. Platform engineering isn't about exposing infrastructure, and it isn't about pretending infrastructure doesn't exist. It's about choosing which complexity to absorb, and putting a reliable contract in front of it.

![Hide the right complexity. Above the waterline, the user experience: simple, reliable contracts. Below it, behind the platform: topology, storage model, failure domains and scaling strategy. Great platforms make complexity disappear.](/assets/img/posts/platform-engineering.webp){: .infographic width="1122" height="1402" }

## Hide decisions, not consequences

A team that wants to deploy a service, expose an endpoint and know whether it's healthy should not have to choose a storage layout or a placement policy first. Those are decisions the platform can make better, more consistently, and once.

What the platform can't hide is the consequence of those decisions. A user may not need to know which storage engine sits underneath. They do need to know whether deleting their service deletes its data, whether that can be undone, and for how long. They need to know what happens at a capacity limit and what recovery time they can plan around.

Joel Spolsky's [Law of Leaky Abstractions](https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/) says that all non-trivial abstractions, to some degree, are leaky. The design choice is whether the leaks are deliberate or accidental. Limits, failure behaviour and data guarantees should leak on purpose, in the documentation and the API, before a user discovers them during an incident.

## The contract is the product

"The platform handles it" is not a contract. A useful one has four parts:

- **Inputs:** a service definition, a capacity class, an availability tier. Small, opinionated, and about the user's needs rather than the platform's internals.
- **Promises:** the SLO for each tier, what happens at a limit, how failover behaves, what deletion means.
- **Signals:** how users see their service's health against those promises, in their terms rather than the names of internal components.
- **Ownership:** where the user's responsibility ends and the platform team's begins, including who gets paged for what.

The CNCF's [platforms white paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) describes this as treating the platform as a product, with reduced cognitive load for its users as one of the goals. Team Topologies' idea of a [thinnest viable platform](https://teamtopologies.com/key-concepts) is the useful counterweight: build the smallest platform that genuinely removes work for the teams using it, not every abstraction you can imagine.

A contract that many teams build on is also expensive to change later, for the reasons in [Price the reversal](/posts/price-the-reversal/). Fields, defaults and identifiers in a platform API deserve the same care as any public API.

## Golden paths and owned exceptions

Most teams should be able to stay on the supported path. Spotify describes a [Golden Path](https://engineering.atspotify.com/2020/08/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem) as the opinionated and supported way to build a system. The word that matters there is *supported*.

Some workloads won't fit, and they need an escape hatch. The danger is an exception with no owner. A team gets a custom configuration to unblock a launch, and two years later it is a second product that nobody planned, staffed or monitored. Every exception should say who owns it and which guarantees change because of it. Sometimes the right answer is to bring the pattern onto the golden path; sometimes it is to say no.

## Failure is part of the interface

An abstraction is tested when something underneath it breaks. If a zone degrades, can a user tell from the platform whether their service is affected, what they can do, and when to escalate? Or do they have to ask in a chat channel and wait for someone who knows the topology?

If a platform's status is expressed only in the names of its internal components, it has hidden the complexity in the wrong place. Users need their service's health measured against the promise the platform made them, which is the job of an SLO anchored in user outcomes; I wrote about that in [Improve the system. Protect the outcome.](/posts/improve-the-system-protect-the-outcome/)

## Measure the journey, not the interface

Counting configuration fields tells you very little. A tiny interface can still be confusing if its promises are vague. Better measures come from watching real work: how long a new team takes to get to its first production deploy, how often users have to ask another team for a fact the platform should have told them, and what they ask during an incident.

Pick one common task and walk through it with a team that hasn't used the platform before. Then walk through one failure. Note every point where they stop to ask someone, and name the responsibility the platform should have taken on at that point. That list is your roadmap: keep the user-facing promise simple, and keep the operational owner explicit.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">The best platforms make complexity disappear.<br><br>Users shouldn’t need to understand your topology, storage model, failure domains, or scaling strategy.<br><br>Platform engineering isn’t about exposing infrastructure.<br><br>It’s about hiding the right complexity behind reliable contracts.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2092093975075418481?ref_src=twsrc%5Etfw">August 25, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
