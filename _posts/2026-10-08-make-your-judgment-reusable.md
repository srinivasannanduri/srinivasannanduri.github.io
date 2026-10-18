---
title: "Make your judgment reusable"
date: 2026-10-08 09:00:00 +0530
categories: [Leadership]
tags: [leadership, technical-writing, architecture, engineering-judgment, decision-making]
description: "A senior engineer's impact isn't measured by the code they write but by how many difficult decisions become simpler because they were involved. That scales only when judgment is written down in a form others can use."
image:
  path: /assets/img/posts/reusable-influence-cover.jpg
  alt: "Make your judgment reusable."
---

The impact of a senior engineer isn't measured by how much code they write. It's measured by how many difficult decisions become simpler because they were involved.

That kind of impact has a ceiling if it only happens in conversation. One person can only join so many meetings. Technical influence scales when knowledge becomes reusable: clear principles, documented decisions, reference architectures, and engineers empowered to apply them on their own. Great engineers solve problems. Great technical leaders improve the quality of decisions across the organization.

![Make your judgment reusable. Write it simply and expose gaps in understanding. Writing feeds four things: clear principles, documented decisions, reference architectures and empowered engineers. Senior impact: difficult decisions become simpler.](/assets/img/posts/reusable-influence.webp){: .infographic width="1122" height="1402" }

## Writing is the cheapest design review

Writing is the cheapest way to find out whether you understand your own architecture. If you can't explain it simply in a post, the design probably needs work.

That isn't a point about prose style. A diagram lets you draw an arrow between two boxes without saying what happens when the call fails, who owns the data, or why the arrow points that way. A paragraph doesn't. Leslie Lamport puts it well: if you think without writing, you only think you're thinking. The sentence you can't finish is usually where the design has a gap.

So before the diagram, write one page: what this design is for, the two or three decisions that shape it, what it deliberately does not do, and how it fails. If that page is hard to write, you have found the next thing to work on, cheaply, before anyone builds on it.

## Start with the question you keep answering

The best candidate for reusable judgment is a question you've answered three times this quarter. Say teams keep asking whether a new feature needs a synchronous call to another service.

You could review every case. Or you could write down the factors you actually weigh: what the user needs to see immediately, how the feature behaves if the other service is slow, what consistency it really requires, and the cost of adding one more dependency to the request path. Add one worked example where those factors led to a synchronous call, and a contrasting one where they didn't. Now the team has a way to reason, not a slogan to apply.

Will Larson makes the same move at a larger scale in [Good engineering strategy is boring](https://lethain.com/good-engineering-strategy-is-boring/): write five design docs, then pull out what they have in common. Strategy built from real decisions is grounded in a way that strategy written from scratch rarely is.

## Four forms of reusable judgment

Each of the four forms in the infographic needs its boundaries written down, or it turns into either a slogan or a mandate:

- **Clear principles.** "Keep the request path simple" is incomplete. Say what it protects, what trade-off it accepts, and which conditions would justify breaking it.
- **Documented decisions.** Record the alternatives and the assumptions that mattered at the time, so a future reader can tell when changed conditions make the decision worth revisiting. Lightweight decision records do this well; I wrote about routing and recording decisions in [Let risk choose the review](/posts/let-risk-choose-the-review/).
- **Reference architectures.** Mark what is required, what is illustrative, and what the consuming team must decide for itself. Otherwise a helpful example quietly becomes a mandatory design nobody intended.
- **Empowered engineers.** The documents only matter if people are trusted to use them: clear ownership, permission to decide within the boundaries, and an escalation path for when they're unsure.

## Test it on someone else

A document that only works when its author explains it isn't reusable yet. Give it to an engineer who wasn't in the original discussion and ask them to apply it to a new case. Watch where they have to come back and ask. That point is missing context, an ambiguous term, or an exception the document never mentions.

Fix it, and name who maintains it. Reusable judgment has to evolve as the system and its constraints change, or it becomes confident, outdated advice.

## Measure by decisions made simpler

You can see whether this is working. The same question stops arriving in your inbox. Teams make sound decisions faster, explain the trade-off in their own words, and recognize when to escalate. Your principles start showing up in other people's design docs, cited rather than copied.

The measure of influence is partly what becomes possible without another meeting with you.

Pick one question you answered more than once recently. Write a page that explains your reasoning, its limits and one example. Then let someone use it while you watch. It's a small experiment, and it turns individual experience into a capability the whole team shares.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Writing is the cheapest way to find out whether you understand your own architecture. If you can&#39;t explain it simply in a post, the design probably needs work.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2108058951107666042?ref_src=twsrc%5Etfw">October 8, 2026</a></blockquote>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">The impact of a senior engineer is not measured by how much code they write.<br><br>It’s measured by how many difficult decisions become simpler because they were involved.<br><br>Great engineers solve problems.<br>Great technical leaders improve the quality of decisions across the organization.<br><br><a href="https://twitter.com/hashtag/EngineeringMusings?src=hash&amp;ref_src=twsrc%5Etfw">#EngineeringMusings</a></p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2098617936483357085?ref_src=twsrc%5Etfw">September 12, 2026</a></blockquote>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Technical influence scales when knowledge becomes reusable: clear principles, documented decisions, reference architectures, and engineers empowered to apply them independently.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2097189923396976801?ref_src=twsrc%5Etfw">September 8, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
