---
title: Custom System
description: How to build a game system for Encounter+ — what a system is made of, how the app loads it, and the edit-reload loop for developing one.
---

A **game system** is what gives Encounter+ its shape. The app itself has no notion of a creature,
a spell or a stat block — it loads one system at a time and builds its entire content model,
library, editors and detail views from the JSON files that system contains.

That means a whole ruleset can be authored without writing a line of app code. This section is the
developer's guide to doing that.

:::note
Looking for how to *use* systems — installing, switching, system settings? See the
[Game Systems guide](/guides/game-systems/). This section is about authoring them.
:::

## What a system is

A system is a folder on disk, identified by a short lowercase id such as `dnd5e`. It lives under
`Documents/systems/<id>/` and is fully visible in the Files app, so it can be edited on the device
or on a computer.

Inside that folder, a handful of JSON files answer a handful of questions:

| Question | Answered by |
| --- | --- |
| What content types exist? | [`entities.json`](/system-development/entities/) |
| What are their fixed value sets? | [`types.json`, `collections.json`](/system-development/types/) |
| How is each type edited? | [`forms/*.json`](/system-development/forms/) |
| How is each type displayed? | [`views/*.json`](/system-development/views/) |
| What does it look like? | [`themes/*.json`](/system-development/themes/) |
| How does the library filter and group? | [`filters.json`](/system-development/config/) |
| How does the app behave for this ruleset? | [`config.json`](/system-development/config/) |
| What text is shown, in which language? | [`lang/*.json`](/system-development/types/#localization) |
| How does old content catch up? | [`migrations/*.js`](/system-development/migrations/) |

Everything else in the folder — icons, images, fonts, web assets — is supporting material those
files point at.

## What a system is not

A system is primarily **definitions, not content**. Creatures, spells and items are user content:
they live in modules and campaigns and merely record which system they belong to. The copy of D&D 5E
bundled inside the app, for example, ships the definitions for a 5E creature but no creatures.

This separation is what lets a system be updated independently of the content authored against it.

A `.system` archive *may* still ship content alongside its definitions, for reference material that
belongs to the ruleset itself — the published D&D 5E package does exactly that with the SRD content.
See [Packaging & Distribution](/system-development/packaging/#distributing-content-for-your-system).

## The development loop

### 1. Create a skeleton

The **System Manager** (reached from the main screen's system button) has a **Create** button. It
asks for a name, short name, version and system id, and writes a minimal system folder containing
`config.json`, `entities.json`, `types.json`, `filters.json`, a default theme and a starter set of
icons.

Starting from an existing system is often faster. Install one, then copy its folder under a new id
and change the `id` in `system.json`.

### 2. Edit the files

Open `Documents/systems/<id>/` in the Files app, or over a file share on a Mac, and edit the JSON
directly. Any text editor works.

:::tip
All system JSON is parsed with **JSON5** enabled, so trailing commas and `//` comments are legal.
The shipped D&D 5E system uses both heavily. Strict JSON is still valid JSON5, so a strict parser
on your side is fine too — just be aware that files you read from other systems may not parse with
one.
:::

### 3. Reload

The system button on the main screen offers **Reload System**. It re-reads every definition file
without restarting the app, so the usual loop is *save → reload → look*.

Reloading also happens automatically when you save system settings, and when a system is installed
or made primary.

### 4. Read the errors

A form, view or theme file that fails to decode does not crash the app and does not silently
disappear — it is replaced with an **error definition** that renders the decoder's message where
the form or view would have been. If a screen shows a wall of Swift decoding text, that is a
malformed JSON file telling you which key it choked on.

Setting `"debug": true` at the top of a view or theme definition turns on layout debugging for
that file.

## Where to look things up

This section is the *guide*. The exhaustive, generated list of every key and every enum value in
every definition file lives in the [schema reference](/reference/schema/) — in particular:

- [EntityDefinition](/reference/schema/entity-definition/)
- [FormDefinition](/reference/schema/form-definition/)
- [ViewDefinition](/reference/schema/view-definition/)
- [ThemeDefinition](/reference/schema/theme-definition/)
- [DataTransform](/reference/schema/data-transform/)
- [Entity](/reference/schema/entity/)
- [System](/reference/schema/system/)

When this guide and the schema reference disagree, the schema reference is right — it is generated
from the app's own data model.

## Where to go next

- [System Structure](/system-development/file-structure/) — every file and folder, and the order they load in.
- [Entity Definitions](/system-development/entities/) — declaring content types and their data.
- [Forms](/system-development/forms/) — building the editors.
- [Views](/system-development/views/) — building the detail screens.
