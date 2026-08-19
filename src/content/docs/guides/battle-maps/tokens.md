---
title: Tokens
description: Putting creatures on the map — placing, moving, sizing and styling tokens, hiding them, and giving them auras and vision.
---

A token is a creature's presence on the map. It holds no statistics of its own — it points at a
creature in your library, and it is linked to that creature's row in the initiative order.

Token and combatant are two views of the same creature. Change a name, label, role or visibility on
one and the other follows.

:::tip
For default token style, movement modes and gestures, see
[Battle Map Settings](/settings/battle-map/).
:::

## Placing tokens

Loading a creature from the library puts a token on the map, if
**[Load Mode](/settings/combat/#load-mode)** includes the map. That is the usual way.

You can also drag a creature onto the map, or create a token directly on it.

To place creatures without your players seeing them arrive, turn on
**[Hidden by Default](/settings/combat/#hidden-by-default)** and reveal them when you are ready.

## Moving tokens

### One creature

1. Tap ![move][icon-move].
2. Drag the token anywhere on the map.

While you drag, the app draws the path and the distance travelled, using the map's grid scale and
units.

**Advanced Pathfinding** routes that path around walls and obstacles instead of drawing a straight
line, so the number you see is the distance the creature actually has to walk.

### Several at once

1. Tap ![select][icon-select].
2. Drag a rectangle over the tokens you want.
3. Drag any token in the group — they all move together.

How they move depends on
**[Party Movement Mode](/settings/battle-map/#party-movement-mode)**:

| Mode | Effect |
| --- | --- |
| **Standard** | The group keeps its formation |
| **Snake** | Everyone follows the leader in single file |

*Snake* is for corridors, where a formation cannot fit.

### Snap to grid

Tap ![snap][icon-snap] to toggle snap to grid. Tokens then line up with cells as you drop them.

It also affects drawing, which is useful when you are sketching rooms and corridors.

### Restricted movement

Restricted movement stops tokens crossing walls.

1. Tap ![move][icon-move] twice.
2. Tap ![move-restricted][icon-move-restricted] to stop tokens crossing
   [walls](/guides/battle-maps/line-of-sight/).
3. Tap ![move][icon-move] again to allow free movement.

Turn it on and your players cannot walk through the dungeon walls by accident — useful during remote
play, where you are not watching every drag. With it off, walls affect vision only.

## Token properties

Open a token to edit it:

| Field | What it does |
| --- | --- |
| **Name** | The creature's name |
| **Label** | The short text drawn on the token — usually a number |
| **Role** | Hostile, friendly or neutral. Sets the ring colour |
| **Size** | Grid size, from tiny to gargantuan |
| **Width** and **Height** | Custom size in grid cells |
| **Scale** | Fine adjustment of the artwork |
| **Style** | Circle or top-down |
| **Elevation** | Height above the ground, in map units |
| **Rotation** | Facing, in degrees |
| **Hidden** | Hides the token from your players |

### Labels

Labels are how you tell four goblins apart. The app numbers duplicates for you when you load several
copies of the same creature.

### Style

| Style | Best for |
| --- | --- |
| **Circle** | Portrait artwork, cropped into a ring coloured by role |
| **TopDown** | Artwork drawn from above, which stays correct when the token is rotated |

Set the default for new tokens under
**[Default Token Style](/settings/battle-map/#default-token-style)**. Existing tokens keep the style
they were made with.

### Hidden tokens

A hidden token is fully visible to you and completely absent for your players — on the external
screen and in the web client alike.

This is how you place an ambush before it springs.

## Vision

Each token has its own **Light / Vision** settings, which matter when line of sight is on.

There are three separate things there:

| Setting | What it means |
| --- | --- |
| **Vision** | Whether this token sees at all |
| **Light** | A light source the token carries, which lights the map for everyone |
| **Darkvision** | The ability to see without light, for this token only |

The difference between the last two is the whole point. A carried torch lights the corridor for the
entire party. Darkvision reveals it to the dwarf and nobody else.

Light and darkvision each have an inner and an outer radius — bright then dim, in grid units. The
usual 5E dwarf is darkvision `0/60`; a torch is light `20/40`.

See [Line of Sight & Fog](/guides/battle-maps/line-of-sight/) for how this fits together.

## Auras

An aura is a coloured area drawn around a token that moves with it. Use one for a paladin's aura, a
dragon's frightful presence, reach, or just a threat range you want to see.

Each aura has a radius, colour, opacity and an optional name. A token can carry several.

An aura follows its creature. For an area anchored to the ground instead, use an area effect — see
[Drawing, Markers & Effects](/guides/battle-maps/drawing-and-effects/).

## Common questions

### My token is on the map but not in initiative

Load Mode was set to *Map* only. Change it under [Combat Settings](/settings/combat/#load-mode), or
add the combatant to combat separately.

### The token is the wrong size

Size follows the creature's size in the library. Override it on the token with **Size**, or set
**Width** and **Height** in grid cells for something unusual.

### Players can walk through walls

Turn on restricted movement, as described above. Without it, walls block vision but not movement.

## Where to go next

- [Line of Sight & Fog](/guides/battle-maps/line-of-sight/) — walls, lights and what players see.
- [Encounters & Combat](/guides/encounters/) — the initiative side of the same combatants.

[icon-move]: /assets/icons/move.png
[icon-move-restricted]: /assets/icons/move-restricted2.png
[icon-select]: /assets/icons/select.png
[icon-snap]: /assets/icons/snap.png
