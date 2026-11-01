---
title: "Every label is a bill"
date: 2026-11-01 17:15:00 +0530
categories: [Observability]
tags: [observability, metrics, prometheus, cardinality, sre]
description: "A metric label looks like a field but behaves like a multiplier, and the engineer who adds it rarely pays for it. Here's what a time series really costs, and how to give teams a cardinality budget."
---

Adding a label to a metric takes one line of code. It passes review, the tests stay green, and the dashboard gains a useful filter. Weeks later the metrics platform is slower, a dashboard times out and alerts fire late. Nobody connects the two, because the person who added the label isn't the person who pays for it.

That's the real problem with metric cardinality. High-cardinality data isn't bad. But a label looks like a field and behaves like a multiplier, and the bill lands on someone else.

## A label multiplies

Every unique combination of label values is its own time series. The [Prometheus naming guide](https://prometheus.io/docs/practices/naming/) warns about this directly, because the consequence is easy to miss: a series count is a product, not a sum.

Take a latency histogram on a single service. These numbers are invented, but the arithmetic is not:

| Dimension | Values | Series so far |
|---|---|---|
| Histogram (12 buckets, plus `_sum` and `_count`) | 14 | 14 |
| `route` | 40 | 560 |
| `status` | 5 | 2,800 |
| `pod` | 30 | 84,000 |
| `customer_id` | 2,000 | up to 168,000,000 |

Not every combination occurs, so the real number will be lower. But look at what the last row changes. Every earlier dimension grows with your code and your deployment. `customer_id` grows with your success. A label that was harmless on launch day becomes an incident in your best quarter.

Prometheus's [instrumentation guidance](https://prometheus.io/docs/practices/instrumentation/) is stricter than most teams assume: keep a metric's cardinality below 10 as a general guideline, and look for an alternative if it could grow past 100.

## Where the bill arrives

Storage is the line item people check first, and it's usually the smallest. Prometheus [averages 1–2 bytes per sample](https://prometheus.io/docs/prometheus/latest/storage/) on disk. The cost shows up elsewhere:

- **Ingestion.** Every scrape parses, hashes and appends every series, even when the value hasn't changed.
- **Memory.** Each active series holds its labels and recent samples in memory. Plan on the order of a few kilobytes per series, then measure your own.
- **Queries.** Work scales with the series a query touches. `sum(rate(...))` reads the same over ten thousand series as over a million. It doesn't cost the same.
- **Alert evaluation.** Rules are queries on a schedule, so slow queries become [late alerts](/posts/alerts-are-a-product/).
- **Restarts.** Replaying the write-ahead log takes longer as active data grows.

Disk is rarely what fails first. Queries and memory usually go before it. A metrics system at its limit rarely crashes outright. It gets brittle: it's up, but dashboards crawl, alerts lag, and a small config change becomes risky.

Point-in-time counts also hide churn. A `pod` label on a service that redeploys daily creates a fresh set of series with every rollout. The old series stop receiving samples, but they stay in storage for the retention period, and any long-range query still has to touch them. Your active series stay flat while the total keeps climbing. Track both.

## Who pays is a design problem

The engineer adding a label gets all of the benefit and shares the cost with everyone on the platform. In a shared system, one team's accidental explosion can slow another team's alerts.

Asking people to be more careful doesn't fix that incentive. Showing the cost to the person making the decision does. That's what a budget is for.

## Give every team a budget

A cardinality budget is a number of active series per team or service, owned by that team and visible to it. It needs three things to work.

**Make the spend visible.** Start with what each metric costs. These queries work on any Prometheus, and the TSDB status API (`/api/v1/status/tsdb`) gives you the same view without a heavy query:

```text
# Top 10 metrics by series count
topk(10, count by (__name__) ({__name__=~".+"}))

# How many values does this label really have?
count(count by (route) (http_request_duration_seconds_count))
```

**Review at the source.** Four questions catch most problems when a label is added:

1. Is the set of values bounded and known? IDs, raw paths, email addresses and free text aren't.
2. Will someone aggregate or alert on it, or is it only for debugging one request?
3. Does it grow with customers or traffic rather than with code?
4. What's the multiplied total across every replica?

**Enforce at the edge.** Reviews miss things, so the platform needs a backstop:

```yaml
scrape_configs:
  - job_name: checkout
    sample_limit: 20000
    label_limit: 30
    static_configs:
      - targets: ["checkout:8080"]
    metric_relabel_configs:
      - regex: customer_id
        action: labeldrop
```

`sample_limit` is deliberately loud: if a target goes over, Prometheus fails the whole scrape. That protects the platform, but it turns a cardinality bug into a monitoring gap for that target. So alert before the limit, on `scrape_samples_post_metric_relabeling`, and give the owning team time to act. Multi-tenant metrics backends offer the same idea as per-tenant series limits.

## Put the dimension where it belongs

None of this means you should throw detail away. High cardinality is exactly what you want when debugging. It's just expensive in a store built for aggregates. Metrics answer "how many, how fast, is it getting worse?" cheaply because they've already discarded identity. Logs and traces keep it.

So most high-cardinality labels have a better home:

- **`customer_id`:** put it on spans and structured logs. If you need it in metrics, use a small bounded label like `tier`.
- **`/users/123`:** record the route template, `/users/{id}`, never the raw path.
- **`request_id`:** never a label. An exemplar links a metric sample to a trace without creating a series, though Prometheus keeps exemplar storage behind a feature flag.
- **`pod`:** keep it on short-lived infrastructure metrics, and use a recording rule such as `sum without (pod) (rate(...))` for dashboards that look back further.

The same test applies to [identity labels](/posts/your-telemetry-is-short-of-identity/). `service.name` is a small, stable set, which is why it's safe everywhere.

## Try this on your own metrics

Run the first query above and look at your top ten metrics. For each one, ask who wanted those labels and what decision they drive.

A handful of metrics usually accounts for a large share of the total, and at least one label in them will have no answer. Drop it. It's the cheapest capacity you'll ever buy.
