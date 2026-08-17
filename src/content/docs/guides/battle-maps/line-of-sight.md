---
title: Line of Sight & Fog
description: Hiding and revealing the map — walls and doors, light sources, token vision, fog of war, and how the two systems differ.
---

Encounter+ has two ways to hide a map from your players, and they solve different problems.

| System | How it works |
| --- | --- |
| **Fog of war** | You paint what is hidden and what is revealed |
| **Line of sight** | The app works out what each token can see, from walls and lights |

Fog of war is manual and predictable. Line of sight is automatic and dramatic. Most maps use both.

<video src="https://encounter.plus/videos/line-of-sight.mp4" width="100%" controls preload></video>

:::tip
For the performance and rendering options, see
[Battle Map Settings → Line of Sight](/settings/battle-map/#line-of-sight).
:::

## Fog of war

### Turning it on

1. Tap ![settings][icon-settings].
2. Enable **Fog of War**.

The fog tools appear on the toolbar, and everything starts hidden.

### Revealing an area

1. Tap ![reveal][icon-reveal].
2. Draw a shape on the map.
3. Tap inside the shape to reveal it.

### Hiding an area

1. Tap ![hide][icon-hide].
2. Draw a shape on the map.
3. Tap inside the shape to hide it.

### Switching modes

Tap ![reveal][icon-reveal] or ![hide][icon-hide] a second time to reach the options:

- Swap between revealing and hiding.
- Choose ![fog-rect][icon-fog-rect] rectangle or ![fog-free][icon-fog-free] freehand drawing.

Rectangles suit rooms. Freehand suits caves.

### Exploration

With **exploration** on, revealed ground stays revealed once the party has been there — the map fills
in as they explore, like a video game map.

With it off, only what is currently visible is shown.

## Line of sight

Enable **Line of Sight** in ![settings][icon-settings] and the app computes what your players can
see, live, from three things:

1. **Walls** — what blocks vision.
2. **Lights** — what illuminates the map.
3. **Token vision** — what each creature can see with.

Move a token and the visible area changes with it. Open a door and the room beyond appears.

### Drawing walls

Draw walls with ![pencil][icon-pencil] or ![highlighter][icon-highlighter] on the wall layer. Draw
along every solid edge — room walls, cliff edges, the outside of a building.

- *Rectangle* and *Line* styles suit rectangular corridors.
- *Freehand* suits caverns.
- Tap ![snap][icon-snap] to snap to the grid. Freehand never snaps.

You do not have to be neat. A wall a few pixels off looks identical in play.

### Wall types

Not everything that stops a creature stops its eyes. Each wall has a type:

| Type | Blocks vision | Blocks movement | Use for |
| --- | --- | --- | --- |
| **Normal** | yes | yes | Ordinary walls |
| **Invisible** | no | yes | Windows, railings, force fields |
| **Ethereal** | yes | no | Curtains, fog banks, hidden passages |
| **Terrain** | at a distance | at a distance | Pillars, boulders, trees |
| **Door** | depends on its state | depends on its state | Doors |
| **Secret door** | like a door | like a door | Doors your players do not know about |

**Terrain** is the clever one. A creature standing beside a pillar can see and move past it, but the
same pillar still blocks vision from across the room — which is how a real pillar behaves.

### One-sided walls

A wall can block from one side only. That gives you a balcony you can see down from but not up to, or
a one-way window.

### Doors

A door wall carries a state — closed, open, or locked — that you change during play. Tap it to open
it, and everything behind it comes into view.

A **secret door** is not shown to your players until you reveal it. To them it looks like wall.

### The walls generator

Drawing walls by hand takes time. The walls generator does it for you, based on the walkable floor
you paint on the **floor** layer.

1. Paint the walkable floor of the dungeon.
2. Tap ![settings][icon-settings].
3. Tap **Walls Generator**.
4. Adjust the parameters and tap **Generate**.

| Parameter | What it does |
| --- | --- |
| **Wall Offset** | How far the wall sits from the edge of the floor |
| **Floor Color** | Only use floor painted in this colour |
| **Continuous** | One unbroken wall per edge, instead of separate segments |

It works best on dungeons with straight corridors. Run it as often as you like — each run replaces
the walls from the last one, so experimenting costs nothing.

## Lights

A light source lights the area around it, out to two radii: bright light first, then dim light.

| Setting | What it does |
| --- | --- |
| **Enabled** | Whether it is lit — a torch can be put out without deleting it |
| **Bright / Dim radius** | How far the light reaches, in grid units |
| **Color** and **Opacity** | How the light tints the map |
| **Always Visible** | Show the light even in areas the players cannot see |

*Always Visible* is for a campfire across the valley, or a lit window in a house the party has not
reached yet.

A light can sit on the map, or be attached to a piece of scenery — a brazier that lights the room and
moves with the furniture.

### Daylight and vision limit

Two map-wide settings shape the whole scene:

- **Daylight** raises the ambient light level. Turn it up for outdoor maps, where nobody needs a
  torch; leave it dark for dungeons.
- **Vision Limit** caps how far anything can be seen, regardless of light. Use it for fog, blizzards
  and heavy undergrowth.

## Token vision

Lights show what is lit. Token vision decides who sees it.

Each token has its own settings — see [Tokens](/guides/battle-maps/tokens/#vision):

- **Vision** off means the token sees nothing and contributes nothing.
- **Light** is a source the token carries, which lights the map for everyone.
- **Darkvision** lets the token see without light, and reveals the map to that token alone.

A party in a dark corridor is the clearest example. The human carrying the torch lights the corridor
for everyone. The dwarf with darkvision sees further, but only for themselves.

## What your players see

Your players see the combined view of the party, and you decide how much is shared.

**Shared Party Vision** in
[External Screen Settings](/settings/external-screen/#shared-party-vision) has three options —
*Never*, *Partial* and *Always*. *Partial* shares vision while exploring but not during combat, which
keeps a scout's discoveries to themselves once the fight starts.

On your own screen, **DM Darkness** controls how dark the unseen areas look. Turn it down when you
need to see the whole map while your players see only their part of it.

## Making it faster

Line of sight is the most expensive thing the map does. Two settings help on large maps and older
devices:

- **Only Update on Drop** recomputes once the token is dropped, rather than continuously while
  dragging.
- **Soft Edges** can be turned off for a small saving.

Both are in [Battle Map Settings](/settings/battle-map/#line-of-sight).

## Common questions

### My players see everything

Check that **Line of Sight** is on for the map, and that the map actually has walls. Without walls
there is nothing to block vision.

### My players see nothing

Usually no light and no darkvision. Give someone a torch, raise **Daylight**, or check that the
tokens have **Vision** enabled.

### Light leaks between rooms

A wall is missing or has a gap in it. Zoom in on the corners of the room — small gaps at wall joins
are the usual cause.

### A door does nothing

Check its type is **Door** rather than **Normal**, and that line of sight is on.

## Where to go next

- [Tokens](/guides/battle-maps/tokens/) — the vision settings each creature carries.
- [Battle Maps](/guides/battle-maps/) — grid, layers and background.
- [Remote Play](/guides/remote-play/) — what online players see.

[icon-pencil]: /assets/icons/pencil.png
[icon-highlighter]: /assets/icons/highlighter.png
[icon-snap]: /assets/icons/snap.png
[icon-settings]: /assets/icons/settings.png
[icon-reveal]: /assets/icons/reveal.png
[icon-hide]: /assets/icons/hide.png
[icon-fog-rect]: /assets/icons/fog-rect.png
[icon-fog-free]: /assets/icons/fog-free.png
