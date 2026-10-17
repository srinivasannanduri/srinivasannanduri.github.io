---
title: "Learn why the code works: invariants, boundaries and progress"
date: 2026-10-14 09:00:00 +0530
categories: [Engineering]
tags: [algorithms, mental-models, invariants, binary-search, engineering-judgment]
description: "Memorized code solves one problem. The reasoning behind it solves a class of problems. Binary search shows how, and the same three questions apply to pagination, backfills and control loops."
image:
  path: /assets/img/posts/mental-models-cover.jpg
  alt: "Learn why the code works."
---

Revisiting algorithms recently reminded me of a distinction that matters more the more senior you get. Memorized code gives you a solution. Understanding why it works gives you a mental model, and a mental model still holds when the problem changes.

Binary search is the cleanest example I know. The code fits in ten lines, almost everyone has written it, and it is still easy to get subtly wrong.

![Memorized code gives you one solution; mental models apply to classes of problems. Binary search illustrates three ideas: invariants, boundaries and progress. When mid is ruled out, exclude it so the search advances.](/assets/img/posts/mental-models.webp){: .infographic width="1122" height="1402" }

## Three questions behind every loop

Here is a standard exact-match search over a sorted array, using an inclusive interval:

```python
def find(a, target):
    low, high = 0, len(a) - 1          # candidates: a[low..high], inclusive
    while low <= high:                 # stop when no candidates remain
        mid = low + (high - low) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            low = mid + 1              # a[mid] is ruled out: exclude it
        else:
            high = mid - 1             # same on the other side
    return -1
```

Remembering `low = mid + 1` is easy. Explaining it takes three ideas:

- **Invariant.** What must stay true on every iteration? If the target exists, it lies within `a[low..high]`.
- **Boundaries.** Which ends are included? Here, both. That single choice decides the loop condition and both updates.
- **Progress.** What makes the remaining work smaller? Every iteration that does not return removes at least `mid` from the range.

Now break the progress rule. Search `[4, 9]` for `9`. The first midpoint is index 0, where the value is `4`. If the update is `low = mid` instead of `low = mid + 1`, the next iteration sees exactly the same range, and the loop never ends. You don't need a large test case to find this. You need the question "what got smaller?"

## The rule is "exclude what is ruled out", not "always exclude mid"

This is where memorization fails. Here is a lower-bound search, which finds the first position whose value is at least `target`:

```python
def lower_bound(a, target):
    low, high = 0, len(a)              # answer lies in [low, high), half-open
    while low < high:
        mid = low + (high - low) // 2  # rounds down, so mid < high
        if a[mid] < target:
            low = mid + 1              # mid is ruled out
        else:
            high = mid                 # mid may be the answer: keep it
    return low
```

Here `high = mid` is correct, because `mid` may still be the answer. It also still makes progress, because a rounded-down midpoint is always strictly less than `high`. Someone who memorized "always exclude mid" will break this version. Someone who reasons from the invariant and the interval convention will write both correctly, and will know not to mix them.

The midpoint line carries its own lesson. For years many binary searches, including the one in the Java standard library, computed `(low + high) / 2`, which overflows on very large arrays. Joshua Bloch [wrote it up in 2006](https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/). The loop logic was correct; an assumption about integer range was not. A mental model includes the assumptions as well as the logic. (Python's integers don't overflow, so the idiom matters in fixed-width languages.)

## Where the same questions show up in production

The same three questions apply well beyond sorted arrays:

- **Cursor pagination.** If the next page starts at `>= last_seen` instead of `> last_seen`, you return duplicates. If the cursor key is not unique, you skip records or stop advancing. That is a boundary and progress bug, the same class as binary search.
- **Backfills and migrations.** The invariant is "every record is either converted or still in the remaining set, never both or neither". Progress is how that set shrinks, and what happens to it when a batch fails halfway.
- **Reconciliation loops.** A controller converges only if each pass moves actual state toward desired state and repeating a pass is safe. Without both, it flaps or stalls.

In design and code review, I find it more useful to ask for the invariant than to debate an unfamiliar arrangement of indexes. "What must stay true, which ends are included, and what gets smaller?" gives both people something concrete to check.

## A habit worth building

After you get an algorithm working, close the editor and write a short explanation that doesn't rely on remembering the code. Then change one condition: duplicates, the first match instead of any match, an empty input. See which part of the explanation has to change.

If you can rebuild the implementation from that explanation, you have learned a class of problems, not one solution. The same holds for the systems you design.

## Where this started

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Revisiting algorithms reminded me of something important:<br><br>Memorizing code gives you a solution. Understanding why it works gives you a mental model.<br><br>Take Binary Search.<br><br>Remembering low = mid + 1 is easy.<br><br>Understanding why mid must be excluded—and how retaining it can cause an infinite loop—teaches you about invariants, boundaries, and progress.<br><br>That understanding extends far beyond binary search.<br><br>Code solves a problem. Mental models solve classes of problems.</p>&mdash; Srinivasan Nanduri (@snanduri_) <a href="https://x.com/snanduri_/status/2110217784336449609?ref_src=twsrc%5Etfw">October 14, 2026</a></blockquote>
<script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>
