---
title: Dice & Roll Tables
description: Rolling dice anywhere in the app, writing dice into your own text, and building roll tables that roll on other tables.
---

Dice come up in three places in Encounter+: the roller you open yourself, the rolls built into stat
blocks and text, and roll tables.

:::tip
For roller settings — public or private rolls, 3D dice, sound and themes — see
[Dice Roller Settings](/settings/dice-roller/).
:::

## The dice roller

Open the **Dice Roller** from the game screen menu and roll whatever you need.

There are two rollers. The **standard** roller is instant. The **3D** roller simulates physics and
drops the dice on screen, and is part of the Premium subscription.

Both use the same random number generator, so they are equally fair. The 3D roller is for the
feeling of it.

### Who sees your rolls

The roller has a **Mode** setting:

| Mode | Effect |
| --- | --- |
| **Public** | Rolls appear on the player screen and in the web client |
| **Private** | Rolls stay on your device |

Switch to private for the rolls your players should not see, and back afterwards.

## Rolling from content

Dice written into a creature's stat block or a page are live. Tap one and it rolls.

That works because text can carry dice macros. You can write them yourself in any page, note or
description:

```
{#dice 2d6+3}
{#roll 1d20+5}
{#attack 1d20+7}
{#damage 2d8+4}
{#save 1d20+3}
{#check 1d20+2}
```

All of them roll. The different names exist so the app can tell an attack from a save — which is what
lets each kind carry its own dice theme.

You can also show different text from the formula, using a pipe:

```
{#dice 2d6+3|fire damage}
```

### Links to other content

The same syntax links content, which is worth knowing while you are writing pages:

```
{#monster Goblin}
{#item Bag of holding}
{#spell Fireball}
{#page Chapter 1}
{#map Cragmaw Hideout}
```

Tapping one opens that entry. Nothing is copied — it is a link.

## Roll tables

A roll table is a table you can roll on: random encounters, treasure, rumours, weather.

### How a table decides the result

It depends on the first column:

- If the first column is named after a dice formula — `d100`, `d20` — its cells are read as ranges
  like `01-50`, `99` or `00`, and the roll is matched against them.
- Otherwise rows are matched by position, and the app rolls a die the size of the table.

So a `d100` table with a `01-50` row hits that row half the time, and a plain twelve-row table is
rolled with a d12.

### Nested tables

A cell can point at another table. When the parent is rolled, the child is rolled too, as part of the
same result.

That is how a treasure table rolls on a gems table which rolls on a magic item table — one tap, the
whole chain resolved.

Nesting is capped, so a table that eventually rolls on itself will stop rather than run forever.

### Entries inside results

Table cells can contain content links, using the same syntax as above:

```
{#item Potion of healing}
```

The result then comes back with the item linked, ready to open.

### Keeping results

**Settings → Save Table Rolls** keeps a record of each result instead of discarding it after the
roll. On by default.

Useful when you roll a shop's stock or a night's encounters ahead of time and want them again later.

### Importing tables

A `.csv` file imports as a table, which is the quickest way to bring in a table you have in a
spreadsheet. See [Import and Export](/guides/import-and-export/).

## Rolls in remote play

Players in the web client can roll too. They type `/roll 2d6+3` — or `/r` — in the shared log, and
the result appears on your device as well as theirs.

Your public rolls appear in their log the same way. See [Remote Play](/guides/remote-play/).

## Common questions

### My dice text is not tappable

Check the syntax — the braces and the `#` are both required, and the formula has to be one the app
can parse, such as `2d6+3`.

### The 3D roller is not there

It needs a Premium subscription. Without one, the **Type** row is not shown and the standard roller
is used.

### Rolls are showing up on the player screen

Set the roller **Mode** to *Private*. See
[Dice Roller Settings](/settings/dice-roller/#mode).

## Where to go next

- [Dice Roller Settings](/settings/dice-roller/) — rollers, sound and dice themes.
- [The Library](/guides/library/) — where roll tables are stored.
- [Remote Play](/guides/remote-play/) — rolling with players who are not in the room.
