---
title: Templates
description: The templating language shared by forms, views, filters and config — tags, filters, partials and formulas.
---

Nearly every string in a system definition is a template. The same language runs in view values,
form summaries, `visibleIf` conditions, filter labels, collection subtitles, combatant details and
data transforms — so learning it once covers the whole system.

The engine is [Stencil](https://stencil.fuller.li/), a Django/Liquid-style templating language,
extended with a set of filters and tags specific to this app.

## Basics

```
{{ name }}                        variable
{{ data.abilities.str }}          dot path
{{ data.classes | join: ', ' }}   filter with an argument
{% if data.level > 0 %}…{% endif %}
{% for class in data.classes %}{{ class.name }}{% endfor %}
```

Stencil's own tags and filters (`if`/`elif`/`else`, `for` with `forloop.first`/`forloop.last`,
`filter`, `default`, `join`, `uppercase`, `lowercase`, `capitalize`, `in`) are all available.

Whitespace control uses the `-` suffix, which matters when generating Markdown:

```
{% if data.ritual -%}
**Ritual**
{% endif -%}
```

The context available to a template is described in
[Entity Definitions](/system-development/entities/#the-rendering-context).

## Filters

### Types and localization

| Filter | Does |
| --- | --- |
| `map: 'Type'[, separator]` | Looks a key up in a named type and returns its **display label**. Given an array, maps each element and joins with `separator` (default `", "`). |
| `valueMap: 'Type'` | Looks a key up in a named type and returns its **raw value** — for lookup tables like `ChallengeRatingToXP`. |
| `l` | Localizes a string key: `{{ 'Common.HitPoints' \| l }}`. |
| `localize` | Localizes with the current context available for interpolation. |

### Numbers

| Filter | Does |
| --- | --- |
| `signed` | Prefixes a `+` on non-negative numbers: `3` → `+3`. |
| `modifier` | Converts an ability score to its modifier: `14` → `+2`. Also formats a modifier object. |
| `ordinal` | `3` → `3rd`. |
| `format` | Locale-aware number formatting. |
| `integer` | Takes the leading numeric part of a string: `"15 (chain mail)"` → `15`. |
| `math: 'sum'` | Sums an array of numbers. |
| `diceAverage` | The average roll of a die of the given size. |
| `units: 'ft'` | Formats with a unit, converting between measurement systems — see [Configuration](/system-development/config/#measurement). |

### Strings

| Filter | Does |
| --- | --- |
| `prefix: 's'` / `suffix: 's'` | Adds text, but **only if the value is non-empty**. |
| `wrap: 's'` | Wraps the value in the given string on both sides. |
| `brackets[: style]` | Wraps in brackets — `round` (default), `square`, `curly`, `angle`. |
| `space` | Appends a single space if non-empty. |
| `trim` / `trimLines` | Trims whitespace, overall or per line. |
| `capitalizeFirstLetter` | Uppercases the first character only. |
| `first` | First character of a string, or first element of an array. |
| `urlencode` | Percent-encodes for use in a URL. |
| `nameWithSource[: style]` | Formats a name plus its source — `short` (default), `long`, `none`. |

The conditional behavior of `prefix`, `suffix`, `brackets` and `space` is what makes one-line
subtitles readable. This produces no stray commas or empty parens when fields are missing:

```
{{data.size | map: 'Size'}}{{data.type | map: 'MonsterType' | prefix: ' '}}{{data.typeDetail | brackets | prefix: ' '}}{{data.alignment | map: 'Alignment' | prefix: ', '}}
```

### Links, dice and Markdown

| Filter | Does |
| --- | --- |
| `link: 'path'` | Turns a value into a Markdown link, resolving name/source pairs into content links. |
| `roll[: name[, type]]` | Turns a dice expression into a tappable roll link. |
| `md` | Renders Markdown to HTML, with dice expressions linked. |
| `diceFormula` | Substitutes variables into a dice expression and simplifies it. |
| `formula` | Substitutes variables into an expression without simplifying. |
| `eval` | Renders the string as a template, then evaluates the result as arithmetic. |
| `resolvePath` | Resolves a relative path against the system or container folder. |
| `json` | Dumps the value as pretty-printed JSON — useful while debugging. |

## Tags

Beyond Stencil's own, these are available:

### `include`

```
{% include 'spell-range.md' %}
{% include 'activation.md' data.activation %}
```

The optional second argument pushes a sub-object as the context for the included file, and it
accepts a dot path. Partials resolve against `views/partials/`.

### `eval`

Evaluates its body as arithmetic after rendering it:

```
{% eval %}10 + {{ data.abilities.wis | modifier | default: 0 }}{% endeval %}
```

Non-numeric results render as `Undef`, which is a useful signal that a path is wrong.

### `set`

Binds a value for later reuse:

```
{% set profBonus %}{{ data.cr | map: 'ProficiencyBonus' }}{% endset %}
{{ profBonus }}
```

or in short form, `{% set name value %}`.

### `macro` and `call`

Define a reusable fragment and invoke it — the template-level equivalent of a function, for
repetition too small to justify its own partial file.

### `markdown`

Renders its body as Markdown to HTML, with dice expressions turned into roll links. An optional
argument names the roll, either as a quoted literal or as a context path:

```
{% markdown "Common.Damage" %}{{ data.damage }}{% endmarkdown %}
```

### `trim`

Strips stray separators — spaces, commas and semicolons — from the start and end of every line of
its body. It exists for lists assembled conditionally, where the separators between missing items
would otherwise be left behind.

## Formulas

In [data transforms](/system-development/views/#computed-attributes), a rendered value beginning
with `#` is evaluated as arithmetic rather than kept as text:

```json
"data.xp": "#{{ data.cr | valueMap: 'ChallengeRatingToXP' }}",
"data.initiativeValue": "# 10 + {{ data.initiativeBonus }}"
```

## Conditions

`visibleIf` and `hiddenIf` on a form section, form field or view accept either a template that
renders to something truthy, or a bare comparison:

```json
{ "visibleIf": "{{ unit == 'reaction' }}" }
{ "visibleIf": "{% if 'M' in data.components %}true{% endif %}" }
{ "visibleIf": "attributes.ruleset == '5.5e'" }
{ "hiddenIf": "level < 3" }
```

## Partials

Two kinds, both living under `views/partials/`:

- **`.md` text partials**, included from inside a template with `{% include %}`. Markdown with
  templating in it, for prose-shaped output.
- **`.json` view partials**, included from a view with `{"type": "partial", "value": "name"}`. See
  [Views](/system-development/views/#partials).

A text partial that formats a spell's range:

```
{% if data.rangeType %}{{ data.rangeType | map: 'SpellRange' }}{% else %}{{ data.range | units: 'ft' }}{% endif %}
```

Included by the detail view, by the compact view, and by the form's summary row — one definition
of how a range is worded.

## Practical notes

- **Missing values render as empty**, and an empty view is dropped. Lean on that rather than
  guarding every line with `visibleIf`.
- **`default:` is your friend**: `{{ data.hp.current | default: 0 }}`.
- **Use `json` to debug.** `{ "type": "text", "value": "{{ data | json }}" }` in a view dumps
  exactly what the context holds — including everything the transform computed.
- **Templates are rendered against cached contexts.** After changing a transform, reload the
  system so contexts are rebuilt.
