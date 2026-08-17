---
title: Remote Play
description: Running a game for players who are not in the room — the built-in web server, the browser web client, and how to get players connected locally or over the internet.
---

Encounter+ can serve the game to your players' browsers. The device running the app starts a small
web server, your players open a page in any modern browser, and they see the map, the initiative
order and the shared log — and, if you allow it, move their own tokens.

There is nothing for players to install and nothing to sign up for. They do not need Encounter+, an
Apple device or an account: a browser and a link is all it takes.

:::note
Remote play is part of the **Premium subscription**. Without it the Remote Play section is not shown.
See [Purchases](/settings/purchases/).
:::

:::tip
For what every individual row on these screens does, see
[Remote Play Settings](/settings/remote-play/).
:::

## How it works

Three pieces have to line up:

| Piece | Where it lives |
| --- | --- |
| **The web server** | Built into the app, off by default |
| **The web client** | A copy of the player page, installed into the app and served by that server |
| **The address** | An `http://<ip>:<port>/client/` URL your players open |

The important part is that **everything is served by your own device**. Older versions of Encounter+
pointed players at a hosted page at `client.encounter.plus` with a `?remoteHost=` parameter. That is
gone — the app now serves the client itself, so the address you hand out is your device's address
and nothing else is involved.

## Setting up

### 1. Install the web client

**Settings → Remote Play → Web Client.**

The client is versioned separately from the app and downloaded on demand, so the row reads *None*
until you install it. Open it and pick the release at the top — that is the newest one. When an
update appears later, the same screen offers it under **Update Available**.

This is the one step that needs an internet connection. Do it before the session, not during it.

### 2. Start the server

**Settings → Remote Play → Web Server → Enabled.**

While the server runs, the screen grows a **Local Access** and a **Public Access** section, and the
device is kept awake so the game does not drop out from under your players.

### 3. Share the address

Open **Local Access** and you get the IP address, the server URL, the **client URL** — the one your
players want — and a QR code. Tap the QR code to share the link through Messages, Discord, mail, or
whatever your table uses.

The client URL looks like this:

```
http://192.168.1.42:8080/client/
```

That address only works for people on the same network as you. For players elsewhere, see
[Playing over the internet](#playing-over-the-internet).

### 4. Have players join

Each player opens the link, sets their **name** and **color** in the client's own settings, and — if
you have set interactions to *Token* — picks the token they control. From then on their moves show
up on your map, and yours on theirs.

## What players see

The web client mirrors the **player screen**, the same view Encounter+ sends to an external display:
the map you have shared, the initiative order, and whatever overlay or handout you are showing. Your
notes, the DM layer and hidden tokens stay on your device.

- The map shown is the one you shared to the player screen, and line of sight follows
  [Shared Party Vision](/settings/external-screen/#shared-party-vision).
- Markers placed on the DM layer are not sent. Pen and highlighter drawings are, whichever layer
  they were made on.
- The log is shared both ways: players can chat and roll dice with `/roll 2d6+3` (or `/r`), and
  their rolls appear on your device.

### What players may touch

**Settings → Remote Play → Interactions** decides that:

| Option | Effect |
| --- | --- |
| **All** | Anyone can move anything |
| **Token** | Each player moves only the token they picked in the client |
| **None** | View only |

*Token* is the usual choice. Note that tokens can be moved through walls unless the map has
restricted movement enabled.

## Playing over the internet

A local address is unreachable from outside your home network, so the connection has to be let
through your router. The app tries to arrange that itself.

1. Open **Settings → Remote Play → Web Server → Public Access**. The address is looked up when the
   screen opens, so give it a moment to appear.
2. Check **UPnP Port Forwarding**. When it reports success, the router has opened the port for you
   and the public client URL is ready to hand out.
3. If it did not, forward the port by hand on your router — the default is **8080**, and it must
   point at the local IP address shown under Local Access. [portforward.com](https://portforward.com)
   has instructions for most routers, otherwise consult your router's manual.

Two things are worth knowing before you troubleshoot for an hour:

- **Some connections cannot be port-forwarded at all.** If your provider puts you behind carrier-grade
  NAT — common on mobile and some cable connections — no amount of router configuration will help,
  because the address the world sees is not yours. Enabling **IPv6** in
  [Server Settings](/settings/remote-play/#ipv6) sometimes works around this if every player also
  has IPv6.
- **The address can change.** Most home connections get a dynamic public address, so the public URL
  from last week's session may not be this week's. Re-check it each time.

## Troubleshooting

### The link does not open at all

Check, in this order:

1. The server is still **Enabled** — it stops when you switch it off, and nothing else turns it on.
2. A web client version is installed. With none installed there is a server but no page to serve.
3. Players are using the **client URL** ending in `/client/`, not the bare server URL.
4. For local play, players are on the same Wi-Fi — a phone that fell back to cellular is off the
   network.

### The browser turns the address into `https://`

The server speaks plain HTTP, so a browser that upgrades the address to `https` will fail to
connect. Have the player type the `http://` address in full, and if the browser still rewrites it,
try a private/incognito window or clear the site data for that address.

### It says it is disconnected, or players drop mid-session

The server restarts when the app has been in the background for more than a few seconds, and clients
reconnect after that. Leaving Encounter+ in the foreground on the DM device keeps the session
stable; on iPad, a split-screen app running beside it is still foreground.

If a client stays disconnected, switch the web server off and on again and have the player reload the
page.

### A change I made in settings has no effect

Everything under **Server Settings** — port, IPv6, UPnP — is read when the server starts. Toggle
**Enabled** off and on again to apply it, then have players reconnect.

### Tokens are missing or stale

Move the token on your device to force a refresh. If that does not do it, restart the server and have
the players reload.

### Which browsers work?

Any current browser. Safari and Chrome get the most testing; Firefox and Edge are fine. On phones,
landscape gives players a usable amount of map.

## Known limitations

- There is no way to kick a connected player, and no per-game password.
- Tokens can pass through walls unless restricted movement is enabled on the map.
- Markers on the DM layer are not visible to players.

## Still stuck?

Ask on our [Discord](https://discord.gg/psWk84h) or on
[r/EncounterPlus](https://www.reddit.com/r/EncounterPlus/).
