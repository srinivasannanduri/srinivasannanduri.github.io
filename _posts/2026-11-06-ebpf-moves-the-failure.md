---
title: "eBPF moves the failure, it doesn't remove it"
date: 2026-11-06 08:00:00 +0530
categories: [Observability]
tags: [observability, ebpf, linux, resilience, sre]
description: "Choosing between a kernel module and an eBPF collector isn't a question of what each can see. It's a question of what fails, when, and who pays. eBPF is the better default, but only if you design for the failures it keeps."
---

A node collector is the one part of an observability stack that shares a failure domain with everything it watches. Run it in the kernel and that domain is the node. Roll it out everywhere and it's the fleet.

So when teams compare kernel modules and eBPF, I'd skip the feature matrix. Both can see syscalls, scheduling and network events. [Falco](https://falco.org/docs/concepts/event-sources/kernel/), for one, offers both as drivers for the same job. The useful question is what each one does on a bad day.

eBPF is the better default. But the case for it is usually made as "it's safe", and that's the wrong mental model. eBPF doesn't remove failure. It moves it, and each new location needs an owner.

## What the verifier buys

A kernel module is trusted code. It runs with the kernel's full privileges, nothing proves it safe before it runs, and a bad pointer can panic the node.

An eBPF program has to pass the verifier first, which checks that it terminates and that its memory access stays in bounds. If it can't prove that, the program doesn't load.

| | Kernel module | eBPF program |
|---|---|---|
| Checked before it runs | Signature, if enforced | Verifier must accept it |
| Its own bug at run time | Can panic the node | Refused at load, in the normal case |
| Tied to | The kernel it was built against | BTF, ring buffer and available hooks |
| Ships as | A build per kernel | One object, adjusted at load by [CO-RE](https://docs.kernel.org/bpf/libbpf/libbpf_overview.html) |
| On Secure Boot hosts | Must be signed | No module to sign, but policy may still restrict it |

That second row is the real trade. A failure at run time, on every node at once, becomes a failure at load time, on the nodes that don't qualify. A collector that refuses to load is a visibility gap. A collector that panics a node is an outage, caused by the tool you bought to see outages.

I'll take that trade every time. But four failures stay behind.

## Cost lands on someone else

The verifier proves a program stops. It doesn't prove the program is cheap.

A program on a syscall tracepoint runs in the thread that made the syscall, so the application pays and the collector's own CPU limit doesn't apply. I tested this on a small Linux VM with `dd` at `bs=1`, which is deliberately close to a worst case at about five million syscalls a second, and the smallest useful probe:

```text
tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }
```

| | Per run |
|---|---|
| No probe | 1.14s |
| Probe attached | 1.35s (about 19% slower) |
| Probe attached, BPF stats on | 1.58s (about 38% slower) |

Over seven runs that added about 1.5 seconds to the workload. The collector's container, capped at 5% of a CPU, used under 2 milliseconds. A real collector does more work in user space, but none of the cost above would show up there.

Real services make far fewer syscalls, so don't read 19% as your number. Read the shape: a collector's cost is cost per event times event rate, and it's billed to the workload. That's the same pattern as [a metric label](/posts/every-label-is-a-bill/), where the person who adds the cost isn't the one who pays it.

## Loss is silent by default

Kernel programs usually hand events to user space through a ring buffer. If the consumer falls behind and the buffer fills, [the reservation simply fails](https://docs.kernel.org/bpf/ringbuf.html). It can't block, because the kernel won't wait for your collector.

That's the right design for the kernel, and it means your data has holes exactly when the node is busiest. For metrics that's a blurry graph. For a security audit trail it's a gap someone could cause on purpose. Count your drops, and [alert on them](/posts/alerts-are-a-product/) like you'd alert on the service itself.

## The kernel contract is narrower than it looks

Kprobes and tracepoints feel like an API, but the [kernel's BPF design notes](https://docs.kernel.org/bpf/bpf_design_QA.html) are clear that neither is stable: both follow internal details that can change between releases. The same notes say the only way to know the verifier will accept a program is to try loading it.

CO-RE helps a lot here, since it handles moved struct fields. It can't help when a function is renamed or inlined, or when a field keeps its name and changes its meaning. The worst case isn't a failed load. It's a probe that attaches happily and quietly reports the wrong thing.

So a kernel upgrade is a collector change, even if nobody touched the collector.

## Verified doesn't mean harmless

The verifier is kernel code, and the kernel beneath it can have bugs. In 2024, Red Hat warned of panics on RHEL 9.4 involving the CrowdStrike Falcon sensor. [The Register reported](https://www.theregister.com/2024/07/21/crowdstrike_linux_crashes_restoration_tools/) that the cause was a kernel bug involving BPF, and that it hit the sensor's user-level BPF code, not its kernel-level code. That's a useful correction to "eBPF can't crash the kernel". It's far less likely, not impossible.

It also doesn't make the loader trustworthy. Per the same design notes, tracing programs can read arbitrary kernel memory through helpers. Loading them takes real privilege, so treat an eBPF collector as a privileged workload with its own threat model. The verifier checks that a program is safe to run, not that it's honest.

## When a module still earns its place

Modules aren't obsolete. Falco's modern probe generally expects kernel 5.8 or later with ring buffer and BTF support, and plenty of long-lived fleets don't have all of that yet.

If you need one, make it a named exception: an owner, a signed build for each kernel you run, and an exit date tied to the OS upgrade. An out-of-tree module also [taints the kernel](https://docs.kernel.org/admin-guide/tainted-kernels.html), so check what that does to your vendor support.

Beware of one design in particular: falling back to a module automatically when eBPF won't load. It sounds resilient, but it means the nodes that failed your safety checks are the ones that get the riskier driver. Fail to a visible gap, and make the fallback a human decision.

## Questions for any node-level collector

Before approving one, I'd want answers to these:

1. **What runs in kernel context, on which paths?** Estimate cost per event times event rate, on your busiest workload, not the average one.
2. **What happens on a kernel it hasn't been tested on?** Refusing to load is fine. Loading and misreporting isn't.
3. **What tells you a node has gone blind?** A failed load, a detached probe and dropped events each need a signal from outside the collector.
4. **What does it do when eBPF won't load?** If the answer is a silent fallback, change it.
5. **How does a change reach the fleet?** Stage by kernel version, and test collector and kernel upgrades against each other.

That last one includes changes that don't look like code. CrowdStrike's [own review of the July 2024 Windows crashes](https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/) traced them to a content update, and its fixes included canary deployment for that content. Anything that feeds the kernel gets a staged rollout, whatever you call it.

## Try this on your own nodes

These work on a recent Linux host with `bpftool` installed:

```bash
# Does this node meet the usual modern eBPF needs?
uname -r
ls -l /sys/kernel/btf/vmlinux

# Has an out-of-tree module been loaded since boot? 1 means yes.
echo $(( $(cat /proc/sys/kernel/tainted) >> 12 & 1 ))

# What is running in your kernel right now?
sudo bpftool prog show

# What is it costing? Check run_time_ns and run_cnt, then turn this off.
sudo sysctl -w kernel.bpf_stats_enabled=1
sudo bpftool prog show | grep run_time_ns
sudo sysctl -w kernel.bpf_stats_enabled=0
```

Don't skip that last line. [The stats have a cost of their own](https://docs.kernel.org/admin-guide/sysctl/kernel.html), and as the table above shows, it can be as large as the thing you're measuring.

Then read the `bpftool prog show` list. Most teams can't name everything on it, and every entry is running in the one place all your workloads share.
