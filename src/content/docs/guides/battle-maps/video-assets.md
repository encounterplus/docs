---
title: Video & Transparent Assets
description: Using video as map artwork — looping spell effects and animated scenery, including transparent video and how to convert WebM files from effect packs.
---

An asset can be a video instead of a still image. Set its **Type** to *Video* in the asset editor and
point it at an `.mp4` file, and every tile, token or area effect using that asset plays it.

This is how animated spell effects work: a fireball that actually burns, a shimmering portal, a
banner that moves in the wind. Most of the effect packs people use are built for exactly this.

## Transparency

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

## Converting a WebM file

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

## Converting on a computer

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

## Playback options

Video assets have a few more parameters:

| Parameter | Default | What it does |
| --- | --- | --- |
| **Loop** | On | Restarts when it reaches the end. Most ambient effects want this. |
| **Muted** | On | A map can hold many videos at once, and none of them should start making noise on their own. |
| **Speed** | 1.0 | A multiplier on normal playback speed. |

:::tip
Keep effect videos short and let them loop. A two-second clip that loops looks the same on the table
as a thirty-second one, and it's a fraction of the size in your exported module.
:::
