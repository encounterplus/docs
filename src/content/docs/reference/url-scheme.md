---
title: URL Scheme
description: Offer content to Encounter+ for import — from a link, or from another device on the network.
---

Encounter+ registers the `encounterplus://` URL scheme. A link using it opens the app and offers
a piece of content for import, so a website can publish an "Add to Encounter+" button instead of
asking readers to download a file and find it again in the Files app.

A link only ever *offers* content. Encounter+ opens its import screen with the link filled in, and
nothing is downloaded or installed until the reader confirms.

The same request can also be sent over the network to a device already running Encounter+ — see
[Triggering an import from another device](#triggering-an-import-from-another-device).

## The two forms

```
encounterplus://import?manifest=<url>
encounterplus://import?url=<url>
```

Exactly one of `manifest` or `url` must be present, and its value must be a **percent-encoded
`https` URL**. A link carrying both is rejected rather than one being chosen for you.

### `manifest` — published packages

Points at a package manifest: the JSON file describing a system or module, its version, and where
to download it. This is the form to use for anything you publish and intend to keep updating.

```
encounterplus://import?manifest=https%3A%2F%2Fexample.com%2Fpackages%2Fdnd5e.json
```

Encounter+ fetches the manifest first, so the import screen can show the package name, version and
type — and whether the reader already has it installed — before anything large is downloaded.

### `url` — a single file

Points directly at an archive or map file: `.module`, `.campaign`, `.system`, `.eplus`, `.uvtt`,
`.dd2vtt`, and the other [supported types](/reference/file-types/).

```
encounterplus://import?url=https%3A%2F%2Fexample.com%2Fmaps%2Fgoblin-cave.uvtt
```

Use this for one-off content, or when a tool generates a file on the fly and can host it. It needs
no manifest and no infrastructure beyond somewhere to serve the file from.

:::note[Only manifests can be updated]
Content imported through `url` has no package identity or version attached, so Encounter+ can
never tell the reader that a newer release exists. Publish a manifest if you want your users to
receive updates.
:::

## Encoding the inner URL

The URL you are linking to sits inside another URL's query string, so it must be percent-encoded
as a whole before being inserted. This is where most broken links come from.

| Problem | Result |
| --- | --- |
| Inner URL inserted raw | Everything from its first `&` onwards is parsed as parameters of the *outer* link, silently truncating it |
| Inner URL form-encoded, with `+` for spaces | `+` is not decoded as a space; the link is rejected |
| `https` omitted, or `http` used | Rejected — see below |

Encode with your language's standard helper, escaping every reserved character:

```js
const link = `encounterplus://import?manifest=${encodeURIComponent(manifestUrl)}`;
```

```python
from urllib.parse import quote
link = "encounterplus://import?manifest=" + quote(manifest_url, safe="")
```

## Rules

- **`https` only.** `http` and `file` URLs are rejected. A link cannot point the app at a local
  path. (The server endpoint below relaxes this for local addresses only.)
- **One source per link.** Supplying both `manifest` and `url` is an error.
- **Import options are not part of the link.** Where the content lands, what it is named, and how
  it is imported are chosen by the reader on the import screen. Any other parameter in the link —
  including analytics parameters like `utm_source` — is ignored, so adding them is harmless and
  your links keep working as the app gains new options.
- **Nothing installs silently.** The import screen always appears, showing where the content is
  coming from.

### When a link is rejected

Encounter+ explains what is wrong with the link rather than failing silently. If a reader reports
one of these, the link itself needs fixing:

| Message | Cause |
| --- | --- |
| The link must include either a 'manifest' or a 'url' parameter | Neither was supplied |
| The link includes both 'manifest' and 'url'. Use only one | Both were supplied |
| Only https URLs can be imported from a link | `http`, `file`, or a missing scheme |
| The URL in the link is not percent-encoded and may be incomplete | The inner URL contains a space |
| Unknown link action | The part after `encounterplus://` is not `import` |

## Triggering an import from another device

A URL scheme only works on the device it is tapped on — there is no way for one device to open
`encounterplus://` on another. When you need to send content *across* devices, Encounter+'s built-in
web server exposes the same import request over HTTP:

```
POST /api/import
```

The server is the one that serves the web client, so it has to be running: turn it on in
**Settings → Web Server**, where the **Server URL** gives you the address and port to use (`8080`
by default). Anything that can reach that address can send the request — normally that means other
devices on the same network, or the wider internet if you have forwarded the port for remote play.

Parameters can go in the query, exactly as in a link:

```bash
curl -X POST "http://192.168.1.42:8080/api/import?manifest=https%3A%2F%2Fgithub.com%2Fencounterplus%2Fdnd5e%2Freleases%2Flatest%2Fdownload%2Fmanifest.json"
```

…or in a JSON body, which needs no percent-encoding and is usually easier to generate:

```bash
curl -X POST http://192.168.1.42:8080/api/import \
  -H 'Content-Type: application/json' \
  -d '{"manifest": "https://github.com/encounterplus/dnd5e/releases/latest/download/manifest.json"}'
```

Both accept the same two parameters — `manifest` or `url`, exactly one of them — and ignore
everything else, exactly as a link does. Sending a source in the query *and* in the body is
rejected in the same way as sending both `manifest` and `url`.

### Serving over plain http

The one rule that differs from links: a tool serving its own manifest can use `http` instead of
`https`, provided the address is on the local network.

```bash
curl -X POST http://192.168.1.42:8080/api/import \
  -H 'Content-Type: application/json' \
  -d '{"manifest": "http://localhost:8000/manifest.json"}'
```

That covers the usual shapes without a certificate: `localhost` and `127.0.0.1` for a tool on the
same device, an RFC 1918 address (`10.x`, `172.16–31.x`, `192.168.x`), a link-local address, or an
mDNS `.local` name for one elsewhere on the network. IPv6 loopback, unique-local and link-local
addresses work too.

Anything else must be `https`. A public hostname over `http` is refused — including one that
happens to resolve to a private address, since the address is judged from the URL itself and never
looked up:

```json
{"error":"Plain http can only be used for a source on the local network, not 'example.com'."}
```

This relaxation applies **only** to the server endpoint. Links are `https`-only whatever host they
name, because a link is composed somewhere else and travels across the internet to get here.

```json
{"status":"accepted"}
```

`202 Accepted` means the import screen is now on the person's device — not that anything has been
imported. **The request only ever raises the prompt**, exactly as a link does; whoever is holding
the device still has to confirm, and there is no way to make an import happen remotely. A malformed
request returns `400` with the same explanation a bad link would produce:

```json
{"error":"Only https URLs can be imported from a link, not 'http'."}
```

This is the path to use for a companion tool, a map generator running on a laptop, or a script that
should hand a freshly published module to the tablet already running the game.

## Local files don't need a link

If you are writing a map editor or another tool that produces a file on the device itself, use the
system's own file handoff rather than a URL — the share sheet on iOS and iPadOS, drag and drop on
iPad, or the file association on macOS. Encounter+ registers its document types, so it appears as a
destination automatically:

`.module` · `.campaign` · `.system` · `.pack` · `.compendium` · `.eplus` · `.uvtt` · `.dd2vtt`

That path hands over the file directly, with no hosting involved. Use `url` only when the file is
already reachable over `https` — a web-based tool with a temporary upload, for example.

## Testing your links

Custom-scheme links are not always tappable in chat apps and note-taking apps, which strip or
ignore unknown schemes. Safari's address bar always works: paste the link there and confirm the
prompt.

If you run the Encounter+ beta alongside the App Store build, both claim `encounterplus://` and the
system chooses between them unpredictably. The beta additionally registers `encounterplus-beta://`,
which accepts exactly the same links and always opens the beta:

```
encounterplus-beta://import?manifest=https%3A%2F%2Fexample.com%2Fpackages%2Fdnd5e.json
```
