---
title: Views
description: Building detail screens — layout, view types, data iteration, computed attributes, partials and the HTML renderer.
---

A **view definition** is the read-only detail screen for an entity type: the stat block, the spell
card, the character sheet. It lives at `views/<label>.json` and is rendered natively.

Reference: [ViewDefinition](/reference/schema/view-definition/).

## Anatomy

The root is a layout container; everything below it is a tree of views:

```json
{
  "spacing": 8,
  "padding": [16],
  "views": [
    {
      "type": "hStack",
      "spacing": 8,
      "views": [
        {
          "type": "vStack",
          "spacing": -1,
          "views": [
            { "style": "title",    "value": "{{name}}" },
            { "style": "subtitle", "value": "{{data.school | map: 'SpellSchool'}}" }
          ]
        },
        { "type": "image", "value": "/icons/spell/{{data.school}}.png", "height": 52 }
      ]
    },
    { "type": "divider" },
    { "type": "text", "value": "{{descr}}" },
    { "type": "tags", "attribute": "tags" }
  ]
}
```

The root accepts `type` (a layout type — `vStack` by default), `spacing`, `padding`, `alignment`,
`bgColor`, `bgImage`, `width`/`height`/`frame`, `views`, `bgViews` (drawn behind the content) and
`debug`.

## Values are templates

Almost every string a view renders is a [template](/system-development/templates/) evaluated
against the entity's context:

```json
{ "type": "text", "value": "{{data.size | map: 'Size'}} {{data.type | map: 'MonsterType'}}, {{data.alignment | map: 'Alignment'}}" }
```

A view whose rendered `value` is empty is **dropped**, along with, in most cases, its container.
That is why a stat block does not show a blank “Damage Resistances” line for a creature that has
none — no `visibleIf` is required for the common case.

## View types

**Layout** — `vStack`, `hStack`, `zStack`, `lazyVStack`, `flow`, `scroll`, `grid`, `gridRow`,
`spacer`, `divider`, `disclosureGroup`, `tabs`.

**Content** — `text`, `label`, `image`, `icon`, `tags`, `progress`, `statBlock`.

**Data-driven** — `list`, `table`, `tableRow`, `partial`, `field`.

**Interactive** — `button`, `buttonGroup`, `menuButton`, `checkbox`, `checkboxGroup`.

Common properties across all of them: `title`, `value`, `attribute`, `attributeType`, `style`,
`link`, `alignment`, `spacing`, `padding`, `color`, `bgColor`, `bgImage`, `borderWidth`,
`borderColor`, `borderEdges`, `cornerRadius`, `width`, `height`, `frame`, `imageResizeMode`,
`visibleIf`, `hiddenIf`, `action`, `custom`, `views`.

`statBlock` is a container that draws itself with the theme's stat-block styling — parchment
background, decorative top and bottom bars, the horizontal rules. Wrap a creature's stats in one
and the framing comes for free.

## Styles

`style` names an entry in the theme's `textStyles` (or `tableStyles` for a table, `buttonStyles`
for a button, and so on):

```json
{ "style": "title",    "value": "{{name}}" }
{ "style": "heading3", "value": "Actions" }
{ "style": "stats-body", "value": "{{data.speed}}" }
```

Keeping every typographic decision in the [theme](/system-development/themes/) rather than inline
on the view is what lets a system be restyled without touching its views.

## Iterating over data

A `list` renders its child views once per element of an array:

```json
{
  "type": "list",
  "attribute": "data.actions",
  "custom": { "divider": true },
  "views": [
    { "type": "partial", "value": "monster-feature" }
  ]
}
```

Inside the loop, paths are relative to the **element**, so `{{name}}` is the action's name, not the
creature's. `custom.divider` inserts a divider between elements, and
`custom.alternatingRowBackground` (`"even"` or `"odd"`) suppresses the row background on
alternating rows.

What the loop yields depends on what the attribute holds:

| `attribute` resolves to | Each iteration provides |
| --- | --- |
| an array of objects | the object itself |
| an array of scalars | `{ "value": … }` |
| a positive integer *n* | *n* iterations of `{ "value": 1 … n }` |
| an object, with `attributeType` set | `{ "key": …, "value": … }`, one per option of that type, in the type's order — including options the object has no entry for |

That last row is how ability scores render: the object `data.abilities` is walked in the order of
the `Ability` type, so STR, DEX, CON, INT, WIS, CHA come out in the right sequence and a missing
score still gets a row.

An empty array renders nothing at all, title included.

### Tables

A `table` with an `attribute` treats its first child view as the header row and its last as the
row template:

```json
{
  "type": "table",
  "style": "clean",
  "attribute": "data.abilities",
  "attributeType": "Ability",
  "views": [
    { "type": "tableRow", "views": [ { "value": "ABILITY", "style": "sheet-label" }, { "value": "MOD", "style": "sheet-label" } ] },
    { "type": "tableRow", "views": [ { "value": "{{key | map: 'Ability'}}" }, { "value": "{{value | modifier}}" } ] }
  ]
}
```

Without an `attribute`, a table simply lays out the rows you give it.

## Context

By default a view sees the **local** context — the entity at the top level, the element inside a
loop. `context` changes that:

```json
{ "context": "global" }   // the whole entity, even inside a loop
{ "context": "mixed" }    // the whole entity, with the local item available as `self`
```

`mixed` is the one to reach for when a row needs both its own values and something from the
creature that owns it.

## Conditional views

```json
{ "type": "partial", "value": "monster-stats-new", "visibleIf": "attributes.ruleset == '5.5e'" },
{ "type": "partial", "value": "monster-stats",     "visibleIf": "attributes.ruleset == '5e' or attributes.ruleset == null" }
```

This is the shape used to ship two stat block layouts in one system and switch between them per
entity.

## Partials

`views/partials/` holds two kinds of reusable fragment.

**View partials** are `.json` files containing a single view, included by name:

```json
{ "type": "partial", "value": "monster-stats" }
```

Adding an `attribute` scopes the partial to a sub-object:

```json
{ "type": "partial", "value": "character-ability", "attribute": "data.abilities.str" }
```

**Text partials** are `.md` files of Markdown-with-templating, included from inside a template
string:

```
{% include 'spell-primary.md' %}
{% include 'activation.md' data.activation %}
```

They are the right tool for prose-shaped output — the “**Casting Time:** 1 action” block of a
spell card is a text partial, not fifteen nested stacks. And because a form's summary row can
include the same file, the editor and the detail view stay phrased identically. See
[Templates](/system-development/templates/#partials).

## Computed attributes

`views/transforms/<label>.json` is a [DataTransform](/reference/schema/data-transform/): a recipe
that enriches an entity's context before any view reads it. Derived values belong here, not in
storage.

```json
{
  "attributes": [
    {
      "data.xp": "#{{data.cr | valueMap: 'ChallengeRatingToXP'}}",
      "data.armor": "#{{data.ac | integer}}",
      "data.passivePerception": "#{% if data.passivePerception %}{{data.passivePerception}}{% else %}{% eval %}10 + {{data.abilities.wis | modifier | default: 0}}{% endeval %}{% endif %}",
      "data.proficiencyBonus": "#{% if data.proficiencyBonus %}{{data.proficiencyBonus}}{% else %}{{data.cr | map: 'ProficiencyBonus', '0'}}{% endif %}"
    },
    {
      "data.initiativeValue": "# 10 + {{data.initiativeBonus}}"
    }
  ]
}
```

Three things to note:

- A rendered result prefixed with `#` is **evaluated as a formula**, so arithmetic works.
- `attributes` is an **array of groups**, processed in order. A later group can read what an
  earlier one computed — that is why `data.initiativeValue` sits in its own group, after
  `data.initiativeBonus` exists.
- The pattern `{% if stored %}{{stored}}{% else %}{{derived}}{% endif %}` gives a computed default
  that an author can override by filling the field in.

A transform also has `references` (key paths whose entity references are resolved and inlined
before attributes are computed, so a character's class data is readable) and `modifiers` (key
paths from which global modifiers are gathered and applied). Transforms follow the same
`extends` fallback as views: an NPC with no transform of its own uses the Monster one.

Because everything a transform computes is present on the context, views, list subtitles and
combatant details all read the same values.

## Compact views

`views/<label>-compact.json` is a second layout for the same type, chosen automatically when the
view is rendered into a narrow enough space — a floating panel over the battle map, a secondary
column. Omit it and the full view is used at every width.

## The HTML renderer

A type can be rendered by a web view instead of native views. Set it in `config.json`:

```json
"entities": {
  "Character": {
    "view": {
      "renderer": "html",
      "template": "character",
      "updateMode": "reload"
    }
  }
}
```

The template is `views/<name>.html` — a full Stencil template with the entity context available,
free to pull in CSS and JavaScript from the system's `assets/` folder. `updateMode` controls
refresh behavior: `load` (once), `reload` (every appearance), `event` (on change) or `none`.

Renderer values are `native` (the default), `html`, `custom` and `sheet`.

Use it when a layout genuinely wants a browser — a full character sheet with interactive
scripting. Native views are faster, themed automatically and work on the player screen and remote
clients without extra work, so they are the better default.

## Debugging

Set `"debug": true` on a view definition to visualize its layout. A file that fails to decode is
replaced with an error view that renders the decoder's message where the content would be, and a
transform that fails to decode writes its message to `data.error`.

## Where to go next

- [Templates](/system-development/templates/) — the filters and tags used throughout this page.
- [Themes](/system-development/themes/) — where `style` names come from.
- [ViewDefinition reference](/reference/schema/view-definition/) — every key and enum value.
