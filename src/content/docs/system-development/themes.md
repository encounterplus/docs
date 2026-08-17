---
title: Themes
description: Styling a system — colors, text styles, stat block framing, tables and buttons, and how themes inherit from one another.
---

A **theme** is where a system's visual identity lives. Views name styles; themes define what those
names look like. Keeping the two apart is what lets a stat block be restyled — parchment to clean,
light to dark — without editing a single view.

Reference: [ThemeDefinition](/reference/schema/theme-definition/).

## Files and selection

- `themes/default.json` — the base theme, used everywhere unless something overrides it.
- `themes/<label>.json` — a theme applied to the entity type with that `label`. The D&D 5E system
  ships a `vehicle` theme so vehicles read differently from creatures.
- Any other `themes/<name>.json` — available by name, useful as a base for others to extend.

Theme lookup follows the same `extends` fallback as views: a type with no theme of its own uses
its parent type's, then the default.

If the system has no `themes/` folder at all, the app's built-in default theme is used.

## Global values

```json
{
  "tintColor": "#58180D",
  "primaryColor": "#9C2B1B",
  "secondaryColor": "#7A7A7A",
  "textColor": "#000000",
  "dividerColor": "#9C2B1B",
  "bgColor": "#ffffff",
  "bgImage": "/images/paper.jpg"
}
```

Colors are hex strings. Image paths beginning with `/` resolve against the system folder.

These are the fallbacks: any style that does not set its own color inherits from here, so a
palette change is usually a handful of lines at the top of the file.

## Text styles

`textStyles` is a map of style name to typography. A view referring to `"style": "title"` picks up
this entry:

```json
"textStyles": {
  "body": {
    "font": "NotoSans-Regular",
    "size": 14,
    "lineSpacing": 2,
    "paragraphSpacing": 6
  },
  "title": {
    "font": "MrEavesSmallCaps",
    "size": 34,
    "color": "#58180D",
    "traits": ["bold"]
  },
  "subtitle": {
    "font": "NotoSans-Italic",
    "size": 13,
    "traits": ["italic"]
  },
  "heading3": {
    "size": 18,
    "case": "uppercase",
    "divider": true
  }
}
```

Available keys: `font`, `size`, `alignment`, `color`, `tintColor`, `bgColor`, `padding`,
`divider`, `lineHeight`, `lineSpacing`, `lineLimit`, `strokeWidth`, `strokeColor`,
`paragraphSpacing`, `paragraphSpacingBefore`, `paragraphHeadIndent`, `traits`, `traitStyles`,
`case`, `caps`, `prefix`, `suffix`.

- `traits` — `bold`, `italic`, `condensed`, `expanded`, `tightLeading`, `looseleading`.
- `case` — `uppercase` or `lowercase`.
- `prefix` / `suffix` — text automatically wrapped around the value, so a label style can supply
  its own trailing colon.

Style names are yours to choose; the D&D 5E system uses `body`, `label`, `title`, `subtitle`,
`section`, `heading1`–`heading6`, `footer` for general text, and prefixed families like
`stats-*` for stat blocks and `sheet-*` for the character sheet. Adopting a similar convention
keeps a large theme navigable.

`font` names a font registered from the system's `fonts/` folder, or any font available on the
device.

## Stat block styles

`statBlockStyles` controls the framing drawn by a `statBlock` view — the part that makes a
creature look like it came out of a book:

```json
"statBlockStyles": {
  "default": {
    "bgImage": "/images/paper3.png",
    "topImage": "/images/top.png",
    "bottomImage": "/images/bottom.png",
    "barImage": "/images/bar.jpg"
  },
  "clean": {
    "bgColor": "#fffefd",
    "borderColor": "#888",
    "borderWidth": 1,
    "borderStyle": "double",
    "cornerRadius": 10,
    "shadowColor": "#00000033",
    "shadowOffsetX": 3,
    "shadowOffsetY": 3,
    "shadowRadius": 3
  }
}
```

`topImage`, `bottomImage` and `barImage` are the decorative rules; `borderStyle` is `single` or
`double`. `padding`, `body` (a text style for the block's default text) and `section` are also
available.

Providing both a decorative `default` and a plain `clean` variant, as above, is a good pattern —
the same views serve both looks.

## Tables

```json
"tableStyles": {
  "default": { "rowColor": "#9C2B1B33" },
  "class":   { "rowStyle": "odd", "rowColor": "#84A5D633" },
  "clean":   { "rowLineWidth": 0.5 }
}
```

`rowStyle` is `even`, `odd`, `underline` or `clean`. `head` and `body` take text styles for the
header row and the body rows; `rowColor`, `rowLineColor` and `rowLineWidth` handle the banding and
rules.

## Other styles

| Map | Controls | Keys |
| --- | --- | --- |
| `buttonStyles` | buttons | `color`, `bgColor`, `borderColor`, `borderWidth`, `cornerRadius`, `padding`, `body` |
| `checkboxStyles` | checkboxes | `tintColor`, `primaryColor`, `icon` (an SF Symbol), `size` |
| `fieldStyles` | labelled value fields | `bgColor`, `borderColor`, `borderWidth`, `cornerRadius`, `spacing`, `alignment`, `padding`, `layout` (`top`/`bottom`/`leading`/`trailing`), `titleWidth`, `title`, `body` |
| `dividerStyles` | dividers | `shape`, `color` |
| `blockQuoteStyles` | block quotes in rendered Markdown | `bgColor`, `borderColor`, `borderWidth`, `borderStyle` (`horizontal`/`vertical`/`left`/`arrows`), `padding`, `body` |

Each map's `default` entry is used when a view names no style.

## Inheritance

`extends` builds a theme on top of another by name:

```json
{
  "extends": "default",
  "bgColor": "#1a1a1a",
  "textColor": "#eeeeee",
  "statBlockStyles": {
    "default": { "bgImage": null, "bgColor": "#222" }
  }
}
```

Anything not set falls back to the parent, and unknown parents fall back to the system default.
Inheritance is resolved after every theme file is loaded, so declaration order does not matter.

## Fonts

Fonts in `fonts/` are registered when the system loads and are then usable by name in `font`. Use
the font's full PostScript name, which is what the app registers them under.

## Debugging

`"debug": true` at the top of a theme turns on visual indicators for how styles are being applied.

## Where to go next

- [Views](/system-development/views/) — where `style` is consumed.
- [ThemeDefinition reference](/reference/schema/theme-definition/) — every key and enum value.
