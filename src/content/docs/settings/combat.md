---
title: Combat Settings
description: How combatants are loaded into an encounter, and how the initiative window is displayed.
---

**Settings → Main Settings → Combat**, or the overflow menu of the initiative window. Both open the
same screen, so the settings you reach for mid-session are one tap away from the initiative order.

## General

### Load Mode

What happens when you load a creature from the library.

| Option | Effect |
| --- | --- |
| **Combat and Map** *(default)* | Add the entity to combat and create a token on the map. |
| **Combat** | Add the entity to combat only. |
| **Map** | Create a token on the map only. |

### Hidden by Default

Whether newly loaded combatants start hidden from the players. Off by default — loaded creatures are
visible straight away.

Turn this on when you build encounters in front of your players and want to reveal creatures
deliberately.

### Hit Points

The formula used to derive a monster's hit points when it is loaded.

| Option | Effect |
| --- | --- |
| **Standard** *(default)* | Roll hit points. |
| **Average** | Use average hit points. |
| **Minimum** | Use minimum hit points. |
| **Maximum** | Use maximum hit points. |

This only works when the monster's hit points are given as a dice formula — either on its own
(`2d8 + 2`) or in parentheses after a fixed value (`11 (2d8 + 2)`). If there is no formula to work
from, the value is used as written and this setting has no effect.

This applies at load time, so it does not change creatures already in the encounter.

## Interface

### Initiative Window Style

The size and behaviour of the initiative window.

| Option | Effect |
| --- | --- |
| **Standard** *(default)* | Standard window size. |
| **Compact** | Compact window size. |
| **Combined** | Compact window size only in combat. |

The compact style trims each row down to the combatant's image, its status icons and — if
**Include Name in Compact Style** is on — its name.

### Include Name in Compact Style

Whether combatant names are shown in the compact style. On by default.

Only shown when **Initiative Window Style** is *Compact* or *Combined* — the standard style always
shows names.

### Initiative/Health Input Window Size

The size of the small window used to enter initiative and health values.

| Option | Effect |
| --- | --- |
| **Standard** *(default)* | More suitable for small fingers. |
| **Large** | More suitable for large fingers. |
