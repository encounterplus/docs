---
title: System Structure
description: Every file and folder inside a game system, what each one does, and the order the app loads them in.
---

A system is a plain folder. This page is the map of it.

## Layout

```
systems/<id>/
├── system.json              # system metadata (id, name, version, author…)
├── manifest.json            # package manifest, for distribution
├── config.json              # ruleset behavior: entity config, measurement, initiative
├── entities.json            # the content types this system defines
├── types.json               # named value sets (enums) and their labels
├── custom-types.json        # user-editable additions to types.json
├── collections.json         # ordering for types, plus type-to-type mappings
├── custom-attributes.json   # extra queryable attributes
├── filters.json             # library filter / group / sort options
├── rules.json               # optional seed content shipped with the system
├── forms/
│   ├── <label>.json         # the editor for one entity type
│   ├── settings.json        # the system's own settings screen
│   └── partials/*.json      # reusable form fragments
├── views/
│   ├── <label>.json         # the native detail view for one entity type
│   ├── <label>-compact.json # the compact variant
│   ├── <label>.html         # optional HTML template instead of a native view
│   ├── partials/            # reusable view fragments (.json) and text partials (.md)
│   └── transforms/*.json    # computed-attribute recipes
├── themes/
│   ├── default.json         # the base theme
│   └── <name>.json          # additional themes
├── lang/
│   └── <code>.json          # localization strings
├── migrations/
│   └── <version>.js         # data migrations, named after the system version
├── icons/                   # collection icons and in-content icons
├── images/                  # banner, cover, backgrounds used by themes
├── fonts/                   # fonts registered when the system loads
├── assets/                  # css/js/img used by HTML views
└── cache/                   # app-managed, do not edit
```

Nothing here is mandatory except `system.json` and `entities.json`. A system with no `forms/`
folder simply has no editors; a system with no `themes/` folder falls back to the app's built-in
default theme.

Content collection files may also sit at the root — `<collection.label>.json` for each entity type,
plus `pages.json`, `maps.json`, `encounters.json` and friends. They are optional: a definitions-only
system has none, and one that ships reference content (the published D&D 5E package and its SRD
entries, for instance) imports them when the system is installed. See
[Packaging & Distribution](/system-development/packaging/#distributing-content-for-your-system).

## The metadata files

### `system.json`

The system's identity. It is what the importer decodes to create the system record in the
database.

```json
{
  "id": "dnd5e",
  "name": "Dungeons & Dragons 5E",
  "shortName": "D&D5E",
  "version": "0.9.14",
  "author": "Encounter+ Dev Team",
  "descr": "This game system provides support for **Dungeons & Dragons 5E**.",
  "shortDescr": "World's Greatest Roleplaying Game",
  "image": "images/icon.jpg",
  "banner": "images/banner.jpg",
  "repository": "https://github.com/encounterplus/dnd5e",
  "package": "https://github.com/encounterplus/dnd5e/releases/latest/download/manifest.json"
}
```

The `id` is load-bearing and effectively permanent: it names the folder on disk, it is the primary
key of the system record, and every entity, module and campaign stores it in its own `system`
field. Changing it orphans content.

`version` drives [migrations](/system-development/migrations/), and `package` is the manifest URL
the app polls for updates. See [System](/reference/schema/system/) for the full field list.

### `manifest.json`

Only used for distribution — see [Packaging](/system-development/packaging/).

## Load order

`SystemManager` reads the folder in a fixed order when a system is loaded or reloaded. It matters,
because later stages look things up in earlier ones:

1. **`config.json`**, then the stored system settings on top of it.
2. **Language** — the `language` setting picks a file from `lang/`.
3. **Measurement and initiative systems** — built from the merged config.
4. **Built-in types** are injected (`SystemLanguage`, `MeasurementSystem`, `Role`,
   `InitiativeGroupType`, `InitiativeRollType`, `DurationType`, `DurationUnit`).
5. **`types.json`**, then **`custom-types.json`** on top, then **`collections.json`** — which
   reorders types that already exist and creates ones that do not.
6. **`custom-attributes.json`**.
7. **Entity definitions** from `entities.json`, each paired with its merged entity config.
8. **Themes** — `themes/default.json` first, then every other `themes/*.json`, then `extends`
   chains are resolved.
9. **Forms** — `forms/*.json`, then `forms/partials/*.json`.
10. **Views** — `views/*.json`, then `views/partials/*.json`, then `views/*.html` templates.
11. **Filters** from `filters.json`.
12. **Fonts** from `fonts/`, and the template environment, whose partial search path is
    `views/partials`.

The practical consequences:

- A `collections.json` key that names a type from `types.json` **sorts** it. A key that names
  nothing **creates** a bare type whose labels are the raw values.
- A filter block keyed by an entity name that `entities.json` does not define is skipped silently.
- Anything a form or view references — a type, a partial, a theme style — must exist by the time
  the form or view is rendered, not by the time it is parsed. Parsing never resolves references.

## Naming conventions that the app relies on

Several files are found by name rather than by being referenced, all of them derived from the
entity definition's `label`:

| Path | Used for |
| --- | --- |
| `forms/<label>.json` | the entity's editor |
| `views/<label>.json` | the entity's native detail view |
| `views/<label>-compact.json` | the compact detail view (panels, small presentations) |
| `views/<label>.html` | an HTML template, used when the entity is configured for the `html` renderer |
| `themes/<label>.json` | a theme applied to that entity type |
| `icons/<collection.label>.png` | the collection's icon in the library sidebar |
| `<collection.label>.json` | the file name content of this type is imported from |

Rename an entity's `label` and all of these have to move with it.

Partials are the exception — they are looked up by the name you pass, so
`{% include 'spell-range.md' %}` resolves to `views/partials/spell-range.md`, and
`{"type": "partial", "value": "monster-stats"}` resolves to `views/partials/monster-stats.json`.

## Paths inside definition files

Paths that appear in view, theme and form definitions are resolved in two ways:

- **Absolute** (`/images/paper.jpg`, `/icons/spell/evocation.png`) — resolved against the system
  folder.
- **Relative** (`monsters/goblin.jpg`) — resolved against the container the entity came from
  (its module or campaign).

The template context exposes both roots as `env.systemURL` and `env.dataURL`, and the
`resolvePath` filter applies the same rules to a value you build yourself.

## Live reload while developing

On macOS debug builds, the app watches the system folder and reloads automatically when anything
under `views/`, `forms/`, `themes/`, `styles/` or `scripts/` changes. On iOS, and in release
builds, use **Reload System** from the system button.

## Things not to put in the folder

`cache/` is app-managed. Deleting it is safe; writing to it is not useful.

macOS packaging junk — `__MACOSX/` forks and `.DS_Store` files — must be stripped before a
`.system` archive is shared, because the importer moves the archive's contents wholesale into the
user's visible Documents folder. See [Packaging](/system-development/packaging/).
