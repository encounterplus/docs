---
title: Server API
description: The HTTP and WebSocket API exposed by the Encounter+ built-in web server — endpoints, payloads and live events.
---

:::caution[Not a stable public interface yet]
Nothing on this page is a stable public interface yet. The REST endpoints, the map and game-client
events, the broadcasts and the payloads that carry the app's own models exist to serve the
built-in web client and the player display.

[Character sheets](/system-development/sheets/) are a **preview**, and so is everything they use:
the sheet protocol ([entity subscriptions](#entity-subscriptions),
[listing and picking entries](#listing-entries), [rolling dice](#rolling-dice) and the
`requestFailed` codes they share), the [sheet SDK](/system-development/sheets/),
`sheet.json` and [model schemas](/system-development/schemas/). The protocol and the SDK carry a
version, and the [compatibility rules](#compatibility) are the ones they will keep once sheets
leave the preview. Until then they can change between releases, without a new version.

All of it can change without a deprecation period, and this page documents only what is currently
implemented. Build against it if you like, but expect to adjust when the app updates.
:::


Encounter+ runs a small HTTP + WebSocket server inside the app. Its main job is to serve the
browser [web client](/guides/remote-play/) and push live game state to it, but everything it does
is plain HTTP and JSON, so any tool on the same network can talk to it.

## Getting started

The server is off by default and is part of the Premium subscription. Turn it on in
[Remote Play settings](/settings/remote-play/); the app shows the address it is listening on.

| | |
| --- | --- |
| **Base URL** | `http://<device-ip>:<port>` |
| **Default port** | `8080` |
| **Protocol** | HTTP/1.1, plus a WebSocket upgrade on the same port |
| **Content type** | `application/json` for everything under `/api` |
| **Dates** | ISO 8601 |

```bash
curl http://192.168.1.42:8080/api
```

:::danger[There is no authentication]
Anyone who can reach the port can read your campaign and write to it. There are no tokens, no
passwords and no per-client permissions, and `Access-Control-Allow-Origin` is `*`, so any web page
your browser loads can read from a server it can reach. The WebSocket refuses pages from elsewhere
on the internet, see [Who can connect](#who-can-connect), but anything on your network can still
connect directly.

Run it on a trusted network. If you forward the port to the internet — the app can do this over
UPnP — understand that you are publishing an unauthenticated read/write interface.
:::

### Errors

Failures return a status code and a one-key JSON body:

```json
{ "message": "Not Found" }
```

| Status | Meaning |
| --- | --- |
| `400 Bad Request` | The body could not be parsed, or an `id` in the body disagrees with the one in the path |
| `404 Not Found` | No object with that id, or no entity collection by that name in the loaded game system |
| `202 Accepted` | Used only by `/api/import` — the request was handed to the app, not completed |

### CORS

Preflight responses currently advertise `Access-Control-Allow-Methods: GET, OPTIONS`, so a
cross-origin `PUT` or `PATCH` from a browser is refused even though the endpoint exists.
Same-origin callers and non-browser clients are unaffected.

## Game state

### `GET /api`

A snapshot of everything the player display needs: the current game, the loaded map, the player
screen configuration, recent chat, and any tracked physical objects. This is what the web client
fetches on load, before it starts following [WebSocket events](#websocket-api).

```json
{
  "version": "5.0",
  "build": 4212,
  "game": { "round": 3, "turn": 1, "started": true, "combatantId": "…", "initiativeId": "…", "resources": [ { "…": "…" } ] },
  "map": { "id": "…", "name": "Goblin Cave", "…": "…" },
  "screen": { "mapId": "…", "overlayType": "…", "…": "…" },
  "messages": [ { "…": "…" } ],
  "trackedObjects": [],
  "paused": false
}
```

| Field | Notes |
| --- | --- |
| `version`, `build` | The running app's version and build number |
| `game` | The primary campaign's [Game](/reference/schema/game/) — initiative order and combat state |
| `map` | The [Map](/reference/schema/map/) currently on the player screen, absent if none is loaded |
| `screen` | Player-screen configuration — overlay, fog, table-top mode, remote interaction |
| `messages` | The 30 most recent [Messages](/reference/schema/message/), oldest first |
| `trackedObjects` | Objects reported by object tracking |
| `paused` | Whether the campaign is paused |

Returns `404` when there is no primary campaign for the loaded system.

`game.resources` lists the loaded system's [game
resources](/system-development/config/#game-resources) that are visible to players, each with its
current value. The definition is resolved in, so a client never needs the system's `config.json`:

```json
"resources": [
  { "id": "fear", "type": "counter", "label": "Fear", "icon": "gi-burning-skull", "min": 0, "max": 12, "value": 5 }
]
```

`max` and `icon` are absent when the system leaves them out. An image `icon` is a path on this
server. Resources with `gm` visibility are never sent, and neither is a `countdown` at `0`. `type`
is `counter` or `countdown`; a client should skip a type it does not know, since later types will
share the list. The list is empty, not absent, when
the system declares no player-visible resources; older app builds leave it out entirely.

### `GET /api/system`

The loaded game system, with every definition a client needs to render its content: entity
definitions, type tables, configuration and settings. This is the largest response the API
produces and is meant to be fetched once per session.

```json
{
  "id": "dnd5e",
  "name": "D&D 5th Edition",
  "config": { "…": "…" },
  "settings": { "…": "…" },
  "definitions": {
    "entities": { "monster": { "…": "…" }, "spell": { "…": "…" } },
    "types": { "size": [ { "…": "…" } ] }
  }
}
```

See [System](/reference/schema/system/) and
[Entity Definition](/reference/schema/entity-definition/).

### `GET /api/clients`

The clients currently connected over WebSocket.

```json
[
  { "channel": 3, "address": "192.168.1.51", "name": "Ellie", "color": "#4caf50",
    "screenWidth": 1180, "screenHeight": 820, "runMode": "normal", "device": "iPad",
    "mapCenterX": 1200, "mapCenterY": 900, "mapZoom": 1.4 }
]
```

`runMode` is `normal` for a player browser; anything else marks the client as a player display,
which gets its own viewport in the app.

## Entities

Entities are the app's generic content objects — monsters, spells, items, and whatever else the
loaded game system defines. The path segment is the **collection label** from the system's entity
definitions, so it varies by system. In D&D 5e: `characters`, `monsters`, `npcs`, `spells`,
`items`, `feats`, `backgrounds`, `species`, `races`, `classes`, `subclasses`, `vehicles`, `rules`,
`tables`.

An unknown collection is a `404` — fetch `/api/system` to discover what the loaded system offers.

### `GET /api/{collection}`

One page of library entries, `{ entries, total }`, filtered and sorted exactly as
[`queryEntities`](#listing-entries) answers: the collection's kind and the kinds extending it.

```bash
curl 'http://192.168.1.42:8080/api/monsters?keys=list'
```

The parameters are those of [`queryEntities`](#listing-entries): `search`, `sort`, `offset`,
`limit`, `where` as a JSON object, and `keys` and `ids` comma separated — `keys=list` for the
system's list keys, alone or with paths (`keys=list,data.weight,view.data.evasion`). A parameter
that can't be read is a `400` saying why. Entries carry only the `data.` and `view.` paths `keys`
asks for; fetch [one entity](#get-apicollectionid) for its whole model.

```bash
curl -G 'http://192.168.1.42:8080/api/items' \
  --data-urlencode 'where={"data.skill": ["axes", "swords"]}' \
  --data-urlencode 'keys=data.skill,data.weight' \
  --data-urlencode 'limit=20'
```

:::caution[`schema` is gone]
The collection once took `schema=list|basic|model|view|entries` and listed the whole kind. It now
always answers a page of entries, and a request that still sends `schema` is a `400`, so an old
client fails at once instead of reading a different shape. `schema=list` is `keys=list`;
`schema=basic` is no `keys`; for `model`, list the ids, then fetch each entity; for `view`, ask for
the computed values you show as `view.` keys, or fetch each entity with `schema=view`.
:::

### `GET /api/{collection}/{id}`

One entity.

| Query | Default | Effect |
| --- | --- | --- |
| `schema=model` | ✓ | The stored model |
| `schema=view` | | The rendering context, with computed and formatted values |
| `references=true` | `false` | Adds a `references` key holding the resolved linked entities |

Returns `404` if no entity has that id, or if the entity exists but is not of the collection's
kind — so `/api/spells/<a-monster-id>` is a `404`, not a monster.

### `PUT /api/{collection}/{id}`

Replaces the entity. The body is a complete [Entity](/reference/schema/entity/), and its `id` must
match the path — a mismatch is a `400`, not a rename. Responds with the stored entity.

### `PATCH /api/{collection}/{id}`

Merges a partial JSON object into the entity, leaving unmentioned keys alone. This is the endpoint
to use for "set current HP" and similar single-field edits. Responds with the merged entity.

```bash
curl -X PATCH http://192.168.1.42:8080/api/monsters/2f1c… \
  -H 'Content-Type: application/json' \
  -d '{"data": {"hp": 12}}'
```

Both writes notify the app, so open views redraw, and a unique entity's linked combatant is
updated to match.

Neither write is checked against the entity type's [model schema](/system-development/schemas/),
and neither is limited by remote interaction: until there are permissions, every client can change
every entity. A [sheet](/system-development/sheets/) writes through
[entity subscriptions](#entity-subscriptions) instead, where every write is checked.

## Combatants

Combatants are entries in the initiative order. They are a fixed model rather than a
system-defined one, so they have their own path, and `combatants` is therefore reserved — a system
collection by that name is unreachable.

| | |
| --- | --- |
| `GET /api/combatants/{id}` | The [Combatant](/reference/schema/combatant/) |
| `PUT /api/combatants/{id}` | Replaces it; the body's `id` must match the path |
| `PATCH /api/combatants/{id}` | Merges a partial object into it |

Writing a shared combatant also pushes its ranges back to the entity it came from.

There is no endpoint that lists combatants — read them from `game` in [`GET /api`](#get-api), or
follow `combatantsUpdated` over the WebSocket.

## Tokens

Tokens are the pieces on the battle map. `tokens` is reserved in the same way `combatants` is.

| | |
| --- | --- |
| `GET /api/tokens/{id}` | The [Token](/reference/schema/token/) |
| `PUT /api/tokens/{id}` | Replaces it |
| `PATCH /api/tokens/{id}` | Merges a partial object into it |

Unlike the other `PUT` endpoints this one does not check the body's `id` against the path; the
body wins.

For moving a token during play, prefer the `tokenMoved` WebSocket event — it animates on every
connected display and respects the host's remote-interaction setting, where a `PATCH` does not.

## Messages

### `POST /api/messages`

Posts a message to the shared log. The body is a [Message](/reference/schema/message/); dice
expressions in it are rolled, and the stored message — with its results and campaign attached —
comes back in the response.

```bash
curl -X POST http://192.168.1.42:8080/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"text": "The door creaks open."}'
```

A `400` means the body did not parse as a message.

## Import

### `POST /api/import`

Offers a piece of content to the device for import. This is the network counterpart of the
`encounterplus://import` [URL scheme](/reference/url-scheme/), and takes the same parameters —
either as a JSON body or as a query string:

```bash
curl -X POST 'http://192.168.1.42:8080/api/import' \
  -H 'Content-Type: application/json' \
  -d '{"manifest": "https://example.com/packages/dnd5e.json"}'
```

```bash
curl -X POST 'http://192.168.1.42:8080/api/import?url=https%3A%2F%2Fexample.com%2Fmaps%2Fcave.uvtt'
```

Exactly one source must be given. Providing one in the body *and* one in the query is rejected, as
is a source the app will not accept.

`202 Accepted` means the import screen is now on the device's display — **not** that anything was
imported. Only the person at the app can confirm it, which is what keeps an open port from being a
way to install content on someone else's iPad. There is no way to poll for the outcome.

It is `POST` rather than `GET` deliberately: a `GET` would fire from an `<img src>` on any page a
user on the network happened to load.

## Static content

The server also serves files, which is how the web client and its media reach the browser.

| Path | Serves |
| --- | --- |
| `/`, `/index.html` | The landing page |
| `/client/` | The installed web client |
| `/icon.png` | The app icon |
| `/modules/`, `/campaigns/` | Imported content — maps, images, handouts |
| `/systems/` | Game system assets — fonts, icons, images |
| `/_app/` | The app's own view resources, among them the [sheet SDK](/system-development/sheets/): `/_app/js/ep.js`, `ep-ui.js`, `ep-schema.js` |
| `/others/` | Temporary images generated during play |
| `/sheets/{sheet}/` | A sheet of the loaded system; see [`GET /sheets/{sheet}/`](#get-sheetssheet) |

### `GET /{reference}`

Any other single-segment path is treated as an entity reference URL and answered with that entity
rendered as HTML — the same markup the app shows in a detail view, using the system's view
templates and theme. Invalid references return `400`, unknown ones `404`. An entity whose type
opens as a sheet redirects (`302`) to its sheet.

### `GET /sheets/{sheet}/`

A sheet is a static web app in the system's `sheets/{sheet}/` folder, opened for an entity at
`/sheets/{sheet}/?id={entity-id}` — the same address the app uses in its own views, so a sheet's
relative URLs resolve the same way in both. The address serves the sheet's `index.html`; paths
below it serve the folder's files, and `/sheets/{sheet}` redirects to the address with the
trailing slash. Sheet files are sent with `Cache-Control: no-cache` and an `ETag`, so a browser asks before using its copy and an unchanged file is an empty `304`. Code and markup under `/systems/`, `/modules/`, `/campaigns/` and `/client/` — `html`, `js`, `mjs`, `css`, `json` — are sent the same way; media can be kept for a year.

A sheet built with its own tooling (a `package.json`, sources, `node_modules`) names the folder of
its build output in a `sheet.json` beside them, `{"root": "dist"}`: only that folder is served, so
the address serves `dist/index.html` and nothing outside `dist/` is reached through it. The system's
folder is served as well, at `/systems/{system}/`, so nothing in it is private. Its other keys are
`api`, the protocol version the sheet was written for, and `entities`, the entity kinds it can show;
all three are optional. A sheet serves nothing when its `api` is one this app doesn't speak, its
`root` isn't a folder inside the sheet, or a value has the wrong type.

The sheet follows the entity through [entity subscriptions](#entity-subscriptions). Entity views
get the address of their type's sheet as `env.sheetURL`. Writing a sheet is covered in
[Character Sheets](/system-development/sheets/).

:::caution[Preview]
Sheets are a preview and may still change between releases; see the note at the top of this page.
:::

## WebSocket API

Live state travels over a WebSocket on the same port. Any path upgrades; the web client connects
to the server root.

Every message, in both directions, is one JSON envelope:

```json
{ "name": "tokenMoved", "data": { "…": "…" }, "requestId": "…", "responseId": "…" }
```

| Field | Notes |
| --- | --- |
| `name` | What the event reports or requests — determines the shape of `data` |
| `data` | The payload; its type follows from `name` |
| `requestId` | Set by a client on a request it wants an answer to; unique on its connection |
| `responseId` | Echoes the `requestId` of the request being answered |

Every event carrying a `requestId` gets exactly one answer with that `responseId`: the reply its
name documents, or `requestFailed { code, message }`. An event without a `requestId` is a
notification and is never answered. An answer can be an ordinary event too: the answer to
`subscribeEntity` is an `entityUpdated`, which says what the event is with `name` and what it
answers with `responseId`.

`code` tells a client what happened, and `message` is for people:

| `code` | Meaning |
| --- | --- |
| `unknownEvent` | The app doesn't know the event's name |
| `unsupportedEvent` | The app knows the name, but doesn't take it on this connection |
| `invalidRequest` | The event's data is missing something or can't be read |
| `unsupportedApi` | The `api` of a `subscribeEntity` is newer than this app speaks |
| `noSuchEntity` | No entity has that id |
| `notSubscribed` | An `updateEntity` for an entity the client doesn't follow |
| `notAllowed` | Reserved for permissions: nothing is refused with it yet |
| `noSchema` | The entity type has no [model schema](/system-development/schemas/), or it failed to load |
| `refused` | A batch of ops was refused; `errors` says why, see [Entity subscriptions](#entity-subscriptions) |
| `failed` | The app could not complete the request |

Names ending in `Updated`, `Created` or `Deleted` are the app broadcasting a change. Names in the
imperative — `createMessage`, `updateDoor` — are a client asking for one. The payloads of the
sheet protocol's events are documented on this page, which is the reference for them. The
generated [WSEvent](/reference/schema/wsevent/) page describes the envelope and the app's model
payloads; it is built from the app's source and can lag behind.

A message a client sends can be up to 1 MB, in one frame or in fragments. A larger one closes the
connection with code `1009`. What the app sends has no limit.

The app turns on TCP keepalive for every connection. Once a connection has been quiet for a
minute, the system checks it every 10 seconds and closes it after five checks go unanswered. A
client that vanished is let go within about two minutes, and routers keep a quiet connection open
through port forwarding. The app sends no WebSocket pings. A client that needs to notice a dead
connection sooner sends a request and closes the socket when no answer comes.

On connect, the app sends an `app` event carrying its `version` and `build`.

### Compatibility

:::caution[Preview]
These are the rules the sheet protocol will keep once sheets leave the preview. Until then a release
can change version `1` itself.
:::

The sheet protocol's version is the `api` a client names in
[`subscribeEntity`](#entity-subscriptions): `1` today. A subscription runs at the version it asks
for, or is refused with `unsupportedApi`.

Within a version the app only adds: new keys in states and answers, new events, new error codes,
new optional fields in requests. A client stays compatible by:

- ignoring keys and events it doesn't know;
- treating a `requestFailed` code it doesn't know as a refusal;
- sending only the fields documented here, since a field the app doesn't know yet may mean
  something later.

A change that would break a client written to this page comes as a new version, and the app keeps
speaking the old one. The [sheet SDK](/system-development/sheets/#compatibility) follows the same
rule: `/_app/js/ep.js` speaks version `1`, and a later version ships as a new file.

### Who can connect

Browsers don't apply CORS to WebSockets, so the app checks the `Origin` a browser sends with the
upgrade and accepts:

| Origin | For |
| --- | --- |
| None | Clients that aren't browsers: native apps, scripts, command-line tools |
| The address the request went to | The app's own pages: the web client, sheets |
| `localhost`, loopback addresses | A page on the same machine, such as a sheet's dev server |
| Private and link-local addresses, `.local` names | A page served from another machine on your network |

Any other page is refused, `null` included (a sandboxed frame or a local file), and the upgrade
gets an ordinary HTTP response instead, so the browser reports a failed connection.

Port forwarding and dynamic DNS names work unchanged: players who open the app's pages at your
public address connect at that same address, and the browser names it in both `Origin` and `Host`.
A web client you serve yourself must be on your network (by address or a `.local` name). A page on
a public server is refused even when it connects to your public address. A reverse proxy must pass
on the `Host` the browser sent (with nginx, `proxy_set_header Host $host;`), or the app's own pages
are refused through it.

### Events a client can send

Anything not listed here is ignored, even when the app knows the name — and refused with
`requestFailed` when it carries a `requestId`. The events marked *both* work the same in the
app's web views ([below](#in-the-apps-web-views)); the others are for connected game clients only.

| Event | Payload | Where | Effect |
| --- | --- | --- | --- |
| `clientUpdated` | `Client` | socket | Registers the client's name, color, device and screen size. Send this first — a client identifying itself with a non-`normal` `runMode` becomes a player display. The name is what the log shows for the client's messages and rolls |
| `mapViewportUpdated` | `Frame` | socket | Reports where this client is looking, so the app can show its viewport |
| `tokenMoved` | `Movement` | socket | Drags a token. Refused when remote interaction is off |
| `updateDoor` | `Door` | socket | Opens or closes a door, recomputing line of sight. Refused when remote interaction is off |
| `pointerUpdated` | `Pointer` | socket | Moves this client's shared pointer. Refused when remote interaction is off |
| `updateToken` | partial object | socket | Merges changes into a token by `id` |
| `subscribeEntity` | `{ id, api, labels? }` | both | Follows an entity; see [Entity subscriptions](#entity-subscriptions) |
| `unsubscribeEntity` | `{ id }` | both | Stops following an entity |
| `updateEntity` | `{ id, ops }` | both | Applies a batch of ops to a subscribed entity; see [Entity subscriptions](#entity-subscriptions) |
| `queryEntities` | `{ entity, search?, where?, sort?, keys?, ids?, offset?, limit? }` | both | Lists a page of library entries; answered with `entitiesQueried { entries, total }`, see [Listing entries](#listing-entries) |
| `pickEntity` | `{ entity }` | both | Lets the user pick library entries in the app's own list; answered with `entityPicked`. Needs someone at the app, so a socket gets `unsupportedEvent`; see [Listing entries](#listing-entries) |
| `rollDice` | `{ formula, label?, type?, mode?, creature?, rolls?, customize? }` | both | Rolls dice and logs the roll, or logs dice the client threw itself; answered with `diceRolled`, see [Rolling dice](#rolling-dice) |
| `createMessage` | `Message` | both | Posts to the shared log, rolling a `/roll` command in it; answered with `messageCreated` on `requestId` |
| `updateCombatant` | partial object | both | Merges changes into a combatant by `id`; answered with `combatantUpdated` on `requestId`, or `noSuchEntity` |
| `listRollOptions` | `{ formula, label?, type? }` | both | Lists what a roll link's menu offers; answered with `rollOptionsListed`, see [Roll menus](#roll-menus) |
| `updateResource` | `{ id, add }` or `{ id, value }` | both | Changes a [game resource](/system-development/config/#game-resources) of the campaign being played; answered with `resourcesUpdated`, see [Game resources](#game-resources) |
| `subscribeResources` | `{}` | both | Asks for the game resources the client may see; answered with `resourcesUpdated`, and a web view gets it after every change from then on, see [Game resources](#game-resources) |
| `getAttribute` | `Attribute` | socket | **Deprecated.** Answers with the request unchanged; use `subscribeEntity` |
| `setAttribute` | `Attribute` | socket | **Deprecated.** Writes `data` without the model schema; use `updateEntity` |
| `trackedObjectCreated` / `trackedObjectUpdated` / `trackedObjectDeleted` / `trackedObjectsUpdated` | `TrackedObject` | socket | Reports physical objects tracked on a table-top display |

:::note[Remote interaction gates the map]
`tokenMoved`, `updateDoor` and `pointerUpdated` are dropped when the host has remote interaction
turned off. Nothing else is gated: entities, tokens and combatants can always be changed, over the
WebSocket as over [REST](#entities). Permissions and authentication are planned for both.
:::

:::caution[Deprecated]
`getAttribute` and `setAttribute` are kept for clients that may still send them, and will be
removed. New clients use [entity subscriptions](#entity-subscriptions).
:::

### Events the app broadcasts

| Group | Events |
| --- | --- |
| Game state | `gameUpdated`, `combatantsUpdated`, `resourcesUpdated`, `systemPaused` |
| Player screen | `screenUpdated`, `interactionUpdated`, `reload` |
| Map | `mapUpdated`, `mapLoaded`, `mapFrameUpdated`, `mapFitScreen`, `mapFocus`, `mapVideoControlUpdated` |
| Map objects | `tokenUpdated`, `tokensUpdated`, `markerUpdated`, `markersUpdated`, `tileUpdated`, `tilesUpdated`, `lightUpdated`, `lightsUpdated`, `areaEffectUpdated`, `areaEffectsUpdated`, `measurementUpdated`, `measurementsUpdated` |
| Movement | `mapMoved`, `tokenMoved`, `markerMoved`, `tileMoved`, `areaEffectMoved`, `pointerMoved` |
| Overlays | `fogUpdated`, `drawingsUpdated`, `lineOfSightUpdated`, `pointerUpdated` |
| Content | `entityCreated`, `combatantCreated`, `combatantUpdated`, `combatantDeleted` |
| Log | `messageCreated`, `messagesUpdated`, `messageDeleted` |
| Clients | `clientConnected`, `clientDisconnected`, `clientUpdated`, `app` |
| Object tracking | `trackedObjectCreated`, `trackedObjectUpdated`, `trackedObjectDeleted`, `trackedObjectsUpdated` |

Broadcasts go to every connected client, including the one whose action caused them.
`entityUpdated` and `entityDeleted` are not broadcast: they go only to clients subscribed to the
entity (see below).

`resourcesUpdated` carries the whole `game.resources` list from [`GET /api`](#get-api) after any
change, and replaces what the client holds; see [Game resources](#game-resources). `gameUpdated`
never carries resources.

### Game resources

One event carries the system's [game resources](/system-development/config/#game-resources),
whatever the reason: `resourcesUpdated`, with the whole list the client may see, each entry in the
shape of `game.resources`. It is the broadcast after every change, the answer to
`subscribeResources`, and the answer to `updateResource`, and it always replaces what the client
holds.

A socket sees the resources the players see; a countdown at `0` is not running yet and is left out.
The app's web views run on the GM's device and see them all.

`subscribeResources` asks for the list:

```json
→ { "name": "subscribeResources", "requestId": "r19", "data": {} }
← { "name": "resourcesUpdated", "responseId": "r19", "data": [{ "id": "fear", "type": "counter", "label": "Fear", "min": 0, "max": 12, "value": 4 }] }
```

A socket gets the broadcast after every change whether it asked or not, so for it this is only a
read. A web view gets no broadcasts, and follows the resources once it has sent this: the same
`resourcesUpdated` arrives after every change, without a `responseId`, until its page goes. With
no campaign being played the list is empty.

`updateResource` changes one resource in the campaign being played — a sheet giving the GM a Fear
when a roll goes with Fear:

```json
→ { "name": "updateResource", "requestId": "r20", "data": { "id": "fear", "add": 1 } }
← { "name": "resourcesUpdated", "responseId": "r20", "data": [{ "id": "fear", "type": "counter", "label": "Fear", "min": 0, "max": 12, "value": 5 }] }
```

| Field | Notes |
| --- | --- |
| `id` | Required. The resource's `id` in the system's `config.json` |
| `add` | A whole number to change the value by, negative to lower it |
| `value` | A whole number to set the value to |

Send exactly one of `add` and `value`. The value is kept within the resource's `min` and `max`, so
Fear at 12 stays at 12, and `add` is applied by the app to the value it holds, so two clients
adding at once both count. The answer is the list as it is now, the changed resource in it — unless
it is a countdown a socket no longer sees, at `0`; everyone else learns of the change from the
`resourcesUpdated` broadcast, the bottom bar and the player display included.

Like `updateEntity`, a request needs a `requestId`: one without is ignored and not applied. Both,
neither, a value that isn't a whole number, or another key is `invalidRequest`. A socket can
change only resources the players see; any other `id`, GM-only ones included, is refused as
unknown (`invalidRequest`, `no such resource`), so a player can't learn that a GM-only resource
exists. The app's web views run on the GM's device and can change them all. With no campaign being
played the request fails with `failed`.

### Entity subscriptions

A client follows an entity by subscribing to it, and gets the entity's whole state as
`entityUpdated` then and after every change — whoever made it: this client, another browser, a
form or the combat bar in the app. Character sheets work this way, in the app and in a browser.

```json
→ { "name": "subscribeEntity", "requestId": "r1", "data": { "id": "k3x9…", "api": 1 } }
← { "name": "entityUpdated", "responseId": "r1", "data": { "id": "k3x9…", "client": "browser", "system": { "id": "dragonbane", "version": "1.2.0", "labels": { "…": "…" } }, "env": { "…": "…" }, "model": { "…": "…" }, "derived": { "…": "…" } } }
```

| Field of `entityUpdated` | Notes |
| --- | --- |
| `id` | The entity |
| `model` | The entity as stored: nothing computed, nothing left out. A link to another object is its id, `combatantId`. The [model schema](/system-development/schemas/) decides what can be written, never what is sent |
| `derived` | What the app and the system's transforms add to or change in the model (the view): the transforms' values, and `reference`, `location`, `source`, `sourceFormatted`, `locationFormatted` and `footer`. Objects are compared key by key; a changed value or list is sent whole; a key the view removes is `null`. Lay it over `model` to get the view |
| `client`, `system`, `env`, `schema` | Only in the answer to `subscribeEntity`: where the client runs, `app` or `browser`; the loaded system as `{ id, version, labels }`, with its labels (below); the view environment; and the address of the entity type's runtime schema (`/systems/{system}/cache/schemas/{label}.json?v=…`), which a client can check writes with before sending them — when the type has a schema |

The labels are `{ language, strings, enums }`: the system's strings in its language by key, with
English for any key the language lacks, and every enum key's label by enum — for sheets, which
have no template filters to localize with. A client that has them or doesn't need them subscribes
with `labels: false`, and the first state leaves them out.

`api` is the protocol version the client speaks, `1` when it is left out. A version newer than the
app's is refused with `unsupportedApi`, and one that isn't a number with `invalidRequest`. The
answer doesn't repeat it: a subscription runs at the version it asked for, or is refused.

State arrives in order, so the last `entityUpdated` received is the current one. When the entity
is deleted, subscribers get `entityDeleted { id }` and the subscription ends; it also ends when
the client disconnects.

#### Starting state

In the app's web views, a sheet gets the entity's first state before it loads, labels included,
so it can draw the entity at once rather than after the subscription answers:
`window.encounterplusStartingState`, set at document start to the `data` of the `entityUpdated`
that answers `subscribeEntity`. Template views get no starting state: they are rendered with the
entity, and one that follows it subscribes like any other client.

```js
window.encounterplusStartingState // { id: "k3x9…", client: "app", system: {…}, env: {…}, schema: "…", model: {…}, derived: {…} }
```

The state the subscription then answers with is the same one unless the entity changed in
between, so a client can compare the two to tell. A page should check `id` first: the web view
keeps the state for the entity it last loaded a sheet of. Browsers get no starting state, and
draw the entity once the subscription answers.

A subscribed client changes the entity with a **batch** of ops, applied whole or not at all. An
update needs a `requestId`, and the state that includes it answers with that `responseId`:

```json
→ { "name": "updateEntity", "requestId": "r7", "data": { "id": "k3x9…", "ops": [
    { "op": "test", "path": "data.weapons[0]", "value": { "name": "Dagger" } },
    { "op": "set", "path": "data.weapons[0].broken", "value": true }
  ] } }
← { "name": "entityUpdated", "responseId": "r7", "data": { "id": "k3x9…", "model": { "…": "…" }, "derived": { "…": "…" } } }
```

| Op | Fields | Effect |
| --- | --- | --- |
| `set` | `path`, `value` | Writes a value, creating missing objects on the way (never list items). `null`, or `""` for anything but text, removes the key |
| `remove` | `path` | Removes a key (nothing happens when it is missing) or a list item |
| `insert` | `path`, `value`, `index?` | Inserts an object into a list, at the end without `index`; creates a missing list. In a list with ids the item keeps an id it brings or gets a new one |
| `move` | `path`, `index` | Moves a list item within its list; `index` is its position afterwards |
| `test` | `path`, `value` | Checks a value without writing; `null` expects the key to be missing |
| `increment` | `path`, `value` | Changes a number by `value`, negative to lower it, counting from the value stored now — so two clients' changes both count — and from 0 when there is none. The result is kept within the declared `min` and `max` rather than refused. Only `integer` and `number` fields; a whole-number field takes whole numbers |
| `embed` | `path`, `ref`, `keys`, `index?` | Adds a copy of a library entry — `ref` is its reference, `/item/axe` — to a list of references, or puts it in a single reference field: the entry's `name`, `ref` as its `reference`, and the listed `keys` of its data (its description as `descr` when the data has none). The entry must be of the kind the schema's `ref` declares, and the keys declared |

Paths start at `data`: `data.hp.current`, `data.actions[2].name` (a list item by position),
`data.items[k3x9].quantity` (by `id`, in a list with ids). Every value is checked and converted
against the entity type's model schema, and paths it doesn't declare are refused; an entity type
without a schema refuses every batch.

Beside `data`, two of the entity's own fields can be written, with `set` and `test` only: `name`,
text that isn't empty (it is trimmed), and `notes`, text, removed by `null` or `""`. A rename leaves
the entity's `slug`, and so its address, as it is. They go in the same batch as `data` ops, applied
whole or not at all. Any other path outside `data` is `invalidPath`. A key the schema doesn't
declare is still sent in `model`: the schema decides what can be written, never what can be read.

The other subscribers get the same state without a `responseId`. A refused batch is answered with
`requestFailed`:

```json
← { "name": "requestFailed", "responseId": "r7", "data": { "code": "refused", "message": "the update was refused", "errors": [
    { "index": 1, "path": "data.hp.current", "code": "outOfRange", "message": "data.hp.current: must be between 0 and 30" }
  ] } }
```

`index` is the failing op; each error's `code` is one of `invalidPath`, `undeclared`, `notWritable`,
`invalidValue`, `outOfRange`, `invalidKey`, `invalidSelector`, `duplicateId`, `invalidOp`,
`missingItem`, `notAList`, `invalidIndex`, `testFailed`, `notAReference` and `missingSource`. `requestFailed` without `errors`
answers a request that could not be handled at all, and its `code` says why: `noSuchEntity`,
`notSubscribed`, `noSchema`, `notAllowed`, or `invalidRequest` for an update without `ops`. An
update without a `requestId` is ignored and not applied, since nothing could answer it.

Entries to embed are found with [`queryEntities`](#listing-entries), or picked by the user with
`pickEntity`.

:::note[`updateEntity` no longer merges]
Earlier versions took `updateEntity` with a partial entity and merged it in. That form is gone:
an `updateEntity` without `ops` is refused with `requestFailed`.
:::

:::note[Preview]
Entity subscriptions are part of the sheet protocol, version `1`, which is a preview; see
[Compatibility](#compatibility).
:::

### Listing entries

A client lists library entries to build its own picker — a dialog, a dropdown, a list of spells
to learn — with `queryEntities`, and gets one page of them with the number of matches in all:

```json
→ { "name": "queryEntities", "requestId": "r9", "data": {
    "entity": "Item", "search": "a", "where": { "type": "weapon", "data.skill": ["axes", "swords"] },
    "sort": "name", "keys": ["data.skill", "data.weight"], "limit": 20 } }
← { "name": "entitiesQueried", "responseId": "r9", "data": { "total": 2, "entries": [
    { "id": "…", "name": "Axe", "kind": "Item", "type": "weapon", "reference": "/module/rules/item/axe", "source": "Core",
      "image": "/modules/rules/items/axe.webp", "tags": ["metal"], "data": { "skill": "axes", "weight": 2 } },
    { "id": "…", "name": "Broadsword", "kind": "Item", "type": "weapon", "reference": "/module/rules/item/broadsword", "source": "Core",
      "data": { "skill": "swords", "weight": 2 } }
  ] } }
```

| Field | Notes |
| --- | --- |
| `entity` | Required. The entity kind as the system's definitions name it (`Item`, not a label); the loaded system's entries of that kind and of the kinds extending it are listed |
| `search` | Part of the name, any case |
| `where` | An object of paths and what their values must be, every one holding: a value to equal, a list to equal one of, or [operators](#where-operators). Paths are `name`, `type`, `kind`, `source`, `tags`, or anything under `data.`. Values are text, numbers and booleans; numbers compare as numbers (`2` matches `2.0`) and never as booleans, text exactly, and a stored list (`tags`) matches when any of its items does. A missing value, `null`, `""` and `[]` are no value, which equals nothing |
| `sort` | A path, as for `where`, descending with a `-` prefix: `-data.weight`. Numbers sort as numbers and text in Finder order; entries without the value go last. Name order when left out |
| `keys` | Paths each entry carries, so a picker can show columns without fetching every entry: `data.` paths in its `data`, stored values, and `view.` paths in its `view`, values the app computes through the system's transforms (`view.data.evasion`). `"list"`, alone or in the list, stands for the `data.` paths the system's list of the kind filters, groups and sorts by (its `filters.json`) — what a picker shows without knowing the system; a kind without filters has none. Computed values cost more: the app works them out for the page it answers, never for the whole kind, which is also why `where` and `sort` read stored values only |
| `ids` | Only these entries — for showing what a sheet already holds |
| `offset`, `limit` | The page: from `offset` (0), up to `limit` entries (50 when left out, at most 200) |

An entry is `{ id, name, kind, type?, reference, source?, detail?, image?, icon?, tags?, data?, view? }`.
`reference` is as a copy of the entry holds it — what `embed` takes as `ref`. `detail` is the line
under the name in the app's library list, the system's `collection.detail` for the kind in
`config.json`, so a picker can show the same. `image` is an address the page reaches the file at,
in the app and in a browser alike; `icon` is a game icon (`gi-…`) as it is, or such an address.
`pickEntity` answers with the same entries.

#### Where operators

A `where` value can be an object of operators instead, which must all hold — so
`{ "gte": 1, "lte": 3 }` is a range:

```json
"where": {
  "data.level": { "gte": 1, "lte": 3 },
  "data.school": { "nin": ["necromancy", "illusion"] },
  "data.ritual": { "exists": true }
}
```

| Operator | Operand | Keeps an entry when its value… |
| --- | --- | --- |
| `ne` | a value | isn't equal to it. No value passes; a stored list passes when no item is equal |
| `nin` | a list of values | is equal to none of them. No value passes; a stored list passes when no item is equal to one |
| `lt`, `lte`, `gt`, `gte` | a number | is a number below, at most, above or at least it. Text, booleans and no value never pass; a stored list passes when any item does |
| `exists` | `true` or `false` | has a value, or has none. `null`, `""` and `[]` count as none, as a cleared form field leaves them |

To keep entries that have a value and aren't one of a list, put `exists` beside `nin`:
`{ "nin": ["cantrip"], "exists": true }`. There is no OR across paths, no case-insensitive or
partial match outside `search`, and no "every item of a list" test.

A query is plain data, matched by the app; it never runs code. A value of the wrong type is refused
with `invalidRequest` naming the problem rather than read as a default — an operand of the wrong
type, an unknown operator, an empty operator object, or `null` as a value (use
`{ "exists": false }`). REST lists the same pages with
[`GET /api/{collection}`](#get-apicollection).

**Picking.** `pickEntity { entity }` shows the app's own library list and is answered with
`entityPicked { entities }`, the entries the user picked, none when they cancelled. It needs
someone at the app, so only the app's web views can make it: a socket gets `unsupportedEvent`, and
lists entries for its own picker instead.

### Rolling dice

`rollDice` rolls dice, logs the roll and answers with it, the same on a socket and in the app's web
views:

```json
→ { "name": "rollDice", "requestId": "r13", "data": { "formula": "1d20+2", "label": "Awareness", "type": "check" } }
← { "name": "diceRolled", "responseId": "r13", "data": { "roll": { "name": "Awareness", "type": "check", "formula": "1d20 + 2", "result": 16, "detail": "(14) + 2",
    "dice": [{ "formula": "1d20", "faces": 20, "result": 14, "rolls": [{ "value": 14 }] }] } } }
```

| Field | Notes |
| --- | --- |
| `formula` | Required. A formula that can't be rolled is refused with `invalidRequest` |
| `label` | The roll's name, as the log shows it |
| `type` | `attack`, `damage`, `heal`, `check` or `save`; an unknown type is left out |
| `mode` | `public` or `private`. In the app's web views it overrides the app's roll mode setting, which applies when it is left out; a socket's rolls are always public for now |
| `creature` | Who the roll is for, as the log shows it. In the app's web views it defaults to the entity the view shows |
| `rolls` | Dice the client threw itself — see below |
| `customize` | `true` opens the app's advanced dice roller with the formula, for the GM to change and roll — the roll menu's *Customize…* item. The answer carries no roll: what is rolled there is the GM's own, logged by the roller. Only the app's web views can, a socket gets `unsupportedEvent` |

**Who throws the dice.** Without `rolls`, the app does:

- In the app's web views the dice roller shows, and the answer is the first roll to finish. `roll`
  is left out when the user closed the roller first, or the view was already showing something.
- On a socket the app rolls without showing anything — the app's screen belongs to the GM, and a
  player's roll must not interrupt it — and the roll appears in the log under the client's name.

With `rolls`, the client threw its own dice — 3D dice in its page, physical dice read off a table —
and the app only checks them and computes the result:

```json
→ { "name": "rollDice", "requestId": "r14", "data": { "formula": "2d20kh1 + 1d6", "label": "Longsword", "type": "attack", "rolls": [[4, 17], [3]] } }
← { "name": "diceRolled", "responseId": "r14", "data": { "roll": { "name": "Longsword", "type": "attack", "formula": "2d20kh1 + 1d6", "result": 20, "clientThrown": true,
    "dice": [{ "formula": "2d20kh1", "faces": 20, "result": 17, "rolls": [{ "value": 4, "dropped": true }, { "value": 17 }] },
             { "formula": "1d6", "faces": 6, "result": 3, "rolls": [{ "value": 3 }] }] } } }
```

`rolls` has one list of faces per dice term, in the formula's order, each holding every die
thrown for the term in the order thrown. A term's own dice come first; dice its modifiers add — an
explosion (`!`), a reroll (`r`) — are taken from the rest, so a client that throws exploding dice
sends the extra dice too. The total is always the app's, computed from the faces with the formula's
modifiers and arithmetic, never taken from the client. Faces that don't fit — a list per term
missing or extra, a face the die doesn't have, too few or too many dice — are refused with
`invalidRequest` saying which. The roll is logged marked as thrown by the client, and the answer
carries `clientThrown: true`.

**The answer.** A roll carries its dice as `dice`, one group per dice term in the formula's order:
`{ formula, label?, faces, result, rolls }`, with every die thrown in `rolls` as `{ value }` and
`dropped: true` on one that doesn't count — kept out by `kh` or `kl`, rerolled, or a failure.
`label` is the term's [label](/reference/dice-expressions/#labelled-terms), `Hope` for
`1d12[Hope]`, and `formula` the term without it. `detail` is the same dice as text, for people;
don't read values out of it.

When the game system reads an outcome from the labelled dice ([`dice.outcomes`](/system-development/config/#dice)),
the roll carries it as `outcome: { id, label, color? }` — Daggerheart's
`{ "id": "hope", "label": "With Hope", "color": "#e8b931" }`. Branch on `id`; `label` is localized
text to show. A roll the system reads no outcome from has none.

Every client gets the logged roll as `messageCreated` too, the roller included, with `content`
holding the roll and its `dice` — so a client with 3D dice can replay another client's throw to the
same faces. A private roll is answered but not logged.

### Roll menus

`listRollOptions` asks what a roll link's menu offers — the menu `ep-ui.js` draws on a right-click
or a long press:

```json
→ { "name": "listRollOptions", "requestId": "r15", "data": { "formula": "1d12[Hope] + 1d12[Fear] + 2", "label": "Agility" } }
← { "name": "rollOptionsListed", "responseId": "r15", "data": { "options": [
    { "id": "roll", "label": "Roll", "formula": "1d12[Hope] + 1d12[Fear] + 2" },
    { "id": "advantage", "label": "Advantage", "formula": "1d12[Hope] + 1d12[Fear] + 2 + 1d6[Advantage]" },
    { "id": "private", "label": "Roll Privately", "formula": "1d12[Hope] + 1d12[Fear] + 2", "mode": "private", "group": "gm" },
    { "id": "customize", "label": "Customize…", "formula": "1d12[Hope] + 1d12[Fear] + 2", "customize": true, "group": "gm" } ] } }
```

The plain roll comes first, with the formula as sent, then the system's
[`dice.options`](/system-development/config/#dice) that apply to the roll, each with the formula it
rolls. In the app's own web views the GM's items come last, `group: "gm"`: the plain roll in the
other roll mode, with that `mode`, and *Customize…*, `customize: true`, which opens the advanced
dice roller with the formula. A socket's rolls are always public and it has no roller, so it gets
none. A formula that can't be rolled is refused with `invalidRequest`.

Choosing an item is a `rollDice` with its `formula`, and its `mode` or `customize` when it has one:
the options change only what is rolled.

**From the chat.** A `/roll` command (or `/r`) posted with `createMessage` is still rolled and
logged, and a request is answered with the logged message:

```json
→ { "name": "createMessage", "requestId": "r12", "data": { "type": "command", "content": "/roll 1d20 [Awareness]", "creature": "Brin" } }
← { "name": "messageCreated", "responseId": "r12", "data": { "id": "…", "type": "roll", "creature": "Brin", "created": "…",
    "content": { "name": "Awareness", "formula": "1d20", "result": 14, "detail": "(14)", "dice": [{ "…": "…" }] } } }
```

The text in brackets names the roll, optionally with a type after a colon — `[Longsword: attack]`;
the name can be left out, `[: attack]`. A command the app can't read is still logged, as a `chat`
message saying so (`"Invalid expression"`, `"Invalid command"`), and that message is the answer, so
check `type` before reading a result. This is for chat; a sheet rolls with `rollDice`.

### In the app's web views

A page in the app speaks the same protocol without a socket: the events are the same, and only how
they travel differs. It sends each event as JSON text to the `API` message handler, and gets every
answer back as an `encounterplus:message` event on its `window`, with the app's event as `detail`:

```js
window.addEventListener('encounterplus:message', (event) => {
  const { name, responseId, data } = event.detail
})
window.webkit.messageHandlers.API.postMessage(JSON.stringify({ name: 'subscribeEntity', requestId: 'r1', data: { id } }))
```

Events arrive in order, as on a socket. The app takes every event marked *both* in
[Events a client can send](#events-a-client-can-send) — entity subscriptions, `queryEntities`,
`pickEntity`, `rollDice`, `createMessage` and `updateCombatant` — and handles each exactly as it
does for a socket; the difference is that a web view has someone at the app, so `pickEntity` shows
the library list and `rollDice` shows the dice roller. Map and client events are answered with
`unsupportedEvent`, and the page gets no broadcasts: it isn't a connected game client. Its rolls
and messages are the GM's in the log.

A plain link to a content address — `<a href="/item/axe">` — opens the entry's card over the view
in the app; in a browser it is an ordinary link to the rendered entry.

### Dragging

Movement events carry a `state`, because a drag is a stream of messages rather than one:

| State | Meaning |
| --- | --- |
| `start` | The drag began |
| `control` | The position is updating continuously |
| `end` | The drag finished; commit the position |
| `block` | The host refused the move; return the object to where it was |
| `cancel` | The sender abandoned the drag |

A client sending a drag should expect `block` and be ready to snap back.

## Known gaps

- No authentication, and no per-client permissions: every client can read and change every
  entity. Both are planned, for the REST API and the WebSocket alike.
- No `DELETE` over HTTP — content can be created and changed, but not removed.
- Nothing creates or deletes an entity or a combatant. `createEntity`, `createCombatant`,
  `deleteEntity` and `deleteCombatant` are accepted and parsed by the WebSocket, but no handler
  acts on them yet.
- CORS advertises only `GET, OPTIONS`, so cross-origin writes from a browser fail preflight.
- `getAttribute` and `setAttribute` are deprecated and will be removed.
