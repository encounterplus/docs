---
title: Encounters & Combat
description: Building an encounter, adding combatants on the fly, rolling initiative, and tracking hit points, conditions and turns while you run the fight.
---

An encounter is a group of combatants you plan to throw at your players. Combat is what happens when
you run it.

This page covers both: building the encounter, then running it.

## What an encounter is

An encounter is a stand-alone thing. **It is not part of a map.**

That is deliberate. Because the two are separate, any encounter can be run on any map. Build
"Kobold Ambush" once and use it on every forest map you own.

An encounter holds combatants, their hit points, and their conditions. A map holds terrain, tokens
and fog. They meet on the game screen.

## Building an encounter

Tap the ![more][icon-more] **More** menu next to the initiative window. You get three ways to add
combatants:

| Action | What it does |
| --- | --- |
| **Load Combatant** | Pick a creature from the library |
| **New Combatant** | Create a one-off combatant by hand |
| **Load Party** | Add every player character in the current campaign |

**Load Combatant** is the usual one. Tap the same creature more than once to add several copies — the
app numbers them for you.

**New Combatant** is for something that only exists in this fight. It is not saved to the library.

**Load Party** needs a current campaign with player characters in it. See
[Campaigns & Modules](/guides/campaigns-and-modules/).

### Roles

Every combatant has a role, and it does more than colour the row:

| Role | Meaning |
| --- | --- |
| **Hostile** | An enemy. The default. |
| **Friendly** | A party member or ally. |
| **Neutral** | A bystander. |

Role decides the token ring colour on the map, whether initiative is rolled automatically, and
whether the combatant counts toward encounter difficulty.

### Hit points

A combatant's hit points are worked out when it is loaded. You choose how under
**Settings → Combat → [Hit Points](/settings/combat/#hit-points)** — rolled, average, minimum or
maximum.

This applies at load time only. Combatants already in the fight keep the hit points they have.

### Difficulty

With D&D 5E loaded, the game screen shows a difficulty rating for the current encounter. It compares
the experience value of the hostile combatants against the levels of your party.

Add or remove a combatant and the rating updates. It is a guide, not a rule.

:::note
Difficulty is a 5E feature. With another system loaded, the rating is hidden.
:::

### Loading onto the map too

By default, loading a combatant adds it to combat **and** puts a token on the map. Change this under
**Settings → Combat → [Load Mode](/settings/combat/#load-mode)**.

If you build encounters in front of your players, turn on
**[Hidden by Default](/settings/combat/#hidden-by-default)** so combatants arrive hidden and you
reveal them when you want.

## Running combat

Tap **start**. The app rolls initiative for the combatants and sorts the list.

By default it does not roll for player characters — you type their numbers in. You can change that in
[Combat Settings](/settings/combat/).

### Turns

- **next** moves to the next combatant.
- **previous** goes back.
- The current turn is highlighted, and rounds count up on their own.

### Hit points

Tap a combatant's hit points to open the damage input. Type a number and it is subtracted.

Switch the input to healing to add hit points instead. Temporary hit points and maximum hit points
can be adjusted the same way.

### Conditions

Swipe a row to reach its actions. From there you can add conditions, edit the combatant, or remove
it.

A condition can carry a duration and a source, so you can see where it came from and when it ends.
Tap a condition under a combatant to read what it does, or to remove it.

### Editing mid-fight

Swipe to edit a combatant to change its name, label, hit points, light or notes, or to hide it from
your players. Everything here is safe to change during combat.

### Ending combat

Tap **stop**. The order is kept, so tapping **start** again resumes where you were — you are asked
whether to re-roll initiative.

Two more actions in the menu are worth knowing:

- **Award Experience** splits the encounter's experience among the party.
- **Reset Encounter** clears the board and starts over.

## Saving and reusing

**Save Encounter** stores the current fight — combatants, hit points and conditions — in your current
campaign. Load it again later in one tap.

Saving a **map** is separate, and keeps token positions, fog of war and drawings.

Because the two are separate, you can save an encounter once and run it on a different map every
time.

## Common questions

### Can I add combatants after combat has started?

Yes. New combatants join at the bottom of the order until initiative is rolled again.

### My player characters are not in the list

**Load Party** only adds player characters attached to the **current campaign**. Check
**Settings → Current Campaign**, and check the characters are assigned to it.

### The difficulty rating is missing

It only appears with a 5E-compatible system loaded.

## Where to go next

- [Combat Settings](/settings/combat/) — every setting on this screen, row by row.
- [Battle Maps](/guides/battle-maps/) — running the same fight on a map.
- [The Player Screen](/guides/player-screen/) — showing the initiative order to your table.

[icon-more]: /assets/symbols/ellipsis.svg
