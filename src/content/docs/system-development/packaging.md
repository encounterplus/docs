---
title: Packaging & Distribution
description: Building a .system archive, writing a package manifest, and publishing updates users can install.
---

A finished system is a folder. To hand it to someone else it becomes a `.system` archive, and to
have updates arrive automatically it gets a package manifest.

## Building the archive

A `.system` file is a zip of the system folder's **contents** — `system.json` at the archive root,
not inside a wrapping directory.

```bash
cd systems/mysystem
zip -r ../mysystem.system . -x '.git/*'
zip -d ../mysystem.system '__MACOSX/*' '*.DS_Store'
```

That second line is not optional. The importer unzips everything and moves it wholesale into
`Documents/systems/<id>/`, which the user browses in the Files app — so `__MACOSX/._*` resource
forks and `.DS_Store` files land in their Documents folder and stay there. Compressing from the
Finder produces both; strip them every time.

Leave `cache/` and any `backup/` folders out too.

The archive is installed by opening it — **Settings → Import**, or tapping the file anywhere iOS
or macOS offers to hand it to the app. Import decodes `system.json`, registers the system, merges
the files into place and makes it primary.

## `manifest.json`

For a system users should be able to *update*, publish a manifest alongside the archive:

```json
{
  "id": "dnd5e",
  "name": "Dungeons and Dragons 5E",
  "type": "system",
  "version": "0.9.14",
  "description": "World's Greatest Roleplaying Game.",
  "download": "https://github.com/encounterplus/dnd5e/releases/download/0.9.14/dnd5e.system",
  "compatibility": { "minimum": "5.0.5" }
}
```

| Field | Notes |
| --- | --- |
| `id` | Must match `system.json`'s `id` — this is what update checks match on. |
| `type` | `system` (or `module` for content packages). |
| `version` | Compared against the installed system's version to offer an update. |
| `download` | Absolute URL of the `.system` archive. |
| `compatibility.minimum` | The oldest app version that can run this system. |

Optional catalog fields — `authors`, `media`, `repository`, `website`, `content`, `category` —
are described in the [Package reference](/reference/schema/package/).

Then point `system.json`'s `package` field at the manifest's URL:

```json
"package": "https://github.com/encounterplus/dnd5e/releases/latest/download/manifest.json"
```

The app polls that URL, compares versions, and offers the update. A `latest/download/` style URL
that always resolves to the newest release means the manifest URL never has to change.

## Releasing an update

1. Make the change.
2. Bump `version` in `system.json`.
3. Add a [migration](/system-development/migrations/) if the `data` shape changed.
4. Build the archive and strip the macOS junk.
5. Publish the archive and update `manifest.json` — the same `version`, and a `download` URL
   pointing at the new archive.

Users are offered the update, and after installing it the system's screen offers to run any
migrations the new version brought.

:::caution
An installed system is never silently overwritten. Users may have edited their copy in the Files
app, and updates go through the normal install path so those edits are handled as an update rather
than a replacement. Do not assume a user's folder is byte-identical to what you shipped.
:::

## Compatibility

`compatibility.minimum` is the guard against a system using features an older app does not have.
Set it to the oldest app version you have actually verified, and raise it when you start using
something new. A system with no `compatibility` block is treated as compatible with everything,
which is only honest for a simple one.

## The package registry

Published systems and modules are listed in the catalog the app reads from
`https://packages.encounter.plus/packages.json`, browsable in **Settings → Package Manager**. That
is where most users will find a system. To be listed there, get in touch with the Encounter+
team — hosting the archive and manifest yourself works regardless, users just install from the URL
or the file.

## Distributing content for your system

A system's job is to carry definitions, and there are two ways to get content to the people
installing it.

**Separate `.module` packages** are the default. They record your system's `id`, and a module
declaring a `system` in its manifest requires that system to be installed first. Keeping them apart
is what lets the ruleset and the content that uses it ship on different schedules, and it keeps the
system archive small.

**Content inside the `.system` archive** is the other option. Collection files placed at the archive
root — `<collection.label>.json` for each entity type, plus `pages.json`, `maps.json`,
`encounters.json` and the other content collections — are imported along with the definitions, and
their entries are tagged with the system's `id`. Use this for reference content that is part of the
ruleset itself rather than an optional add-on. The published D&D 5E package works this way: it is
the same system as the bundled copy, plus the SRD content.

The bundled copy of D&D 5E inside the app is definitions only, which is why a user who installs it
offline starts with an empty library, while the downloaded package starts with a full one. It is
worth saying which of the two your package is in its manifest `description`, since both install
identically and the difference is only visible afterwards.

## Checklist

- [ ] `system.json` has a stable `id`, a bumped `version` and a `package` URL.
- [ ] Migrations exist for any change to the `data` shape, and older ones are still present.
- [ ] Archive built from the folder's contents, with `system.json` at the root.
- [ ] `__MACOSX/` and `.DS_Store` stripped; `cache/` and `backup/` excluded.
- [ ] `manifest.json` published, `id` and `version` matching, `download` reachable.
- [ ] `compatibility.minimum` set to a version you have tested.
- [ ] Installed from the archive on a clean device and the library checked.

## Where to go next

- [Migrations](/system-development/migrations/) — the version bump's other half.
- [Package reference](/reference/schema/package/) — every manifest field.
- [Import and Export](/guides/import-and-export/) — the user-facing side of installing.
