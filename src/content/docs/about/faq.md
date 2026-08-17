---
title: Frequently Asked Questions
description: The questions that come up before you know which guide to open — what a system, module and campaign are, what the library holds, how the external screen and web client work, and what you can import.
---

If you are looking for what a particular control does, the [Settings](/settings/overview/) section
covers every screen. This page answers the questions that come up before that.

## The app

### Do I have to pay for anything?

No. Encounter+ runs a complete game out of the box — the library, creating and editing content,
encounter building, the initiative tracker, campaigns and modules, import and export, roll tables
and the dice roller are all included, and there are **no ads, ever**.

Two purchases add to that: a **one-time Battle Map purchase** for maps, tokens, lighting and line of
sight, and an **optional Premium subscription** for remote play, 3D dice, animated tiles and weather
effects. See [Purchases](/settings/purchases/).

### Does it work offline?

Yes, entirely. Everything lives in a local database on your device — the app never needs a network
to run a game. A connection is only used for optional things: downloading packages, remote play, and
iCloud backup.

### Where is my data stored?

In a local database on the device, plus a folder tree in the app's **Documents** directory that
holds systems, modules, campaigns, maps and images. That folder is visible in the Files app, so you
can get at your own content — but it also means it can be deleted from there, so take backups. See
[Backups](#backups) below.

:::danger[Deleting the app deletes everything]
On iOS and iPadOS, removing Encounter+ removes its entire Documents folder with it — your library,
campaigns, modules, maps, images and every database backup. There is no undo, and reinstalling does
not bring it back.

The same applies to offloading the app, and to a device reset. **Export your content and keep the
files somewhere else** before deleting or resetting anything.
:::

### Which devices does it run on?

iPhone, iPad and Mac. The Mac version is the iPad app running natively, so your purchases and
content formats are the same across all three.

## Content and terminology

### What is a game system?

A **system** is the ruleset the app is currently shaped around. It is not hard-wired: the system
defines what content types exist (creatures, spells, items, whatever your game needs), what fields
they have, how their forms look, and how they are displayed. Switching the system changes the shape
of the entire library.

The app ships with a `generic` system and a `dnd5e` one; others can be installed from the Package
Manager or imported as a `.system` file, and you can build your own.

See [Current System](/settings/content/#current-system) and the
[System schema](/reference/schema/system/).

### How do I install a game system?

**The app asks you.** Whenever no system is installed, you get a **Game System Required** screen with
an **Install D&D 5E** button — that copy ships inside the app, so it needs no download, no network
and no account. One tap and you have a working 5E setup.

If you want something else, or you dismissed that screen:

| Where | What it does |
| --- | --- |
| **Settings → Current System** | Lists the systems you have installed and switches between them |
| **Settings → Package Manager** | Downloads published systems you do not have yet |
| **Settings → Import** | Installs a system from a `.system` file |

You only need one, and you can change it later. Switching systems does not delete anything — content
belongs to the system it was made for, and reappears when you switch back.

### What is the difference between a module and a campaign?

Both are containers for pages, maps, encounters and content. The difference is who they belong to:

| | Module | Campaign |
| --- | --- | --- |
| **What it is** | Authored content meant to be distributed | Your own working container for one table |
| **Where it comes from** | Imported from a `.module` file or the Package Manager | You create it |
| **Typical use** | A published adventure, a bestiary, an asset collection | The game you are actually running |
| **Live state** | None | Holds the running combat, the map on screen, your party |

Exactly one campaign is **primary** at a time — that is the one the battle map and the player
display are driving. Modules can be attached to a campaign so their content is available while you
play.

See [Campaigns & Modules](/guides/campaigns-and-modules/), and the
[Module](/reference/schema/module/) and [Campaign](/reference/schema/campaign/) schemas.

### What is the library?

The library is the browser for everything you own — creatures, spells, items, players, notes, roll
tables, maps, pages and encounters — across every source at once: the built-in content, imported
modules, and anything you created yourself. It is where you search, filter, edit and organise, as
opposed to the game screen, where you play.

See [Working with Library](/guides/library/).

### What is the Package Manager?

A browser for content published for Encounter+ — systems, compendia and modules — that installs with
one tap, as opposed to files you import yourself. It also tells you when something you installed has
an update.

**Settings → Package Manager.** See [Content Settings](/settings/content/#package-manager).

### Why are there so few monsters, spells and items?

The content included by default is limited to what the *Open Gaming License* permits — essentially
the [Systems Reference Document](https://dnd.wizards.com/articles/features/systems-reference-document-srd).
Anything beyond that has to come from you: create it, import it from a file, or install a package.

### My library is empty — where is my content?

If you have just updated from version 4, this is expected and nothing is lost. See
[Upgrading from Version 4](/about/upgrading/), which explains it and takes one tap to fix.

## Import and export

### What files can I import?

| Format | What it holds |
| --- | --- |
| `.module` | A distributable body of content — pages, maps, encounters, entities, assets |
| `.campaign` | A whole campaign, including its content |
| `.system` | A game system |
| `.collection` | A mixed set of content in one archive |
| `.eplus` | The same content as a single JSON file, with images embedded |
| `.dd2vtt` / `.uvtt` | A single map exported from Dungeondraft, Universal VTT and similar tools |
| `.csv` | Tabular data — roll tables and bulk entity import |
| `.jpg` / `.png` / `.webp` | Images, imported as maps or artwork |

Legacy `.compendium` and `.pack` XML archives from older versions still import as well. See
[Import and Export](/guides/import-and-export/) and the
[schema reference](/reference/schema/) for the current formats.

### What can I export?

A single entity or a selection of them, a module, a campaign, the current system, or everything at
once. **Settings → Export.**

`.eplus` is import-only by design — there is no export to it.

### Can I import from Dropbox, Google Drive or somewhere other than iCloud?

Yes. Import uses the system file picker, so anything that appears there works — Dropbox, Google
Drive, Files, a USB drive, wherever. Install the provider's app first if its location is not
already listed, then pick it under **Locations** in the picker.

### Does importing move or copy my original file?

Neither — the file is read in place from wherever you picked it, and importing never moves, changes
or deletes the original.

## Backups

### What is the best way to back up my content?

**Export it yourself, regularly.** Everything else is a safety net; this is the actual backup.

Use **Settings → Export** to write your campaigns, modules and content out to files, then keep those
files somewhere that is not the device — iCloud Drive, Dropbox, a computer, anywhere. An exported
file is portable content, so it can be restored on any device, on a reinstall, on a newer version of
the app, or shared with someone else. Nothing else you can do is as durable.

How often is up to you, but a good habit is after any session where you created something you would
mind losing.

### Isn't the automatic database backup enough?

It covers a different problem. **Settings → Advanced Settings → Local Database → Automatic Backups**
keeps scheduled snapshots of the database file, and it is on by default — leave it on. It is what
saves you when the database itself becomes unreadable, which is the failure it exists for.

But those snapshots live on the same device, in the app's own folder. They do not survive deleting
the app, losing the device, or wiping the Documents folder from the Files app. So:

| | Protects against | Survives losing the device |
| --- | --- | --- |
| **Manual export** | Anything — corruption, deletion, mistakes, moving to a new device | Yes, if you store the files elsewhere |
| **Automatic database backup** | Database corruption on this device | No |

Run both. The scheduled backup handles corruption without you thinking about it; the exports are
what you actually rely on.

### How do I take a database backup right now?

**Settings → Advanced Settings → Local Database → Backup** writes a compacted snapshot immediately.
**Last Backup** above it shows the date of the most recent one.

If the database has gone more than a month without a backup, opening Settings offers to take one.

### Something went wrong — how do I restore?

From an export, import the file: **Settings → Import**, pick it, done.

From a database backup, the switch is in the **iOS Settings app** rather than in Encounter+ — open
**Settings → EncounterPlus → Launch issues → Restore database**, then launch the app. It restores
the most recent snapshot and keeps your current database alongside it. It sits there deliberately,
so it is reachable even when the app cannot start.

:::caution
Restoring the database replaces everything with the state at the time of that snapshot — anything
created since is not in it. Export first if the app still opens.
:::

## At the table

### What is the external screen?

A second, player-facing view of the game: the map, the initiative order, images and handouts —
without your notes. You show it on a TV, a projector or a second monitor while you keep the full app
on your own device.

Connect it over AirPlay screen mirroring (an Apple TV or an AirPlay-capable display), with an HDMI
adapter, or — on Mac — as a second window.

See [External Screen Settings](/settings/external-screen/).

### What is the bar along the edge of the external screen?

The initiative tracker. Where it sits and what it shows is
[Initiative Style](/settings/external-screen/#initiative-style) — the edge positions leave room for
a map, the full-screen layouts are available when no map is shown, and *None* turns it off.

### How do I show something to the players mid-session?

The external screen splits in two by how often you change things. The **settings** screen holds the
setup you do once — themes, the rig, the AirPlay connection. The **controls**, opened from the game
screen, hold what changes scene to scene: which map is shown, the overlay, the handout.

## Remote play

### What is the web client?

A browser page your players open to see the map and move their own tokens, served by a web server
built into the app. Nothing to install on their side — any modern browser on any device works, and
they do not need Encounter+ or an Apple device.

Remote play is part of the **Premium subscription**. See the
[Remote Play guide](/guides/remote-play/) and
[Remote Play Settings](/settings/remote-play/).

### Do my players need to be on my network?

For a local game, yes — they connect to the **Local Access** address and it just works.

Over the internet, your router has to let the connection through. The app tries this automatically
with UPnP port forwarding; where that is not supported you forward the port by hand. The
**Public Access** section shows the current status.

### What can players actually do?

That is up to you: **All** lets anyone move anything, **Token** limits each player to the token they
are assigned, and **None** makes it view-only. *Token* is the usual choice. See
[Interactions](/settings/remote-play/#interactions).

### It is not connecting — what now?

See the [Web Client FAQ](/guides/web-client-faq/), which covers the common failures: the wrong
address, browsers forcing `https`, and tokens not appearing.

## Still stuck?

Ask on our [Discord](https://discord.gg/psWk84h) or on
[r/EncounterPlus](https://www.reddit.com/r/EncounterPlus/).
