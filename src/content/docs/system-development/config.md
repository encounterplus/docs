---
title: Configuration
description: config.json — per-type behavior, combat tracker bars, measurement systems, initiative, game resources and view themes.
---

`entities.json` says what types exist and `forms/` and `views/` say how they are edited and shown.
`config.json` says how the app **behaves** for them.

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
| `view.sheet` | Which `sheets/<id>/` folder the type's [sheet](/system-development/sheets/) is. With the `sheet` renderer the type opens as it, `default` when this is left out; with `html` the template links to it through `env.sheetURL`. |
| `view.updateMode` | `load`, `reload`, `event`, `none`. |
| `load` | What loading the type produces — `creature`, `statusEffect`, `areaEffect`. See below. |

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

A bar's `type` says what `current` holds. The default, `pool`, is what is **left**: a combatant
starts at `maximum`, damage subtracts, and it is defeated at `minimum` (0). A system whose rules
mark slots instead — Daggerheart's Hit Points and Stress — sets `marked`, and `current` becomes what
is **marked**:

```json
"bars": [
  { "attribute": "data.hp", "title": "Common.HitPoints", "label": "Common.HP", "type": "marked" }
]
```

| `type` | `current` is | Starts at | Damage | Defeated at |
| --- | --- | --- | --- | --- |
| `pool` (default) | what is left | `maximum` | subtracts | `minimum` |
| `marked` | what is marked | `minimum` (0) | adds, kept within `minimum`–`maximum` | `maximum` |

A marked bar draws the marks: empty at the start and filling as the combatant is hurt, in the same
colours as a pool — red once bloodied, which here means half or more marked. Sheets and templates read and write the same marked
count. An unknown `type` is read as `pool`, with a warning in the log when the system loads.

#### States

`combatant.states` maps a state name to a condition template. `defeated` is the one the app acts
on:

```json
"states": { "defeated": "#{{data.hp.current|default: 1}} <= -{{data.hp.maximum|default: 0}}" }
```

The leading `#` makes it a [formula](/system-development/templates/#formulas). This example is the
D&D 5E instant-death rule; without it, the default rule of reaching zero applies.

#### Load targets

`loadable` in [`entities.json`](/system-development/entities/) decides whether a type can be
loaded at all. `load` decides what loading it produces:

```json
"Spell": { "load": ["statusEffect", "areaEffect"] }
```

| Target | Produces | Needs in the entity data |
| --- | --- | --- |
| `creature` | A combatant and/or token, following the load mode. | — |
| `statusEffect` | A status effect on the selected token. | `data.duration`, `data.durationUnit` or `data.durationType` |
| `areaEffect` | An area effect placed on the map. | `data.areaEffectShape` |

Without the key a loadable type loads as a creature only, so status and area effects need the
type to list them. An entity's duration or area data alone never makes one. An empty list loads
nothing.

The app tries the targets in order: a status effect when a token is selected, then an area
effect, then a creature. An entity that lists effects but has neither the data nor a selected
token is reported as an error instead of being loaded as a creature, unless the list also
includes `creature`. The combat/map load-mode menu is shown only for types whose list includes
`creature`.

### Status effect menus

```json
"statusEffects": { "menuProvider": ["Rule:condition"] }
```

Each entry names an entity type to offer as status effects, optionally narrowed by a
subtype after a colon. `Rule:condition` is what makes a 5E system's conditions appear in the
tracker's status effect menu — the conditions are ordinary content, not a hardcoded list.

### Linked status effects

A character sheet's condition toggles can show as status effects on the character's combatant, and
so on its token. List them under the entity type, in `statusEffects`:

```json
"Character": {
  "statusEffects": [
    { "attribute": "data.conditions.vulnerable", "reference": "/condition/vulnerable", "name": "Condition.Vulnerable", "icon": "gi-broken-shield" },
    { "attribute": "data.exhaustion", "name": "Condition.Exhaustion" }
  ]
}
```

| Key | Values |
| --- | --- |
| `attribute` | Required. The flag's path, starting with `data.`, made of plain keys. No list items |
| `name` | Required. The effect's name; a localization key works here |
| `icon` | A `gi-` game icon name, or the icon path a status effect holds. Wins over the rule's icon |
| `reference` | The entity describing the effect, such as `/condition/vulnerable` |

The flag is the source of truth, and the two stay in step in both directions:

- Turning a flag on adds its effect, unless the combatant already has a matching one. Turning it
  off removes every matching effect.
- Adding a matching effect turns the flag on, and removing the last one turns it off, however the
  effect was added or removed: from the menu, in a form, or when its duration runs out.
- Anything else is left alone. Changing hit points doesn't touch effects, and adding Bless doesn't
  touch flags.

A flag is on when it is `true` or a number other than zero, so a level such as Exhaustion works as
well as a boolean. When an effect turns a flag on, a boolean is written as `true` and a number as
`1`; a level already above zero is kept. Removing the last effect writes `false` or `0`.

An effect matches a link by `reference`, compared on the label and slug only, so
`/condition/vulnerable/srd` matches `/condition/vulnerable` whichever source provides the rule.

Write the address the app gives the entity. A [`dynamic`](/system-development/entities/) type goes
by its subtype, so a `Rule` of type `condition` is `/condition/vulnerable`, not `/rule/vulnerable`.
References that differ never match, even when the names are the same, so a wrong label means an
effect added from the menu doesn't turn its flag on.

When the link or the effect has no reference they are compared by name, ignoring case. Name
matching uses the translated name, so prefer a `reference` when the system has rules to point at.
With one, the effect also takes its description, color, duration, modifiers and aura from the rule,
if the rule is installed.

Links need three things, and a link missing one is reported as a warning when the system loads:

- The entity type is `standalone`. Only those entities share one combatant, so links on any other
  type are ignored. A flag written to such an entity is saved as plain data.
- The type has a [model schema](/system-development/schemas/).
- `attribute` is declared in the schema as a boolean, integer or number.

A flag that is already on when a combatant is created gets its effect then. A flag turned on before
the links were added to the system, on a combatant that already exists, gets no effect until it is
toggled.

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

### Game resources

Counters the table spends and accumulates during play, such as Daggerheart's Fear:

```json
"resources": [
  { "id": "fear", "label": "Fear", "icon": "gi-burning-skull", "min": 0, "max": 12, "visibility": "players" }
]
```

`resources` is always a list, even for a system with a single resource. Each entry becomes a
counter in the game screen's bottom bar, where the GM changes it with `−` and `+`, sets it directly
from a menu on the value, or resets it.

| Key | Values |
| --- | --- |
| `id` | Required. Identifies the resource and the value stored for it; keep it stable across system versions |
| `label` | The name shown with the value; a localization key works here. Defaults to the `id`, capitalized |
| `icon` | A `gi-` game icon name, or the path of an image in the system folder |
| `type` | `counter` (default) or `countdown` |
| `min` | The lowest value; defaults to `0` |
| `max` | The highest value; leave it out for no upper limit |
| `initial` | The starting value; defaults to `min` |
| `visibility` | `gm` (default) or `players` |

A resource with `players` visibility is shown on the player display and the web client. One with
`gm` visibility stays with the GM; its value never leaves the device. The default is `gm`, so a
resource is only shown to players when the system says so. Players see the `max` beside the value
(`5 / 12`) when the resource has one, and the value alone when it does not.

The menu on a counter's value lists every value from `min` to `max`, so the GM can set it in one
step. Without a `max` it lists `min` to `min + 12`; `+` still goes past that.

A `countdown` works like a counter for the GM, who sets it and counts it down. Players see it only
while it is running: at `0` it is hidden, at any other value it shows (when its visibility is
`players`). Daggerheart's countdowns are a good fit:

```json
{ "id": "countdown", "label": "Countdown", "type": "countdown", "visibility": "players" }
```

Values belong to the campaign. They persist across sessions and never reset on their own, not even
when combat ends. A resource the GM has not changed reads as its `initial` value, and a value is
always kept within `min` and `max`, even after a system update narrows them.

Besides the GM's bottom bar, a sheet can change a resource — Daggerheart's sheet gives the GM a
Fear when a roll goes with Fear — with [`EP.adjustResource`](/system-development/sheets/#game-resources);
in a browser only resources with `players` visibility.

An entry without an `id`, a repeated `id`, or a `type` the app does not know is skipped, so a
system written for a newer app still loads.

### Dice

How labelled dice look in the 3D roller, what outcome a roll's labelled dice give, and what a roll
link's menu offers besides the plain roll. A label is
written after a dice term in a formula, `1d12[Hope]` (see
[Labelled terms](/reference/dice-expressions/#labelled-terms)); this is Daggerheart's duality roll:

```json
"dice": {
  "labels": {
    "Hope": { "color": "#e8b931" },
    "Fear": { "color": "#5b2a86", "textColor": "#ffffff" }
  },
  "outcomes": [
    { "id": "critical", "label": "Roll.Critical", "color": "#e8b931", "when": { "equal": ["Hope", "Fear"] } },
    { "id": "hope", "label": "Roll.WithHope", "color": "#e8b931", "when": { "greater": ["Hope", "Fear"] } },
    { "id": "fear", "label": "Roll.WithFear", "color": "#5b2a86", "when": { "greater": ["Fear", "Hope"] } }
  ],
  "options": [
    { "id": "advantage", "label": "Roll.Advantage", "when": { "labels": ["Hope", "Fear"] }, "add": "1d6[Advantage]" },
    { "id": "disadvantage", "label": "Roll.Disadvantage", "when": { "labels": ["Hope", "Fear"] }, "add": "-1d6[Disadvantage]" }
  ]
}
```

A sheet then rolls `1d12[Hope] + 1d12[Fear] + 2`, and the log shows the roll as
`Hope (7) + Fear (3) + 2` marked **With Hope**. Every part is optional, and a system without them
rolls as before.

**`labels`** gives the dice of a label their colours, matched without regard to case:

| Key | Values |
| --- | --- |
| `color` | The dice's colour, `#rrggbb`, tinting the material the user picked in the dice roller settings |
| `textColor` | The colour of the numbers, `#rrggbb` |

**`outcomes`** is a list of rules, tried in order after every roll; the first that matches is the
roll's outcome:

| Key | Values |
| --- | --- |
| `id` | Required. What sheets branch on: a roll carries it as `outcome.id` |
| `label` | The name the log shows; a localization key works here. Defaults to the `id`, capitalized |
| `color` | The colour the log shows the name in, `#rrggbb` |
| `when` | Required. One comparison of two labels' results: `equal` (the same) or `greater` (the first is higher) |

A comparison uses the results of the dice with those labels — other dice and the modifier don't
count, so an advantage die changes the total but not the outcome. Should more than one term carry a
label, their results are added. A roll missing either label matches no rule, so a plain `2d12` or a
damage roll gets no outcome. An entry without an `id`, or with a `when` the app can't read, is
skipped.

The outcome is worked out wherever the roll is — the dice roller, a roll from chat, a sheet's
`EP.roll` — and stored with the roll, so the log keeps it, the web client shows it, and a sheet gets
it as `roll.outcome`. It only names the result: what follows from it, such as gaining Hope or giving
the GM Fear, is the sheet's to apply, since only the sheet knows whether the roll was one that
counts.

**`options`** lists what a roll link's menu offers after the plain roll — a right-click, or a long
press on a touch screen, wherever `ep-ui.js` is loaded (see [Roll menus](/system-development/sheets/#roll-menus)).
Each option that applies to the link's roll is listed, in order, with the formula it rolls
instead:

| Key | Values |
| --- | --- |
| `id` | Required. What a view's `ep-roll` handler sees as `option`. `roll`, `public`, `private` and `customize` are the app's own |
| `label` | The name the menu shows; a localization key works here. Defaults to the `id`, capitalized |
| `add` | A term added at the end of the formula, subtracted with a leading `-`: `-1d6[Disadvantage]` |
| `transform` | What changes in the roll's dice: `advantage` (each d20 becomes `2d20kh1`), `disadvantage` (`2d20kl1`) or `critical` (every dice term rolls twice the dice) |
| `when` | Which rolls the option applies to; every key given must hold, and an option without `when` applies to every roll |

An option has one of `add` and `transform`. `when` tests the roll:

| Key | Holds when |
| --- | --- |
| `labels` | Every label named is on one of the roll's dice terms: `["Hope", "Fear"]` |
| `faces` | The roll has dice, and every dice term has one of these faces: `[20]` |
| `types` | The roll's type is one of these: `["damage"]`. A link without a type has none |

D&D 5e's, which the app's older menu had built in:

```json
"options": [
  { "id": "advantage", "label": "Roll.Advantage", "when": { "faces": [20] }, "transform": "advantage" },
  { "id": "disadvantage", "label": "Roll.Disadvantage", "when": { "faces": [20] }, "transform": "disadvantage" },
  { "id": "critical", "label": "Roll.Critical", "when": { "faces": [4, 6, 8, 10, 12] }, "transform": "critical" }
]
```

An option changes only what is rolled: the result is logged as any roll is, with its outcome. In
the app's own views the menu also offers the GM a roll in the other roll mode — *Roll Privately*
when rolls are public — and *Customize…*, which opens the advanced dice roller with the roll's
formula. An entry without an `id`, with a reserved or repeated one, or with anything
the app can't read is skipped.

### View themes

Named looks for the system's HTML views — pages, entity views rendered with the `html` renderer,
and tables — that the user picks under **Appearance** in the system settings:

```json
"viewThemes": [
  { "id": "parchment", "label": "Parchment" },
  { "id": "clean", "label": "Clean" }
]
```

| Key | Values |
| --- | --- |
| `id` | Required. Letters, digits, `-` and `_`; keep it stable, it is what the user's choice is saved as |
| `label` | The name shown in the picker; a localization key works here. Defaults to the `id`, capitalized |

The app does no styling of its own. It writes the selected id as `data-view-theme` on `<html>`,
and your stylesheet does the rest:

```css
:root { --accent: #58180d; --paper: #fdf1dc; }
:root[data-view-theme="clean"] { --accent: #1f4e79; --paper: #ffffff; }
```

With no theme picked — the default — there is no `data-view-theme`, so your base rules are the
default look. Your own templates in `views/*.html` write the attribute themselves from
`env.theme`:

```html
<html lang="en" data-kind="{{kind}}"{% if env.theme %} data-view-theme="{{env.theme}}"{% endif %}>
```

The bundled templates already do. A theme that needs more than variables can live in its own file,
linked from your template through `{{ env.systemURL }}styles/themes/{{ env.theme }}.css`.

Modules with their own look (`styles/page.css`) and older modules (`assets/css/global.css`) never
load the system's styles, so themes do not reach them. A theme is shown everywhere the view is,
the web client included.

#### Light and dark

With no theme picked, views follow the app's appearance, which the user sets for the whole app.
Declare which schemes your stylesheet supports and write colours with `light-dark()` (or system
colours such as `Canvas`), and they follow it:

```css
:root { color-scheme: light dark; }
body { color: light-dark(#222, #eee); background: light-dark(#fff, #1e1e1e); }
```

To offer a look that is always light or always dark, make it a theme and force the scheme in CSS.
`light-dark()`, `Canvas`, form controls and scrollbars all follow `color-scheme`:

```css
:root[data-view-theme="night"] { color-scheme: dark; }
:root[data-view-theme="parchment"] { color-scheme: light; }
```

`@media (prefers-color-scheme: dark)` does not follow `color-scheme`, only the app's appearance,
so rules written with it ignore a forced theme.

[Pico](https://picocss.com) switches its colours on a `data-theme="light"` or `"dark"` attribute
rather than on `color-scheme`, and CSS cannot set an attribute. A Pico-based system writes it in its
own templates, from the theme:

```html
<html lang="en"{% if env.theme == "night" %} data-theme="dark"{% endif %}>
```

Keep `data-theme` for that alone: Pico reads any value on `<html>` as a forced scheme, so a theme id
there would turn off its automatic dark mode. That is why the app writes themes as
`data-view-theme`.

## Where to go next

- [Templates](/system-development/templates/) — the expressions in `detail` and `states`.
- [Forms](/system-development/forms/#the-system-settings-form) — exposing config to users.
