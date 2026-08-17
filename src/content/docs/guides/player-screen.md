---
title: The Player Screen
description: The player-facing display — connecting a TV or projector, what your players see, and the controls you use during play.
---

The player screen is the second view Encounter+ draws — the one your players look at. It shows the
map, the initiative order and whatever you are presenting, without your notes.

It goes to an AirPlay display, a monitor connected by cable, or a second window on Mac. The same view
is what online players see in the browser, so setting it up once covers both. See
[Remote Play](/guides/remote-play/).

## Connecting a display

| How | What to do |
| --- | --- |
| **AirPlay** | Mirror to an Apple TV or AirPlay-capable screen |
| **Cable** | Connect an HDMI or USB-C adapter |
| **Mac** | Open the player screen as a second window |

Once connected, the external screen controls show the **status** and the **resolution** of the
display, so you can confirm it is really connected before your players arrive.

On Mac, **Open Window** puts the player view in its own window, which you can drag to a second
monitor.

## The two halves

The player screen is configured in two places, split by how often you change things:

- **The controls** — what you are showing right now. Opened from the game screen.
- **The settings** — how it looks. In **Settings → External Screen**, and linked from the controls.

If you are mid-session and want to change what your players see, you want the controls.

## The controls

### Battle map

**Presenting** picks which of the loaded maps is on the player screen — or none.

The **viewport** shows you what part of the map your players can currently see, drawn on your own
screen. **Fit Screen** matches their view to yours, which is the quickest way to get everyone looking
at the same thing.

### Overlay

The overlay covers the screen with something other than the map:

| Type | What it shows |
| --- | --- |
| **None** | Nothing — the map or the default theme |
| **Image** | A picture, full screen |
| **Handout** | Text you write, in your chosen style |

Use **Image** for artwork, a portrait or a battle map you are not running yet. Use **Handout** for a
letter, a prophecy, or anything the party reads out.

## The look

The rest is set up once, in [External Screen Settings](/settings/external-screen/):

- **Default theme** — a title and background shown when nothing else is on screen.
- **In-combat theme** — a background and the initiative order's position and style.
- **Shared party vision** — how much of the party's line of sight is pooled.
- **Screen margins** and **overscan** — for TVs that crop the edges of the picture.

### The initiative order

The initiative display can fill the screen or sit along one edge.

The full-screen layouts — flow, detail and grid — are only available when no map is shown, because a
map fills the display. With a map up, you get the edge positions or nothing at all.

You also choose which names are labelled: everyone, monsters only, players only, or none. Hiding
monster names is a simple way to keep an unidentified creature mysterious.

## What stays on your device

Your players never see:

- Hidden tokens.
- Anything on the DM layer.
- Hidden markers.
- Your notes, the library and settings.

They also see only what their characters can see, if line of sight is on. See
[Line of Sight & Fog](/guides/battle-maps/line-of-sight/).

## Directing attention

Double-tapping the map can move the players' camera to that spot, show a pointer ripple, or both,
depending on
**[Double Tap Action](/settings/battle-map/#double-tap-action)**.

It is the fastest way to say "look here" without describing where.

## Common questions

### The display is connected but shows nothing

Check the **status** row in the controls. If it reports a connection, check that a map is selected
under **Presenting**, or that a default theme background is set.

### The edges are cut off on my TV

Use **Overscan** and **Screen Margins** in
[External Screen Settings](/settings/external-screen/). Many TVs crop the picture slightly.

### My players can see something they should not

Check three things: the token's **Hidden** flag, which layer the drawing is on, and whether the
marker is hidden.

## Where to go next

- [External Screen Settings](/settings/external-screen/) — every row on the settings screen.
- [Remote Play](/guides/remote-play/) — the same view, in a browser.
- [Battle Maps](/guides/battle-maps/) — what you are presenting.
