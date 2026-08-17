---
title: Drawing, Markers & Effects
description: Annotating a map during play — pen and highlighter, markers, the measuring tool, spell areas, and scenery tiles from asset packs.
---

Everything on this page is something you add on top of the map: a sketch, a note, a spell template, a
piece of furniture.

They differ in one useful way — some are for your players, and some are only for you.

## Drawing

You can draw on a map to highlight an area, add environmental effects, or sketch a dungeon.

### Drawing

1. Tap ![pencil][icon-pencil] or ![highlighter][icon-highlighter].
2. Draw with a finger, a stylus or a mouse.

### Changing colour, size or style

1. Tap ![pencil][icon-pencil] or ![highlighter][icon-highlighter] a second time.
2. Pick a colour, size or style.

Styles are freehand, line, rectangle and ellipse.

### Erasing and undoing

- Tap ![eraser][icon-eraser], then tap a stroke to erase it.
- Tap ![undo][icon-undo] to take back your last stroke.

### Snap to grid

Tap ![snap][icon-snap] to snap drawings to the grid. Freehand never snaps.

### Scrolling while drawing

Use two fingers to pan and zoom without leaving the drawing tool.

### Which layer you draw on

This is the part worth getting right.

- Draw on the **object** layer and your players see it.
- Draw on the **DM** layer and only you do.

So a highlighted room is an object-layer drawing, and a note about the trap in it belongs on the DM
layer. Drawings stay editable, and can be moved between layers afterwards.

:::note
Drawings are sent to players during [Remote Play](/guides/remote-play/), whichever layer they are on
— except the DM layer.
:::

## Markers

A marker is a pin on the map that holds a note. Use them for room descriptions, read-aloud text,
traps and anything else you want to find again mid-session.

### Adding a marker

1. Tap ![markers][icon-markers].
2. Tap ![add][icon-add] to add one.

Or just **double-tap the map** to drop a marker where you tapped.

### Editing and deleting

1. Tap an existing marker twice.
2. Choose **Edit** or **Delete**.

### Marker settings

| Field | What it does |
| --- | --- |
| **Name** | Floating text above the marker |
| **Label** | The character drawn inside it |
| **Color** | Its colour |
| **Shape** | Marker, pin, circle or label |
| **Size** | Tiny through huge, relative to the grid |
| **Content** | The text you read when you tap it |
| **Hidden** | Hides it from your players. On by default |
| **Locked** | Stops it being moved by accident |

Markers are hidden by default, which is usually what you want — they are your notes. Reveal one when
the party finds what it describes and it appears on the player screen too.

A marker can also point at a page or another entry, so tapping it opens your prepared text instead of
holding a copy of it.

## Measuring

The measuring tool draws a path and tells you how long it is.

Two counting methods:

| Type | How distance is counted |
| --- | --- |
| **Grid** | Counts the cells crossed, as tabletop rules do |
| **Precise** | True geometric distance |

A measurement can be left on the map, so a planned move or a spell's reach stays visible while people
argue about it.

## Area effects

An area effect is a spell template anchored to the map — a fireball's sphere, a breath weapon's cone,
a wall of fire's line.

| Shape | Sized by |
| --- | --- |
| **Sphere** | Radius |
| **Cylinder** | Radius |
| **Cone** | Length, aimed by angle |
| **Line** | Length and width |
| **Square** | Width |
| **Cube** | Width |

Each has a colour and opacity, and can be hidden from your players or locked in place.

An area effect stays where you put it. For an area that follows a creature instead, use an aura — see
[Tokens](/guides/battle-maps/tokens/#auras).

## Tiles and asset packs

A tile is scenery: furniture, doors, props, decals, overlays. Anything on the map that is not a
creature.

Tiles come from **asset packs** you import or download from the Package Manager. Place one, then
size, rotate and layer it like any object.

Two things make tiles more than decoration:

- A tile can carry a **light**, so a brazier both appears on the map and lights the room around it.
- A tile can carry a **reference**, which makes it tappable — opening a page, a creature or another
  entry.

Tiles can be locked so they stop moving once the scene is dressed.

:::note
Animated tiles are part of the **Premium** subscription.
:::

## What players see

A quick summary, since this is where most confusion starts:

| Thing | Players see it? |
| --- | --- |
| Drawings on the object layer | Yes |
| Drawings on the DM layer | No |
| Markers | Only when not hidden |
| Area effects | Yes, unless hidden |
| Tiles | Yes, unless hidden |
| Measurements | Yes, unless hidden |

## Where to go next

- [Battle Maps](/guides/battle-maps/) — layers, grid and background.
- [Line of Sight & Fog](/guides/battle-maps/line-of-sight/) — hiding the map itself.
- [Import and Export](/guides/import-and-export/) — getting asset packs in.

[icon-pencil]: /assets/icons/pencil.png
[icon-highlighter]: /assets/icons/highlighter.png
[icon-eraser]: /assets/icons/eraser.png
[icon-undo]: /assets/icons/undo.png
[icon-snap]: /assets/icons/snap.png
[icon-markers]: /assets/icons/markers.png
[icon-add]: /assets/icons/add.png
