---
title: Game Systems
description: What a game system is, installing and switching between systems, system settings, and how to start building your own.
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

This is also where updates appear once a system is installed.

### From a file

**Settings → Import** installs a `.system` file. See
[Import and Export](/guides/import-and-export/).

## Switching systems

Two places do the same thing:

- **Settings → Current System** — pick from the installed systems.
- The **System Manager**, reached from the main screen's system button.

Switching reloads the app's definitions. Your content is not touched — but the library only shows
content belonging to the loaded system, so it will look like content came and went.

Nothing is deleted by switching. Switch back and everything reappears.

## System settings

A system can define its own settings, separate from the app's.

Reach them from **Settings → Current System → System Settings**, or the system button →
**Settings**. What they contain depends on the system.

Saving reloads the system so the new values take effect.

## Reloading a system

The system button also offers **Reload System**. Use it after editing a system's files by hand, to
pick up the changes without restarting.

## Content belongs to a system

Every piece of content records which system it belongs to. That is what keeps a D&D 5E creature out
of a library running a different ruleset.

It also means importing 5E content requires the 5E system to be installed first — see
[Upgrading from Version 4](/about/upgrading/).

## Building your own

The System Manager has a **Create** button, which makes an empty system with a name, short name,
version and system ID.

From there the work is editing the system's files. The whole folder is visible in the Files app under
Encounter+, so you can edit it on the device or on a computer and reload.

From there it is a developer job, and it has its own section:
[Custom System](/system-development/) covers the folder layout, entity definitions, forms,
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

The bottom of the library sidebar shows the loaded system's name and version. So does
**Settings → Current System**.

### Can I have several systems installed?

Yes. Install as many as you like and switch between them. Only one is loaded at a time.

## Where to go next

- [How it works](/guides/how-it-works/) — where systems sit in the app.
- [Import and Export](/guides/import-and-export/) — installing `.system` files.
- [Custom System](/system-development/) — building a system of your own.
- [Schema reference](/reference/schema/) — the definition formats, for building a system.
