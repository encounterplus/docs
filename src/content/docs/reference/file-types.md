---
title: File Types
description: Every file extension Encounter+ opens or writes, what has to be inside it, and what the app does with it.
---

Encounter+ decides what a file is from two things: its extension, and — for archives — the file
found at the root inside it. This page lists every type the app accepts, what each one has to
contain, and where its contents end up.

For how to actually run an import or an export, see [Import and Export](/guides/import-and-export/).
For the JSON inside the archives, see the [schema reference](/reference/schema/).

## At a glance

| Extension | What it is | Direction |
| --- | --- | --- |
| `.system` | A game system | Import · Export |
| `.module` | A module — pages, maps, encounters, entities, assets | Import · Export |
| `.campaign` | A campaign and its content | Import · Export |
| `.eplus` | An archive of loose content, with its images beside it | Import · Export |
| `.zip` | Any of the above under a neutral extension | Import |
| `.compendium` | Legacy version 4 compendium | Import only |
| `.pack` | Legacy version 4 asset pack | Import only |
| `.dd2vtt` / `.uvtt` | One battle map exported from a map editor | Import only |
| `.csv` | Rows for a roll table | Import only |
| `.jpg` / `.jpeg` / `.png` / `.webp` | An image, imported as a battle map | Import only |

Extensions are matched case-insensitively. Anything else is refused with *Unsupported file type*.

## Content archives

`.system`, `.module`, `.campaign`, `.eplus` and `.zip` are all the same thing: a ZIP archive of JSON
files with the images and other resources they reference stored alongside them. What separates them
is the file at the **root of the archive**, which is what the importer actually reads:

| Root file | Imported as |
| --- | --- |
| `system.json` | A game system |
| `campaign.json` | A campaign |
| `module.json` | A module |
| *none of the above* | A loose collection (see below) |

Because the root file decides, the extension is only a hint — it tells the operating system which
apps can open the file, and it tells you what to expect. An archive whose root is `module.json`
imports as a module whether it is named `.module`, `.eplus` or `.zip`.

### Resources

Every JSON field that points at an image, a video or a font holds a **file name relative to the
archive root**, not an absolute path:

```json
{ "name": "Goblin", "image": "monsters/goblin.webp" }
```

On import the whole tree is merged into the destination's folder, so those relative paths keep
working afterwards. Entity images and tokens that carry a bare file name are resolved against the
folder named after their collection — `goblin.webp` inside `monsters.json` is read as
`monsters/goblin.webp`.

### Loose collections

An archive with no `system.json`, `campaign.json` or `module.json` at its root is treated as a
**collection**: a set of content to be filed into somewhere that already exists, rather than a
container of its own. This is what an entity export produces, and it is the easiest format to
generate from a script.

Each JSON file at the root is one array, named after the collection it belongs to:

| File | Holds |
| --- | --- |
| `maps.json` | Battle maps |
| `pages.json` | Pages |
| `groups.json` | Groups |
| `references.json` | References |
| `encounters.json` | Encounters |
| `assets.json` | Assets |
| *`<collection>.json`* | Entities — `monsters.json`, `spells.json`, `items.json`, … |

The entity file names are not fixed: they come from the collections the **loaded game system**
defines, so a custom system has whatever names its entity definitions declare. A file whose name
matches no collection in the current system is ignored rather than rejected.

You choose the destination — a module, a campaign, or the system itself — on the import screen.

### Packaging your own archives

- **Store the entries at the root**, not inside a wrapper folder. The importer reads
  `module.json`, not `MyModule/module.json`.
- **Strip macOS packaging junk** before you ship an archive. The archive is unpacked wholesale into
  a folder the user can see in the Files app, so `__MACOSX/._*` forks and `.DS_Store` files land in
  their Documents and stay there:

  ```bash
  zip -d MyModule.module '__MACOSX/*' '*.DS_Store'
  ```

- Compression is optional. Encounter+ writes its own archives uncompressed, since almost everything
  inside is already-compressed image data, but it reads compressed archives without trouble.

## Legacy version 4 archives

`.compendium` and `.pack` are the XML archives from Encounter+ version 4. They still import, and
they are recognised the same way — by their root file:

| Root file | Imported as |
| --- | --- |
| `compendium.xml` | Compendium — monsters, spells, items, characters |
| `pack.xml` | Asset pack |
| `module.xml` | Legacy module |
| `campaign.xml` | Legacy campaign |

A legacy `.module` or `.campaign` archive — one holding `module.xml` rather than `module.json` —
imports too, and needs no renaming.

:::caution[Compendiums need D&D 5E installed]
Legacy compendium content is D&D 5E content and is filed into the `dnd5e` system by name. If that
system is not installed the import fails with *dnd5e system not found* rather than guessing where
the content belongs. See [Upgrading from v4](/about/upgrading/).
:::

There is **no XML export**. Anything imported from a legacy archive is exported in the current JSON
format from then on. The element-by-element description of the old format is kept in
[Legacy XML](/reference/legacy-xml/overview/).

## Battle maps from other tools

`.dd2vtt` and `.uvtt` are the Universal VTT export format written by Dungeondraft and other map
editors. Both are JSON, both are read identically, and each file is exactly one map. Encounter+
reads:

- the map image, embedded in the file, and the grid resolution
- `line_of_sight` polygons, imported as walls
- `portals`, imported as door walls — a portal marked open becomes an invisible wall
- `lights`, with position, radius and intensity

The file must declare a `format` number; without one it is rejected as *Invalid format*.

Two options are offered on import: the **name**, and **Colored Lights** — off by default, so lights
come in white rather than in the colours the editor assigned them.

Maps are capped at **8192 px** on their longest side. A larger map is scaled down on import, and its
grid size scaled with it, so the grid stays aligned.

## Images

A `.jpg`, `.jpeg`, `.png` or `.webp` file imported on its own becomes a **new battle map** with that
image as its background, a 50 px grid and the grid overlay turned on. You align the grid yourself
afterwards — see [Battle Maps](/guides/battle-maps/#the-grid).

The stored image keeps the format it arrived in, and is downscaled to 8192 px if it is larger.

Other image formats — HEIC, TIFF, BMP, PDF — are not accepted by the importer. Convert to PNG or
WebP first.

## Table data

A `.csv` file becomes one **roll table**. The file must be UTF-8, and three delimiters are offered
on import: comma, semicolon and tab.

**Header Row** is on by default and takes the first line as the column names. With it off, the first
line is data and the columns are named `Column 0`, `Column 1`, and so on.

CSV is import-only; a table is exported as part of the content it belongs to, in JSON.

## Files used inside content

These are not importable on their own — they arrive inside an archive, or are picked from a form
field while you are editing.

| Type | Used for |
| --- | --- |
| `.png` `.jpg` `.webp` | Map backgrounds, entity images, tokens, asset artwork |
| `.gif` `.webp` (animated) | Assets set to the **Animated Image** type |
| `.svg` | Icons and artwork |
| `.otf` `.ttf` `.ttc` | Fonts, loaded from a game system's `fonts` folder |

Images picked with the **file** picker are stored exactly as they are, which is what keeps an
animated GIF or WebP animated. Images taken from the Photos picker or the built-in editor are
re-encoded, and animation is lost — pick animated artwork as a file.

Images are downscaled when they are saved, by role: **2048 px** for an entity image, **1024 px** for
a token, **4096 px** for an asset, **8192 px** for a map background.

A sprite sheet is an ordinary still image; the frame size and animation duration live in the asset's
parameters rather than in the file.

## What export writes

| You export | You get |
| --- | --- |
| A selection of entities | One `.eplus` archive |
| A module | One `.module` archive |
| A campaign | One `.campaign` archive |
| The current game system | One `.system` archive |
| Everything | One file per module, campaign and system |

Every one of them is the same ZIP-of-JSON described above, so anything Encounter+ writes can be
edited by hand and imported straight back.

## Opening files from outside the app

Encounter+ registers `.system`, `.module`, `.campaign`, `.eplus`, `.pack`, `.compendium`, `.uvtt`,
`.dd2vtt` and `.zip` as document types, so it appears as a destination in the Files app, in the
share sheet, in AirDrop and in drag and drop. Images and `.csv` files are handed over the same way.

Files are read **in place**. Importing never moves, changes or deletes the file you picked, so
importing straight from iCloud Drive, a USB drive or another app's folder is safe.

To offer a file over the network or from a web page instead, see the
[URL Scheme](/reference/url-scheme/).
