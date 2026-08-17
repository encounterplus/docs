---
title: Development
description: Developer documentation for Encounter+ — building game systems, and the open repositories behind the app and its content.
---

Most of Encounter+ is extensible without touching the app. Game systems, content packages and the
browser client are all separate, versioned artifacts, and much of it is developed in the open.

This section is for people building on top of the app rather than using it.

:::note
Everything here is developer material. If you are looking for how to *use* a feature, start with
the [Guides](/guides/quick-start/).
:::

## What's here

- **[Custom System](/system-development/)** — the guide to authoring a game system.
- **[Schema reference](/reference/schema/)** — the generated reference for every JSON format the
  app reads and writes, from import archives to definition files.
- **[URL scheme](/reference/url-scheme/)** — driving the app from links.

## Repositories

### App and site

| Project | What it is | Repository |
| --- | --- | --- |
| Documentation | This site — Astro + Starlight, contributions welcome | [encounterplus/docs](https://github.com/encounterplus/docs) |
| Wiki | Legacy notes and community documentation | [encounterplus/encounterplus](https://github.com/encounterplus/encounterplus/wiki) |
| Web client | The browser player client served over Remote Play | [encounterplus/web-client](https://github.com/encounterplus/web-client) |
| Package registry | The catalog the Package Manager reads | [encounterplus/packages](https://github.com/encounterplus/packages) |

### Game systems

Each system is its own repository, released as a `.system` archive with a package manifest. See
[Packaging](/system-development/packaging/) for how a release is put together.

| System | Ruleset | Repository |
| --- | --- | --- |
| D&D 5E | Dungeons & Dragons 5th Edition — ships bundled with the app | [encounterplus/dnd5e](https://github.com/encounterplus/dnd5e) |
| Pathfinder 2E | Pathfinder Second Edition | [encounterplus/pf2e](https://github.com/encounterplus/pf2e) |
| Shadowdark | Shadowdark RPG | [encounterplus/shadowdark](https://github.com/encounterplus/shadowdark) |
| Daggerheart | Daggerheart | [encounterplus/daggerheart](https://github.com/encounterplus/daggerheart) |

### Content and tools

| Project | What it is | Repository |
| --- | --- | --- |
| Module Packer | Builds `.module` archives from Markdown sources | [encounterplus/module-packer](https://github.com/encounterplus/module-packer) |
| Example module | A minimal module showing the package format | [encounterplus/example-module](https://github.com/encounterplus/example-module) |

## Contributing

Systems and content packages are the easiest place to start — they need no app build, only a text
editor and a device to reload on. Corrections to this site are welcome in the docs repository.

If you have published a system or a tool that belongs on this page, get in touch and it can be
listed here and in the package registry.
