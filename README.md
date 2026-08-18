# Encounter+ Docs

[![Built with Starlight](https://astro.badg.es/v2/built-with-starlight/tiny.svg)](https://starlight.astro.build)

Documentation site for **Encounter+**, a virtual tabletop / DM tool for iOS and macOS. Built with [Astro](https://astro.build) and the [Starlight](https://starlight.astro.build) docs theme.

The deliverable here is content — Markdown/MDX pages — not application code.

Live site: **<https://docs.encounter.plus>** — the canonical origin, configured as `site` in [astro.config.mjs](astro.config.mjs) and matching the Pages custom domain.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                | Action                                                    |
| :--------------------- | :-------------------------------------------------------- |
| `npm install`          | Installs dependencies                                     |
| `npm run dev`          | Starts local dev server at `localhost:4321`               |
| `npm run build`        | Builds the production site to `./dist/`                   |
| `npm run preview`      | Previews the production build locally                     |
| `npm run astro check`  | Type-checks content and config                            |

There is no test suite. `npm run build` is the closest thing to CI validation — it fails on broken internal links and invalid frontmatter, so run it after editing the sidebar or cross-page links.

## 🚀 Project structure

```
.
├── public/
│   ├── assets/            # static icons/images served as-is
│   └── schemas/           # generated JSON Schemas (source of truth)
├── scripts/               # schema + icon tooling (Python, dependency-free)
├── src/
│   ├── assets/            # images referenced from docs (processed by Astro)
│   ├── content/docs/      # all documentation pages
│   ├── schema-sidebar.json  # generated sidebar fragment
│   ├── styles/
│   └── content.config.ts
├── astro.config.mjs       # site config + manual sidebar
└── package.json
```

Starlight maps every `.md`/`.mdx` file in `src/content/docs/` to a route based on its path (`guides/quick-start.md` → `/guides/quick-start/`). Renaming a file changes its URL and breaks inbound links.

The **sidebar is configured manually** in `astro.config.mjs` — a new page won't appear in navigation until a matching entry is added there.

### Doc sections

| Section              | Contents                                                              |
| :------------------- | :-------------------------------------------------------------------- |
| `about/`             | Intro, FAQ, upgrading                                                 |
| `guides/`            | User-facing guides — quick start, encounters, battle maps, remote play |
| `settings/`          | Reference for each settings screen                                     |
| `development/`       | Developer-facing overview                                              |
| `system-development/`| Building custom game systems — config, entities, forms, views, themes  |
| `reference/`         | URL scheme, generated schema reference, legacy XML format              |

`reference/legacy-xml/` documents the legacy Encounter+ XML format. XML is still supported for **import only**; JSON is the primary exchange format for both import and export.

## 📐 Generated schema reference

`src/content/docs/reference/schema/` and `src/schema-sidebar.json` are **fully generated — do not hand-edit.** The app's Swift `Codable` types are the source of truth:

```bash
# Swift symbol graph → JSON Schema 2020-12 (one flat file per type)
scripts/symbolgraph-to-schema.py <symbols-dir> public/schemas

# JSON Schema → Markdown pages + sidebar fragment
scripts/schema-to-markdown.py public/schemas src/content/docs/reference/schema \
  --base-path /reference/schema \
  --schema-url-base /schemas \
  --sidebar-out src/schema-sidebar.json
```

`public/schemas/` is served verbatim at `/schemas/*.schema.json`. Grouping and page layout are driven by `- SchemaGroup:` / `- SchemaMerge:` doc-comment tags on the Swift types. See [CLAUDE.md](CLAUDE.md) for the full tag reference.

## 🎨 Icon tooling

`scripts/strip-sf-symbol.py` extracts a single weight/scale variant from an SF Symbols template SVG export:

```bash
./scripts/strip-sf-symbol.py SOURCE.svg OUTPUT.svg --group Light-S
```

Generated icons are committed under `public/assets/`.

## 👀 Want to learn more?

Check out [Starlight's docs](https://starlight.astro.build/) and [the Astro documentation](https://docs.astro.build).
