---
title: Upgrading from Version 4
description: What changed in version 5, why your library may look empty at first, and how to get your existing content back.
---

Version 5 keeps all of your content. There is one extra step after upgrading, and this page explains
what it is and why it is needed.

:::tip[The short version]
Your content is intact. It is D&D 5E content, and version 5 only shows content belonging to the
game system that is loaded — so **install the D&D 5E system and everything comes back.** The app
offers to do it for you, from a copy bundled inside the app, with no download needed. That copy is
the game system alone — it brings no content, because you already have yours.
:::

## What changed

In version 4 the app *was* a D&D 5E app. The content types, the character sheets, the stat blocks
and the rules assumptions were built into the code, so supporting another ruleset meant rewriting the
app.

Version 5 pulls all of that out into a **game system**: a self-contained definition of what content
types exist, what fields they have, how their forms are laid out and how they are displayed. The app
loads one system at a time and takes its shape from it.

D&D 5E did not go away — it became the `dnd5e` system. Nothing was cut, and none of the 5E
behaviour was lost. What you gain is that the system can be updated on its own schedule without an
app release, and that other rulesets are now possible at all.

## Context menus almost everywhere

Version 5 puts a context menu on most things you can see. **Long press** on iPhone and iPad,
**right click** (or two-finger click) on Mac, and a menu of the actions for that thing appears where
you are already looking, instead of in a toolbar or a detail screen.

They are worth trying on:

- **Combatants** in the initiative list — damage and healing, conditions, duplicating, removing.
- **Tokens** on the battle map — the same combatant actions, plus map-side ones.
- **Library entries** — open, edit, duplicate, bookmark, add to a campaign or module, export, delete.
- **Rows inside forms** — reordering and removing list items, and the per-row actions of that field.
- **Maps, pages, encounters, campaigns and modules** in their lists.

Nothing is *only* available in a context menu, so nothing is lost if you never use them — but they
are usually the shortest route, and multi-step jobs like building an encounter are much faster with
them.

## Why your library may look empty

When your database was migrated, all of your existing content was tagged as **D&D 5E** content,
because that is what it is.

The library only shows content belonging to the system that is currently loaded. Until the D&D 5E
system is installed and selected, none of your content matches the loaded system — so the library
comes up empty.

**Nothing was deleted.** No content needs to be re-imported, and no backup needs to be restored.

## Installing the D&D 5E system

**The app asks you.** Whenever no game system is installed — on a first launch, and again after
updating — you get a **Game System Required** screen with an **Install D&D 5E** button.

Because you already have content, that button installs the copy of D&D 5E that ships inside the
app — no download, no network and no account. It is the **game system only**: the definitions your
existing content needs in order to be displayed, with no content of its own. One tap and it is in;
your library fills back up with what you already had.

The published package in the Package Manager is the same system plus the **SRD reference content**.
Install that one if you want the SRD entries as well — but for getting your own library back, the
bundled copy is all that is needed.

If you dismissed that screen and want to do it by hand:

1. Open **Settings**.
2. Tap **Current System**.
3. Pick **D&D 5E** from the list of installed systems.

If it is not listed at all, **Settings → Package Manager** downloads it, and
**Settings → Import** installs it from a `.system` file you already have.

:::note
The bundled copy is only offered while D&D 5E is genuinely absent. Once it exists it belongs to
you — the app will not write over it later, so a newer version you downloaded from the Package
Manager, or edits you made to the system folder yourself, are safe.
:::

## Legacy content you import yourself

Legacy `.compendium` and `.pack` XML archives from version 4 still import.

Because that content is 5E content, **the D&D 5E system has to be installed before you import it** —
otherwise the import fails rather than guessing where the content belongs. If an old archive refuses
to import, this is usually why.

The current formats are `.module`, `.campaign`, `.system` and `.eplus`; see
[Import and Export](/guides/import-and-export/) and [File Types](/reference/file-types/). Nothing
forces you to convert — your old archives keep working.

## Purchases

Purchases from older versions are honoured; version 5 is a free update, not a new app.

If something you own is not being recognised — after reinstalling, or on a new device — use
**Settings → Restore Purchases**. It costs nothing and never charges you again. See
[Purchases](/settings/purchases/#restore-purchases).

## Before you upgrade

Not required, but worth doing once: **export your content** from version 4 and keep the files
somewhere other than the device. The migration is well-trodden, but an export is the one thing that
protects you regardless of what happens — and it is useful afterwards as an ordinary backup. See
[Backups](/about/faq/#backups).

## Still missing something?

Ask on our [Discord](https://discord.gg/psWk84h) or on
[r/EncounterPlus](https://www.reddit.com/r/EncounterPlus/) — include what you are looking for and
which system is loaded under **Settings → Current System**.
