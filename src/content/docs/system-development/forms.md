---
title: Forms
description: Building the editors — sections, fields, conditional visibility, lists, nested forms and partials.
---

A **form definition** is the editor for an entity type. The app has no hand-written editor for a
creature or a spell; it reads `forms/<label>.json` and builds one.

Reference: [FormDefinition](/reference/schema/form-definition/).

## Anatomy

A form is a tree three levels deep: **form → sections → fields**.

```json
{
  "title": "Spell",
  "sections": [
    {
      "type": "group",
      "title": "Common.General",
      "fields": [
        { "title": "Common.Level",  "type": "picker", "attribute": "data.level",  "attributeType": "SpellLevel" },
        { "title": "Spell.School",  "type": "picker", "attribute": "data.school", "attributeType": "SpellSchool" },
        { "title": "Spell.Ritual",  "type": "toggle", "attribute": "data.ritual" }
      ]
    }
  ]
}
```

Titles are localization keys, so `Common.Level` renders as whatever `lang/<code>.json` says. See
[Localization](/system-development/types/#localization).

### Tabs

A form with `tabs` instead of `sections` becomes a tabbed editor, each tab a form of its own:

```json
{
  "title": "Character",
  "tabs": [
    { "title": "Main",   "icon": "person",   "sections": [ /* … */ ] },
    { "title": "Spells", "icon": "wand.and.stars", "sections": [ /* … */ ] }
  ]
}
```

`icon` is an SF Symbol name.

## Attribute paths

`attribute` is a dot path into the entity, and it is the only connection between a field and
storage:

```json
{ "type": "number", "attribute": "data.hp.maximum" }
{ "type": "picker", "attribute": "data.abilities.str" }
{ "type": "text",   "attribute": "name" }
```

Intermediate objects are created as needed — writing `data.hp.maximum` on an entity with no `hp`
object produces one. Nothing validates the path against a schema, because there is no schema; the
shape of `data` is whatever your forms write and your views read. Keeping the two in agreement is
your job, and a spelling mistake in a path shows up as a field that saves into a place nothing
reads.

Inside a **nested form or a list item** the path is relative to that item, not to the entity —
`"attribute": "unit"` inside a casting-time subform writes `data.activation.unit`.

## Section types

| `type` | Behavior |
| --- | --- |
| `group` | The default. A titled block of `fields`. |
| `list` | A repeatable array. Rows are added and removed by the user; `form` defines the row editor. |
| `picker` | The section *is* a picker — no `fields`, just `attribute` and `attributeType`. |
| `multiPicker` | Same, allowing multiple selections. |

A `picker` section renders as a full-width selector with its own screen, which is why the D&D 5E
forms use section-level pickers for primary choices and field-level pickers for secondary ones.

## Field types

| `type` | Input |
| --- | --- |
| `text` | Single-line text. The default when `type` is omitted. |
| `textArea` | Multi-line text, Markdown-aware. |
| `number` | Integer stepper/keyboard. |
| `decimal` | Fractional number. |
| `toggle` | Boolean switch. |
| `checkbox` | Boolean checkbox. |
| `picker` | One value from an `attributeType`. |
| `multiPicker` | Several values from an `attributeType`. |
| `menu` | Inline menu selection. |
| `colorPicker` | A color. |
| `tags` | A free list of strings, or of entity references. |
| `reference` | A link to another entity. |
| `attributes` | An editor for the entity's `attributes` store. |
| `modifiers` | An editor for the entity's `modifiers`. |
| `list` | A repeatable array, at field level. |
| `form` | A nested form behind a summary row. |
| `hStack` | Lays its child `fields` out side by side. |

Supporting keys: `title`, `placeholder`, `detail` (subtitle text), `units` (a unit label on
numeric fields, which participates in [measurement conversion](/system-development/config/#measurement)),
`defaultValue`, `alignment`, `filter` (restricts a picker or reference to matching entities), and
`custom` for anything type-specific.

## Pickers and types

A picker's options come from a named type. Everything in
[Types & Collections](/system-development/types/) applies:

```json
{ "title": "Common.Size", "type": "picker", "attribute": "data.size", "attributeType": "Size" }
```

`attributeType` may also name an **entity type** rather than a value set, in which case the picker
offers the user's content of that type:

```json
{
  "title": "Spell.Classes",
  "type": "tags",
  "attribute": "data.classes",
  "attributeType": "Class",
  "custom": { "includeSource": true }
}
```

## Conditional visibility

`visibleIf` and `hiddenIf` take a template expression, evaluated against the current form data.
Both a bare comparison and a full template work:

```json
{ "visibleIf": "{{ unit == 'reaction' }}" }
{ "visibleIf": "{% if 'M' in data.components %}true{% endif %}" }
{ "hiddenIf": "level < 3" }
```

They can sit on a section or on a field. Use them to keep forms honest — the components detail box
only appears once a material component is selected, the range value only once the range type calls
for a number.

## Lists

A `list` section stores an array and gives each element the form under `form`:

```json
{
  "title": "Monster.Actions",
  "type": "list",
  "attribute": "data.actions",
  "form": {
    "title": "Monster.Action",
    "partial": "monster-feature"
  }
}
```

`custom.itemDetail` sets the subtitle shown on each row, rendered against that row's data:

```json
"custom": { "itemDetail": "{{ level | ordinal | default: '1st' }} level" }
```

## Nested forms

A `form` field is a single value edited on its own screen, presented in the parent as a summary
row. `text` is the summary:

```json
{
  "title": "Spell.CastingTime",
  "type": "form",
  "attribute": "data.activation",
  "text": "{% include 'activation.md' data %}",
  "form": {
    "title": "Spell.CastingTime",
    "sections": [
      { "type": "group", "fields": [ { "title": "Common.Time", "type": "number", "attribute": "time" } ] },
      { "title": "Common.Unit", "type": "picker", "attribute": "unit", "attributeType": "ActivationUnit" },
      {
        "type": "group",
        "visibleIf": "{{ unit == 'reaction' }}",
        "fields": [ { "placeholder": "Common.Condition", "type": "textArea", "attribute": "condition" } ]
      }
    ]
  }
}
```

Note the summary reuses the same [text partial](/system-development/templates/#partials) the
detail view uses, so the editor and the stat block phrase the casting time identically.

### Copying from a referenced entity

When a nested form or list item points at another entity — a character's species, class or feat —
`custom.map` copies fields out of the referenced entity onto the owning one when it is selected:

```json
{
  "type": "form",
  "attribute": "data.species",
  "attributeType": "Species",
  "custom": {
    "map": {
      "size": "data.size",
      "speed": "data.speed",
      "traits": "data.traits",
      "modifiers": "modifiers"
    }
  },
  "form": { "title": "Species", "partial": "character-species" }
}
```

Left side is the path in the referenced entity, right side the destination on the character.

## Partials

`forms/partials/*.json` hold reusable form fragments, referenced by file name:

```json
"form": { "title": "Monster.Action", "partial": "monster-feature" }
```

A partial is a form definition like any other. The D&D 5E system uses one `monster-feature`
partial for traits, actions, bonus actions, reactions, legendary actions and mythic actions — six
list sections, one editor.

Split a form into partials as soon as the same block appears twice. It is the difference between
one editor to fix and six.

## The system settings form

`forms/settings.json` is a form like any other, but it edits the **system's own settings** rather
than an entity. It is what appears under **Settings → Current System → System Settings**.

```json
{
  "title": "Settings",
  "sections": [
    {
      "type": "group",
      "title": "Common.Locale",
      "fields": [
        { "type": "picker", "title": "Common.Language",    "attribute": "language",    "attributeType": "SystemLanguage" },
        { "type": "picker", "title": "Common.Measurement", "attribute": "measurement", "attributeType": "MeasurementSystem",
          "defaultValue": "imperial" }
      ]
    }
  ]
}
```

Attributes here are paths into the settings object, and those settings are merged over
`config.json` when the system loads — so `"attribute": "combat.initiative.autoRoll"` lets the user
override the config's default. See [Configuration](/system-development/config/).

Saving reloads the system.

## Debugging

A form file that fails to parse is replaced by an error form that displays the decoder's message.
If an editor opens showing Swift decoding text, that is the file naming the key it could not read.

## Where to go next

- [Views](/system-development/views/) — displaying what these forms captured.
- [Templates](/system-development/templates/) — the expression language in `visibleIf` and `text`.
- [FormDefinition reference](/reference/schema/form-definition/) — every key and every enum value.
