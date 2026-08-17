---
title: Migrations
description: Versioning a system and rewriting existing user content when the shape of its data changes.
---

A system's `data` shape is an API to content authored against it. When you change that shape, the
content that already exists still has the old one — and it belongs to users, not to you.

**Migrations** are how it catches up: small JavaScript files, named after the system version that
introduces the change, that rewrite each affected entity.

## Versioning

`system.json` carries the system's `version`, and every entity records the `systemVersion` it was
last written against. That pair is all the app needs to know what is out of date.

Bump `version` in `system.json` in the same change that reshapes the data — a migration named
after a version the system never claims will never run.

## Writing one

`migrations/<version>.js` exports a single `migrate` function:

```js
function migrate(entity, migration) {
  // change character race to species
  if (entity.kind === "Character") {
    var data = entity.data
    const race = data.race
    if (race && !data.species) {
      data.species = race
      delete data.race
    }

    entity.data = data
    return entity
  }

  // return null to indicate no changes were made
  return null
}
```

- **`entity`** is the entity as plain JSON — `kind`, `name`, `slug`, `type`, `data` and the rest.
- **`migration`** carries context: `migration.version` is the version being applied, and
  `migration.app` holds the running app's `version` and `build`.
- **Return the entity** to save the changes, or **return `null`** to say nothing changed. Returning
  nothing at all is an error.
- `console.log`, `console.debug` and `console.error` are available and their output is collected
  into the migration report shown to the user.

Only a defined set of fields is written back: `data`, `name`, `slug`, `type`, and `kind` — the last
only if the new value names a type the system actually defines. Everything else on the entity is
left alone, so a migration cannot damage images, tags, sources or combat state.

## How it runs

The user starts it from the system's screen when the app notices a version gap. Then:

1. Migration files are sorted by version and applied in ascending order.
2. For each version, entities whose `systemVersion` is **older** than that version are processed;
   entities already at or past it are skipped.
3. Before each version runs, the system's content is **backed up** to
   `backup/migration-<version>-<timestamp>/` inside the system folder.
4. Each migrated entity's `systemVersion` is set to the version just applied.

Because versions are applied in sequence, each migration only has to handle the step it owns.
A user upgrading across three versions gets all three, in order.

If a script throws, or returns something that cannot be decoded, the migration stops with an error
naming the entity that failed — and the backup taken at the start of that version is still there.

## Guidelines

**Make it idempotent.** The example above checks `race && !data.species` before moving anything, so
running it twice does nothing the second time. Version tracking should prevent a second run, but
idempotence costs one condition and removes a whole class of failure.

**Filter by `kind` first.** Every entity in the system passes through the function, spells and
maps included. Return `null` early for anything you do not handle.

**Never delete without moving.** Copy to the new location, verify, then delete the old key — and
only when the copy succeeded.

**Test on real content.** Install the system on a device with a substantial library, run the
migration, and check both the migrated entities and the ones that should have been left alone.

**Keep old migrations forever.** A user who has not opened the app in a year needs the whole chain.
Deleting an old migration file strands them.

**One version, one concern.** A migration file that does three unrelated things is a migration file
that fails halfway through.

## When a migration is not the answer

If the change is additive — a new optional field, a new entity type, a new view — nothing needs
migrating. Views and forms read missing values as empty, and a `{% if %}` or a `default:` filter
handles the gap. Reserve migrations for renames, restructures and deletions.

## Where to go next

- [Entity Definitions](/system-development/entities/#data--where-your-ruleset-lives) — designing a
  `data` shape you will migrate less often.
- [Packaging](/system-development/packaging/) — shipping the version bump.
