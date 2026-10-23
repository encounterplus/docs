---
title: Content Settings
description: Importing, exporting and deleting content, the package manager, and the current system and campaign.
---

These are the sections at the top of the main **Settings** screen. They cover the content the app
holds and where it comes from.

## Resources

### Documentation

Opens this documentation site, [docs.encounter.plus](https://docs.encounter.plus), inside the app.

### Package Manager

Browses the packages available for download and installs them. Packages are content published for
Encounter+ — systems, compendia and modules — as opposed to files you import yourself.

## Local Content

Three buttons in a single row.

### Import

Opens the import sheet, for bringing in a `.module`, `.campaign`,  or `.system` file, a map
in `.dd2vtt` / `.uvtt` format, a CSV, or images. See
[Import and Export](/guides/import-and-export/).

Files are read in place from wherever you picked them, so importing never moves or deletes the
original.

### Export

Opens the export sheet, for writing your content back out to a file.

### Delete

Deletes content in bulk, after asking what to remove:

| Option | Effect |
| --- | --- |
| **All Campaigns** | Deletes every campaign except the primary one. |
| **All Modules** | Deletes every imported module. |
| **All Systems** | Deletes every game system, then recreates and loads the generic one. |

:::danger
These cannot be undone. Take a backup first — either [export](#export) the content you want to keep,
or at least back up the database with **Settings → Advanced Settings → Local Database →
[Backup](/settings/advanced/#backup)**.
:::

## Current System

The game system in use. The row shows its artwork, name, description and version; tapping it opens
that system's detail screen — its package details, updates, entity migrations and recommended
content. See [The system screen](/guides/game-systems/#the-system-screen).

**Manage**, at the trailing end of the section header, opens the **System Manager**: every installed
system, where you load a different one, create, import, edit or delete systems, or get more from
the Package Manager. See [The System Manager](/guides/game-systems/#the-system-manager).

A system defines what content types exist and how they are displayed, so switching it changes the
shape of the whole library.

### System Settings

The current system's own settings, which come from the system rather than from the app — what they
contain depends on which system is loaded. A system that ships view themes adds an **Appearance**
section with a **Theme** picker.

Saving here reloads the system so the new values take effect. The same screen is reachable from the
game screen's system button → **System Settings**, the library sidebar's system row, and the
system's detail screen.

## Current Campaign

The primary campaign for the loaded system. The row shows its artwork, name and description;
tapping it opens that campaign's detail screen. **Manage**, in the section header, opens the
campaign list, where you can switch to another. With no campaign loaded the row reads
**Choose Campaign** and opens the list. See [Campaigns & Modules](/guides/campaigns-and-modules/).

### Campaign Settings

Shown when a campaign is loaded. Opens that campaign's play settings:

| Setting | What it does |
| --- | --- |
| **Party** | The members **Load Party** adds to combat, in order. Any entity type can be added. |
| **Random Assets** | Modules searched, by asset name or tag, for artwork when a token, area effect or aura is created. |

Changes are kept when you tap **Save**. See
[Campaign settings](/guides/campaigns-and-modules/#campaign-settings) for how each one behaves.
