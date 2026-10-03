---
title: Tips & Tricks
description: Faster ways to do common things at the table — dragging combatants onto the map, turning spells into status effects, and running combat from the keyboard.
---

Useful tips and tricks to speed up your prep and your game sessions. None of them replace the
regular way of doing things — buttons, forms and menus still work as described in the other guides.
These are extra shortcuts that get the same thing done in fewer steps.

## Context menus almost everywhere

**Long press** on iPhone and iPad, or **right click** on Mac, on almost anything you can see. A menu
of the actions for that thing appears where you are already looking, instead of in a toolbar or a
detail screen.

Try it on:

- **Combatants** in the initiative list — damage and healing, conditions, initiative, tokens.
- **Tokens** on the battle map — the same combatant actions, plus map-side ones.
- **Library entries** — open, edit, duplicate, bookmark, add to a campaign or module, export, delete.
- **Rows inside forms** — reordering and removing list items.
- **Maps, pages, encounters, campaigns and modules** in their lists.

Nothing is *only* in a context menu, but it is usually the shortest route.

## Combat and tokens

### Drag a combatant onto the map

Drag a creature from the initiative list and drop it on the map to give it a token there. This is
handy when [Load Mode](/settings/combat/#load-mode) is set to combat only, or when a creature joins
the fight before you have decided where it stands.

While combat is running, dragging a combatant *within* the list moves it in the turn order instead.

See [Tokens](/guides/battle-maps/tokens/#placing-tokens).

### Add a status effect from a spell or condition

Select a token on the map, then load an entity that has a duration — a spell like *Bless*, for
example. Instead of adding the entity to combat, the app creates a status effect on the selected
token, with its name and duration filled in from the entity.

If the entity has no duration, the app says it cannot make a status effect from it. Deselect the
token first if you meant to load the entity normally.

### Place an area effect by loading it

With no token selected, loading an entity that has an area shape — *Fireball*, *Cone of Cold* —
places that area effect on the map instead of adding a combatant.

See [Drawing, Markers & Effects](/guides/battle-maps/drawing-and-effects/).

### Give new tokens and effects artwork automatically

Add a module of artwork under **Campaign Settings →
[Random Assets](/guides/campaigns-and-modules/#random-assets)**, and the app picks artwork from it
when it creates:

- **Tokens** created by loading a creature or an encounter, or from a combatant's menu.
- **Area effects** placed by loading a spell like *Fireball*.
- **Auras** added with a status effect.

An asset matches when its name or one of its tags equals the creature's or effect's name, ignoring
case. When several match, one is picked at random — tag five goblin images `goblin` and a pack of
goblins no longer all look alike.

A matching asset takes precedence over the creature's own token image. When nothing matches, the
token keeps the image from its entity as usual.

### Pick a condition straight from the combatant menu

Touch and hold a combatant in the initiative list and open **Status Effects**. Besides **New**, the
menu lists the conditions (and any other entities your game system offers there). Picking one opens
the status effect form already filled in from it, so you only confirm.

The same [context menu](#context-menus-almost-everywhere) rolls initiative, makes the creature
active, applies damage, and creates or deletes its token.

See [Encounters & Combat](/guides/encounters/).

## Library and content

### Drag an entity from the library onto the map

Drag a creature or any other entity from the library and drop it on the battle map. The app creates
a token there, linked to that entity.

See [Tokens](/guides/battle-maps/tokens/#placing-tokens).

### Drop images from other apps onto the map

Drag an image from Files, Photos, Safari or any other app straight onto the battle map. The app
adds it as an asset and places it, based on the [layer](/guides/battle-maps/#layers) you have
selected:

- On the **Token** layer, it becomes a token using that image.
- On any other layer, it becomes a tile on that layer.

### Drop images into a module or campaign

Drag images from Files, Photos or another app onto a module or campaign's content list. Each one is
added as an asset, ready to use as a token image or map tile.

See [Assets](/guides/battle-maps/assets/).

### Long press a dice roll in a stat block

Tapping a dice expression in a stat block or entity view rolls it. Long press it instead for more
options:

- **Roll Dice** — the same as a tap.
- **Advantage** and **Disadvantage** for checks, or **Critical Damage** for damage rolls (D&D 5E
  compatible systems).
- **Customize** — opens the roll in the advanced dice roller so you can change it first.

See [Dice & Roll Tables](/guides/dice/).

### Tap an entity's title to search the web

In most game systems, tapping the title at the top of an entity's view starts a web search for its
name.

### Reorder and nest content by dragging

In a module or campaign, drag items to reorder them. Drop an item onto a group to move it inside.

## Keyboard

With a hardware keyboard — an iPad keyboard or a Mac — the game screen responds to these keys:

| Keys | Action |
| --- | --- |
| <kbd>⌘</kbd> <kbd>Return</kbd> | Start or stop the encounter |
| <kbd>⌘</kbd> <kbd>↓</kbd> or <kbd>⌘</kbd> <kbd>→</kbd> | Next turn |
| <kbd>⌘</kbd> <kbd>↑</kbd> or <kbd>⌘</kbd> <kbd>←</kbd> | Previous turn |
| <kbd>↑</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> | Move the selected token one grid square (one token at a time) |
| <kbd>Esc</kbd> | Close the open panel, or clear the map selection |

Hold <kbd>⌘</kbd> on iPad to see the list in the app.

The number pads accept typing too:

| Pad | Keys |
| --- | --- |
| **Damage / healing** | Digits enter the amount. <kbd>Space</kbd> switches between damage and healing. <kbd>Delete</kbd> removes a digit. <kbd>Return</kbd> applies, <kbd>Esc</kbd> cancels. |
| **Initiative** | Digits enter the value. <kbd>Space</kbd> flips the sign. <kbd>Delete</kbd> removes a digit. <kbd>Return</kbd> or <kbd>Esc</kbd> closes. |
| **Dice roller** | Digits, <kbd>d</kbd>, <kbd>+</kbd>, <kbd>-</kbd>, <kbd>x</kbd>, <kbd>/</kbd> build an expression. <kbd>Delete</kbd> removes the last part. <kbd>Return</kbd> rolls. |
