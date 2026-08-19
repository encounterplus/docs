---
title: Writing Content
description: Markdown formatting, links to your own content, and live dice — the syntax behind every piece of text in the app.
---

Most text you type in Encounter+ is Markdown: creature traits, item descriptions, notes, roll table
cells — everything the app renders itself. The same rules apply everywhere, so what you learn
writing a trait also works in a table.

Two things make it more than plain Markdown: a link can point at your own content, and dice are live.

:::note[Pages are different — for now]
Module and campaign **pages** are written in a rich text editor and stored as HTML, so the Markdown
formatting below does not apply to them. Links and dice rolls in pages still work — see
[Pages](#pages). Pages are moving to Markdown in a future update.
:::

## Formatting

Standard Markdown, with the usual pieces:

```markdown
# Heading
## Smaller heading

**bold**, *italic*, ~~struck through~~ and `code`

- a list
- another item
  - nested

1. numbered
2. and so on

> A quote. Your game system styles these — in D&D 5E they read as boxed text.

---
```

Tables use the GitHub pipe syntax:

```markdown
| Roll | Result |
| --- | --- |
| 1-3 | Nothing happens |
| 4-6 | A patrol |
```

A blank line separates paragraphs. A single line break inside a paragraph is kept as a line break.

:::note
Raw HTML is not rendered — write `<b>bold</b>` and you get the tag text, not bold text. Use Markdown
instead.
:::

How all of this actually looks — fonts, colours, how a quote is drawn — comes from the loaded game
system's theme, not from the text. The same page looks different under a different system.

## Images

Images are Markdown images, relative to the content they live in:

```markdown
![A map of the ruins](ruins.jpg)
```

You can size them with a fragment after the filename:

| Fragment | Effect |
| --- | --- |
| `#width=400` | Scale to 400 points wide, keeping the aspect ratio |
| `#height=200` | Scale to 200 points tall |
| `#size=400x200` | Exactly 400 × 200 points |
| `#width=auto` | Fill the available width |

```markdown
![The tavern](tavern.jpg#width=400)
```

## Links to your content

A link whose destination is a **content type** points at something in your library. The link text is
what you are pointing at:

```markdown
[Goblin](monster)
[Bag of holding](item)
[Fireball](spell)
[Cragmaw Hideout](map)
[Chapter 1: Goblin Arrows](page)
```

Tapping one opens that entry. Nothing is copied — it stays a link, so editing the creature updates
every page that points at it.

The name is matched loosely: case and accents are ignored, and the entry's slug or id works too.

### Which destinations work

Anything your **game system** defines is a valid destination — in D&D 5E that is `monster`, `npc`,
`character`, `spell`, `item`, `feat`, `background`, `species`, `race`, `class`, `subclass`,
`vehicle`, `rule` and `table`. A different system gives you a different list, and its own types work
the same way.

Alongside those, your own content:

| Destination | Points at |
| --- | --- |
| `page` | A page |
| `map` | A battle map |
| `encounter` | A prepared encounter |
| `group` | A group |
| `asset` | An asset |

### When two entries share a name

Add the source after a `#`:

```markdown
[Goblin](monster#MM)
```

If nothing matches that source, the app falls back to the first entry with the right name, so the
link never dead-ends.

You can also link by id, which never goes stale:

```markdown
[Goblin](/entity/2C1D2E30-8E39-4C1E-BD1C-8B0A2A1F0000)
```

### Pointing into a specific module

A destination starting with `/` is used as a path, which lets you say exactly where to look:

```markdown
[Camp Vengeance](/module/tomb-of-annihilation/page/camp-vengeance)
```

Without the module part, a link is resolved inside the content it is written in first, then anywhere
in your library — which is usually what you want, so reach for full paths only when a name is
ambiguous across modules.

External links behave normally and open in a browser:

```markdown
[The rules](https://example.com/rules)
```

## Dice

In text the app renders itself, dice expressions in ordinary prose are found automatically. Write

```markdown
The trap deals 2d10 piercing damage.
```

and `2d10` is tappable — no markup at all. Attack bonuses like `+7` and `Recharge 5-6` are picked up
the same way.

Under D&D 5E the app also guesses what kind of roll it is, which is what lets each kind carry its own
dice theme: a leading `+` reads as an attack, anything with a `d20` as a check, and a formula
followed by *damage* as damage.

### Writing a roll yourself

To be explicit — or to roll something the text does not spell out — link to `roll`:

```markdown
[2d6+3](roll)
```

Add a label with a link title, and it shows up in the roll log so you can tell one roll from another:

```markdown
[2d6+3](roll "fire damage")
```

The full form is a path, and takes the roll type as well:

```markdown
[+7](/roll/d20+7/Longsword/attack)
```

The types are `attack`, `damage`, `check` and `save` — the same ones the dice themes are set up
against. See [Dice & Roll Tables](/guides/dice/).

## Where this all works

| Where | Notes |
| --- | --- |
| Entity descriptions and traits | The main use — rendered in the detail view |
| Roll table cells | A cell can link an item or another table, and the result comes back linked |
| Notes | Anywhere the app gives you a plain text box |
| Pages | Rich text rather than Markdown — see below |

### Pages

Pages have their own editor: you format with its toolbar, and the page is stored as HTML rather than
Markdown. Everything in *Formatting* above is handled by the toolbar instead of by typing.

Links still do the same two jobs, written as paths with the editor's link tool:

| Link address | Result |
| --- | --- |
| `/monster/goblin` | Opens the creature |
| `/page/goblin-arrows` | Opens the page |
| `/roll` | Rolls the link's own text, so link the text `2d6+3` |

A `/roll` link takes its label from the link's title, the same way `[2d6+3](roll "fire damage")`
does elsewhere. Dice written as ordinary text in a page are *not* picked up automatically — in a
page, a roll has to be a link.

## Content written for v4

Older content used curly-brace macros for links and dice instead of Markdown. It still imports and
still works, so nothing you own breaks — but write anything new as Markdown. It is the format the app
is built around now, and it stays readable if you ever open the file outside Encounter+.

## Where to go next

- [Campaigns & Modules](/guides/campaigns-and-modules/) — where pages live.
- [Dice & Roll Tables](/guides/dice/) — rolling, roll tables and dice settings.
- [Game Systems](/guides/game-systems/) — what defines the content types you can link to.
