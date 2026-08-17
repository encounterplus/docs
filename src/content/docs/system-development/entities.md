---
title: Entity Definitions
description: Declaring the content types a system provides, and the shape of the data each one stores.
---

Everything a system lets a user create — creatures, spells, items, classes, vehicles — is an
**entity**. There is one storage model behind all of them; what differs is the definition that
describes it.

`entities.json` is the list of those definitions. It is the file that decides what your library
looks like.

## Declaring a type

`entities.json` is an array of [EntityDefinition](/reference/schema/entity-definition/) objects:

```json
[
  {
    "name": "Monster",
    "label": "monster",
    "collection": { "label": "monsters" },
    "loadable": true
  },
  {
    "name": "NPC",
    "label": "npc",
    "extends": "Monster",
    "collection": { "label": "npcs" },
    "loadable": true
  },
  {
    "name": "Spell",
    "label": "spell",
    "collection": { "label": "spells" }
  }
]
```

That is enough to give you a Monsters section in the library, an NPCs section, and a Spells
section.

### `name`

The canonical identifier, singular and capitalized by convention (`Monster`, `Spell`,
`Subclass`). It is what an entity stores in its `kind` field, what `config.json` and
`filters.json` key their blocks by, and what `attributeType` refers to when a form field points at
this type.

Renaming it after content exists orphans that content — the entities keep the old `kind` and no
longer match any definition.

### `label`

The lowercase, singular, file-safe form. It selects the definition's form, view and theme files:
`forms/<label>.json`, `views/<label>.json`, `views/<label>-compact.json`, `views/<label>.html`,
`themes/<label>.json`.

### `collection`

How a group of these appears in the library.

```json
"collection": {
  "title": "Magic Items",
  "label": "magic-items",
  "icon": "icons/items.png"
}
```

- `label` — lowercase and plural. It names the icon (`icons/<label>.png` by default) and, more
  importantly, the **file that content of this type is imported from**: a module archive carries a
  `magic-items.json` array, with per-entity images under `magic-items/`.
- `title` — the plural display name. Omit it and the app derives one by pluralizing the
  localization key `Entity.<name>`.
- `icon` — overrides the default icon path.

### `title`

The singular display name. Omit it and the app localizes `Entity.<name>` — so a `Monster`
definition with no `title` looks up the `Entity.Monster` key in `lang/en.json`. Providing the
strings there rather than hardcoding `title` is what makes a system translatable.

## Type relationships

### `extends`

Declares this type as a specialization of another:

```json
{ "name": "NPC", "label": "npc", "extends": "Monster", "collection": { "label": "npcs" } }
```

An extending type is stored as the parent's base type with its own name recorded as a *kind*, so
NPCs and Monsters share storage but are separately listed, separately filtered and separately
configurable. Definition lookups fall back to the parent: if `views/npc.json` does not exist, an
NPC renders with the Monster view; the same fallback applies to
[data transforms](/system-development/views/#computed-attributes).

Use it when two types are mechanically the same thing with different presentation. Use two
independent definitions when they are not.

### Behavior flags

| Flag | Meaning |
| --- | --- |
| `loadable` | This type can appear in an encounter and be loaded into combat — creatures and vehicles, not spells. It also makes the type selectable wherever the app offers a list of entity types. |
| `standalone` | The type is a singleton-ish object with specialized handling rather than an ordinary library row. `Character` uses this. |
| `dynamic` | Instances are subclassified at runtime. When set, the app reads the type `<name>Type` and registers one library label per option — this is how the single `Rule` definition produces conditions, actions, senses and the rest as separate browsable groups. |
| `system` | Borrow definitions from a different installed system rather than this one. Rarely needed. |
| `custom` | Free-form JSON for your own use. It is carried through untouched and is readable from the entity's view context. |

## The data model

Every entity, whatever its type, is stored as the same
[Entity](/reference/schema/entity/) record. The fields worth knowing when authoring a system:

```json
{
  "id": "5B3F…",
  "kind": "Monster",
  "system": "dnd5e",
  "name": "Goblin",
  "slug": "goblin",
  "descr": "A small, black-hearted humanoid…",
  "notes": "",
  "image": "monsters/goblin.jpg",
  "token": "monsters/goblin-token.png",
  "icon": null,
  "data": { "cr": "1/4", "ac": 15, "abilities": { "str": 8, "dex": 14 } },
  "attributes": { "ruleset": "5e" },
  "tags": ["humanoid", "goblinoid"],
  "sources": [{ "name": "MM", "page": 166 }],
  "modifiers": []
}
```

### `data` — where your ruleset lives

`data` is a free-form JSON object, and it is the part you design. The app never inspects its
contents; it only stores them, hands them to your forms and views, and lets your migrations
rewrite them. Nesting, arrays, objects — all fine.

Everything addresses into it with dot paths:

```json
{ "type": "picker", "attribute": "data.school", "attributeType": "SpellSchool" }
```

and templates read it the same way:

```
{{data.abilities.str}}
{{data.classes | join: ', '}}
```

Some conventions that pay off:

- **Store raw, display formatted.** Keep `data.cr` as `"1/4"` and let the view render
  `CR 1/4 (50 XP)` through a type mapping. A stored display string cannot be filtered or sorted.
- **Store keys, not labels.** `"school": "evocation"`, not `"school": "Evocation"` — the label
  comes from `types.json` and is translatable; the key is not.
- **Derive rather than duplicate.** Passive Perception, proficiency bonus and XP are computed by a
  [transform](/system-development/views/#computed-attributes) at render time, so they cannot drift
  out of sync with the values they depend on.
- **Design for change.** The shape of `data` is your API to your own users' content. Reshaping it
  later means writing a [migration](/system-development/migrations/).

### `attributes` — the queryable side

A flat key-value store, separate from `data`, for values that need to be indexed or read outside
the rendering path. The D&D 5E system uses `attributes.ruleset` to switch a creature between the
2014 and 2024 stat block layouts.

Extra keys can be declared in `custom-attributes.json` — see
[Types & Collections](/system-development/types/#custom-attributes).

### Standard fields

`name`, `slug`, `descr`, `notes`, `image`, `token`, `icon`, `tags` and `sources` exist for every
entity regardless of system, and the app has behavior attached to several of them: `slug` is used
for links, `token` for the battle map, `sources` for the source filter, `tags` for tag filtering.
Prefer them over reinventing equivalents inside `data`.

`type` also exists as a lightweight subtype string, but on a modern system `data` is almost always
the better place — the exception is a `dynamic` entity type, where `type` selects the runtime
subclassification.

## The rendering context

Forms, views and templates all read the same JSON context, built from the entity:

| Key | Contents |
| --- | --- |
| `name`, `slug`, `descr`, `notes`, `image`, `token`, `icon`, `type` | the standard fields |
| `data` | your ruleset data, after transforms have run |
| `attributes` | the queryable attributes |
| `tags`, `sources` | arrays |
| `combatant` | combat state, when the entity is in a fight |
| `location` | where the entity sits in the library tree |
| `created`, `modified` | timestamps |
| `source`, `nameWithSource`, `sourceFormatted`, `locationFormatted`, `footer` | pre-formatted display strings |
| `env` | `baseURL`, `dataURL`, `systemURL`, and `type: "catalyst"` on macOS |

Views additionally see whatever the entity's [transform](/system-development/views/#computed-attributes)
computed, plus a `data.modifiers` array of currently active modifiers.

## Worked example: adding a type

Say the ruleset needs **Factions**.

1. **Define it** in `entities.json`:

   ```json
   {
     "name": "Faction",
     "label": "faction",
     "collection": { "label": "factions" }
   }
   ```

2. **Name it** in `lang/en.json`:

   ```json
   { "Entity.Faction": "Faction", "Faction.Influence": "Influence" }
   ```

3. **Add an icon** at `icons/factions.png`.

4. **Add a value set** in `types.json`, if the type has fixed choices:

   ```json
   "FactionScope": {
     "local": "FactionScope.Local",
     "regional": "FactionScope.Regional",
     "global": "FactionScope.Global"
   }
   ```

5. **Write the editor** at [`forms/faction.json`](/system-development/forms/).

6. **Write the detail view** at [`views/faction.json`](/system-development/views/).

7. **Optionally add filters** for it in `filters.json`.

8. **Reload the system.**

The library now has a Factions section, users can create factions, and modules can ship a
`factions.json`.

## Where to go next

- [Types & Collections](/system-development/types/) — the value sets your fields point at.
- [Forms](/system-development/forms/) — the editor for the type you just declared.
- [Views](/system-development/views/) — its detail screen.
