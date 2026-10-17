---
title: "Price the reversal: not all technical debt is equal"
date: 2026-10-17 18:00:00 +0530
categories: [Architecture]
tags: [technical-debt, api-design, architecture, design-review, engineering-judgment]
description: "Before GA, the useful question is not whether a decision can be fixed later, but what it will cost to reverse once others depend on it."
image:
  path: /assets/img/posts/technical-debt-and-tradeoffs-cover.jpg
  alt: "Price the reversal: technical debt is not all equal."
---

"We can fix it later" is true of almost every engineering decision. It says nothing about the price.

We tend to keep technical debt in a single ledger. It belongs in two. Some debt sits behind an interface you own: you repay it on your own schedule, and nobody outside the team notices. Other debt leaks into a contract, such as an API shape, an identifier format, an error code, a default or a stored record. From GA onward, repaying that debt needs the time and cooperation of everyone who built on it.

![Two kinds of technical debt on a scale: deferred optimization creates a performance cost, while deferred API or data model decisions create a compatibility cost. Make trade-offs explicit. Before GA, ask how expensive the decision will be to reverse.](/assets/img/posts/technical-debt-and-tradeoffs.webp){: width="1122" height="1402" }

## Two ledgers

**Encapsulated debt** is a slow query, a missing cache, a naive retry loop. The cost is performance or operational toil, your team pays it, and the fix ships behind the same interface. Its reversal cost stays roughly flat over time.

**Contractual debt** is the resource model, the meaning of an identifier, pagination behaviour, the error taxonomy, the schema of data you persist. The cost is compatibility, your consumers pay it, and the fix needs a migration, a period of dual support, or both. Its reversal cost grows with every integration and every stored record.

That growth is what teams underprice. [Hyrum's Law](https://www.hyrumslaw.com/) states it plainly: with enough users, every observable behaviour of a system will be depended on by somebody. After GA, your contract is no longer what you documented; it is what clients observed. Google's [AIP-180](https://google.aip.dev/180) says the same thing formally. Renaming a component is equivalent to removing it and adding a new one, and code written against an earlier version must keep receiving what most reasonable developers would expect.

## A worked example

A service is preparing for GA with two open decisions.

The first is a caching layer the team wants to defer, because launch load fits without it. That is a fair deferral. Write down the load at which it stops being fair, alert on it, and name an owner.

The second is whether a resource identifier should encode the customer's current region. It looks like a convenience. But identifiers end up in scripts, audit logs, billing exports and other teams' databases. When a customer moves region, you either change what the identifier means or keep one that is no longer true. Reversing the choice later means a migration across systems you do not own.

Both get described as "debt we'll take for launch." Only one should pass a GA review without a written answer.

## Put the price on the decision record

For every decision deferred at GA, I ask for four lines in the decision record or launch review:

1. **Who depends on it?** Only our code, or customers, partner teams and stored data?
2. **Can we change the implementation without changing the contract?** If yes, it is encapsulated: set a trigger and move on.
3. **What would reversal take?** A new API version, a dual-read period, a backfill, a deprecation window, and roughly how long each would run.
4. **What signal makes us revisit it, and who owns that?**

This turns "we can fix it later" into a statement a reviewer can accept or reject: "Reversing this means supporting both formats for two release cycles, and the storage team owns the backfill."

## Lower the price before you ship

When a contractual decision cannot be settled before GA, you can still make it cheaper to reverse:

- **Keep meaning out of the contract.** Use opaque identifiers rather than meaningful ones, and server-side defaults rather than client-visible ones.
- **Label what is not final.** Ship it as a preview or beta with a stated compatibility promise.
- **Version from day one,** so that a second version is routine work rather than an emergency.
- **Measure usage,** so you know who depends on a field before you decide to change it.

## A lens, not a goal

None of this argues for maximum optionality. Abstractions and extension points added just in case carry their own cost, and they are debt too. Reliability, performance, simplicity and flexibility still have to be traded against each other. Reversal cost is one more column in that trade-off, and it is the one most often left blank.

In your next design review, pick one deferred decision and write down its repayment path. If that path runs through someone else's code or your persistent data, it needs attention before release, not after.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Not all technical debt is equal.<br><br>A deferred optimization may cost performance.<br><br>A deferred API contract or data model decision may cost years of compatibility.<br><br>Before GA, ask not just “Can we fix this later?” but “How expensive will it be to reverse?”</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2109451438103683304?ref_src=twsrc%5Etfw">October 12, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
