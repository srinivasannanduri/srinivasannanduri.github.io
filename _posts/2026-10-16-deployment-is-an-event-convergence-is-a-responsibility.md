---
title: "Deployment is an event. Convergence is a responsibility."
date: 2026-10-16 09:00:00 +0530
categories: [Platform]
tags: [gitops, devops, sre, kubernetes, platform-engineering]
description: "A pipeline and a GitOps controller can both deploy and both enforce desired state. The real difference is who keeps the environment converged between deployments, and how quickly."
image:
  path: /assets/img/posts/deployment-and-convergence-cover.jpg
  alt: "Deployment is an event. Convergence is a responsibility."
---

A deployment pipeline answers one question: *how do we apply this change?* A GitOps controller answers another: *does the environment still match what we declared?*

Teams often compare the two by asking which one can deploy. Both can. Both can enforce desired state, too. The useful architectural question is a different one: **who is responsible for bringing the environment back to its declared state, and when?**

![Deployment is an event; convergence is a responsibility. A deployment pipeline asks how to apply a change: build and package, test and validate, deploy to an environment. A GitOps controller asks whether the environment still matches declared intent, in a continuous loop. Both can deploy and enforce desired state. The distinction is who ensures convergence, and when.](/assets/img/posts/deployment-and-convergence.webp){: .infographic width="1122" height="1402" }

## An event and a loop

A pipeline is event-driven. Something triggers it, it applies a change, it reports success, and it stops. Its green tick describes the environment at one moment.

A controller is a loop. The Kubernetes documentation describes a [controller](https://kubernetes.io/docs/concepts/architecture/controller/) as a non-terminating control loop, like a thermostat: it keeps comparing the actual state with the desired state and acts on the difference. [OpenGitOps](https://opengitops.dev/) makes this one of its four principles: desired state is declarative, versioned and immutable, pulled automatically, and *continuously reconciled*, meaning agents keep observing actual state and attempt to apply the desired state. "Attempt" matters. A loop that is running is not the same as a loop that is succeeding.

The labels don't settle the question. A pipeline that runs a scheduled drift check is partly a loop. A GitOps tool may not correct drift at all unless you turn that on: in Argo CD, for example, [changes made directly to the live cluster do not trigger an automated sync by default](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/). Self-healing is a separate setting. So look at the actual loop and its authority, not the name of the tool.

## The time between deployments

Take a service whose declared configuration says three replicas. A release leaves it at three. During an incident, someone scales it to six by hand and doesn't change the declaration afterwards.

What happens next depends entirely on who owns convergence:

- **Pipeline only:** the environment stays at six until the next release, which might be weeks away. Then a routine deployment silently reverts the hand-made fix, and the next incident starts with a surprise.
- **Controller without self-heal:** the resource is flagged as out of sync, but stays at six. Someone has to notice and decide.
- **Controller with self-heal:** it goes back to three within minutes, possibly in the middle of the incident the change was meant to fix.

None of these is automatically right. Each is a decision about who acts on drift and how fast. The mistake is not making that decision on purpose.

## Decide what the controller owns

Restoring declared state only helps when the declaration is the real source of intent. When two writers own the same field, you get a fight instead of convergence.

The classic case is a Deployment with `replicas: 3` in Git and a Horizontal Pod Autoscaler scaling it to ten. The autoscaler raises it, the GitOps controller puts it back, and the service flaps. Kubernetes' own [autoscaling guidance](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) is to remove `spec.replicas` from the manifest once an autoscaler is enabled. The general rule: give every field exactly one owner. [Server-side apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/) helps by recording which manager owns each field and reporting a conflict when another one tries to change it.

Emergency changes need a defined path as well. Who may pause reconciliation? Where is the change recorded? Does the fix get committed to the declaration, or deliberately reverted once the incident is over? An undocumented live edit is drift that someone will rediscover the hard way.

## Watch the loop, not just the pipeline

A controller can lose permissions, crash, or retry an invalid manifest forever while its dashboard says "running". A green pipeline from last Tuesday tells you nothing about the environment today.

Treat reconciliation as something with its own health signals: time since the last successful sync, how long resources have been out of sync, and the count of reconcile errors. Alert on "not converging" the same way you would alert on "not serving". It's the same idea as progress in any loop: if nothing gets closer to the goal, the loop is stuck. I wrote about that in [Learn why the code works](/posts/learn-why-the-code-works/).

## Write down who owns convergence

A short ownership table often reveals what a deployment diagram hides:

| Resource | Source of intent | Reconciled by | When | On drift | Failure signal |
|---|---|---|---|---|---|
| Container image | Git (app repo) | GitOps controller | Continuously, self-heal on | Revert | Sync failing for 15 min |
| Replica count | Autoscaler policy | Autoscaler | Continuously | Not managed by GitOps | Autoscaler at its maximum |
| DNS record | Terraform | Pipeline | Nightly plan | Alert, no auto-apply | Plan shows changes |

The rows are illustrative; yours will differ. What matters is that every important resource has an answer in every column.

For your next delivery review, trace one resource from a declared change through a later drift event. The answer should say who notices, who acts, and who finds out if the correction fails. That is where responsibility for convergence stops being a slogan and becomes a design.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">A deployment pipeline answers: “How do we apply this change?”<br><br>A GitOps controller answers: “Does the environment still match our declared intent?”<br><br>Both can deploy. Both can enforce desired state.<br><br>The distinction isn’t deployment capability.<br><br>It’s who ensures convergence—and when.<a href="https://twitter.com/hashtag/DevOps?src=hash&amp;ref_src=twsrc%5Etfw">#DevOps</a> <a href="https://twitter.com/hashtag/SRE?src=hash&amp;ref_src=twsrc%5Etfw">#SRE</a></p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2110897084287381788?ref_src=twsrc%5Etfw">October 16, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
