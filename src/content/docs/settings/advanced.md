---
title: Advanced Settings
description: App interface chrome, housekeeping actions, and the local database backup.
---

**Settings → Advanced Settings.**

These configure the app itself rather than the game you are running.

## Interface

### Bottom Bar

Shows the bottom bar on the game screen. On by default. Not available on Mac.

### Status Bar

Shows the system status bar — clock, battery, indicators — on the game screen. On by default. Not
available on Mac.

Turning both off gives the map the whole display, which is worth doing when you present from a
tablet.

### Open Library Action

What opening the library does. Not shown on iPhone, which has no second window.

| Option | Effect |
| --- | --- |
| **Modal View** *(default)* | Open the library over the current screen. |
| **New Window** | Open the library in a separate window. |

*New Window* suits a large display or a Mac, where the library and the map can sit side by side.

### Appearance

The app's light or dark appearance.

| Option | Effect |
| --- | --- |
| **Dark** *(default)* | Always dark. |
| **Light** | Always light. |
| **System** | Follow the system setting. |

The default is dark rather than system: the app is normally used at a table in low light.

## Maintenance

Both actions run behind a progress overlay and report when they finish. Neither touches your
content.

### Clear Cache & Temporary Files

Clears the image caches, cached page HTML and the temporary directories.

Use it if the app is taking up more storage than it should, or if a page renders with stale content.
Everything cleared here is rebuilt on demand.

### Remove Unused Image Files

Deletes image files that nothing references any more.

Images can be left behind when content is deleted or re-imported. This reclaims that space, and only
removes files no entity points at.

## Local Database

Your content lives in a local database. These settings cover backing it up.

### Backup

Writes a compacted backup of the database now.

### Last Backup

The date of the most recent backup, or *Not Found* if there has never been one. Read-only.

### Automatic Backups

Keeps backups on a schedule. On by default.

Leave this on. If the database has gone more than a month without a backup, opening Settings offers
to take one — that prompt is why it appears on the main Settings screen rather than here.
