---
title: "SmoothGUI 0.9 adds site and long-form components"
date: 2026-07-22
author: Rakuen Software
tags: [release, smoothgui]
excerpt: "The library that builds our appliance consoles now builds public pages too. This website is the first thing shipped with it."
---

SmoothGUI started as the console vocabulary for SmoothNAS: `AppShell`, `Panel`,
`DataTable`, `Wizard`. Everything you need to administer an appliance, and
nothing you need to explain one.

0.9.0 adds the other half.

## What is new

`SiteHeader` and `SiteFooter` for page chrome. `Hero`, `Section` and
`CallToAction` for structure. `FeatureGrid`, `FeatureCard` and `Card` for content
grids. `Prose` for rendered markdown and `ArticleCard` for listings. `CodeBlock`
has a copy button and no syntax-highlighting dependency.

There are new dark-band and content-width tokens too, so a hero and a footer
share one definition of "dark surface" instead of inventing it twice.

## Routing stays your business

Navigational components have to emit links, but a component library has no
business deciding how you route. SmoothGUI does not import a router. The
components take an optional `linkComponent` instead:

```tsx
const RouterLink: LinkComponent = ({ href, ...rest }) => <Link to={href} {...rest} />;

<SiteHeader brand={<span>Rakuen Software</span>} items={NAV} linkComponent={RouterLink} />
```

Pass nothing and you get plain anchors, which is what a static page wants. Pass
an adapter and you get client-side navigation.

## Upgrading

Every existing export is unchanged. It is a purely additive release, so
consumers move to 0.9.0 without edits.

The same library now ships the appliance console, the installer that runs before
the appliance exists, and this website. Building a public site out of a console
library found every place we had quietly assumed a sidebar.
