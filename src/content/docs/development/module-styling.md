---
title: Styling Modules
description: How a module or campaign customises the look of its pages and entity views with its own CSS and JavaScript.
---

:::caution[Work in progress]
Page styling is still being built. What this page describes works today, but details may change
before it settles.
:::

Layout belongs to the game system: it renders every page and entity view from its templates. A
module or campaign changes how they look with CSS and JavaScript only, from fixed paths in its
folder.

## Two ways to style pages

**Adjust the system's look** — the default. Add either or both of:

| File | Loaded on |
| --- | --- |
| `styles/custom.css` | every page and entity view, after the system's styles |
| `scripts/custom.js` | every page and entity view, after the page has rendered |

**Use your own look instead** — add `styles/page.css`. Your pages then load none of the
system's styles, so this stylesheet has to style everything. `custom.css` and `custom.js` still
load after it. This suits content converted from another source that brings its own design.

Entity views always use the system's look; `page.css` affects pages only.

## Targeting pages and entity views

`custom.css` reaches both pages and entity views, so scope rules with these attributes:

```css
/* pages only */
html[data-page-id] body > main { max-width: 42rem; margin-inline: auto; }

/* one page, by its id */
html[data-page-id="3F2A9C1E-…"] body > main { background: url("../images/parchment.jpg"); }

/* entity views only, or one kind of entity */
html[data-entity-id] h1.title { letter-spacing: 0.05em; }
html[data-kind="monster"] h1.title { color: darkred; }
```

- When the user has picked one of the system's view themes, `<html>` also carries
  `data-view-theme="<id>"`, so `custom.css` can adjust to it:
  `html[data-view-theme="clean"] h1.title { … }`.
- In Markdown pages, `:::` blocks and `{.class}` attributes put your own class names on the
  content, for rules like `body > main .sidebar { … }` — see
  [Writing Content](/guides/writing-content/#attributes).
- Page content sits in `<main>`, directly inside `<body>`. Write `body > main` rather than
  `main`: converted content may have a `<main>` of its own.
- Paths in `url()` and `@import` are relative to the stylesheet, so from `styles/` your images
  are `../images/…` and fonts `../fonts/…`.
- `page.css` can split into several files with `@import url("../css/fonts.css");`, so a module can
  keep its own folder layout.

## Reserved paths

These paths change how a module renders just by existing, so use them only for their purpose:

- `styles/custom.css`, `styles/page.css`, `scripts/custom.js`
- `assets/css/global.css` — marks an older module, whose pages keep their original look. Adding
  `styles/page.css` takes precedence over it.

Anything in a subfolder is never treated specially. Keep embedded web apps and other bundled
files in a folder of their own, such as `apps/<name>/`.

## Packing with build tools

When a build tool produces the module, pack the output folder (for example `dist/`), not the
project root. Everything in the archive ends up in the user's Documents and is served to players'
browsers over Remote Play. On import, the app drops `node_modules`, `.git` and `.env` files, but
nothing else.
