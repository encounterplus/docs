---
title: Battle Map Settings
description: Party movement, default token style, input gestures, rendering performance, and line of sight.
---

**Settings → Main Settings → Battle Map.**

The whole screen requires the **Battle Map** purchase; without it the row is not shown on the main
Settings screen. For how to use the map itself, see the [Battle Map guide](/guides/battle-map/).

## General

### Party Movement Mode

How the party moves when you drag them as a group.

| Option | Effect |
| --- | --- |
| **Standard** *(default)* | Party members keep their relative formation as the group moves. |
| **Snake** | Party members follow the leader's path in single file. |

*Snake* suits corridors and narrow passages, where a formation cannot hold.

### Default Token Style

The style applied to newly created tokens. Existing tokens keep the style they were created with.

| Option | Effect |
| --- | --- |
| **TopDown** *(default)* | Top-down artwork drawn as-is, which reads correctly when the token is rotated. |
| **Circle** | A circular portrait, cropped and ringed by the token's role colour. |

### Double Tap Action

What a double tap on the map does.

| Option | Effect |
| --- | --- |
| **Point** *(default)* | Place a pointer at the tapped location. |
| **Camera Move** | Move the players' camera to the tapped location. |
| **Camera Point** | Move the players' camera and place a pointer there. |

The camera actions affect the external screen and the web client, so they are the ones to use when
you want to direct your players' attention.

### Touchpad Scroll Action

What a two-finger scroll on a trackpad does. **Pan** by default.

Options are **Pan** and **Zoom**.

### Mouse Scroll Action

What a mouse scroll wheel does. **Zoom** by default.

Options are **Pan** and **Zoom**.

Touchpad and mouse are configured separately because the same gesture means different things on the
two devices — the defaults match what each is normally expected to do.

### Token Movement Path

Draws the path while a token is dragged, with the distance travelled. On by default.

### Advanced Pathfinding

Routes the drawn movement path around obstacles rather than drawing a straight line. On by default.

Only shown when **Token Movement Path** is on — there is no path to route without it.

### Low Power Mode

Throttles the map renderer to save battery. Off by default.

Turn it on for long sessions on battery, or on older devices where the map feels warm or drains
quickly. Animation smoothness is reduced in exchange.

## Line of Sight

See the [Line of Sight guide](/guides/battle-maps/line-of-sight/) for what these affect in play.

### Only Update on Drop

Recomputes line of sight once the token is dropped, rather than continuously while it is dragged. On
by default.

Leaving this on keeps dragging smooth on large maps. Turn it off if you want the visible area to
update live as a token moves.

### Soft Edges

Feathers the edges of the visible area instead of cutting them off sharply. On by default.
