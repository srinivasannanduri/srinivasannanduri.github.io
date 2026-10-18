---
title: "Alerts are a product, not a byproduct"
date: 2026-10-18 06:55:00 +0530
categories: [Observability]
tags: [observability, alerting, sre, slo, on-call]
description: "Most alerts are created as a side effect and owned by nobody. Treat them as a product, with users, a contract, an owner, a release process and quality metrics, and on-call gets quieter and more useful."
image:
  path: /assets/img/posts/alerts-are-a-product-cover.jpg
  alt: "Alerts are a product, not a byproduct."
---

Most alerts are created as a side effect of something else. A dashboard panel gets a threshold. An incident review ends with "add an alert so this never happens again". A new service copies the alert rules of the last one. Nobody owns the result, and over time the alert set describes what was worrying at the time each rule was written, not what users experience now.

The fix is a change of stance: treat alerts as a product. A product has users, a contract, an owner, a release process, quality metrics and a way to retire features. Alerts need all six.

![Alerts are a product, not a byproduct. Byproduct alerts flood a phone with notifications nobody owns; product alerts have an owner, a runbook and an SLO. Every alert needs a user, a contract, an owner, a review, a scorecard and an exit. Page on user pain, not machine state.](/assets/img/posts/alerts-are-a-product.png){: .infographic width="1122" height="1402" }

## Know who the user is

The user of a page is a person, often woken up, who has to decide what to do in the next five minutes. They need three things: what is broken for users, how bad it is, and what to do first.

That is why the SRE book insists that [every page should be actionable](https://sre.google/sre-book/monitoring-distributed-systems/), and why it separates three outputs of monitoring: pages for problems that need a human now, tickets for problems that can wait days, and logs for everything else. An alert that does not fit one of those is not yet a product. It is an unanswered question about what you are trying to protect.

## Write the contract into the rule

Every alert should carry the answers its user needs, in a form the pipeline can check:

```yaml
- alert: CheckoutErrorBudgetFastBurn
  expr: |
    (
      sum(rate(http_requests_errors_total{service="checkout"}[1h]))
        / sum(rate(http_requests_total{service="checkout"}[1h]))
    ) > (14.4 * 0.001)
    and
    (
      sum(rate(http_requests_errors_total{service="checkout"}[5m]))
        / sum(rate(http_requests_total{service="checkout"}[5m]))
    ) > (14.4 * 0.001)
  labels:
    severity: page
    service: checkout
    signal: availability
    team: payments
  annotations:
    summary: "Checkout is spending its 30-day error budget 14x too fast"
    runbook_url: https://runbooks.example.com/checkout/error-budget-burn
```

Two things matter here more than the query. The rule names its owner, its severity and its runbook. And it says nothing about *where* the alert goes. More on that below.

Make the contract mandatory. A lint step in CI can reject any rule without a severity, an owning team or a runbook link before it ever reaches production. When rules change only through reviewed pull requests, and nobody edits alerting configuration by hand, the alert set stays something you can reason about.

## Alert on user pain, not machine state

The rule above pages on a symptom users feel, failed checkouts, rather than on a cause such as high CPU or a full disk. Causes belong on dashboards for debugging; they page only when they reliably predict user pain.

The most useful symptom alerts are tied to a service level objective. Instead of "error rate above 1%", alert on how fast you are spending the error budget. The Google SRE Workbook's [guidance on alerting on SLOs](https://sre.google/workbook/alerting-on-slos/) gives sensible starting points: page when 2% of a 30-day budget burns in an hour (a burn rate of 14.4) or 5% burns in six hours, and open a ticket when 10% burns over three days. Pairing each long window with a short one, a twelfth of its length, means the alert stops soon after the problem does.

The effect is fewer pages, and each one is about something users would notice.

## Separate what an alert means from where it goes

Many alert sets hard-code a destination into each rule: this one posts to that channel, that one calls this webhook. It works until teams reorganise, a channel is renamed, or a service changes owners. Then routing becomes a search-and-replace across hundreds of rules.

A better split: alerts emit labels that describe meaning, such as service, component, severity, signal, team and region. A routing layer maps those labels to receivers. Teams change how they are reached without touching a single rule, and the same alert can reach a pager, a ticket queue and a chat channel based on severity.

This only works with a shared label vocabulary, enforced when rules are written rather than discovered when routing fails. Agree on the names once, put them in the lint, and treat a new label as a design decision.

## Make delivery reliable, and test it

An alert that evaluates correctly but never arrives is the worst kind of failure, because everything looks healthy. Two practices help.

First, decouple evaluation from delivery. Put a durable, at-least-once buffer between the component that decides an alert fired and the component that delivers it, so a slow or failing destination causes a retry with backoff rather than a lost page.

Second, test the whole path continuously. A heartbeat alert that always fires, and pages someone when it *stops* arriving, proves the pipeline is alive end to end. Periodic synthetic alerts injected at the source prove that routing still sends each kind of alert where it should go.

## Measure alerts like product quality

Products improve because someone looks at how they are used. Alerts rarely get that attention. A small set of questions, asked monthly, changes that:

- **Which alerts fire most?** The noisiest few usually account for most of the pages.
- **What fraction of pages led to action?** A page nobody acted on is a false positive with a human cost.
- **Which alerts have no runbook, or no owner?** That is a coverage gap, not a documentation gap.
- **Which alerts have not fired in a year?** Either the risk is gone or the rule is broken. Find out which.
- **How many incidents per on-call shift?** The SRE book's [on-call chapter](https://sre.google/sre-book/being-on-call/) sets a ceiling of two incidents per 12-hour shift. Above that, responders stop investigating and start silencing.

Store fired alerts as data, so these questions are queries rather than archaeology. Then act on the answers: tune thresholds, merge duplicates, demote pages to tickets, and delete what no longer protects anything. Deleting an alert is a feature.

## Ownership is the point

None of this is new tooling. It is ownership. Before an alert is merged, someone should be able to say who it serves, what it protects, what the responder does first, and how we will know if it is wrong. If nobody can, it is noise waiting to happen.

In your next design review, ask to see the alerts alongside the architecture, and ask who answers each one. It is one of the fastest ways to learn whether a system is ready for production.
