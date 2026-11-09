---
title: Character Sheets
description: Interactive sheets for system authors — static web apps that follow an entity and change it, in the app and in a browser, through the sheet SDK.
---

:::caution[Preview]
Sheets are a preview, meant for system authors for now. The sheet protocol, the SDK, `sheet.json`
and [model schemas](/system-development/schemas/) are not a stable public interface yet: they can
change between releases without a deprecation period, so expect to adjust your sheet when the app
updates. The protocol and the SDK already carry a version; see [Compatibility](#compatibility).
:::

A **sheet** is a small web app that shows one entity and lets the user change it. It lives in your
system's `sheets/<id>/` folder, and opens at the same address in the app and in a browser:
`/sheets/<id>/?id=<entity-id>`.

A sheet is plain files, so any tool that produces HTML and JavaScript works. The app gives it two
things:

- **The entity, live.** The sheet gets the entity as the app stores it, plus everything your
  [transforms](/system-development/views/#computed-attributes) compute, and an update whenever
  anyone changes it: a form, the combat bar, another browser.
- **Checked writes.** The sheet sends changes as small operations, and the app checks each one
  against the entity type's [model schema](/system-development/schemas/). Your sheet can't store
  something the schema doesn't allow.

The **sheet SDK**, `ep.js`, is the easy way to use both. It is optional: everything it does goes
through the [WebSocket protocol](/reference/server-api/#entity-subscriptions), which a sheet can
speak without it.

Before you start, give the entity type a [model schema](/system-development/schemas/). A sheet
without one can read the entity, but every write is refused.

## Sheet or template?

A [view template](/system-development/views/#the-html-renderer) is rendered by the app, once, with
everything it needs. A sheet is drawn in the page, and changes as the entity changes.

| Use | When |
| --- | --- |
| A template | The view mostly displays. It can still bind a few live values, see [Templates](#in-a-template) |
| A sheet | The view is mostly inputs, tabs and rules, and should feel like an app |

The two work well together. An entity type can open as a small GM card with a button to its sheet,
which is how the Dragonbane system does it.

## A first sheet

This sheet needs no build step: one file, in `sheets/default/`.

```html title="sheets/default/index.html"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Character</title>
  <link href="/systems/my-system/styles/default.css" rel="stylesheet">
</head>
<body>
  <main id="sheet" hidden>
    <h1 data-text="name"></h1>
    <label>Hit points <input type="number" min="0" data-bind="data.hp.current"></label>
    <progress data-bar="data.hp.current" data-max="view.data.hp.maximum"></progress>
    <p><a href="/roll/1d20/Awareness">Roll Awareness</a></p>
  </main>
  <p id="message" hidden></p>

  <script src="/_app/js/ep.js"></script>
  <script src="/_app/js/ep-ui.js"></script>
  <script>
    const character = EP.entity

    function explain(text) {
      const message = document.getElementById('message')
      message.textContent = text
      message.hidden = false
    }

    if (character) {
      character.addEventListener('error', (event) => {
        explain(`Not saved: ${event.detail.errors.map((error) => error.message).join('; ')}`)
      })
      character.connect().then(
        () => {
          EP.bind(document, character)
          document.getElementById('sheet').hidden = false
        },
        (error) => explain(error.message)
      )
    } else {
      explain('The address needs ?id=<entity-id>.')
    }
  </script>
</body>
</html>
```

Then tell the entity type to open it, in `config.json`:

```json
{
  "entities": {
    "Character": {
      "view": { "renderer": "sheet" }
    }
  }
}
```

Reload the system and open a character. The input writes `data.hp.current`, the bar follows it, and
the link rolls in the app's dice roller, or in the shared log in a browser. Change the value in the
character's form and the sheet follows.

## Connecting a sheet to an entity type

Two keys in an entity type's [configuration](/system-development/config/#per-entity-configuration)
decide what a type opens as:

| `view` | Opens as |
| --- | --- |
| `{ "renderer": "sheet" }` | The sheet in `sheets/default/` |
| `{ "renderer": "sheet", "sheet": "hero" }` | The sheet in `sheets/hero/` |
| `{ "renderer": "html", "sheet": "hero" }` | Its template, which links to the sheet through `env.sheetURL` |

A template's link is an ordinary one, and the app opens it over the card:

```html
{% if env.sheetURL %}<a href="{{ env.sheetURL }}">Open sheet</a>{% endif %}
```

Users can change this per entity type under **System Settings → Sheets**, which lists the sheets
that can show the type. In a browser, every sheet opens at its own address, and an entity's
reference (`/hero/brin`) redirects to its sheet when its type opens as one.

### `sheet.json`

A file beside the sheet, with optional keys. A sheet with none of these needs no file at all.

```json
{
  "root": "dist",
  "api": 1,
  "entities": ["Hero"]
}
```

| Key | Default | Meaning |
| --- | --- | --- |
| `root` | the sheet's folder | The folder the sheet's address serves. Nothing outside it is reached through `/sheets/<id>/`, but your system's folder is served too, at `/systems/<id>/`, so keep nothing secret in it |
| `api` | `1` | The protocol version the sheet was written for |
| `entities` | any | The entity kinds it can show, as definitions name them. System Settings lists the sheet only for these |

A sheet is **unavailable** when its `api` is one this app doesn't speak, when `root` isn't a folder
inside the sheet, or when a value has the wrong type. It serves nothing, and the reason is in the
app's log.

:::tip
A sheet with a build step should always name its `root`. Without it, the app serves the whole
folder, sources included.
:::

## The store

`EP.entity` is the entity the sheet shows, as a **store**, or `null` when the address names none.
A sheet shows and changes this one entity. It changes the entity itself, never a combatant: a
[standalone](/system-development/entities/#behavior-flags) type such as a character keeps the two
in step, but for other types each combatant keeps state of its own, which a sheet doesn't change.

`connect()` resolves once the store has the entity, so start your sheet there. In the app that is
at once, because the app hands the sheet its first state before the page loads, and the sheet draws
in its first frame. In a browser it waits for the app to answer. It rejects when the entity doesn't
exist or the app can't be reached.

```js
const hero = await EP.entity.connect()

hero.subscribe(({ model, view, pending, status }) => {
  // called at once, and after every change
})
```

Each change gives you a new, frozen **snapshot**:

| Field | Holds |
| --- | --- |
| `model` | The entity as stored, with your waiting changes applied. This is what you write to |
| `view` | The model with your transforms' computed values laid over it. This is what you display |
| `pending` | How many of your writes the app hasn't confirmed yet |
| `status` | `connecting`, `connected` or `disconnected` |

The rule of thumb: **inputs bind to the model, displays read the view.** A hero's stored hit points
are `data.hp.current`, and a computed maximum is `view.data.hp.maximum`.

`subscribe` is the standard store contract, so frameworks use the store directly:

```js
// Svelte: $hero in a component, nothing else needed

// React
const snapshot = useSyncExternalStore(hero.subscribe, () => hero.snapshot)
```

### Reading values

`get` reads a value by path, from the model, or from the view with a `view.` prefix:

```js
hero.get('name')
hero.get('data.hp.current')
hero.get('view.data.damageBonus')
hero.get('data.weapons[0].name')    // a list item by position
hero.get('data.items[k3x9].weight') // by id, in a list with ids
```

Read the entity's id from the store, `hero.id`.

`hero.env` is the view's environment: `dataURL`, `systemURL`, `theme` and `styles`. Image paths in
content are relative, so `hero.resolvePath(hero.get('image'))` gives the address the page can load.
`hero.client` says where the sheet runs, `app` or `browser`, for the few things that differ between
them; see [In the app and in a browser](#in-the-app-and-in-a-browser).

### What the model holds

`model` is the entity as the app stores it, nothing computed and nothing left out: the app's own
fields (`name`, `image`, `tags`, `notes`…) beside your system's `data`. Every stored key is there to
read, whether or not your schema declares it; the schema decides only what a sheet can write. A
link to another object is its id: `combatantId` is the entity's combatant, and having one doesn't
mean the entity is in combat.

What is computed is in `view` only: your transforms' values, and a few the app adds — `reference`
(the entity's address, `/hero/brin`), `location` (its module or campaign), and the display strings
`source`, `sourceFormatted`, `locationFormatted` and `footer`.

## Writing

Only `data.…` paths can be written, and of those only what the
[model schema](/system-development/schemas/) declares. A key the schema doesn't declare can still be
read, but a write to it is refused, even though the entity's form saves it. Each write returns a
promise that resolves when the app has applied it, and rejects when it fails.

```js
await hero.set('data.hp.current', 7)
await hero.remove('data.conditions.dazed')
await hero.insert('data.notes', { text: 'Owes the guild' })
await hero.move('data.weapons[2]', 0)

// several changes at once, applied whole or not at all
await hero.update((data) => {
  data.hp.current = data.hp.maximum
  data.rest.round = false
})
```

`update` gives you a copy of `data` to change, and sends what you changed. A batch is applied whole
or not at all, so use it whenever two values must change together.

**Any write can be refused** — by the schema today, and by permissions once the app has them — so a
sheet handles refusals once. The sheet shows a write at once, before the app answers. If the app
refuses it, the value goes back and the store reports why. Listening once, at the top of your
sheet, covers every write:

```js
hero.addEventListener('error', (event) => {
  showMessage(event.detail.errors.map((error) => error.message).join('; '))
})
```

Each error has a `message`, a `code`, and the failing op's `index` and `path`; the codes are listed
under [Entity subscriptions](/reference/server-api/#entity-subscriptions). The store also dispatches
`deleted` when the entity is deleted.

### Without a connection

Nothing waits for a connection. A write made while the sheet has none is refused at once, with the
code `disconnected`, and never shows; nothing is sent later. `EP.field` and `EP.bind` disable their
inputs from the moment the connection goes until the entity's state arrives again. Disable your own
controls while `status` is `disconnected`; a write in the moment between reconnecting and the state
arriving is refused as well.

A write that was on its way when the connection went, or that the app didn't answer within ten
seconds, fails with `disconnected` or `timeout`. Its value goes back, but the app may have applied
it, and the next state shows what happened. The SDK never sends a write again, so a sheet that
retries one decides for itself that doing it twice is safe.

In the app the connection is the web view itself, so this happens only in a browser.

In a browser the SDK reconnects by itself while a store follows its entity. It tries again half a
second to a second after the connection goes, and waits twice as long after each attempt that
fails, up to 30 seconds. When the browser comes back online, or the page is shown again, it tries
at once. A connection can look open when it is gone, after a phone wakes up or the network changes,
so a page shown again after 10 seconds or more asks the app for its entity once more. Without an
answer within five seconds the SDK closes the connection and reconnects. Each time it reconnects,
the store subscribes again and the entity's state arrives in full.

### Inputs

`EP.field` binds one input, select or text area to a model path. It returns what a Svelte action
returns, so it works directly with `use:`:

```svelte
<input type="number" use:EP.field={{ store: hero, path: 'data.hp.current' }}>
```

Elsewhere, call it yourself and call `destroy()` when the element goes:

```js
const field = EP.field(element, { store: hero, path: 'data.hp.current' })
```

The field shows the value and writes on `change`:

| Input | Writes |
| --- | --- |
| Checkbox | `true` or `false` |
| Radio | Its `value`, when picked |
| Number, range | A number |
| Anything else | Its text |
| Emptied | Removes the key |

An input someone is typing in is left alone until it loses focus, and a refused write puts the
stored value back. While there is no connection the input is disabled.

### In a template

`EP.bind` connects the markup a [template](/system-development/views/#the-html-renderer) already rendered,
which suits a card with a few live values. Load `ep.js` in the template, and mark up what is live:

```html
<h2 data-text="name">{{ name }}</h2>
<input type="number" data-bind="data.hp.current" value="{{ data.hp.current }}">
<span data-text="data.kin" data-label="Kin"></span>

<script src="/_app/js/ep.js"></script>
<script>
  EP.configure({ labels: false })
  EP.bind(document, EP.entity, { refresh: 'main' })
</script>
```

| Attribute | Does |
| --- | --- |
| `data-bind="data.…"` | An input, as `EP.field` binds one |
| `data-text="path"` | Shows the value as text; with `data-label="Enum"`, its label |
| `data-count="data.…"` | Draws a count across the checkboxes inside. `data-max="path"` disables those past the maximum |
| `data-bar="path"` | With `data-max="path"`: sets `value` and `max` of a `<progress>` or `<meter>`, else the `--value`, `--max` and `--ratio` CSS variables |

Values the template rendered stay until the first state arrives. With `refresh`, a change made
elsewhere that no bound element shows, such as a weapon added on the sheet, renders that part of the
page again from the server. The view's own writes never do.

Templates get no starting state, since they are rendered with the entity.

## The library, dice and text

### Picking from the library

`EP.pick` lets the user choose a library entry. `embed` adds a copy of it to the entity, with the
listed keys of its data; the app makes the copy and checks it like any write.

```js
const axe = await EP.pick({ entity: 'Item' })   // null when cancelled
if (axe) {
  await hero.embed('data.weapons', axe, ['skill', 'damage'])
}

const several = await EP.pick({ entity: 'Item', multiple: true })
```

`entity` is the kind as your definitions name it, and includes the kinds extending it. In the app,
`EP.pick` shows the app's library list. In a browser it needs `ep-ui.js` or your own picker; see
[Optional scripts](#optional-scripts).

### Listing the library

A sheet that draws its own picker — a dialog, a dropdown, the spells a class can learn — lists
entries with `EP.query`. It resolves with one page of entries and how many match in all:

```js
const { entries, total } = await EP.query({
  entity: 'Item',
  search: 'a',                                                  // part of the name
  where: { type: 'weapon', 'data.skill': ['axes', 'swords'] },  // equal to a value, or one of a list
  sort: '-data.weight',                                         // a path; - for descending
  keys: ['data.skill', 'data.weight'],                          // data each entry carries
  limit: 20,                                                    // 50 by default, at most 200
  offset: 0
})
for (const entry of entries) {
  console.log(entry.name, entry.data?.skill, entry.image)
}
```

Each entry is `{ id, name, kind, type?, reference, source?, detail?, image?, icon?, tags?, data?,
view? }`, the same as `EP.pick` gives, so `embed` takes it as it is. `image` is an address the page
can use as it is, in the app and in a browser; `data` holds the `keys` you asked for, at their
paths. `ids` lists only the entries you name, for showing what the sheet already holds.

`keys` can also ask for values the app computes, with a `view.` prefix: `view.data.evasion` is
evasion with its modifiers applied. They arrive in the entry's `view`, apart from the stored values
in `data`, so you can tell which is which; `embed` copies stored values only. Computed values are
worked out for the page answered, so `where` and `sort` read stored values only.

`keys: 'list'` asks for the paths your system's `filters.json` filters, groups and sorts that kind
by — the columns the app's own library list works with. It suits a picker that should show useful
values without naming them, such as one shared across systems; it can sit among paths too,
`keys: ['list', 'data.price']`.

Every entry also carries `detail`, the line under its name in the app's own library list — your
`config.json`'s `entities.<Kind>.collection.detail`, rendered — so a picker's second line matches the
app's without asking for it.

`where` reads `name`, `type`, `kind`, `source`, `tags` and anything under `data.`, and an entry is
kept when every path holds the value given, or one of the list given; a list the entry holds, like
`tags`, matches when any of its items does. For anything else, give a path operators, which must
all hold:

```js
where: {
  'data.level': { gte: 1, lte: 3 },        // numbers: lt, lte, gt, gte
  'data.school': { nin: ['necromancy'] },  // not equal: ne for one value, nin for a list
  'data.ritual': { exists: true }          // has a value, or has none with false
}
```

`null`, `''` and `[]` count as no value, which never equals anything, so `ne` and `nin` keep
entries without one; add `exists: true` when they shouldn't. It is plain data, not an expression,
and a query the app can't read rejects with an `EP.Error` saying why. The details are under
[Where operators](/reference/server-api/#where-operators).

### Rolling dice

A link to `/roll/<dice>/<name>` rolls, and is the simplest way:

```html
<a href="/roll/1d20/Awareness">Roll Awareness</a>
<a href="/roll/2d6%2B3/Longsword/damage">Damage</a>
```

Encode the formula, since `+` and spaces must survive the address. Text the app rendered from
Markdown already has such links. The optional last part is the roll's type: `attack`, `damage`,
`heal`, `check` or `save`. Long-pressing a link in the app opens the roller's menu.

When the sheet needs the result, call `EP.roll`:

```js
const roll = await EP.roll('1d12+1d12+2', { label: 'Action', type: 'check' })
if (roll) {
  const [hope, fear] = roll.dice.map((group) => group.result)
  console.log(roll.result, hope, fear)   // 17, 9, 6
}
```

It rejects when the formula can't be rolled, and the roll reaches the shared log unless it is
private. In the app, the dice roller shows the roll and `roll` is the first result to finish;
rolling again in the same roller is the user's own. It is `null` when the user closed the roller
first, or something else was already showing. So a sheet always needs a way forward without a
result. In a browser the app rolls without showing anything on its screen, and the result goes to
`onRoll` (`ep-ui.js` shows it in a banner).

`mode: 'private'` (or `'public'`) overrides the app's roll mode in the app; a browser's rolls are
always public for now. In the app the roll is for the entity the view shows, as its combatant is
named when it has one.

#### Your own dice

A sheet with its own dice — 3D dice in the page — throws them itself and lets the app do the
rest. Pass a `roller`, and `EP.roll` calls it before asking the app:

```js
EP.configure({
  roller: async ({ formula, label, type }) => {
    const faces = await myDice.throw(formula)   // [[4, 17], [3]] for 2d20kh1 + 1d6
    return faces                                // or null when the user cancels
  }
})
const roll = await EP.roll('2d20kh1 + 1d6', { label: 'Longsword', type: 'attack' })
// roll.result is 20, roll.clientThrown is true
```

The roller gives one list of faces per dice term, in the formula's order, each holding every die
thrown for that term in the order thrown — including the extra dice of an explosion (`!`) or a
reroll (`r`), which the app takes from the end of the term's list. The app checks the faces,
computes the result with the formula's modifiers, logs it marked as the client's dice, and
`EP.roll` resolves with it, `clientThrown: true`. Faces that don't fit the formula reject. A roller
that returns `null` resolves `EP.roll` with `null` and sends nothing. This works the same in the app
and in a browser.

`dice` has one group per dice term, in the formula's order, so `1d12+1d12` keeps the two dice apart
where `2d12` would add them up. Each group is `{ formula, faces, result, rolls }`, and `rolls` holds
every die thrown as `{ value }`, with `dropped: true` on one that doesn't count: the lower die of
`2d20kh1`, a reroll, a failure. `detail` is the roll as text, for showing; don't read values out of
it.

### Text

The system's strings and enum labels come with the first state:

```js
EP.t('Common.HitPoints')    // from lang/, in the system's language
EP.label('Kin', 'elf')      // an enum key's label
```

A view that uses neither saves the transfer with `EP.configure({ labels: false })`, before it
connects.

### Asking first

`EP.confirm` asks the user before a change they can't take back, such as removing a list entry. It
resolves `true` when they take the action.

```js
if (await EP.confirm(`Remove ${item.name}?`, { action: 'Remove', destructive: true })) {
  await hero.remove(`data.items[${item.id}]`)
}
```

`action` names the button that takes it (`OK` by default), and `destructive` marks an action that
removes something. `EP.confirm` shows `ep-ui.js`'s dialog, or your own `confirmer`, the same in the
app and in a browser. Without either it falls back to the page's `confirm`, which the app shows as
its own alert, with Cancel and OK, and a browser in its own style.

### Opening things

`EP.open('/item/broadsword')` opens a reference the way a link to it would: the app shows its card
over the sheet, a browser goes to it. A plain `<a href="/item/broadsword">` does the same, so a
link is usually enough; in a browser it leaves the sheet, so give it `target="_blank"` to keep the
sheet open.

## Optional scripts

`ep.js` loads nothing else by itself. Add what your sheet needs as script tags, after it:

| Script | Adds |
| --- | --- |
| `/_app/js/ep-ui.js` | The dialog for `EP.confirm`, in the app and in a browser; and for browsers, the search dialog for `EP.pick` (over `EP.query`, each entry with its `detail` line) and a banner with each `EP.roll` result, where the app's own UI is used in the app. All in one style; see [Colours](#colours) below |
| `/_app/js/ep-schema.js` | The app's write checks in the page. See below |

To use your own look instead of `ep-ui.js`, pass your own functions:

```js
EP.configure({
  picker: async ({ entity, multiple }) => openMyDialog(entity, multiple),  // a list of entries, empty when cancelled
  confirmer: async ({ message, action, destructive }) => askMyWay(message, action),  // true to take the action
  onRoll: ({ name, formula, result, detail }) => showMyBanner(name, result),  // in a browser
  roller: async ({ formula }) => myDice.throw(formula)  // your own dice; see Rolling dice
})
```

### Colours

`ep-ui.js` draws in the system colours, which follow the viewer's light or dark appearance, rather
than in your page's: a page's colour variables can disagree with each other (text pinned light while
the background follows a dark scheme), and pairing them can put dark text on a dark card. Set any of
these on the page to use your own:

| Variable | For | Default |
| --- | --- | --- |
| `--ep-ui-background` | The dialogs' and the banner's background | `Canvas` |
| `--ep-ui-color` | Their text | `CanvasText` |
| `--ep-ui-accent` | Focus rings and a dialog's main button | `AccentColor` |
| `--ep-ui-danger` | The button of a destructive action | The system's red, light or dark |

Buttons on the accent and danger colours have white text, so choose colours dark enough for it.
Set just one or two to keep the rest following the viewer's appearance:

```css
:root {
  --ep-ui-danger: #8F332E;
}
```

**`ep-schema.js` is rarely needed.** The app checks every write anyway. With it, a write the app
would refuse never shows, and `set` converts values the way the app will (`"7"` to `7`) at once.
Without it, a refused write shows briefly and goes back, and a value is converted when the state
arrives. It costs a request for the schema on every open and about 13 KB of script, so leave it out
unless the flash of a refused value matters to your sheet.

## Styling

A sheet links its own stylesheets. Your system's are at `/systems/<id>/styles/`, and anything in
your system can be reached the same way.

The SDK gives a sheet what a template writes itself, from the first state:

- `data-entity-id`, `data-kind`, `data-type` and `data-view-theme` on `<html>`, so a stylesheet
  shared with your templates works the same: `:root[data-view-theme="night"] { … }`.
- Links to the container's `styles/custom.css`, from `env.styles`.

The app ships no theme files, so a [view theme](/system-development/config/#view-themes) with its
own stylesheet links it from the sheet, using `store.env.theme`. A container's `scripts/custom.js`
does not run in sheets.

## Building a sheet with Svelte

Any framework works; the sheet only has to end up as static files. This is a complete Svelte
project, built the same way as the Dragonbane and Daggerheart sheets. It lives in
`sheets/character/`, as its own Node project.

The app serves the build, `dist/`, so `dist/` belongs in your system and `node_modules/` doesn't.
Import drops `node_modules` anyway.

```json title="sheets/character/sheet.json"
{
  "root": "dist",
  "api": 1,
  "entities": ["Character"]
}
```

```json title="sheets/character/package.json"
{
  "name": "my-system-character-sheet",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "check": "svelte-check --tsconfig ./tsconfig.json"
  },
  "devDependencies": {
    "@sveltejs/vite-plugin-svelte": "^7.3.1",
    "@tsconfig/svelte": "^5.0.8",
    "svelte": "^5.57.2",
    "svelte-check": "^4.7.7",
    "typescript": "^6.0.3",
    "vite": "^8.3.5"
  }
}
```

```ts title="sheets/character/vite.config.ts"
import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// The app's web server. `npm run dev` serves the sheet itself and forwards everything else there.
const server = process.env.EP_SERVER ?? 'http://localhost:8080'

export default defineConfig({
  plugins: [svelte()],
  // the sheet is served at /sheets/character/: relative addresses only
  base: './',
  define: {
    __EP_SERVER__: JSON.stringify(server)
  },
  server: {
    proxy: Object.fromEntries(['/systems', '/modules', '/campaigns', '/api', '/_app'].map((path) => [path, server]))
  }
})
```

```js title="sheets/character/svelte.config.js"
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'

export default {
  preprocess: vitePreprocess()
}
```

```json title="sheets/character/tsconfig.json"
{
  "extends": "@tsconfig/svelte/tsconfig.json",
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "types": ["vite/client"],
    "strict": true,
    "noEmit": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts", "src/**/*.svelte", "../../cache/ep.d.ts"]
}
```

```html title="sheets/character/index.html"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Character</title>
  <link href="/systems/my-system/styles/default.css" rel="stylesheet">
</head>
<body>
  <div id="app"></div>
  <script src="/_app/js/ep.js"></script>
  <script src="/_app/js/ep-ui.js"></script>
  <script type="module" src="./src/main.ts"></script>
</body>
</html>
```

```ts title="sheets/character/src/env.d.ts"
/// <reference types="svelte" />
/// <reference types="vite/client" />

/** The app's web server that `npm run dev` forwards to. */
declare const __EP_SERVER__: string
```

```ts title="sheets/character/src/character.ts"
import type { CharacterData } from '../../../cache/schemas/character'

/** The character's store, typed by the model schema's export. */
export type Character = EPEntityStore<CharacterData>

/** The character the address names, or `null` when it names none. */
export const character = EP.entity as Character | null
```

```ts title="sheets/character/src/main.ts"
import { mount } from 'svelte'
import App from './App.svelte'
import { character } from './character'

// `npm run dev` serves the sheet from Vite: the SDK's web socket goes to the app's server
if (import.meta.env.DEV) {
  EP.configure({ server: __EP_SERVER__ })
}

const target = document.getElementById('app')!

function explain(message: string) {
  target.appendChild(document.createElement('p')).textContent = message
}

// the sheet mounts with the entity: in the app from its first frame, in a browser when the
// subscription answers
if (character) {
  character.connect().then(
    (store) => mount(App, { target, props: { character: store } }),
    (error) => explain(`No character: ${error.message}`)
  )
} else {
  explain('The address needs ?id=<character-id>.')
}
```

```svelte title="sheets/character/src/App.svelte"
<script lang="ts">
  import type { Character } from './character'

  let { character }: { character: Character } = $props()

  /** The last refused write. */
  let refusal = $state<string | null>(null)

  $effect(() => {
    const onError = (event: CustomEvent<EPErrorDetail>) => {
      refusal = event.detail.errors.map((error) => error.message).join('; ')
    }
    character.addEventListener('error', onError)
    return () => character.removeEventListener('error', onError as EventListener)
  })

  const view = $derived($character.view)
</script>

<main>
  <h1>{view.name}</h1>
  <label>
    Hit points
    <input type="number" min="0" use:EP.field={{ store: character, path: 'data.hp.current' }}>
  </label>
  <p>Maximum: {view.data.hp?.maximum ?? '–'}</p>
  <p><a href="/roll/1d20/Awareness">Roll Awareness</a></p>

  {#if refusal}
    <p role="alert">Not saved: {refusal}</p>
  {:else if $character.status === 'disconnected'}
    <p>Disconnected, trying again…</p>
  {/if}
</main>
```

```sh
npm install      # once
npm run build    # dist/; reload the sheet to see it
npm run dev      # live reload, forwarding to the app's web server
npm run check    # types, including the model's
```

**`npm run build`** is all you need: the app serves `dist/`, and a sheet always shows its latest
build.

**`npm run dev`** serves the sheet at `http://localhost:5173/?id=<entity-id>`. The SDK, your system's
files and the entity all come from the app, so the app must be running with its web server on, and
`EP_SERVER` must point at it. With the app closed you'll see a proxy error (`ECONNREFUSED`) and an
empty page; start the app and reload. The app accepts web socket connections from pages on `localhost` and
your own network, so open the dev server by one of those addresses rather than a public domain
name; see [Who can connect](/reference/server-api/#who-can-connect).

**Types** come from the app. When it loads your system it writes the SDK's types to `cache/ep.d.ts`
and your model's to `cache/schemas/<label>.d.ts`, so open the system in the app once before running
`npm run check`. `cache/` is generated, so leave it out of your repository and your package.

## In the app and in a browser

The same sheet runs in both, with a few differences:

| | In the app | In a browser |
| --- | --- | --- |
| First state | Before the page loads | When the subscription answers |
| Connection | The web view | A web socket to the app, which reconnects by itself |
| `EP.pick` | The app's library list | `ep-ui.js`, or your `picker` |
| `EP.confirm` | `ep-ui.js`, your `confirmer`, or the app's alert | `ep-ui.js`, your `confirmer`, or the browser's `confirm` |
| `EP.roll` | The dice roller; can resolve `null` | Rolled by the app without showing anything, logged under the browser's name; shown by `ep-ui.js` or your `onRoll` |
| `EP.roll` with a `roller` | Your dice; the app computes the result | The same |
| `EP.query` | The same | The same |
| `store.client` | `app` | `browser` |
| Without a connection | Doesn't happen | Writes are refused and inputs disabled, see [Without a connection](#without-a-connection) |

A browser that can't reach the app when the page loads gets a rejected `connect()`, so give the user
a message and let them reload. Once a sheet is open, it reconnects by itself, and `status` says what
is happening.

## Keeping it fast

Sheets open during play, so a few habits are worth keeping:

- **Mount after `connect()`.** In the app that gives you the entity in your first frame, with no
  loading state to draw.
- **Leave out what you don't use.** `ep-schema.js` costs a request on every open. A card with no
  `EP.t` can decline labels with `EP.configure({ labels: false })`.
- **Link the SDK, don't bundle it.** `/_app/js/ep.js` is shared and kept by the web view. Bundled
  file names with a hash, such as Vite's `assets/index-C-zLHah5.js`, are kept too, so repeat opens
  are cheaper.
- **Keep the build small.** A sheet is opened far more often than it is edited.

## Compatibility

:::caution[Preview]
This is how sheets will stay compatible once they leave the preview. Until then a release can change
`ep.js` and protocol version `1` themselves, and a sheet may need adjusting when the app updates.
:::

The address `/_app/js/ep.js` stays compatible. The app updates it, and existing sheets keep working.
A breaking change arrives as a new file, `ep-2.js`, next to it, so a sheet moves when you choose.

`api` is the protocol's version. `EP.version` gives the one the SDK speaks, and `sheet.json`'s `api`
says which one your sheet was written for.

Within a version the app only adds: new keys in states and answers, new events, new error codes, new
SDK functions. A sheet keeps working by ignoring what it doesn't know, and by treating an error code
it doesn't know as a refusal. The protocol's own rules are under
[Compatibility](/reference/server-api/#compatibility) in the server API.

The SDK comes with the app, so a sheet that uses something new needs an app that has it. Raise your
system's [`compatibility.minimum`](/system-development/packaging/#compatibility) when you start
using it.

Permissions and authentication are planned. A sheet that handles a refused write, as above, needs
no change for them.

## Where to go next

- [Entity subscriptions](/reference/server-api/#entity-subscriptions) — the protocol, for a sheet
  without the SDK: every event, op and error code.
- [Model Schemas](/system-development/schemas/) — declaring what a sheet can write.
- [Views](/system-development/views/#computed-attributes) — the transforms behind `view`.
- [Packaging & Distribution](/system-development/packaging/) — shipping a system with its sheets.
