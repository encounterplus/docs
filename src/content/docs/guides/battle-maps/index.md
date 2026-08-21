---
title: Battle Maps
description: Creating a map, setting up the background and grid, understanding layers, and sharing the map with your players.
---

A battle map is the playing surface. It is a background image, a grid that says how big a square is,
and layers of things placed on top: tokens, scenery, walls, lights and your own drawings.

This page covers the map itself. The things you put on it have their own pages:

- [Tokens](/guides/battle-maps/tokens/) — creatures on the map.
- [Line of Sight & Fog](/guides/battle-maps/line-of-sight/) — hiding and revealing.
- [Drawing, Markers & Effects](/guides/battle-maps/drawing-and-effects/) — annotation and spell areas.

:::note
Battle maps need the one-time **Battle Map** purchase. Without it the map screen and its settings are
not available. See [Purchases](/settings/purchases/).
:::

:::tip
For every option on the map's settings screen, see [Battle Map Settings](/settings/battle-map/).
:::

## The toolbar

| Icon | Tool | What it does |
| --- | --- | --- |
| ![pencil][icon-pencil] | **Pencil** | Draw lines and shapes |
| ![highlighter][icon-highlighter] | **Highlighter** | Shade an area |
| ![eraser][icon-eraser] | **Eraser** | Remove a stroke |
| ![undo][icon-undo] | **Undo** | Take back the last drawing |
| ![move][icon-move] | **Move** | Pan the map and drag tokens |
| ![select][icon-select] | **Select** | Select several objects at once |
| ![layers][icon-layers] | **Layers** | Choose which layer you are working on |
| ![snap][icon-snap] | **Snap to Grid** | Align movement and drawing to the grid |
| ![reveal][icon-reveal] | **Fog of War** | Reveal and hide parts of the map |
| ![markers][icon-markers] | **Markers** | Add and manage markers |
| ![tools][icon-tools] | **Tools** | Grid align, map resize and the walls generator |
| ![settings][icon-settings] | **Settings** | The map's own settings |

Several tools have a second set of options. **Tap the tool a second time** to open them — that is how
you change ink colour, switch fog between rectangle and freehand, or turn on restricted movement.

## Creating a map

Tap **New Map** from the game screen menu, or create one inside a campaign or module in the library.

A new map starts empty. Give it a name, then add a background.

Maps live in a campaign or module, like any other content. See
[Campaigns & Modules](/guides/campaigns-and-modules/).

## The background

A map can use an **image** or a **video** as its background.

1. Tap ![settings][icon-settings].
2. Tap **Image** and choose *Photo Library* or *Browse Files*.
3. Pick your file.

A video background loops, which suits water, fire and weather. Everything else works the same as with
an image.

You can also import a map made in another tool. `.dd2vtt` and `.uvtt` files bring their own walls,
lights and grid, so they arrive ready to play. See
[Import and Export](/guides/import-and-export/).

## The grid

The grid is what turns a picture into a playing surface. It tells the app how far a square is, which
makes movement, distances, light radii and spell areas mean something.

### Matching the grid to your image

Most map images already have a grid drawn on them. Your job is to line the app's grid up with it.
The **Grid Align** tool does this for you, and is the way to do it.

1. Tap ![tools][icon-tools] and choose **Grid Align**.
2. A 3x3 mesh appears on the map. Drag it into place and resize it until its nine cells sit exactly
   on nine squares of the image.
3. Tap **Apply**.

The app works out the grid size and offset from the mesh, so the whole grid lines up at once. Using
three squares rather than one spreads out any small error you make, which is what keeps the far
corner of the map aligned as well as the near one.

You can still set **Grid Size**, **Offset X** and **Offset Y** by hand in the map's settings if you
want to nudge the result, or if the image has no grid to match.

### Grid options

| Option | What it does |
| --- | --- |
| **Grid Visible** | Show or hide the grid |
| **Grid Size** | The size of one grid square |
| **Offset X** / **Offset Y** | Slide the grid to match the image |
| **Grid Type** | Square, or hex with flat or pointed tops |
| **Grid Style** | Full lines, or short marks at the cell corners |
| **Grid Color** and **Opacity** | How strongly the grid is drawn |
| **Scale** and **Units** | What one cell means — 5 ft by default |

Corner marks are worth knowing about: they keep the grid readable without drawing lines all over
someone's artwork.

**Scale** and **Units** feed every distance in the app. Set them to match your game — 5 ft, 1.5 m, or
whatever your system uses — and movement paths, light radii and area effects follow.

## Tools

![tools][icon-tools] holds three tools that change the map as a whole, rather than editing one thing
on it.

### Grid Align

Lines the grid up with the grid drawn on your background image. See
[Matching the grid to your image](#matching-the-grid-to-your-image) above.

### Map Resize

Changes the size of the map. Give it a new width and height, or a percentage to scale by.

Everything on the map is resized with it — tokens, drawings, lights and walls all keep their position
relative to the background, so a map you have already walled and lit survives the change.

This is mostly a [performance](#performance) tool. Very large map images are the usual cause of a
sluggish map on an older device, and scaling one down is the most direct fix. Reach for it before
turning renderer settings off.

### Walls Generator

Builds walls automatically from the **Floor** layer. Paint the walkable ground on the floor layer
first; the generator then traces its edges and creates walls along them.

It is the fast way to get [line of sight](/guides/battle-maps/line-of-sight/) working on a map — a
few minutes of painting floor instead of drawing every wall by hand. Treat the result as a starting
point and tidy it up: doors in particular need to be placed yourself, since the generator only sees
where the floor ends.

## Layers

Everything on a map sits on a layer. Layers decide what is drawn over what, and who can see it. Tap
![layers][icon-layers] to switch.

| Layer | What belongs there |
| --- | --- |
| **Map** | The background image or video |
| **Floor** | Walkable ground, used by the walls generator and pathfinding |
| **Object** | Scenery and drawings — the default layer |
| **Token** | Creature tokens |
| **Light** | Light sources |
| **Wall** | Walls, doors and obstacles used by [line of sight](/guides/battle-maps/line-of-sight/) |
| **DM** | Your own notes and drawings — never shown to players |

The **DM** layer is the important one. Anything you draw there is yours alone, so it is where the
secret door goes, and the arrow reminding you which way the ambush comes from.

## Moving around

1. Tap ![move][icon-move].
2. Drag with one finger to pan. Pinch with two to zoom.

On a trackpad or mouse, scroll to pan or zoom — the two are configured separately in
[Battle Map Settings](/settings/battle-map/#touchpad-scroll-action).

Double-tap to point at something. Depending on your settings this shows a ripple, moves the players'
camera, or both. The camera actions are how you direct attention: a double tap can pull every
player's view to the thing you are talking about.

## Showing the map to players

The map you edit and the map your players see are the same map, drawn differently. Your hidden
tokens, DM-layer drawings and notes stay on your side.

Share the map to the player-facing view, then show it either way:

- **In the room** — AirPlay or HDMI. See [The Player Screen](/guides/player-screen/).
- **Online** — the built-in web server. See [Remote Play](/guides/remote-play/).

Two map settings only affect *your* screen, not theirs:

- **DM Darkness** — how dark the areas your players cannot see appear to you. Turn it down when you
  need to see the whole map while running line of sight.
- **DM Marker Style** — how markers are drawn on your side.

## Weather

A map can carry a weather effect — rain, snow and similar — with an intensity you control. It is
drawn over the whole map and is shown to your players too.

:::note
Weather effects are part of the **Premium** subscription.
:::

## Saving

Maps save their own state: token positions, fog of war, drawings and markers. Save the map and it
comes back exactly as you left it.

That is separate from saving an encounter. An encounter holds combatants; a map holds the board. See
[Encounters & Combat](/guides/encounters/).

## Performance

Large maps on older devices can feel heavy. The first thing to try is scaling the map down with
[Map Resize](#map-resize) — an oversized background image is the usual culprit.

Beyond that, three settings help, all in [Battle Map Settings](/settings/battle-map/):

- **Low Power Mode** throttles the renderer.
- **Only Update on Drop** recomputes line of sight once per move instead of continuously.
- **Advanced Pathfinding** can be turned off if drawn movement paths cost too much.

## Where to go next

- [Tokens](/guides/battle-maps/tokens/) — putting creatures on the map.
- [Line of Sight & Fog](/guides/battle-maps/line-of-sight/) — the part that takes the most setup.
- [Drawing, Markers & Effects](/guides/battle-maps/drawing-and-effects/) — annotating during play.

[icon-pencil]: /assets/icons/pencil.png
[icon-highlighter]: /assets/icons/highlighter.png
[icon-eraser]: /assets/icons/eraser.png
[icon-undo]: /assets/icons/undo.png
[icon-move]: /assets/icons/move.png
[icon-select]: /assets/icons/select.png
[icon-layers]: /assets/icons/layers.png
[icon-snap]: /assets/icons/snap.png
[icon-reveal]: /assets/icons/reveal.png
[icon-markers]: /assets/icons/markers.png
[icon-tools]: /assets/symbols/wrench.and.screwdriver.png
[icon-settings]: /assets/icons/settings.png
