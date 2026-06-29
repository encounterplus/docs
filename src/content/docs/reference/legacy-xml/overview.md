---
title: Legacy XML
description: Reference for the legacy Encounter+ XML format used by previous versions.
sidebar:
  order: 0
---

These pages describe the legacy XML import/export format used by previous versions of Encounter+.

Legacy exports are ZIP archives that contain one root XML definition file, plus optional folders for images, tokens, fonts, styles, and other imported files. The archive extension identifies the package type, but the XML file in the archive root defines the content.

Use this reference when maintaining older exports, inspecting archived content, or migrating data into a newer Encounter+ format.

## Compendium

A `.compendium` archive contains a `compendium.xml` file in the archive root. It can include `monsters`, `players`, `items`, and `spells` folders with related images.

- [Compendium](/reference/legacy-xml/compendium/)

Elements:

- [Monster](/reference/legacy-xml/monster/)
- [Player](/reference/legacy-xml/player/)
- [Item](/reference/legacy-xml/item/)
- [Spell](/reference/legacy-xml/spell/)

Shared monster blocks:

- [Trait, Action, Reaction, Legendary](/reference/legacy-xml/custom/)

## Module and Campaign

A `.module` or `.campaign` archive contains a `module.xml` or `campaign.xml` file in the archive root. It can include folders with imported files, and an `assets` folder for HTML styles, JavaScript, fonts, and images.

- [Module](/reference/legacy-xml/module/)
- [Campaign](/reference/legacy-xml/campaign/)

Elements:

- [Page](/reference/legacy-xml/page/)
- [Encounter](/reference/legacy-xml/encounter/)
- [Map](/reference/legacy-xml/map/)
- [Group](/reference/legacy-xml/group/)

Encounter elements:

- [Combatant](/reference/legacy-xml/combatant/)

Map elements:

- [Asset](/reference/legacy-xml/asset/)
- [Component](/reference/legacy-xml/component/)
- [Light](/reference/legacy-xml/light/)
- [Marker](/reference/legacy-xml/marker/)
- [Tile](/reference/legacy-xml/tile/)

## Pack

A `.pack` archive contains a `pack.xml` file in the archive root. It can include folders with files that are copied during import.

- [Pack](/reference/legacy-xml/pack/)

Elements:

- [Asset](/reference/legacy-xml/asset/)
- [Group](/reference/legacy-xml/group/)
