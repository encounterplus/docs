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

## Schema reference generation

The developer-facing format/config/template reference is **generated**, not hand-written. The app's Swift `Codable` types are the source of truth; two dependency-free Python scripts turn them into docs:

1. `scripts/symbolgraph-to-schema.py <symbols-dir> public/schemas` — Swift symbol graph → JSON Schema 2020-12, one flat `*.schema.json` per type. `public/schemas/` is the **single source of truth** and is served verbatim at `/schemas/*.schema.json`.
2. `scripts/schema-to-markdown.py public/schemas src/content/docs/reference/schema --base-path /reference/schema --schema-url-base /schemas --sidebar-out src/schema-sidebar.json` — schemas → Markdown pages + a sidebar fragment.

**`src/content/docs/reference/schema/` and `src/schema-sidebar.json` are fully generated — do not hand-edit.** They carry an `AUTO-GENERATED` banner and are marked `linguist-generated` in `.gitattributes`. To change them, edit the schema/tags and rerun the script. Pages are written **flat** (`reference/schema/<name>.md`), so a page's URL never encodes its group — re-grouping in the sidebar never breaks a link.

This is **developer** reference on an otherwise end-user site, so the sidebar stays slim. By default (`--sidebar-mode index`) the generator emits a single landing page (`reference/schema/index.md` → `/reference/schema/`) that lists every schema grouped with descriptions + raw-JSON links, and the sidebar fragment is just **one** "Schema" link to it. The per-type detail pages are still generated and reachable from the index and via search — they're just not enumerated in the nav. `--sidebar-mode tree` enumerates the full group tree instead (kept for a possible standalone API-docs build). `astro.config.mjs` imports the fragment and spreads it into the Reference group, so regenerating updates the nav automatically.

### The `- SchemaGroup:` and `- SchemaMerge:` tags

Filtering, section placement, and page layout are driven by two independent DocC tags on each Swift type:

```swift
/// A battle map and everything placed on it.
///
/// - SchemaGroup: Content
struct Map: Codable { ... }

/// A drawing placed on a map, documented on the Map page.
///
/// - SchemaGroup: Content
/// - SchemaMerge: Map
struct Drawing: Codable { ... }
```

- **`- SchemaGroup:`** is a **single section name** (stored as `x-group`, stripped from the description). It only decides which section/sidebar group the type is listed under — it carries **no layout meaning**: no trailing slash, no nested `A/B` paths (a slash-bearing value is collapsed to its first segment with a warning). By default each type gets its **own standalone page**.
- **`- SchemaMerge: <Host>`** (stored as `x-merge`, stripped from the description) folds the type **into `<Host>`'s page** — `<Host>` names another type, whose page then concatenates its mergers as `##` sections. A host and its mergers share one page keyed by the host name (so `Map` + `Drawing` + `Wall` … all render on `map.md`).
- **Filtering:** only types tagged with `SchemaGroup` **or** `SchemaMerge` — plus everything they transitively `$ref` — are emitted. Untagged, unreferenced Codable types are dropped; reached-but-fully-untagged types fall back to the `Shared` group. (If nothing is tagged, all Codable types are emitted unfiltered.)
- **Listing:** a merged type with **no `SchemaGroup` of its own** is rendered on its host page but **not listed** on the landing page; give it a `SchemaGroup` too if it should appear there.

Pages are written **flat** (named after the host type), so the section a type sits in never affects its URL. Until the app source carries these tags, `public/schemas/*.schema.json` are tagged via an interim hand-maintained mapping; the next tagged app build overwrites them.

### The `- SchemaAllOptional:` tag

A separate doc-comment tag that marks a type whose every field is optional:

```swift
/// - SchemaAllOptional: true
struct Foo: Codable { ... }
```

When set (a bare or truthy value enables it; `false`/`no`/`0` disables it), the type's `required` array is omitted entirely. Use it for types with **hand-written** `Codable` conformance that decodes with `decodeIfPresent` — there, whether a property is `?` in Swift no longer says whether its key must be present, and the symbol graph can't see the custom coding. The tag is stripped from the description and leaves no marker in the docs.

## Icon tooling

`scripts/strip-sf-symbol.py` extracts a single weight/scale variant from an SF Symbols template SVG export, stripping template guides/notes to produce a compact SVG for the docs. Usage:

```bash
./scripts/strip-sf-symbol.py SOURCE.svg OUTPUT.svg --group Light-S
```

`--group` selects the variant (e.g. `Regular-S`, `Light-M`); if the group isn't found the script prints the available group ids. Generated icons are committed under `public/assets/`.
