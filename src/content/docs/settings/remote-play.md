---
title: Remote Play Settings
description: The built-in web server, the web client, and what connected players are allowed to interact with.
---

**Settings → Remote Play.**

The whole section requires a **Premium subscription**; without it these rows are not shown. For
setting up a remote session end to end, see the [Remote Play guide](/guides/remote-play/) and the
[Web Client FAQ](/guides/web-client-faq/).

## Web Server

The row shows *Enabled* or *Disabled*; tapping it opens the web server screen.

### Enabled

Starts and stops the built-in server. Off by default.

While it is running, the screen gains the access sections described below.

### Local Access

The address to hand to players on the same network. Tapping it opens the full address, ready to be
shared.

### Public Access

The address to hand to players over the internet, plus the status of **UPnP Port Forwarding**.

The address is looked up when the screen opens, so it may take a moment to appear; the row stays
disabled until it does.

:::note
You probably need to enable port forwarding or UPnP on your router to make this work.
:::

### Network Interfaces

Lists the network interfaces the device has, so you can tell which address corresponds to which
connection when a device is on more than one network.

## Server Settings

Reached from the web server screen. **A server restart is required** for changes here to take
effect — switch **Enabled** off and on again.

### Port

The port the server listens on. **8080** by default.

Change it only if something else on the device already uses that port, or your network requires it.
The port is part of the address your players connect to.

### IPv6

Serves over IPv6 as well as IPv4. Off by default.

### UPnP Port Forwarding

Asks the router to open the port automatically. On by default.

It works only if your router supports UPnP and has it enabled. When it does not, the port must be
forwarded by hand — the Public Access section shows the current status.

## Web Client

The row shows the installed client version, or *None*. Tapping it opens the client manager, where
you can install the web client, update it when a new release is available, browse other releases, or
delete the installed copy.

The web client is the page your players open in their browser, so a copy must be installed for
remote play to work.

## Interactions

What connected players are allowed to move.

| Option | Effect |
| --- | --- |
| **All** | No restrictions, be careful! |
| **Token** | Players can move tokens associated in the web client settings. |
| **None** | No interactions. |

*Token* is the usual choice: each player moves the token they are assigned and nothing else.
