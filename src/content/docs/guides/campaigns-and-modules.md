---
title: Campaigns & Modules
description: Organising your material — what a campaign is, what a module is, groups, pages and references, and how the current campaign works.
---

A **campaign** is your own container for one ongoing game. A **module** is a bundle of content made
to be shared.

That is the whole difference. Both hold the same kinds of things — pages, maps, encounters and
entries — but a campaign is where you work, and a module is what you install.

| | Campaign | Module |
| --- | --- | --- |
| Made by | You | You or someone else |
| Comes from | Created in the app | Imported or downloaded |
| Holds | Your notes, maps, encounters, party | Published adventure content |
| Deleting it | Removes its content | Removes everything it brought |

## Campaigns

A campaign holds the material for one table, plus the state of the game you are running: the current
map, the loaded maps, and the initiative order.

### Creating one

Open the library, go to **Content → Campaigns**, and add one. Give it a name and a description.

### The current campaign

One campaign is the **current** one at a time. That is the campaign the game screen, battle map and
player display are driving.

Switch it under **Settings → Current Campaign**, or from the campaign list.

Switching changes what **Load Party** finds, which maps are to hand, and where new content is filed.

### Campaign settings

Each campaign has its own settings for play. Open them from **Settings → Current Campaign →
Campaign Settings**, or from the menu on the campaign's detail screen → **Campaign Settings**.

Changes are kept only when you tap **Save**.

#### Party

The characters **Load Party** adds to combat. Tap **Add Party Member** and pick them from the
library — you can pick several at once. Drag to reorder, and swipe to remove one.

- **Any entity can join.** Player characters are the usual members, but NPCs, companions and
  sidekicks can be added alongside them.
- **Order is kept.** Load Party adds members in the order listed.
- **Some members remember their state.** Entities of a *standalone* type — player characters in
  D&D 5E — keep one combatant between sessions, so hit points and conditions carry over. Any other
  member joins with fresh stats from its entry each time.
- **Nobody is added twice.** A member already in combat is skipped, so loading the party again
  after adding a latecomer is safe.

Once loaded, player characters in combat also feed the 5E encounter difficulty rating. Both are
described in [Encounters & Combat](/guides/encounters/).

#### Random Assets

Modules the app draws artwork from when it creates a token, an area effect or a status effect's
aura. An asset matches by its name or one of its tags; when several match, one is picked at random.
On a token, a matching asset replaces the creature's own token image.

Tap **Add Module** to pick from your installed modules. Leave the list empty to turn this off.

:::note
Both lists store links rather than the items themselves. If you delete a party member or a module
and later import it again, the campaign picks it back up. Links that no longer point at anything
are skipped.
:::

## Modules

A module is content packaged for distribution — an adventure, a compendium, a rules supplement, an
asset pack.

Modules arrive two ways: **Settings → Package Manager** downloads published ones, and
**Settings → Import** installs a `.module` file you already have. See
[Import and Export](/guides/import-and-export/).

A module carries its own name, author, version and description, so you can see where content came
from and whether an update exists.

:::caution
Deleting a module deletes everything it brought with it. Content you created yourself belongs to your
campaign, not to the module, and is not affected.
:::

## What goes inside

Both campaigns and modules hold the same building blocks:

| Item | What it is |
| --- | --- |
| **Page** | Written content — notes, read-aloud text, house rules |
| **Map** | A battle map |
| **Encounter** | A prepared fight |
| **Group** | A folder, for structure |
| **Reference** | A shortcut to something else |

### Pages

Pages are the prose half of an adventure. Write your session notes, room descriptions and handouts
here.

Pages are written in a rich text editor, and links do double duty: a link to `/monster/goblin` opens
the creature, and a link to `/roll` rolls its own text. See
[Writing Content](/guides/writing-content/#pages).

### Groups

Groups are folders. Use them to give an adventure chapters and a campaign sections.

Groups nest, so you can go as deep as you need.

:::note
Deleting a group does **not** delete what is inside it. The contents move back to the top level of the
campaign or module.
:::

### References

A reference is a shortcut. It points at something else — a creature, a map, a page — and shows up in
the tree with its own name.

This is how one thing appears in two places without being copied. The goblin defined in a compendium
can also be listed in the chapter where it ambushes the party.

References are soft links. If the target is deleted, the reference is left pointing at nothing.

## How this relates to the library

The library holds all your content. Campaigns and modules organise it.

Nothing is duplicated: filing a creature into a campaign does not make a second copy of it. See
[How it works](/guides/how-it-works/).

## Common questions

### Where did my new content go?

New content is filed into the current campaign unless you say otherwise. Check
**Settings → Current Campaign**.

### Can content belong to both a campaign and a module?

Yes. Content records where it came from, and can sit in both.

### I deleted a module and lost content

A module owns what it brought. If you edited one of its entries, make a **Copy** first — the copy is
yours and survives. See [The Library](/guides/library/#copying).

## Where to go next

- [Import and Export](/guides/import-and-export/) — installing modules and exporting your campaign.
- [Encounters & Combat](/guides/encounters/) — the party and encounter difficulty.
- [Battle Maps](/guides/battle-maps/) — maps live in campaigns and modules too.
