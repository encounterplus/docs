---
title: Dice Expressions
description: The full dice syntax Encounter+ understands — dice, arithmetic, and every modifier (kh, kl, dh, dl, r, ro, !, !o, cs, cf, df, sf).
---

Every roll in Encounter+ goes through the same parser, so the syntax on this page works wherever a
formula is accepted. For how rolling fits into play — the roller, roll tables, rolls in text — see
[Dice & Roll Tables](/guides/dice/).

## Where expressions are accepted

| Place | Notes |
| --- | --- |
| The dice roller's custom formula field | The full syntax |
| Dice in rendered text | Found automatically, or written as `[2d6+3](roll)` — see [Writing Content](/guides/writing-content/#dice) |
| A roll table's first column name | `d100`, `d20` — decides how rows are matched |
| Hit point formulas on a creature | `4d8+12` rolls average or random hit points |
| Initiative formulas | From the game system's initiative configuration |
| The web client chat | `/roll 2d6+3` or `/r 2d6+3` — see [Remote Play](/guides/remote-play/) |
| Roll links in content | `/roll/<formula>/<name>/<type>` |

Expressions are case-insensitive and whitespace is ignored, so `2D6 + 3` and `2d6+3` are the same.

## Dice

```
[count]d<faces>[modifier]
```

`count` is optional and defaults to 1, so `d20` and `1d20` are identical. `faces` is required.

```
d20        one twenty-sided die
4d6        four six-sided dice, summed
2d10       two ten-sided dice
100d6      one hundred six-sided dice
```

Any number of faces works, not just the physical dice — `d7`, `d3` and `d1000` are all valid.

### The bare modifier shorthand

An expression that is *only* a signed number is read as a d20 roll with that modifier — the common
case of tapping a `+7` in a stat block.

```
+7    →  d20 + 7
-2    →  d20 - 2
```

## Arithmetic

Dice and numbers can be combined with the usual operators:

| Operator | Meaning |
| --- | --- |
| `+` | Add |
| `-` | Subtract |
| `*`, `x`, `×` | Multiply |
| `/`, `÷` | Divide |
| `(` `)` | Group |

Multiplication and division bind tighter than addition and subtraction, and brackets override that.

```
2d6 + 3
1d8 + 1d6 + 4
(1d6 + 3) * 2
d6 x (100 + d6)
4d6 / 2
```

:::note[Whole numbers only]
Everything is integer arithmetic. Division truncates — `7/2` is `3` — and a division by zero is not
evaluated at all.
:::

## Modifiers

A modifier is written directly after the die, with no space. Most take an optional
[comparison](#comparison-operators) and a number; where one is omitted the default in the table
applies.

| Modifier | Name | Default | What it does |
| --- | --- | --- | --- |
| `kh[n]` | Keep highest | `kh1` | Keeps the `n` highest dice, discards the rest |
| `kl[n]` | Keep lowest | `kl1` | Keeps the `n` lowest dice, discards the rest |
| `dh[n]` | Drop highest | `dh1` | Discards the `n` highest dice |
| `dl[n]` | Drop lowest | `dl1` | Discards the `n` lowest dice |
| `r[cmp]<n>` | Reroll | `r1` | Rerolls any matching die, repeatedly, until it no longer matches |
| `ro[cmp]<n>` | Reroll once | `ro1` | Rerolls any matching die exactly once, keeping the new value whatever it is |
| `![cmp]<n>` | Explode | max face | Adds an extra die for every matching die, and keeps going while the new die also matches |
| `!o[cmp]<n>` | Explode once | max face | Adds one extra die for every matching die, and stops there |
| `cs[cmp]<n>` | Count successes | `cs1` | The result becomes the *number* of matching dice, not their sum |
| `cf[cmp]<n>` | Count failures | `cf1` | The result becomes the number of matching dice, counted as failures |
| `df[cmp]<n>` | Deduct failures | `df1` | Sums the dice, then subtracts 1 from the total for each matching die |
| `sf[cmp]<n>` | Subtract failures | `sf1` | Sums the dice, with each matching die subtracted instead of added |

Discarded and rerolled dice are not thrown away in the display — they stay in the roll detail with a
`☓` beside them, so you can see what the dice actually did.

### Comparison operators

`r`, `ro`, `!`, `!o`, `cs`, `cf`, `df` and `sf` all take an optional comparison in front of their
number:

| Written | Matches |
| --- | --- |
| `=` or nothing | Equal to |
| `>` | Greater than |
| `>=` | Greater than or equal |
| `<` | Less than |
| `<=` | Less than or equal |

So `r1` and `r=1` are the same, and `r<3` rerolls anything under 3.

### Examples

```
2d20kh1        advantage — roll two d20, keep the higher
2d20kl1        disadvantage
4d6dl1         ability score — roll four d6, drop the lowest
4d6r1          great weapon fighting — reroll 1s until they are not 1s
4d6ro<3        reroll 1s and 2s, once each
2d6!           exploding sixes, chaining
2d6!o          one extra die per six, no chain
1d10!>=8       explode on 8, 9 or 10
6d10cs>=7      count how many dice rolled 7 or better — a result of 3 is three successes
10d6sf<3       sum the dice, subtracting any that rolled under 3
```

:::caution[One modifier per die]
A die group takes a single modifier. `4d6dl1kh2` is not stacked — parsing stops at the second
modifier and the rest of the expression is dropped. Combine dice in separate groups instead, or pick
the one modifier that expresses what you want.
:::

## Advantage, disadvantage and criticals

The roller can upgrade an expression rather than making you rewrite it:

| Upgrade | Effect |
| --- | --- |
| **Advantage** | Every `d20` in the expression becomes `2d20kh1`; other dice are untouched |
| **Disadvantage** | Every `d20` becomes `2d20kl1` |
| **Critical** | Every die's count is doubled — `2d6+3` becomes `4d6+3` |

Advantage and disadvantage replace any modifier already on the d20, so a formula written with `kh`
by hand and then rolled with advantage does not compound.

## Roll names and types

A roll can carry a label and a type, which is what lets the roll log tell one roll from another and
what selects the dice theme it is rolled with.

The types are `attack`, `damage`, `heal`, `check` and `save`.

In Markdown, the label is the link title and the full form is a path:

```markdown
[2d6+3](roll "fire damage")
[+7](/roll/d20+7/Longsword/attack)
```

In the web client chat, the label goes in brackets, optionally with the type after a colon:

```
/roll 2d6+3 [Fire damage]
/roll d20+7 [Longsword: attack]
```

Under D&D 5E the app also guesses the type when none is given — a leading `+` reads as an attack, a
`d20` as a check, and a formula near the word *damage* as damage.

## Limits and edge cases

- **Dice count and faces** are each capped at 1,000,000.
- **Rerolling and exploding** stop after about 100 extra dice per die, so `d6!` on a run of sixes
  terminates rather than hanging.
- **Roll detail** — a group of more than 10 dice reports only its total; the individual rolls are not
  listed or sent to players.
- **Thousands separators** in a number are ignored: `1,000d6` is a thousand d6.
- **Automatic detection in text is narrower than the parser.** Prose is scanned for the plain
  `2d6+3` shape only, so an expression with `!`, `r`, `cs` or brackets in it has to be written as an
  explicit [`(roll)` link](/guides/writing-content/#writing-a-roll-yourself) to become tappable.
- **An unparseable expression** produces no roll at all rather than a partial one — in chat it comes
  back as *Invalid expression*.

## Where to go next

- [Dice & Roll Tables](/guides/dice/) — the roller, rolls in content, and roll tables.
- [Writing Content](/guides/writing-content/) — dice inside Markdown, and links to your own content.
- [Dice Roller Settings](/settings/dice-roller/) — rollers, random generator, sound and themes.
- [URL Scheme](/reference/url-scheme/) — opening the app with a link.
