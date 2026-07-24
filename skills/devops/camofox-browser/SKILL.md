---
name: camofox-browser
description: "Deploy Camofox anti-detection browser server for Hermes Agent — npm install, port configuration, systemd service, and Hermes integration"
triggers:
  - "Camofox"
  - "camofox"
  - "anti-detection browser"
  - "stealth browser"
  - "CAMOFOX_URL"
  - "camofox-browser"
  - "browser fingerprinting"
---

# Camofox Anti-Detection Browser

Self-hosted Node.js server wrapping Camoufox (Firefox fork with C++ fingerprint spoofing). Exposes a REST API that maps 1:1 to Hermes browser tools. When `CAMOFOX_URL` is set, all browser_* tools route through this instead of the default `agent-browser` CLI.

## Architecture

```
Hermes Agent → CAMOFOX_URL=http://localhost:9377
                ↓
         Camofox Server (Node.js, port 9377)
                ↓
         Camoufox Browser Engine (Firefox fork, ~300MB)
                ↓
         XVFB Virtual Display (:99)
```

## Quick Deploy

```bash
# 1. Clone and install (downloads ~300MB Camoufox + 66MB GeoIP on first run)
git clone https://github.com/jo-inc/camofox-browser.git /root/camofox-browser
cd /root/camofox-browser
npm install

# 2. Start (MUST override default port 8088 — conflicts with arifOS)
CAMOFOX_PORT=9377 node server.js &

# 3. Verify
curl http://localhost:9377/
# → {"ok":true,"enabled":true,"running":true,"engine":"camoufox","browserConnected":true}
```

## Port Conflict

Camofox defaults to port **8088**, which conflicts with arifOS kernel (port 8088). Always override with `CAMOFOX_PORT=9377` (the port Hermes expects by default).

```bash
# Check for port conflicts before starting
ss -tlnp | grep -E "8088|9377"
```

## Systemd Service

For persistence across reboots (`/etc/systemd/system/camofox.service`):

```ini
[Unit]
Description=Camofox Anti-Detection Browser Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/node /root/camofox-browser/server.js
WorkingDirectory=/root/camofox-browser
Environment=CAMOFOX_PORT=9377
Environment=NODE_ENV=production
Restart=on-failure
RestartSec=10
User=root
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now camofox.service
```

## Hermes Integration

Set the env var in `~/.hermes/.env`:

```bash
echo 'CAMOFOX_URL=http://localhost:9377' >> ~/.hermes/.env
```

Hermes auto-detects `CAMOFOX_URL` and routes all `browser_*` tools through Camofox instead of the default browser stack.

## Docker (Alternative)

The Docker image `jo-inc/camofox-browser` is not publicly accessible (pull access denied). Use the npm approach instead.

```bash
# NOT available:
docker pull jo-inc/camofox-browser  # → access denied
```

## Health Check

```bash
# API health
curl -s http://localhost:9377/ | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'engine={d[\"engine\"]}, running={d[\"running\"]}, browserConnected={d[\"browserConnected\"]}')"

# Systemd status
systemctl status camofox.service --no-pager

# Port check
ss -tlnp | grep 9377
```

## Resource Footprint

- **Camoufox binaries:** ~300MB (downloaded once on `npm install`)
- **GeoIP database:** ~66MB
- **npm packages:** ~450 packages
- **Memory:** ~200-500MB at runtime (full Firefox browser engine)
- **Disk:** ~1GB total (node_modules + binaries)

## Pitfalls

- **Default port 8088 conflicts with arifOS.** Always set `CAMOFOX_PORT=9377`.
- **Docker image is private.** Don't try `docker pull jo-inc/camofox-browser` — it fails. Use npm install.
- **First `npm install` downloads ~370MB.** Postinstall script fetches Camoufox binaries + GeoIP. This takes 30-60 seconds.
- **Needs XVFB for headless mode.** The server auto-launches `Xvfb` on display `:99`. If it fails, check `xvfb` is installed.
- **Separate from Hermes browser tools.** Camofox is a replacement backend, not an additional tool. When `CAMOFOX_URL` is set, all `browser_navigate`, `browser_click`, `browser_snapshot`, etc. route through Camofox.
- **The systemd service uses `Type=simple`.** The server stays in the foreground. Don't use `Type=forking`.

## Provenance

- **Born:** 2026-07-24 — from Camofox deployment on arifOS federation VPS. Port 8088 conflict with arifOS kernel, resolved to 9377. Docker image inaccessible, used npm install. Systemd service created for persistence.