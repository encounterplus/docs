---
title: Writing Content
description: Markdown formatting, links to your own content, and live dice — the syntax behind every piece of text in the app.
---

Most text you type in Encounter+ is Markdown: creature traits, item descriptions, notes, roll table
cells, module and campaign pages. The same rules apply everywhere, so what you learn writing a trait
also works in a table or a page.

Two things make it more than plain Markdown: a link can point at your own content, and dice are live.
Pages go a little further again, with raw HTML and a few extra kinds of block — see [Pages](#pages).

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
Outside pages, raw HTML is not rendered — write `<b>bold</b>` in a trait and you get the tag text,
not bold text. Use Markdown instead. Pages do render it.
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

In pages, size an image with an attribute instead — see [Pages](#pages).

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
| Pages | Everything above, plus the extras below |

## Pages

Pages are written in Markdown too, and everything above works in them: formatting, links to your
content, written rolls, and dice found in ordinary text. A page also understands a few things the
rest of the app does not.

### Raw HTML

HTML in a page is rendered. Reach for it when Markdown has no syntax for what you want:

```markdown
The <mark>red door</mark> is trapped. H<sub>2</sub>O, x<sup>2</sup>.
```

Links inside raw HTML are kept exactly as written: dice in them are not linked, and a link like
`<a href="monster">` is not turned into a content link. Write links in Markdown to get those.

### Attributes

Curly braces after an element give it a class, an id or any other attribute, which your module's CSS
can then style (see [Styling Modules](/development/module-styling/)):

```markdown
## The Ambush {#ambush .boxed}

A paragraph with a class.
{.flavor}

![The tavern](images/tavern.jpg){width=400}
```

That last line is how to size an image in a page — the `#width=400` fragment from
[Images](#images) does not apply here.

### Blocks

A block between `:::` lines becomes a group your CSS can style as one — a sidebar, read-aloud text, a
GM note. The opening line names it, and can carry attributes too:

```markdown
::: sidebar
### Optional rule

Goblins flee at half strength.
:::

::: {.note #warning}
Not for the players' eyes.
:::
```

A `:::` with no name is plain text. To put one block inside another, give the outer one a longer
fence, such as `::::`.

### Footnotes and definition lists

```markdown
The tomb was sealed in the year of the comet.[^1]

[^1]: Or so the priests claim.

Darkvision
: You see in dim light as if it were bright light.
```

### Links between pages

A link whose destination is a page's slug opens that page from anywhere in the same module or
campaign, and a heading can be linked directly:

```markdown
[Camp Vengeance](camp-vengeance)
[The ambush](camp-vengeance#the-ambush)
[See below](#the-ambush)
```

Every heading gets an anchor from its text: lowercase, accents dropped, and each run of anything
other than letters, digits and hyphens turned into a single hyphen — *The Ambush!* becomes
`#the-ambush`. Give a heading its own
with an attribute (`## The Ambush {#ambush}`) when you want one that survives a rename.

### Images

Tapping an image in a page opens it in the image viewer, from which you can show it on the player
screen. An image inside a link follows the link instead, and `{.no-preview}` after an image leaves it
untappable:

```markdown
![Floor plan](images/plan.jpg){.no-preview}
```

Wide tables scroll sideways rather than widening the page.

### The page editor

The page editor is a Markdown editor with highlighting. Its toolbar has Bold, Italic and Heading, and
two menus for what is fiddly to type:

- **Link** — *From Library…* links anything in your library, by its name, as many entries as you pick.
- **Image** — *Photo Library…*, *Choose File…* or *From Container…* (an image the module already
  has). New images are copied into the module's `images` folder. You can also paste an image.

**Preview** shows the rendered page beside the editor and follows it as you scroll.

### HTML pages

Pages written before Markdown support, and pages from older modules, are HTML. They still display
as they always have, and open in the same editor as HTML source, without the formatting toolbar.
In an HTML page, dice in ordinary text are not picked up — a roll has to be a link, such as
`<a href="/roll/2d6+3">2d6+3</a>`.

To switch a page to Markdown, tap the page's title in the editor and choose **Format**. **Convert**
rewrites the HTML as Markdown, keeping as HTML whatever Markdown cannot express; **Keep Text** changes
only the format. Converting back to HTML writes out the page as it displays, with content and dice
links as plain links.

## Content written for v4

Older content used curly-brace macros for links and dice instead of Markdown. It still imports and
still works, so nothing you own breaks — but write anything new as Markdown. It is the format the app
is built around now, and it stays readable if you ever open the file outside Encounter+.

## Where to go next

- [Campaigns & Modules](/guides/campaigns-and-modules/) — where pages live.
- [Dice & Roll Tables](/guides/dice/) — rolling, roll tables and dice settings.
- [Dice Expressions](/reference/dice-expressions/) — every formula, operator and modifier.
- [Game Systems](/guides/game-systems/) — what defines the content types you can link to.
