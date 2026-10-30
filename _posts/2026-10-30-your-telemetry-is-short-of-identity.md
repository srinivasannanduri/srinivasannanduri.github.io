---
title: "Your telemetry is short of identity, not volume"
date: 2026-10-30 14:52:00 +0530
categories: [Observability]
tags: [observability, opentelemetry, aiops, data-quality, sre]
description: "When logs, metrics and incidents each name the same service differently, no dashboard or AI agent can join them. Before adding another signal, give every signal the same identity, and write it once, at the edge."
---

Most observability programs respond to a hard incident the same way: collect more. More logs, finer metrics, longer retention. But in the incidents I've learned most from, the data was usually there. What was missing was a way to connect it.

Here's the same running service, as three systems see it:

```text
logs:      {app="checkout"}
metrics:   {job="checkout-api", instance="10.2.3.4:8080"}
incident:  CI "Checkout Service (PROD)", record 7f3a91c2
```

A person can look at those and say "same thing". That person is the join key, and during an incident they're doing the integration work by hand, across three browser tabs, at the worst possible time.

Most operational data isn't short of volume. It's short of identity.

## AI doesn't fix a missing key

It's tempting to assume an AI agent will bridge the gap. It can read all three, after all, and "checkout" looks a lot like "checkout-api".

That works until it doesn't. Fuzzy matching will happily connect `checkout` to `checkout-worker`, or to the staging deployment, and it'll present the result with the same confidence as a correct answer. The output looks plausible, varies from run to run, and on-call engineers stop trusting it. No amount of model capability recovers a join key that was never written.

I've argued before that [AI should reason over observability](/posts/ai-reasons-over-observability/) rather than replace it, and that [relationships matter as much as documents](/posts/better-agents-need-better-context-architecture/). Both depend on this much duller layer. Correlation should be a lookup, not a guess.

## Pick one vocabulary

The first decision is which names to use, and you shouldn't invent them. [OpenTelemetry's semantic conventions](https://opentelemetry.io/docs/concepts/semantic-conventions/) already define them:

```text
service.name                 = checkout
service.namespace            = payments
service.version              = 2.14.1
deployment.environment.name  = production
cloud.region                 = us-east-1
```

The point isn't that these names are perfect. It's that every signal uses the same ones. Logs, metrics and traces carry them as resource attributes, so the identity belongs to whatever produced the signal, not to each query that reads it. Add trace context to logs and exemplars to metrics, and you can move from a spike on a graph to the request behind it.

Keep identity bounded. `service.name` is a small, stable set, so it's safe as a metric label. A request ID or user ID isn't; put those on events and traces, where high cardinality is affordable.

## Write it once, at the edge

The next decision is where identity gets attached. There are two options, and they age very differently.

Resolving at query time feels cheap. Each dashboard, alert and agent keeps its own mapping from local names to services. But each consumer then reimplements the same fragile logic, the copies drift, and a rename breaks them all quietly.

Resolving at ingest costs more up front and then stops costing. The collector enriches every signal with canonical attributes before it lands anywhere, so everything downstream simply inherits them. It's also the kind of decision that [gets more expensive to reverse](/posts/price-the-reversal/) with time. Adding a key while you're designing the pipeline costs almost nothing. Adding it after every service has onboarded is a re-instrumentation program.

The same applies beyond telemetry. Deployments are usually the first thing you want to correlate during an incident, so change events need the key too. So do alerts, and tickets should inherit it from the alert that opened them. This is another reason to treat [alerts as a product](/posts/alerts-are-a-product/): an alert's labels are part of its contract.

## Give the mapping an owner

Legacy systems won't all adopt a new vocabulary, and a configuration database has its own record IDs. You need one authoritative place that maps each system's local identifier to the canonical key: a service catalog.

It earns its keep if a few things are true:

- **It's generated, not hand-maintained.** Populate it from deployment metadata where you can. A catalog that depends on people remembering to update it will be wrong by next quarter.
- **It separates the stable ID from the display name.** Services get renamed, split and merged. History needs to survive that.
- **It carries more than names.** Owner, tier and dependencies turn a list of services into something an incident responder or agent can traverse.

## Treat missing identity as a defect

Conventions decay unless something enforces them. A signal without a resolvable identity is a data-quality bug, and it should be tracked like one.

Don't drop those signals, because they may be the only evidence of a problem. Don't let them through unlabeled either, or they'll quietly erode every join. Route them to a quarantine stream or tag them as unresolved. That queue becomes an honest burn-down list for the long tail of older workloads. OpenTelemetry helps here: when `service.name` isn't set, SDKs use a value starting with `unknown_service`, so searching for that prefix is a useful first query.

Then publish the coverage: the share of logs, metrics, alerts and incidents that resolve to a known entity, per signal and per team. It's an unglamorous number, but it predicts how much you can trust everything built on top of it.

## Try this on your last incident

Here's a quick test. Open the ticket from your last incident and try to reach the service's logs, metrics and most recent deployment without translating a single name in your head. Use the keys in the data, nothing else.

If you can, your telemetry has an identity, and more data might really help. If you can't, adding another signal will only give you one more thing to join by hand. Fix the key first. It's a small schema decision that everything else depends on.
