---
title: "Introducing Rakuen Software"
date: 2026-07-22
author: Rakuen Software
tags: [announcement]
excerpt: "What we build, and why the appliances share a kernel, an installer and a component library instead of each maintaining their own."
---

We build Linux appliances and the tooling that goes with them.

`SmoothNAS` is a storage appliance running mdadm, LVM and ZFS. `SmoothFS` is the
stacked kernel filesystem that gives it tiering behind a single mount. `nonraid`
implements Unraid-style parity arrays in Go. `SmoothRouter` is a Debian router
administered from a browser. `aimee` is a local server that gives AI coding tools
persistent memory, a map of your code, cheap delegate models and guardrails they
cannot write past.

Three more exist so the others can: `SmoothGUI` is the shared React component
library, `SmoothISO` builds the installer ISOs, and `SmoothKernel` builds the
kernel.

## The tools stay reachable

SmoothNAS drives mdadm, LVM and ZFS. SmoothRouter drives nftables and dnsmasq.
These are the actual tools, configured by the appliance and still there when you
SSH in. If the UI cannot do what you need, you have a shell and a system you
recognise.

That matters most when something breaks. Recovering a hidden storage stack by
hand starts with working out what it did to your disks.

## Shared foundations

Four flavours need an installer and a kernel. Maintaining four of each would
guarantee they drift.

- `SmoothKernel` builds one kernel line into Debian packages. Every flavour
  installs the same one, so driver coverage and firmware baselines match.
- `SmoothISO` builds installer ISOs for any product. Products supply hooks;
  nobody forks the builder.
- `SmoothGUI` is one component library across every console, every installer and
  this site.

Flavour differences stay in userspace, where they are cheap: udev rules, sysctls,
tuned profiles, packages, services and UI.

## What is public

`smoothnas`, `smoothfs`, `nonraid`, `smoothgui`, `smoothiso`, `smoothkernel` and
`aimee` are all on [GitHub](https://github.com/RakuenSoftware). SmoothRouter is
running in production here but is not public yet.
