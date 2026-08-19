---
title: How it works
description: The core concepts behind Encounter+ — the game system, the library, campaigns and modules, and the game screen — and how they fit together.
---

Encounter+ is built from a handful of core concepts. Almost every question about the app is really
a question about which one you are in. Once you know them, the rest of the app makes sense.

## The core concepts

| Concept | What it does |
| --- | --- |
| **Game system** | Decides what kinds of content exist |
| **Library** | Holds all your content |
| **Campaigns & modules** | Organise content into adventures |
| **Game screen** | Where you play |

### 1. The game system

A game system is the ruleset the app takes its shape from. It decides what content types exist, what
fields they have, and how they look on screen.

With the D&D 5E system loaded, you get creatures, spells, items and character sheets built for 5E.
Load a different system and you get different content types.

The app loads **one system at a time**. This matters for one reason: the library only shows content
that belongs to the loaded system. If your library looks empty, the system is usually why. See
[Upgrading from Version 4](/about/upgrading/).

### 2. The library

The library is where all your content lives. Every creature, spell, item, note, player and roll table
is stored in one place, and you can search all of it at once.

Content gets into the library in three ways:

- You create it yourself.
- You import a file.
- You download a package.

It does not matter which — once it is in, it is all the same library.

### 3. Campaigns and modules

A campaign is one long adventure. A module is a smaller piece you can drop into a campaign.

Both organise content, and neither holds a separate copy of anything. They group what is already in
the library, and they add the maps, pages and encounters that belong to that story.

One campaign is the **current campaign** at any time. That is the one the game screen uses.

### 4. The game screen

The game screen is where you actually play. It holds the initiative tracker, the battle map, the dice
roller and the shared log.

## How they connect

They stack. Each one builds on the one before it:

```
Game system   →   what content can exist
     ↓
Library       →   the content you have
     ↓
Campaigns     →   how it is organised
     ↓
Game screen   →   what you are running right now
```

A creature is defined by the system, stored in the library, organised into a campaign, and loaded
onto the game screen as a combatant. It is the same creature the whole way down.

## Where this shows up on screen

The library sidebar is a map of the same idea:

| Sidebar section | What it holds |
| --- | --- |
| **Library** | All Entries and Bookmarks — search across everything |
| **Content** | Campaigns, Modules and System |
| **Compendium** | The content types the loaded system defines |

The **Compendium** section is the one that changes between systems. What you see there comes from the
system, not from the app.

### Everything in there is an entity

A creature, a spell, an item, a class, a vehicle — internally they are all the same thing, an
**entity**. The app has no built-in idea of what a creature is. It stores entities, and the loaded
system tells it what each kind of entity means:

| The system defines | What you see |
| --- | --- |
| **Data** | Which fields an entry stores, and what type each one is |
| **Form** | The editor screen you get when you create or edit one |
| **View** | The read-only detail screen — the stat block, the spell card |
| **Appearance** | The fonts, colours and layout it is drawn with |

That is why a 5E stat block looks like a 5E stat block. Nothing about it is hardcoded — it is the
system's definition of the Monster entity, rendered.

It also explains a few things that would otherwise look odd:

- A new content type can appear without an app update. The system adds it, and a new Compendium
  section appears with a working editor and detail screen.
- Two systems can both have "spells" that store completely different fields and look nothing alike.
- Everything works the same everywhere. Search, filters, bookmarks, import and export are written
  against entities in general, so they apply to content types the app has never heard of.

If you want to define your own entity types, see [Custom System](/system-development/).

## What is yours and what is not

Content you make is yours. Content that comes from a system or a downloaded module belongs to that
package, and can be replaced when the package updates.

You can always copy something and edit the copy. That is the safe way to change content you did not
make.

## Where to go next

- Never used the app? [Quick Start](/guides/quick-start/) gets you to a running fight.
- Want to know what the library can do? See [The Library](/guides/library/).
- Ready to run combat? See [Encounters & Combat](/guides/encounters/).
