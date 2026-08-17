---
title: Content Settings
description: Importing, exporting and deleting content, the package manager, and the current system and campaign.
---

These are the sections at the top of the main **Settings** screen. They cover the content the app
holds and where it comes from.

## Resources

### Help Center

Opens this documentation site.

### Package Manager

Browses the packages available for download and installs them. Packages are content published for
Encounter+ — systems, compendia and modules — as opposed to files you import yourself.

## Local Content

Three buttons in a single row.

### Import

Opens the import sheet, for bringing in a module, campaign, pack, compendium or system file, a map
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
| **Everything** | Deletes all database content along with the campaign, module and system directories, then recreates and loads the generic system. |

:::danger
These cannot be undone. Take a backup first — **Settings → Advanced Settings → Local Database →
[Backup](/settings/advanced/#backup)**.
:::

## Current System

The game system in use. The row shows its name, description and version; tapping it opens the list
of installed systems, where you can switch to another one.

A system defines what content types exist and how they are displayed, so switching it changes the
shape of the whole library.

### System Settings

The current system's own settings, which come from the system rather than from the app — what they
contain depends on which system is loaded.

Saving here reloads the system so the new values take effect. The same screen is reachable from the
main screen's system button → **Settings**, and from the system's detail screen.

## Current Campaign

The primary campaign. The row shows its name and description, or *None*; tapping it opens the
campaign list, where you can switch to another. See
[Campaigns & Modules](/guides/campaigns-and-modules/).
