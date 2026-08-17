---
title: Configuration & Filters
description: config.json — per-type behavior, combat tracker bars, measurement systems and initiative — plus the library's filter, group and sort options.
---

`entities.json` says what types exist and `forms/` and `views/` say how they are edited and shown.
`config.json` says how the app **behaves** for them, and `filters.json` says how the library
**browses** them.

## `config.json`

### Per-entity configuration

The `entities` block is keyed by entity `name`, with a `Default` block applying to all of them:

```json
{
  "entities": {
    "Default": {
      "combatant": {
        "bars": [
          { "attribute": "data.hp", "title": "Common.HitPoints", "label": "Common.HP", "temporary": true }
        ]
      }
    },
    "Monster": {
      "collection": {
        "detail": "{{data.size|map: 'Size'}}{{data.type|map: 'MonsterType'|prefix: ' '}}{{data.alignment|map: 'Alignment'|prefix: ', '}}"
      },
      "combatant": {
        "detail": "{{'Common.AC'|l}} {{data.armor}} • {{'Common.PP'|l}} {{data.passivePerception}} • {{'Common.CR'|l}} {{data.cr}}"
      }
    },
    "NPC": { "role": "neutral" },
    "Character": {
      "role": "friendly",
      "combatant": {
        "states": { "defeated": "#{{data.hp.current|default: 1}} <= -{{data.hp.maximum|default: 0}}" }
      }
    }
  }
}
```

Values resolve in four layers, each overriding the last: `config.json`'s `Default`, the user's
settings `Default`, `config.json`'s entity block, the user's settings for that entity. That is
what allows a system to ship a sensible default and still let a user change it from the
[settings form](/system-development/forms/#the-system-settings-form).

| Key | Meaning |
| --- | --- |
| `role` | The side this type joins combat on — `friendly`, `neutral`, `hostile`. |
| `collection.detail` | Template for the subtitle in library lists. |
| `collection.image` | Which image a library row shows. |
| `combatant.detail` | Template for the subtitle in the combat tracker. |
| `combatant.image` | Which image a combatant row shows. |
| `combatant.bars` | Tracked value bars — see below. |
| `combatant.states` | Named state conditions — see below. |
| `view.renderer` | `native` (default), `html`, `custom`, `sheet`. |
| `view.template` | Which `views/*.html` file the `html` renderer uses. |
| `view.updateMode` | `load`, `reload`, `event`, `none`. |

`collection.detail` and `combatant.detail` are the one-line summaries under a name. They are
ordinary [templates](/system-development/templates/) over the entity's context, which means they
can read anything a [transform](/system-development/views/#computed-attributes) computed — the AC,
passive Perception and CR in the example above are all derived values.

#### Tracked bars

`combatant.bars` declares what the combat tracker tracks. Each entry names an attribute holding a
`current` / `maximum` (and optionally `temporary`) group:

```json
"bars": [
  { "attribute": "data.hp", "title": "Common.HitPoints", "label": "Common.HP", "temporary": true }
]
```

The **first** bar is the primary one: it backs the defeated and bloodied states and is what the
tracker shows most prominently. A system with more than one pool — stamina, stress, sanity — adds
further entries.

#### States

`combatant.states` maps a state name to a condition template. `defeated` is the one the app acts
on:

```json
"states": { "defeated": "#{{data.hp.current|default: 1}} <= -{{data.hp.maximum|default: 0}}" }
```

The leading `#` makes it a [formula](/system-development/templates/#formulas). This example is the
D&D 5E instant-death rule; without it, the default rule of reaching zero applies.

### Status effect menus

```json
"statusEffects": { "menuProvider": ["Rule:condition"] }
```

Each entry names an entity type to offer as status effects, optionally narrowed by a
subtype after a colon. `Rule:condition` is what makes a 5E system's conditions appear in the
tracker's status effect menu — the conditions are ordinary content, not a hardcoded list.

### Measurement

Declares the measurement systems the ruleset uses, their units, display format and conversions:

```json
"measurement": {
  "imperial": {
    "default": true,
    "title": "MeasurementSystem.Imperial",
    "units": ["ft", "mi", "lb"],
    "format": "@value @unit.",
    "conversion": {
      "metric": { "ft": { "m": "@value * 0.3" }, "mi": { "km": "@value * 1.5" }, "lb": { "kg": "@value * 0.5" } }
    }
  },
  "metric": {
    "title": "MeasurementSystem.Metric",
    "units": ["m", "km", "kg"],
    "format": "@value @unit",
    "conversion": {
      "imperial": { "m": { "ft": "@value / 0.3" }, "km": { "mi": "@value / 1.5" }, "kg": { "lb": "@value * 2" } }
    }
  }
}
```

Units are listed in matching order across systems, so the first unit of one maps to the first of
another. `@value` and `@unit` are the placeholders. The `default` system applies until the user
picks one in system settings.

Every value passed through the `units` filter, and every form field with a `units` key, is
converted accordingly:

```
{{ data.range | units: 'ft' }}
```

A creature authored in feet displays in metres for a metric user, with no change to the content.

### Initiative

```json
"combat": {
  "initiative": {
    "mode": "roll",
    "rollFormula": "d20 + @entity.data.initiativeBonus",
    "autoRoll": "hostileAndNeutral",
    "group": null,
    "everyRound": false,
    "sortOrder": "desc"
  }
}
```

| Key | Values |
| --- | --- |
| `mode` | `roll` (default), `draw`, `fixed` |
| `rollFormula` | The expression rolled; defaults to `d20 + @entity.data.initiativeBonus` |
| `rollTimes` | How many times to roll |
| `drawPool` | Highest value in the draw pool, for `draw` mode (default 20) |
| `autoRoll` | `all`, `hostile`, `hostileAndNeutral` (default), `none` |
| `group` | How ties are grouped |
| `everyRound` | Re-roll initiative each round |
| `sortOrder` | `desc` (default) or `asc` |

A card-draw system sets `"mode": "draw"`; a system where initiative is a fixed derived score sets
`"mode": "fixed"`.

Everything here can be exposed to users through the settings form, since settings merge over
config.

## `filters.json`

The library's filter, group and sort controls, keyed by entity name:

```json
{
  "Monster": {
    "params": [
      { "attribute": "data.size", "attributeType": "Size", "title": "Common.Size" },
      { "attribute": "data.type", "attributeType": "MonsterType", "title": "Common.Type" },
      { "attribute": "data.environments", "attributeType": "Environment", "title": "Common.Environment" },
      { "attribute": "sources.name", "title": "Common.Source", "dynamic": true }
    ],
    "group": [
      { "attribute": "data.cr", "attributeType": "ChallengeRating", "title": "Common.CR",
        "text": "CR {{value}} ({{value|map:'ChallengeRatingToXP', '0'}} XP)" },
      { "attribute": "name", "title": "Common.Name" }
    ],
    "sort": [
      { "attribute": "name", "title": "Common.Name" },
      { "attribute": "data.cr", "title": "Common.CR", "text": "{{value|valueMap:'ChallengeRatingToXP'}}" }
    ]
  }
}
```

- **`params`** — the filter controls. With `attributeType`, options come from that
  [type](/system-development/types/). With `"dynamic": true`, options are gathered from the values
  actually present in the user's content — the right choice for sources, class names and anything
  open-ended.
- **`group`** — the group-by options. `text` is a template for the section header, with the group's
  value bound to `value`.
- **`sort`** — the sort options. `text` supplies a sort key when the stored value does not sort
  correctly on its own; sorting challenge ratings by their XP value is how `"1/8"` ends up before
  `"1"` instead of after it.

A filter over an attribute the entities do not actually carry simply produces no options, and a
block keyed by an entity name that `entities.json` does not define is skipped. If a type is
sourcable and you declare no `params` at all, a source filter is added automatically.

## `rules.json`

Optional seed content shipped with a system — the conditions, senses, skills and other reference
entries a ruleset needs to function. It is content rather than definition, and it is what
`statusEffects.menuProvider` draws on.

## Where to go next

- [Types & Collections](/system-development/types/) — what `attributeType` refers to.
- [Templates](/system-development/templates/) — the expressions in `detail`, `text` and `states`.
- [Forms](/system-development/forms/#the-system-settings-form) — exposing config to users.
