---
title: Assets
description: The artwork behind tokens, tiles and effects — where assets come from, the asset types, tags and components, and video assets including transparent video and WebM conversion.
---

An **asset** is a piece of artwork used on a map. Every token, tile, area effect and aura is drawn
with one.

An asset is more than an image file. It has a name and tags, a **type** that decides how its file is
played, and parameters that control size and placement. Open one in the asset editor to change any
of these.

## Where assets come from

Assets live in the library, inside a module, a campaign or a game system. Asset packs from the
Package Manager are the usual source, and you can add your own to any campaign.

Assets in the library are **blueprints**. When you place one on a map, the tile or token gets its
own copy of it:

- **Editing a placed asset changes only that object.** Tint one brazier red and the others on the
  map, and the original in the library, stay as they were.
- **Editing a library asset does not change what is already on your maps.** It applies the next time
  you place it.
- **Copies do not use extra space.** Every copy of an asset points at the same file on disk, so
  placing the same tree a hundred times costs one image.

## Asset types

| Type | What it is |
| --- | --- |
| **Image** | A single still image. The default. |
| **Pattern** | An image repeated to fill the area it covers, such as a floor texture or a hedge. |
| **Sprite Sheet** | A grid of frames played in sequence — the classic format for animated effects. |
| **Animated Image** | A file that carries its own animation, such as an animated GIF or WebP. |
| **Video** | A video file, played in place. It can be transparent — see [Video assets](#video-assets). |

:::note
Animated tiles are part of the **Premium** subscription. See [Purchases](/settings/purchases/).
:::

### Parameters

Every asset has these:

| Parameter | What it does |
| --- | --- |
| **Grid Size** | How many grid squares the artwork covers, written as `2x3`. |
| **Scale** | A multiplier on the drawn size. |
| **Horizontal / Vertical Offset** | Nudges the artwork off centre, as a percentage. |

Some types add their own:

| Type | Parameter | What it does |
| --- | --- | --- |
| Pattern | **Grid Align** | Lines the repeating pattern up with the map grid. |
| Sprite Sheet | **Frame Width / Height** | The size of one frame, in pixels. |
| Sprite Sheet | **Duration** | The length of the animation, in seconds. Set to 1 second on import. |

Video's parameters are covered in [Video assets](#video-assets).

### Set from the file name

When you import an image or video, the app reads its file name to fill in the type and parameters,
so a well-named asset pack needs no editing:

| In the file name | Sets |
| --- | --- |
| `2x3` | **Grid Size** to 2 × 3 squares |
| `fx256x256` | **Sprite Sheet**, with 256 × 256 pixel frames |
| `.gif`, or `afx` | **Animated Image** |
| A video extension | **Video** — see [the naming rules](#converting-on-a-computer) for transparency |

You can always correct what was guessed in the asset editor.

## Names and tags

An asset's name and tags are how you find it again in a large pack.

They also drive **random assets**. When the app places something that has no artwork of its own,
such as a status effect's aura, it looks through the modules chosen in the current campaign's
[Campaign Settings](/guides/campaigns-and-modules/#random-assets) for an asset whose name or tag
matches, and picks one at random. Tag a few flame effects `fire` and every fire effect gets one of
them.

## Components

Components change how an asset is drawn without editing its file. Add them under **Components** in
the asset editor; an asset can have one of each.

| Component | What it does |
| --- | --- |
| `filter.hsb` | Shifts hue, saturation and brightness. |
| `filter.tint` | Tints the artwork towards a colour, at an intensity you choose. |
| `animation.rotation` | Spins the artwork. |
| `animation.opacity` | Fades it in and out. |
| `animation.scale` | Pulses its size. |

The animations each take a start and end value, a duration, a repeat count and whether to play back
in reverse. A still image of a portal becomes a living one with a slow rotation and a pulse.

A component can be switched off without deleting its settings. Components set on the asset apply
wherever it is used.

## Video assets

An asset can be a video instead of a still image. Set its **Type** to *Video* in the asset editor and
point it at an `.mp4` file, and every tile, token or area effect using that asset plays it.

This is how animated spell effects work: a fireball that actually burns, a shimmering portal, a
banner that moves in the wind. Most of the effect packs people use are built for exactly this.

### Playback options

| Parameter | Default | What it does |
| --- | --- | --- |
| **Loop** | On | Restarts when it reaches the end. Most ambient effects want this. |
| **Muted** | On | A map can hold many videos at once, and none of them should start making noise on their own. |
| **Speed** | 1.0 | A multiplier on normal playback speed. |

### Transparency

A spell effect has to sit on top of the map without a black box around it. That needs transparency,
and no video format the iPad can play carries a transparency channel reliably.

Encounter+ solves it the way the wider effects community does: a **split alpha** video. Each frame
of the file is twice the size of the picture — one half is the artwork, the other half is the
transparency mask in greyscale, where white is solid and black is invisible. The app reassembles the
two halves as it draws.

So the file looks wrong if you open it in a normal video player. That's expected. What matters is
that the asset's parameters describe how it's packed:

| Parameter | What it does |
| --- | --- |
| **Transparent (Split Alpha)** | Tells the app the frame is packed this way. Off means the video is drawn opaque. |
| **Alpha Layout** | *Side by Side* — artwork left, mask right. *Top and Bottom* — artwork top, mask bottom. |

Both are set for you when you use the built-in conversion below.

### Converting a WebM file

Almost every transparent effect pack you'll find online ships as `.webm`, which iOS cannot play at
all. Encounter+ can convert one for you.

In the asset editor, open the menu beside the video row and choose **Convert WebM (Experimental)**,
then pick the file. A progress sheet appears while it works — a few seconds for a typical effect —
and when it finishes the converted video is attached to the asset with its transparency parameters
already filled in.

The conversion happens entirely on your device. Nothing is uploaded anywhere, and it works offline.

:::note
This is a new feature and marked experimental. If a file won't convert, the error message names the
reason — most often the codec. Converting it on a computer, as below, always works.
:::

A few things worth knowing:

- **AV1 files can't be converted.** They're rare in effect packs today but becoming less so. The app
  will tell you if you hit one.
- **A WebM without transparency still converts**, to an ordinary opaque video. That's still useful,
  since iOS couldn't open the original.
- **Very wide videos are packed top-and-bottom** instead of side by side. A 4000 × 400 line effect
  would be 8000 pixels wide packed side by side, which is more than the video encoder accepts.
- **Converted files can be larger than the original.** WebM is an efficient format, and the
  converted video is twice the size of its picture. This matters because assets travel inside every
  module you export.

### Converting on a computer

If you'd rather convert in bulk, or the in-app conversion refuses a file, [ffmpeg](https://ffmpeg.org)
does the same job:

```sh
ffmpeg -i effect.webm -filter_complex \
  "[0:v]alphaextract,format=yuv420p[a];[0:v]format=yuv420p[c];[c][a]hstack=inputs=2" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -an effect_sbs.mp4
```

That produces a side-by-side file. For a top-and-bottom one, replace `hstack=inputs=2` with
`vstack=inputs=2`.

The `_sbs` suffix isn't decoration. When Encounter+ imports a video file, it reads the name to work
out how the frame is packed:

- `_sbs` or `_alpha` — side by side
- `_tb` — top and bottom

Name your files this way and the transparency parameters are set automatically on import. You can
always correct them by hand in the asset editor.

:::tip
Keep effect videos short and let them loop. A two-second clip that loops looks the same on the table
as a thirty-second one, and it's a fraction of the size in your exported module.
:::

## Where to go next

- [Drawing, Markers & Effects](/guides/battle-maps/drawing-and-effects/) — placing tiles and area
  effects.
- [Tokens](/guides/battle-maps/tokens/) — token artwork and auras.
- [Campaigns & Modules](/guides/campaigns-and-modules/#random-assets) — choosing the modules random
  assets come from.
