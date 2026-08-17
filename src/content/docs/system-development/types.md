---
title: Types & Collections
description: Named value sets, their ordering, lookup tables, custom attributes and localization — the vocabulary a system's forms, views and filters share.
---

Pickers need options. Filters need option lists. Stat blocks need to turn `"evocation"` into
“Evocation”. All of that comes from one place: the system's **types**.

## `types.json`

A map of type names to value sets. Each value set maps a **stored key** to a **display value**:

```json
{
  "SpellSchool": {
    "abjuration": "SpellSchool.Abjuration",
    "conjuration": "SpellSchool.Conjuration",
    "evocation": "SpellSchool.Evocation"
  },
  "Size": {
    "T": "Size.Tiny",
    "S": "Size.Small",
    "M": "Size.Medium"
  }
}
```

The key is what an entity stores in its `data`. The value is what is shown — and because it is
run through localization, the convention is to make it a localization key rather than literal
text, and to put the actual words in `lang/`.

Once a type exists, everything can point at it by name:

```json
{ "type": "picker", "attribute": "data.school", "attributeType": "SpellSchool" }
```
```json
{ "attribute": "data.school", "attributeType": "SpellSchool", "title": "Spell.School" }
```
```
{{ data.school | map: 'SpellSchool' }}
```

### Ordering

Options are sorted **by display name**, using a numeric-aware comparison, unless
`collections.json` says otherwise. That is fine for alphabetical lists and wrong for anything with
an inherent order — sizes, spell levels, rarities. See below.

### Numeric keys

If *every* key in a value set is numeric, the keys are converted to numbers. That is what lets
`SpellLevel` be looked up with the integer stored in `data.level`:

```json
"SpellLevel": {
  "0": "SpellLevel.Cantrip",
  "1": "SpellLevel.1st-Level",
  "2": "SpellLevel.2nd-Level"
}
```

Mixing numeric and non-numeric keys leaves everything as strings, so `ChallengeRating` — which has
`"1/8"` in it — stays textual.

### Option details

A picker row can show a subtitle under its label. It comes from the display value's localization
key with `.detail` appended, so `"condition": "RuleType.Condition"` picks up a
`RuleType.Condition.detail` string from `lang/` if one exists. No extra declaration is needed;
add the key and the subtitle appears.

### Lookup tables

A value set does not have to hold display text. When the value is data, the type becomes a lookup
table, read with `valueMap` instead of `map`:

```json
"ChallengeRatingToXP": { "0": 10, "1/8": 25, "1/4": 50, "1/2": 100, "1": 200 },
"ProficiencyBonus":    { "0": 2, "1": 2, "5": 3, "9": 4, "13": 5, "17": 6 }
```

```
{{ data.cr | valueMap: 'ChallengeRatingToXP' }} XP
```

The distinction is worth internalizing: **`map` returns the label, `valueMap` returns the raw
value.**

### Built-in types

Some types are injected by the app before yours are read, and can be used without declaring them:
`SystemLanguage`, `MeasurementSystem`, `Role`, `InitiativeGroupType`, `InitiativeRollType`,
`DurationType`, `DurationUnit`, and `Entities` (the list of loadable entity types). They are
mainly useful in `forms/settings.json`.

### `custom-types.json`

Same format, loaded after `types.json` and merged over it. A key present in both wins from
`custom-types.json`. Use it for values you expect a user to extend — extra languages, extra damage
types — so a system update replacing `types.json` does not overwrite them.

## `collections.json`

Two unrelated jobs share this file, distinguished by whether the value is an array or an object.

### Ordering a type

An **array** of keys reorders an existing type into exactly that sequence:

```json
{
  "Size": ["T", "S", "M", "L", "H", "G", "C"],
  "SpellLevel": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
  "ItemRarity": ["common", "uncommon", "rare", "veryrare", "legendary", "artifact", "unknown"]
}
```

Without this, `Size` would list as Colossal, Gargantuan, Huge, Large… in alphabetical order.

Keys omitted from the array are dropped from the type, which is also a way to hide options
without deleting them from `types.json`.

If the named type does **not** exist in `types.json`, a new one is created whose options are the
raw values, unlocalized. That is a convenient way to declare a simple ordered list:

```json
{ "Ability": ["str", "dex", "con", "int", "wis", "cha"] }
```

### Mapping one type onto another

An **object** of arrays declares a mapping — a grouping of one type's keys under another's:

```json
{
  "ItemTypeCategoryMapping": {
    "armor":     ["lightArmor", "mediumArmor", "heavyArmor", "shield"],
    "weapon":    ["meleeWeapon", "rangedWeapon", "ammunition"],
    "magicItem": ["potion", "ring", "rod", "scroll", "staff", "wand", "wondrousItem"]
  }
}
```

This is what drives cascading pickers: choose a category, and the second picker offers only the
item types belonging to it.

## Custom attributes

`custom-attributes.json` declares extra keys for an entity's `attributes` store — the flat,
queryable side of an entity, as opposed to the free-form `data`:

```json
[
  { "key": "campaignArc", "name": "Campaign Arc", "type": "String" },
  { "key": "threatLevel", "name": "Threat Level", "type": "Int" }
]
```

`name` is localized like any other display string. Keep the list small; `data` is the right home
for ruleset mechanics, and `attributes` for the handful of values that need to be read cheaply
outside the rendering path.

## Localization

`lang/<code>.json` is a flat map of key to string:

```json
{
  "Entity.Monster": "Monster",
  "SpellSchool.Evocation": "Evocation",
  "RuleType.Condition": "Condition",
  "RuleType.Condition.detail": "A temporary state affecting a creature",
  "Common.HitPoints": "Hit Points",
  "Common.HP": "HP"
}
```

Which file loads is decided by the system's `language` setting, falling back to the device
language and then to `en`.

Everywhere a system definition takes a display string — a form field `title`, a section header, a
view `title`, a filter `title`, a type's display value — that string is looked up as a
localization key first, and used verbatim if no entry exists. So `"title": "Spell.School"` is
translatable and `"title": "School"` is not; both work.

In templates, the `l` filter localizes explicitly:

```
{{ 'Common.HitPoints' | l }}
```

Adding a language is adding a file. `lang/fr.json` with the same keys, and the system offers
French in its settings.

:::tip
Because type display values are localization keys, `map` output is translated for free. A stat
block written as `{{ data.size | map: 'Size' }}` needs no changes to work in another language.
:::

## Where to go next

- [Forms](/system-development/forms/) — where `attributeType` is consumed.
- [Templates](/system-development/templates/) — `map`, `valueMap`, `l` and the rest.
- [Configuration & Filters](/system-development/config/) — filters built on these types.
