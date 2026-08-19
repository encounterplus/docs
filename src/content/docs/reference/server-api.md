---
title: Server API
description: The HTTP and WebSocket API exposed by the Encounter+ built-in web server — endpoints, payloads and live events.
---

:::caution[Experimental — work in progress]
This API exists to serve the built-in web client and the player display. It is **not a stable
public interface**: endpoints, payload shapes and event names change between releases without a
deprecation period, and this page documents only what is currently implemented.

Build against it if you like — but expect to adjust when the app updates, and do not rely on
anything here staying put.
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
your browser loads can call the API of a server it can reach.

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
  "game": { "round": 3, "turn": 1, "started": true, "combatantId": "…", "initiativeId": "…" },
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

Every entity in the collection.

| Query | Default | Returns |
| --- | --- | --- |
| `schema=list` | ✓ | Compact list rows, including the data keys the system's filters need |
| `schema=basic` | | Compact list rows, without the filter data keys |
| `schema=model` | | The full stored model of each entity |
| `schema=view` | | The rendering context — computed and formatted values, as the app displays them |

Any other value returns `400`.

```bash
curl 'http://192.168.1.42:8080/api/monsters?schema=basic'
```

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
| `/others/` | Temporary images generated during play |

### `GET /{reference}`

Any other single-segment path is treated as an entity reference URL and answered with that entity
rendered as HTML — the same markup the app shows in a detail view, using the system's view
templates and theme. Invalid references return `400`, unknown ones `404`.

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
| `requestId` | Set by a client on a request it wants an answer to |
| `responseId` | Echoes the `requestId` of the request being answered |

Names ending in `Updated`, `Created` or `Deleted` are the app broadcasting a change. Names in the
imperative — `createMessage`, `updateDoor` — are a client asking for one. The full envelope,
including the payload type for each name, is documented under
[WSEvent](/reference/schema/wsevent/).

On connect, the app sends an `app` event carrying its `version` and `build`.

### Events a client can send

Anything not listed here is ignored, even when the app knows the name.

| Event | Payload | Effect |
| --- | --- | --- |
| `clientUpdated` | `Client` | Registers the client's name, color, device and screen size. Send this first — a client identifying itself with a non-`normal` `runMode` becomes a player display |
| `mapViewportUpdated` | `Frame` | Reports where this client is looking, so the app can show its viewport |
| `tokenMoved` | `Movement` | Drags a token. Refused when remote interaction is off |
| `updateDoor` | `Door` | Opens or closes a door, recomputing line of sight. Refused when remote interaction is off |
| `pointerUpdated` | `Pointer` | Moves this client's shared pointer. Refused when remote interaction is off |
| `updateToken` | partial object | Merges changes into a token by `id` |
| `updateEntity` | partial object | Merges changes into an entity by `id` |
| `updateCombatant` | partial object | Merges changes into a combatant by `id` |
| `createMessage` | `Message` | Posts to the shared log, rolling any dice in it |
| `getAttribute` | `Attribute` | Reads an entity's attributes; answered on `requestId` |
| `setAttribute` | `Attribute` | Writes an entity's attributes |
| `trackedObjectCreated` / `trackedObjectUpdated` / `trackedObjectDeleted` / `trackedObjectsUpdated` | `TrackedObject` | Reports physical objects tracked on a table-top display |

:::note[Remote interaction gates the interactive events]
`tokenMoved`, `updateDoor` and `pointerUpdated` are dropped when the host has remote interaction
turned off. The direct `updateToken` / `updateEntity` / `updateCombatant` merges are **not** gated
— they apply regardless.
:::

`getAttribute` currently echoes the request back rather than resolving attribute values; it is
unfinished.

### Events the app broadcasts

| Group | Events |
| --- | --- |
| Game state | `gameUpdated`, `combatantsUpdated`, `systemPaused` |
| Player screen | `screenUpdated`, `interactionUpdated`, `reload` |
| Map | `mapUpdated`, `mapLoaded`, `mapFrameUpdated`, `mapFitScreen`, `mapFocus`, `mapVideoControlUpdated` |
| Map objects | `tokenUpdated`, `tokensUpdated`, `markerUpdated`, `markersUpdated`, `tileUpdated`, `tilesUpdated`, `lightUpdated`, `lightsUpdated`, `areaEffectUpdated`, `areaEffectsUpdated`, `measurementUpdated`, `measurementsUpdated` |
| Movement | `mapMoved`, `tokenMoved`, `markerMoved`, `tileMoved`, `areaEffectMoved`, `pointerMoved` |
| Overlays | `fogUpdated`, `drawingsUpdated`, `lineOfSightUpdated`, `pointerUpdated` |
| Content | `entityCreated`, `entityUpdated`, `entityDeleted`, `combatantCreated`, `combatantUpdated`, `combatantDeleted` |
| Log | `messageCreated`, `messagesUpdated`, `messageDeleted` |
| Clients | `clientConnected`, `clientDisconnected`, `clientUpdated`, `app` |
| Object tracking | `trackedObjectCreated`, `trackedObjectUpdated`, `trackedObjectDeleted`, `trackedObjectsUpdated` |

Broadcasts go to every connected client, including the one whose action caused them.

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

- No authentication, and no per-client permissions.
- No `DELETE` over HTTP — content can be created and changed, but not removed.
- Nothing creates or deletes an entity or a combatant. `createEntity`, `createCombatant`,
  `deleteEntity` and `deleteCombatant` are accepted and parsed by the WebSocket, but no handler
  acts on them yet.
- No pagination on collection listings; `GET /api/{collection}` returns everything.
- CORS advertises only `GET, OPTIONS`, so cross-origin writes from a browser fail preflight.
- `getAttribute` does not yet resolve values.
