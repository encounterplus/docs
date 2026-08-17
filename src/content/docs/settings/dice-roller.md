---
title: Dice Roller Settings
description: Roll visibility, the standard and 3D dice rollers, random number generation, sound, and dice themes.
---

**Settings → Main Settings → Dice Roller.**

## General

### Mode

Whether dice rolls are shared with your players.

| Option | Effect |
| --- | --- |
| **Public** *(default)* | Dice rolls will be visible on the external screen and web client. |
| **Private** | Dice rolls will be hidden. |

### Type

Which roller is used. **Premium subscription only** — without it, the standard roller is used and
this row is not shown.

| Option | Effect |
| --- | --- |
| **Standard** *(default)* | Standard dice roller using a pseudo-random number generator. |
| **3D** | 3D dice roller using a high precision physics simulation. |

Choosing **3D** reveals the 3D sections described below, directly under this row.

### Random Generator

The source of randomness behind every roll, for both roller types.

| Option | Effect |
| --- | --- |
| **Mersenne Twister** *(default)* | Fast PRNG using the GameplayKit `GKMersenneTwisterRandomSource` implementation. |
| **System Random** | Standard PRNG using the Swift random (`arc4random_buf`) implementation. |
| **Crypto Secure** | Cryptographically secure PRNG using the `SecRandomCopyBytes` implementation. |

All three are fair; they differ in speed and in how the randomness is produced. The default is the
fastest and is fine for play.

### Sound Effects

The dice rolling sound. On by default, and applies to both the standard and the 3D roller.

## 3D Dice

Shown only with a Premium subscription and **Type** set to *3D*.

### Physics Speed

How fast the dice simulation runs.

| Option | Effect |
| --- | --- |
| **Normal** *(default)* | 1.0× normal speed. |
| **Fast** | 2.0× normal speed. |
| **Ultra** | 3.0× normal speed. |

Faster speeds settle the dice sooner, which keeps play moving.

### Performance Stats

Overlays the renderer's performance statistics on the dice view. Off by default; this is a
diagnostic aid, not a play feature.

## Dice themes

A theme is a **material** plus an optional **tint colour** and **text colour**.

### Default Theme

The theme used by every roll that has no theme of its own.

### Custom Theme

Four roll kinds can each carry a theme of their own — **Attack**, **Damage**, **Save** and
**Check** — so you can tell at a glance what was rolled. Any of them may be left unset, shown as
*Default* in the list, in which case it follows the default theme.

### Editing a theme

Tapping a theme opens the editor, which shows a live preview above the settings:

- **Material** — the dice surface, picked from the built-in materials.
- **Tint Color** — the body colour. Swipe the row to reset it back to the material's own colour.
- **Text Color** — the number colour. Swipe the row to reset it likewise.

The editor is the one place in Settings that does not save instantly: press **Save** to keep the
changes, or **Reset** to clear the theme entirely and fall back to the default.
