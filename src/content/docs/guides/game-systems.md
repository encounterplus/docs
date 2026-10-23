---
title: Game Systems
description: What a game system is, installing, switching and managing systems, system settings, and how to start building your own.
---

A game system is the ruleset the app takes its shape from. It decides what content types exist, what
fields they have, how forms are laid out and how entries are displayed.

The app loads **one system at a time** and rebuilds its interface around it. That is why the library
shows creatures and spells with D&D 5E loaded, and something else entirely with another system.

:::tip
For the short version of how this fits with the library and campaigns, see
[How it works](/guides/how-it-works/).
:::

## What a system contains

A system is a folder of definitions, not code:

- The content types it defines — creatures, spells, items, or whatever the ruleset needs.
- The fields each type has, and the forms used to edit them.
- The views used to display them, including stat block layouts.
- Filters, themes, icons, fonts and translations.
- Its own settings.

Every entry of every type is an **entity** — one underlying storage model that the system gives
meaning to through those definitions. See
[Everything in there is an entity](/guides/how-it-works/#everything-in-there-is-an-entity).

Because none of that is built into the app, a system can be updated on its own schedule, and anyone
can write one.

### Definitions only, or definitions plus content

Most systems are **definitions only**: they give the library its shape and leave it empty. You fill
it yourself, or by importing `.module` packages authored for that system.

A system package *can* also carry content of its own — entries packed into the same `.system`
archive and imported alongside the definitions. The published D&D 5E package is the example: it
brings the SRD reference content with it, so the library is already full when the install finishes.

Both kinds are the same file type and install the same way. The difference shows up afterwards, in
whether the library has anything in it — so it is worth reading a package's description before
assuming content comes with it.

## Installing a system

### D&D 5E

The **Game System Required** screen appears whenever no system is installed, and offers D&D 5E two
ways:

- **Install D&D 5E** downloads the published package. It is the newer of the two and **includes the
  SRD reference content**, so the library is populated as soon as it finishes. It needs a network
  connection.
- **Install D&D 5E Offline Copy** installs the copy that ships inside the app. That one is the
  **game system only, without any content** — no download, no network and no account.

If you are upgrading from version 4 you already have your content and only need the definitions, so
the bundled copy is the one offered first in that case. See
[Upgrading from Version 4](/about/upgrading/).

Neither is ever installed automatically, and neither overwrites a copy you already have.

### From the Package Manager

**Settings → Package Manager → Systems** lists published systems and installs them directly. The
listing describes what each package contains — some are definitions only, some ship reference
content as well.

The [System Manager](#the-system-manager) reaches the same list from its **+** button →
**Get More…**.

### From a file

**Settings → Import** installs a `.system` file, and so does the System Manager's **+** button →
**Import…**. See [Import and Export](/guides/import-and-export/).

## Where systems are managed

Three places lead to the same screens:

| Where | What it offers |
| --- | --- |
| **Settings → Current System** | The loaded system's row opens its [detail screen](#the-system-screen). **System Settings** sits below it, and **Manage** in the section header opens the [System Manager](#the-system-manager). |
| The **system button** on the game screen | Labelled with the loaded system's short name. Its menu has **System Info**, **Reload System**, **System Settings** and **System Manager**. |
| The **library sidebar** | The loaded system's name and version sit at the bottom. Tap it for the detail screen; long-press it for **Reload System**, **System Settings** and **System Manager**. |

## The System Manager

The System Manager lists every system installed on the device, each as a card with its banner, name
and short description. The loaded one shows **Loaded**; every other one has a **Load** button.

- **Tap a card** to open that system's [detail screen](#the-system-screen).
- **Long-press a card** for **Load**, **Edit** and **Delete**, without opening it.
- **+** in the toolbar adds one: **Create System**, **Import…**, or **Get More…** for the Package
  Manager.

The loaded system cannot be deleted — its **Delete** is disabled until you load a different one.

## Switching systems

Tap **Load** on a system's card in the System Manager, or on its detail screen.

Switching reloads the app's definitions. Your content is not touched — but the library only shows
content belonging to the loaded system, so it will look like content came and went.

Nothing is deleted by switching. Switch back and everything reappears.

## The system screen

Each system has a detail screen: its banner and icon, its description, and the details from its
package — **Author**, **Website**, **Repository**, **Version**, **Short Name**, **Package** and
**System ID** — followed by the content types it defines.

It also shows whatever needs attention:

- **Latest Version** with an **Install** button, when the system was installed from a package and a
  newer version has been published. The check runs each time the screen opens; the **⋯** menu →
  **Check for updates** runs it on demand.
- **Entity migrations available**, when a system update changed the shape of entries you already
  have. **Run** opens the migration screen, which updates them to the new version.
- **Additional Content**, when the system's package recommends companion packages — the published
  D&D 5E package recommends its SRD content this way. Each one shows whether it is installed, and
  can be installed or updated from here.

The **⋯** menu holds the rest:

| Action | What it does |
| --- | --- |
| **Load** / **Reload System** | Loads the system, or re-reads the loaded one's files. |
| **Check for updates** | Asks the system's package for a newer version. Shown only for systems installed from a package. |
| **System Settings** | The system's own settings. Loaded system only. |
| **Debug Info** | The loaded definitions, types, config, settings and fonts as JSON, with a key-path filter — for system authors. Loaded system only. |
| **Edit** | The system's name, short name, version, author, links, image and banner. The system ID cannot be changed. |
| **Delete** | Removes the system and every entry belonging to it. Not available for the loaded system. |

:::caution
Deleting a system deletes its content with it, and cannot be undone. Export anything you want to
keep first.
:::

## System settings

A system can define its own settings, separate from the app's.

Reach them from **Settings → Current System → System Settings**, the system button → **System
Settings**, or the system screen's **⋯** menu. What they contain depends on the system.

A system that ships more than one look for its pages adds an **Appearance** section with a
**Theme** picker. It changes how the system's entries and pages are displayed, in the app and in the
web client alike.

Saving reloads the system so the new values take effect.

## Reloading a system

**Reload System** — from the system button, the library sidebar, or the system screen — re-reads
the loaded system's files. Use it after editing them by hand, to pick up the changes without
restarting.

## Content belongs to a system

Every piece of content records which system it belongs to. That is what keeps a D&D 5E creature out
of a library running a different ruleset.

It also means importing 5E content requires the 5E system to be installed first — see
[Upgrading from Version 4](/about/upgrading/).

## Building your own

The System Manager's **+** button → **Create System** makes an empty system. It asks for a name,
short name, short description, version and system ID, and an optional description. The system ID
must be unique and cannot be changed later.

From there the work is editing the system's files. The whole folder is visible in the Files app under
Encounter+, so you can edit it on the device or on a computer and reload.

From there it is a developer job, and it has its own section:
[System Development](/system-development/) covers the folder layout, entity definitions, forms,
views, templates, themes and packaging. The underlying formats are listed in the
[schema reference](/reference/schema/).

:::note
A `.system` archive should not contain macOS packaging leftovers. Strip `__MACOSX` folders and
`.DS_Store` files before sharing one, or they end up in other people's Documents folder.
:::

## Common questions

### My library is empty after switching

That is expected. The library only shows content for the loaded system. Switch back, or install the
system your content belongs to.

### Which system am I running?

The bottom of the library sidebar shows the loaded system's name and version, the game screen's
system button shows its short name, and **Settings → Current System** shows its name, description
and version.

### Can I have several systems installed?

Yes. Install as many as you like and switch between them. Only one is loaded at a time.

## Where to go next

- [How it works](/guides/how-it-works/) — where systems sit in the app.
- [Import and Export](/guides/import-and-export/) — installing `.system` files.
- [System Development](/system-development/) — building a system of your own.
- [Schema reference](/reference/schema/) — the definition formats, for building a system.
