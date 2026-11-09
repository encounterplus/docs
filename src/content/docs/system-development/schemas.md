---
title: Model Schemas
description: Declaring the keys an entity type may store in its data — types, lists, maps, entity copies and options — how saves are checked against them, and the files generated for sheets.
---

:::caution[Preview]
Model schemas exist for interactive [character sheets](/system-development/sheets/) and, like them,
are a preview: the format may still change between releases, without a deprecation period. Writing
one for your system is safe — a schema only ever checks what is saved, it never changes stored
data — but expect to adjust it when the app updates.
:::

An entity's `data` has whatever shape your forms write and your views read. A **model schema**
writes that shape down: which keys an entity type may store, and what kind of value each one
holds. With a schema in place, the app checks every save of that type against it, and generates
type definitions a sheet or a code editor can use.

Schemas are optional and per entity type. A type without one saves exactly as before.

A schema declares **writable keys only**. Values a view computes — a total, a modifier, a tier
derived from level — are not part of it; they belong in
[data transforms](/system-development/views/#computed-attributes), which only shape what a view
shows and never what is stored.

## Where schemas live

```
systems/<id>/
├── schemas/
│   ├── <label>.json        # the schema of one entity type
│   └── partials/*.json     # object types shared by every schema
└── cache/
    └── schemas/            # generated from the above when the system loads
```

A schema is found by the entity definition's `label`, like its form and view: the `character`
type uses `schemas/character.json`. An [extending type](/system-development/entities/#extends)
without a schema of its own uses its parent's.

Schema files are JSON5, like every other system file, so comments and trailing commas are fine.

## A first schema

```json
// schemas/character.json
{
  "defs": {
    "Track": {
      "current": { "type": "integer", "min": 0, "max": 12, "play": true },
      "maximum": { "type": "integer", "min": 0, "max": 12 }
    }
  },
  "data": {
    "level": { "type": "integer", "min": 1, "max": 10, "default": 1 },
    "pronouns": "string",
    "hp": "Track",
    "stress": "Track",
    "traits": { "map": "integer", "keys": "Trait" },
    "experiences": { "type": ["Experience"], "ids": true },
    "class": { "ref": "Class", "properties": { "domains": ["Domain"] } },
    "notes": "text"
  }
}
```

The file has two keys:

- **`data`** declares the keys of the entity's `data`, each mapped to its declaration.
- **`defs`** (optional) names object types the schema uses more than once, such as `Track` above.

A `$schema` key is allowed and ignored. Any other key at the top level is an error.

## Declarations

Every declared key takes one of three forms:

| Form | Example | Meaning |
| --- | --- | --- |
| a type name | `"notes": "text"` | a value of that type |
| a list | `"languages": ["Language"]` | a list of values of one type |
| an object | `"level": { "type": "integer", "min": 1 }` | a declaration with options |

An object is **always** a declaration, never an inline set of data keys. It takes exactly one of
these keys, plus [options](#options):

| Key | Declares |
| --- | --- |
| `type` | a value of a named type, or a list: `{ "type": ["Experience"], "ids": true }` |
| `properties` | an inline object: `{ "properties": { "current": "integer" } }` |
| `map` | an object whose keys are chosen by the data — see [Maps](#maps) |
| `ref` | a copy of another entity — see [Entity copies](#entity-copies) |

This keeps every data key free to use: Daggerheart's weapons store a `type`, and inside
`properties` that is just a key like any other. There is no `"type": "object"` — an inline object is
written with `properties`.

Unknown keys in a declaration are errors, so a misspelt option is reported rather than ignored.
`variants`, `access` and `accept` are reserved for later versions of the format.

## Types

A type name is looked up in this order:

1. a **primitive** (below);
2. a **definition** — the schema's own `defs`, or a [partial](#partials);
3. an **enum** — a value set from [`types.json`](/system-development/types/).

A name that is both a definition and an enum is an error: rename the definition. Entity names are
never types on their own — a copy of an entity is declared with [`ref`](#entity-copies).

### Primitives

| Type | Holds |
| --- | --- |
| `string` | short, single-line text |
| `text` | long-form text; Markdown or HTML is up to your system, its syntax is never checked |
| `integer` | a whole number |
| `number` | any number, whole numbers included |
| `boolean` | `true` or `false` |
| `dice` | a dice formula, such as `2d6+3` — stored as text |
| `url` | a reference to a file or page, as content stores it: absolute, `/`-prefixed for the system folder, or relative to the container |

The names follow JSON Schema where it has one. Note that two of them differ from the
[form field types](/system-development/forms/#field-types) of the same purpose: a form's `number`
field edits an `integer`, and a form's `text` field edits a `string`.

`object` is reserved, and none of these names can be used for a definition.

### Enums

Any value set from `types.json` (and `custom-types.json`) is a type:

```json
"trait": "Trait",
"tier": "Tier"
```

The set's keys are **suggestions, not a closed list**. Pickers offer them and views show their
labels, but a value the set doesn't list is saved too: homebrew, or content from a playtest that is
ahead of your system. A domain card can name a new domain before `types.json` knows it.

Keys are stored the way `types.json` reads them, so a set whose keys are
[all numeric](/system-development/types/#numeric-keys), like `Tier`, stores numbers. A value
outside such a set is stored as a number when it is one (`"5"` becomes `5`), and as text otherwise.
Only values that can't be a key are refused: booleans, fractions, objects.

[Map keys](#maps) drawn from a set are different: they stay closed, since your system lists and
labels exactly those keys.

### Definitions

A `defs` entry, and each entry of a partial file, is written like `data` — its keys mapped straight
to their declarations, without a `properties` wrapper:

```json
"defs": {
  "Experience": {
    "name": "string",
    "bonus": { "type": "integer", "min": 0, "default": 2 }
  }
}
```

A definition can use other definitions, but not itself, directly or through another one. Every
`defs` entry is checked when the schema loads, whether anything uses it or not.

### Partials

Object types more than one schema needs go into `schemas/partials/*.json`, a file of definitions:

```json
// schemas/partials/common.json
{
  "Feature": {
    "name": "string",
    "text": "text"
  }
}
```

Every schema of the system can use them by name. A partial can use primitives, enums and other
partials, but not a schema's own `defs`. A name declared by two partial files keeps the first, in
file name order, and the second is reported.

## Objects

Data keys inside an object can't be empty, and can't contain `.`, `[` or `]`, which separate the
parts of a [path](#paths).

```json
"thresholds": { "properties": { "major": "integer", "severe": "integer" } },
"armor": "Thresholds"
```

## Lists

A list declares one item type, and what it holds decides what kind of list it is:

- **Primitives and enums make a set** — `["Language"]`, `["string"]`. Duplicates are dropped on
  save.
- **Objects make a list of items** — `["Experience"]`, or `[{ "properties": { … } }]`.

A list can't hold lists or maps. Options go on the list, never on its item:

```json
"experiences": { "type": ["Experience"], "ids": true }
```

### Items with ids

By default list items are addressed by position, which is all most lists need — a monster's
features, a spell's damage parts. A list that a sheet edits item by item, where items move, can
declare **`ids`**. Each item then carries an `id`, which the app assigns when the item is first
saved and which can't be written directly. Items already stored without one get theirs the next
time they are edited.

**`tree`** makes the items a tree, the way a form's tree list stores them. It implies `ids`, and
each item also carries `parentId` and `container`.

## Maps

A map is an object whose keys are chosen by the data, with every value of the same type:

```json
"traits": { "map": "integer", "keys": "Trait" },
"counters": { "map": "integer" }
```

With **`keys`**, the keys must be keys of that enum. Without it, any key is allowed that would be
a valid [object key](#objects). The value can be any declaration, options included:

```json
"traits": { "map": { "type": "integer", "min": -5, "max": 10 }, "keys": "Trait" }
```

## Entity copies

When a form copies another entity onto this one — a character's class, ancestry or armor — the
copy is declared with **`ref`**, naming the entity type as `entities.json` writes its `name`:

```json
"class": {
  "ref": "Class",
  "properties": {
    "domains": ["Domain"],
    "evasion": "integer",
    "features": ["Feature"]
  }
}
```

Every copy carries the entity's `name` (a `string`) and `reference` (a `url` pointing at it)
without declaring them. `properties` declares whatever else the copy holds — usually the keys your
form's [`custom.map`](/system-development/forms/#copying-from-a-referenced-entity) copies.

A list of copies works the same way:

```json
"weapons": { "type": [{ "ref": "Weapon", "properties": { "damage": "dice", "active": "boolean" } }], "ids": true }
```

## Options

| Option | On | Meaning |
| --- | --- | --- |
| `default` | primitives, enums, sets | the value a missing key stands for, carried into the generated files. Nothing applies it: a missing key stays missing in stored data and in what a sheet reads |
| `min`, `max` | `integer`, `number` | the allowed range; a value outside it is refused, never clamped |
| `label` | anything | a display label, as a localization key or plain text |
| `description` | anything | a note for authors, carried into the generated files |
| `play` | anything | marks play state — hit points, conditions, slots used — rather than part of the build |
| `ids` | lists of objects | items carry an `id`; see [Items with ids](#items-with-ids) |
| `tree` | lists of objects | items form a tree; implies `ids` |

A `default` must be a valid value of its type, within its range.

## Paths

Errors and generated files name a value by its path, written the way form attributes are, starting
at `data`:

| Path | Addresses |
| --- | --- |
| `data.hp.current` | a key of an object, or of a map |
| `data.features[2].name` | an item of a list without ids, by position |
| `data.experiences[k3x9q2…].bonus` | an item of a list with ids, by its `id` |

## How saves are checked

When an entity type has a schema, its editor checks the edited `data` before saving it. That
covers the editor form, the JSON data editor inside it and partial editors opened from actions.
If anything is wrong, nothing is saved: an alert lists each problem with its path —
`data.hope: must be between 0 and 6` — and the editor stays open with your edits.

**Only what changed is checked.** The edited data is compared with the stored data, and values that
are the same are saved as they are — including keys the schema does not declare. Data an older
version of your system wrote survives an edit next to it. A new entity is checked in full.

List items are matched to their stored versions before they are compared: by `id` in a list with
ids, then by identical content wherever an item moved, then the rest in order. Inserting an item in
the middle of a list or reordering it does not make the items around it count as changed.

**Values are converted to their declared type**, from text where that is unambiguous:

| Type | Accepts | Refuses |
| --- | --- | --- |
| `integer` | `7`, `7.0`, `"7"` | `7.5`, `true`, `"seven"` |
| `number` | `7`, `7.5`, `"7.5"` | `true`, `"lots"` |
| `boolean` | `true`, `"true"`, `"false"` | `1`, `"yes"` |
| `string`, `text`, `dice`, `url` | text | numbers, booleans |
| an enum | a key, or its text: `"2"` for a numeric key; any other text or whole number, trimmed | booleans, fractions, objects |

`null` removes a key. So does an empty string for anything but `string`, `text` and `dice`, where
an empty string is a value — clearing a number field removes the number.

**Keys the schema doesn't declare are saved as written** by entity editors, unconverted, so you can
try a key in a form before declaring it. Each such save logs a warning that lists them, which is
how a misspelt key shows up. Enum values the set doesn't list are logged the same way. A map key
outside its enum is still refused. A
[sheet](/system-development/sheets/) can't do this: its write to an undeclared key is refused with
`undeclared`, though it still reads the key.

**A schema that fails to load blocks every save** of its entity type, with the load error in the
alert. Saving unchecked would let wrong data in exactly when you are working on the schema.

[Sheets](/system-development/sheets/) are checked on every write. Not checked: content imports,
combat changes such as hit points from the token bar, migrations, and writes through the
[REST API](/reference/server-api/#entities).

## Errors

Schemas are loaded with the system. A schema with a problem fails on its own — the others load —
and the error names the file and the key path of the declaration:

```
schemas/character.json: data.weapons.type[0].properties.range: unknown type "Ranges"
schemas/character.json: data.pronouns: "max" is not valid here
schemas/partials/b.json: "Feature" is already declared in schemas/partials/a.json
```

Errors are written to the app's log as `schema load error: …`, and a broken schema is also
reported in the save alert of its entity type.

## Generated files

Each time the system loads, every schema that loaded is written to `cache/schemas/` in three
forms:

| File | Holds |
| --- | --- |
| `<label>.json` | the **runtime schema**: the resolved declarations, for a sheet's own checks (`ep-schema.js`) |
| `<label>.schema.json` | the schema as [JSON Schema 2020-12](https://json-schema.org/), for validators and editors |
| `<label>.d.ts` | **TypeScript** declarations, for writing sheets |

A file is rewritten only when its contents change, and the files of a schema that was removed or
failed to load are deleted. Like everything in `cache/`, they are generated: don't edit them, and
leave them out of your package.

Views reach them through the system's address, in the app and in the web client alike:

```
{{ env.systemURL }}/cache/schemas/character.json
```

### JSON Schema

The generated JSON Schema describes `data`. Definitions and enums go into `$defs`. An enum's def
is `anyOf` its keys and any string (or integer, for numeric keys), so editors still suggest the
keys; map keys from an enum are listed in `propertyNames` and stay closed. Objects stay
open — `additionalProperties` is never set — because stored data may hold keys the schema does not
declare. What JSON Schema has no word for is annotated:

| Annotation | Marks |
| --- | --- |
| `x-ep-type` | `text`, `dice` or `url` on a `string` |
| `x-ep-ref` | the entity type of a copy |
| `x-ep-play` | play state |
| `x-ep-ids`, `x-ep-tree` | lists with ids, and trees |

### TypeScript

The declarations name the root type after the label — `character` becomes `CharacterData`,
`domain-card` becomes `DomainCardData`. Enums become union types and definitions interfaces. A
field of an enum is typed `Domain | (string & {})` (plus `(number & {})` for numeric keys): the keys
still autocomplete, and your code has to handle a value it doesn't know. Map keys keep the closed
union. Every
key is optional, because stored data may lack any of them, and a list item's `id` is `readonly`.
Descriptions, defaults and ranges appear as doc comments.

```ts
export type Trait = "agility" | "finesse" | "instinct" | "knowledge" | "presence" | "strength";

export interface Track {
  /**
   * @minimum 0
   * @maximum 12
   */
  current?: number;
  // …
}

export interface CharacterData {
  experiences?: Array<Experience & {
    readonly id?: string;
  }>;
  hp?: Track;
  traits?: Partial<Record<Trait, number>>;
  // …
}
```

## Live reload

On macOS debug builds, editing a file under `schemas/` reloads the system, so the next save is
checked against your change and the generated files are rewritten.
