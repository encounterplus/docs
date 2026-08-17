---
title: External Screen Settings
description: The player-facing display — default and in-combat themes, shared vision, physical setup, and AirPlay.
---

**Settings → Main Settings → External Screen**, or the Settings row inside the external screen
controls on the game screen.

The external screen is what your players see, on an AirPlay display, a connected monitor, or a
second window on Mac. It is split in two by how often you change it:

- **This screen** holds the setup — themes, the physical rig, the AirPlay connection — which you
  configure once for a display or a campaign.
- **The external screen controls**, opened from the game screen, hold what changes from scene to
  scene: which map is shown, the overlay, the handout.

Every change here applies immediately, except the AirPlay section, which needs a reconnect.

## Default Theme

What the players see when nothing else is being shown.

### Title

A title displayed on the screen. Leave it empty for none — clearing the field removes the title
rather than storing a blank one.

### Background Image

The backdrop for the default screen. You can pick from the photo library, the file browser or the
clipboard, and you can also drag an image straight onto the row.

Images are written as soon as they are picked; there is no Save button on this screen.

## In-Combat Theme

What the players see while combat is running.

### Initiative Style

Where and how the initiative order is drawn.

| Option | Notes |
| --- | --- |
| **Flow**, **Detail**, **Grid** | Full-screen layouts. Available only when no map is being shown. |
| **Top**, **Bottom**, **Left**, **Right** | The order sits along one edge, leaving the rest of the screen for the map. |
| **None** | No initiative order on the external screen. |

The available options change with what is on screen: a map fills the display, so while one is shown
only the edge styles and *None* remain.

### Initiative Labels

Which combatant names are labelled in the initiative order.

| Option | Effect |
| --- | --- |
| **All** | Label every combatant. |
| **Monsters Only** | Label monsters only. |
| **Players Only** | Label player characters only. |
| **None** | No labels. |

### Background Image

The backdrop shown during combat, picked the same way as the default background above.

## Line of Sight

### Shared Party Vision

Whether party members see through each other's eyes on the player-facing screen.

| Option | Effect |
| --- | --- |
| **Never** | No shared vision at all. |
| **Partial** | Shared vision for all party members outside of player turn/combat. |
| **Always** | Shared vision for all party members all the time. |

*Partial* is the middle ground: the party shares what it can see while exploring, but during combat
each character sees only for themselves.

## Screen

The physical display: how large it is, and how much of it the app may draw on.

### TableTop Mode

Draws the map at physical scale, for a screen laid flat in the table with miniatures on it. Off by
default.

With it on, the app locks the map to a fixed zoom so that the map grid matches real-world size — one
grid tile on the screen measures one inch on the table, the same as a standard miniature's base. Free
zooming on the external screen is disabled as a result.

It depends on the physical width below being correct — that is what the scale is computed against.

### Physical Width

The real width of the display, in centimetres or inches depending on your region's measurement
system. Measure the visible picture, not the bezel.

### Margins

Top, right, bottom and left margins in pixels, shown on the row as `top,right,bottom,left`.

Use these to keep the picture clear of a bezel, a frame, or the edge of a table cut-out.

## AirPlay Settings

These apply to an AirPlay connection. **Reconnect to apply** — changes do not affect a session
already in progress.

### Mirroring Mode

Mirrors the game screen to the external display instead of showing the separate player-facing view.
Off by default. Not available on Mac.

### Portrait Mode

Draws the player-facing view in portrait orientation. Off by default.

### Overscan

How the picture is fitted to a display that crops its edges — common on televisions. Not available
on Mac.

| Option | Effect |
| --- | --- |
| **Scale** | Scale the picture down so the whole of it lands inside the visible area. |
| **Inset Bounds** | Inset the drawing area, leaving a border. |
| **None** | No compensation. |
