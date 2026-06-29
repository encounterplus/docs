# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Documentation site for **Encounter+**, a virtual tabletop / DM tool app for **iOS and macOS** (macOS via Catalyst). Built with [Astro](https://astro.build) + the [Starlight](https://starlight.astro.build) docs theme. The deliverable is content (Markdown/MDX), not application code — most work here is editing docs pages, not writing components.

This site documents a **new version** of the app. Most existing pages still describe the old version and are being migrated (see "Obsolete content" below). The docs cover four things:

1. **Guides** — how to use the app.
2. **Import/export format** — JSON is now the primary exchange format for all imports and exports. XML is a **legacy format**: still supported but **import-only** (no XML export).
3. **Game system configuration** — the app now supports custom, user-defined game systems built from a set of configuration files.
4. **Form/view template format** — templates that game systems use for editing input (form templates) and display (view templates).

## Commands

```bash
npm install        # install dependencies
npm run dev        # dev server at localhost:4321
npm run build      # production build to ./dist/
npm run preview    # preview the production build locally
npm run astro check  # type-check content and config (run before committing structural changes)
```

There is no test suite. `npm run build` is the closest thing to CI validation — it fails on broken internal links and invalid frontmatter, so run it after editing sidebar config or cross-page links.

## Content architecture

- All pages live in `src/content/docs/` as `.md`/`.mdx`. **File path = route** (e.g. `guides/quick-start.md` → `/guides/quick-start/`). Renaming a file changes its URL and breaks inbound links.
- The content collection is defined in `src/content.config.ts` using Starlight's `docsLoader` + `docsSchema`. Every page needs frontmatter with at least `title`; see existing pages for `description`, `sidebar.order`, etc.
- The **sidebar is configured manually** in `astro.config.mjs`, not auto-generated. Adding a new doc page requires adding a matching `{ label, link }` entry there, or it won't appear in navigation. Links in the sidebar must match the page's route exactly.
- Images referenced from docs go in `src/assets/` (embedded via relative Markdown links, processed by Astro). Truly static files (favicon, icon PNGs) go in `public/` and are served as-is at the root path.

### Doc sections

- `about/` — intro, FAQ
- `guides/` — user-facing guides (quick start, encounter management, battle maps, web client, etc.)
- `reference/legacy-xml/` — reference for the **legacy** Encounter+ XML format (import-only in the new version; JSON is the primary format for both import and export). Each file documents one XML element (monster, spell, map, tile…); `overview.md` is the index that ties them together. These describe ZIP archives (`.compendium`, `.module`, etc.) whose root XML file defines the package type. The new JSON format, game-system configuration, and form/view template references don't exist yet and will need new `reference/` sections.

### Obsolete content

Many guide pages are mid-migration to app v5 and carry an `:::caution[Obsolete]` admonition with a `TODO: update to v5` note. When editing a page, check whether its obsolete notice still applies before treating its content as current.

## Icon tooling

`scripts/strip-sf-symbol.py` extracts a single weight/scale variant from an SF Symbols template SVG export, stripping template guides/notes to produce a compact SVG for the docs. Usage:

```bash
./scripts/strip-sf-symbol.py SOURCE.svg OUTPUT.svg --group Light-S
```

`--group` selects the variant (e.g. `Regular-S`, `Light-M`); if the group isn't found the script prints the available group ids. Generated icons are committed under `public/assets/`.
