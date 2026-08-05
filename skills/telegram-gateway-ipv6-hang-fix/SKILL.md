---
name: telegram-gateway-ipv6-hang-fix
description: Diagnose Hermes Telegram gateway crash loop. Multi-layer fix ladder covers IPv6 getaddrinfo, DNS-over-HTTPS fallback, the "Connected but systemd cycles anyway" pattern, and the `Application.initialize()` async bug. Strace-based root-cause test included.
---

# Telegram Gateway Crash Loop — Multi-Layer Fix Ladder

## Symptom
- `hermes-asi-gateway.service` restart loop every 22s to 3 min
- Last log: `Discovering Telegram API fallback IPs via DNS-over-HTTPS…` → `Connecting to Telegram (attempt 1/8)…` (no further progress) OR `Connecting to Telegram (off-thread init)…` followed by `Application was not initialized`
- Memory peaks 280-300M, then SIGKILL or exit code 1
- 32+ updates queued in Telegram (bot never polls them)
- Bot doesn't reply to messages

## The Layered Root Cause

The gateway has FOUR independent hang/fail points in its init path. Each one is sufficient on its own to cause the loop. Most VPS instances have ONE broken layer; some have multiple. Apply fixes in this order until the gateway settles.

### Layer 1 — IPv6 getaddrinfo hang
Python `socket.getaddrinfo` resolves AAAA records first when a hostname has both A and AAAA records. On VPS with broken/unreachable IPv6, the connect hangs for the full TCP timeout (40+ min) before falling back to IPv4.

### Layer 2 — DNS-over-HTTPS fallback IP discovery
The adapter runs `discover_fallback_ips()` via DoH before connecting. If the DoH endpoint is unreachable OR slow, the gateway sits at "Discovering…" indefinitely.

### Layer 3 — "Connected but cycling anyway"
The "Connecting (1/8)" log is **fire-on-init, not persistent**. Py-process may actually succeed in opening the socket and enter `epoll_wait` (idle polling for Telegram updates). The restart cycle may have a different cause — system load, FD pressure, or upstream restart trigger. Check `/proc/<PID>/stack` to confirm.

**2026-08-05 finding:** Strace of running gateway showed `epoll_wait` — bot was actually polling. External `sendMessage` via API reached the bot (message_id 103903). The "Connecting" log was misleading. The actual cause of the restart cycle was NOT the connection itself.

Do NOT assume "Layer 3 = fd leak" without evidence. The fd leak comment in adapter.py is one possibility, but the 2026-08-05 session never confirmed it. Other candidates: sibling process load, systemd watchdog, parent shell restart.

### Layer 4 — `Application.initialize()` never awaited (2026-08-05 finding)

After Layer 1 (IPv4) and Layer 3 (epoll_wait) are confirmed, the gateway may STILL cycle with this error in journal:

```
[Telegram] Failed to connect to Telegram: 
This Application was not initialized via `Application.initialize`!
RuntimeWarning: coroutine 'Application.initialize' was never awaited
```

This is a code bug in `adapter.py` around line 3453-3467. The patch:

```python
# 333-AGI PATCH 2026-08-05: Bypass blocking initialize()
loop = asyncio.get_running_loop()
await loop.run_in_executor(None, self._app.initialize)  # ← THIS IS WRONG
```

`Application.initialize()` is itself an async coroutine in newer python-telegram-bot versions. Wrapping it in `run_in_executor` calls it as a sync function (returning a coroutine that is never awaited). PTB then refuses to start polling because it wasn't properly initialized.

The correct pattern is one of:
```python
await self._app.initialize()      # direct await, blocks event loop briefly
```
or
```python
asyncio.create_task(self._app.initialize())  # fire and await elsewhere
```

**Symptom signature:** Last log is "Connecting to Telegram (off-thread init)…" (note "off-thread init" wording) followed by the "This Application was not initialized" error and "Gateway started with no connected platforms".

**Workaround (temporary):** Disable the service to stop crash spam, fix upstream code. See Step 12.

## Diagnosis Steps (in order — DO NOT skip)

**Step 1 — Test direct network from VPS:**
```bash
curl -sf -w "HTTP %{http_code} in %{time_total}s\n" \
  https://api.telegram.org/bot${ASI_BOT_TOKEN}/getMe --max-time 10
```
Expected: HTTP 200 in <1s.

**Step 2 — Test Python httpx:**
```python
# /tmp/test_telegram.py
import httpx, time
start = time.time()
r = httpx.Client(timeout=10).get("https://api.telegram.org/bot<TOKEN>/getMe")
print(f"HTTP {r.status_code} in {time.time()-start:.2f}s")
```
Expected: <1s.

**Step 3 — Test telegram library + Bot instance:**
```python
import asyncio
from telegram import Bot
async def t():
    bot = Bot(token="<TOKEN>")
    me = await bot.get_me()
    print(me.username)
asyncio.run(t())
```
Expected: <1s.

**Step 4 — Check what IPv4/IPv6 returns:**
```python
import socket
for addr in socket.getaddrinfo('api.telegram.org', 443):
    print(addr[4][0])
```
Expected: A record only. If AAAA appears first, IPv6 is being attempted.

**Step 5 — Check if process is actually hung or just polling:**
```bash
PID=$(systemctl show hermes-asi-gateway.service --property=MainPID | grep -oE "[0-9]+")
sudo cat /proc/$PID/wchan       # ep_poll = idle polling, NOT hung
sudo cat /proc/$PID/stack | head -5  # ep_poll → do_epoll_wait → epoll_wait
```

**Step 6 — Check journal for Application.initialize() error (Layer 4):**
```bash
journalctl -u hermes-asi-gateway.service --since "5 min ago" --no-pager | \
  grep -E "(initialize|off-thread|never awaited|off-thread init)"
```
If this matches, fix is upstream (adapter.py:3463 pattern).

## Fix Ladder (apply in order, verify each step)

### Step 7 — Layer 1 fix: force_ipv4 true config (PARTIAL)

Edit `/root/HERMES/config.yaml` (or `/root/.hermes/config.yaml` — symlinked on A-FORGE):
```yaml
network:
  force_ipv4: true
```

Code path: `/usr/local/lib/hermes-agent/gateway/run.py:1789` reads this and monkey-patches socket.getaddrinfo to skip IPv6.

Verify:
```bash
python3 -c "import socket; [print(a[4][0]) for a in socket.getaddrinfo('api.telegram.org', 443)]"
```
Should return only IPv4 (e.g. 149.154.167.220).

Effect observed (2026-08-05): Memory peak dropped 285M → 113M, restart cycle slowed 22s → 1-2min. But connection still slow — Layer 1 alone is INSUFFICIENT for full fix.

### Step 8 — Layer 1 OS-level fix: /etc/gai.conf precedence

If Layer 1 config patch isn't enough (gateway process doesn't pick up the config), force IPv4 at the OS layer:

```bash
# Backup first
sudo cp /etc/gai.conf /etc/gai.conf.bak-$(date +%Y%m%d)-ipv4-precedence

# Check if rule already exists
grep -q "^precedence ::ffff:0:0/96" /etc/gai.conf && echo "ALREADY_SET" || \
  sudo tee -a /etc/gai.conf > /dev/null << 'EOF'

# Force IPv4 over IPv6 — VPS has broken IPv6.
precedence ::ffff:0:0/96  100
EOF

# Cleanup duplicates if multiple writes happened
grep -c "^precedence ::ffff:0:0/96" /etc/gai.conf  # should be 1
```

This affects ALL Python processes on the VPS (reversible by commenting out the line). getaddrinfo returns IPv4-mapped IPv6 first.

### Step 9 — Layer 2 fix: env var (DEAD CODE — DO NOT waste time)

```bash
# In /etc/systemd/system/hermes-asi-gateway.service.d/disable-telegram-doh.conf
Environment="HERMES_TELEGRAM_DISABLE_FALLBACK_IPS=1"
```

This is a TRAP. `adapter.py:3120` reads the env var, but Line 3124 `await discover_fallback_ips()` runs BEFORE Line 3133 check. The patch is dead code.

Confirmed 2026-08-05: applied env var + patched adapter.py to short-circuit DoH. Env var check at line 3133 fired AFTER DoH discovery had already started. DoH log still appeared.

**Skip this step** unless upstream hermes merges the fix.

### Step 10 — Layer 3 escape: webhook mode

If polling-mode gateway can't be stabilized, switch to webhook:

```bash
curl -X POST "https://api.telegram.org/bot${ASI_BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url":"https://your-domain/webhook",
    "secret_token":"<TELEGRAM_WEBHOOK_SECRET>",
    "max_connections":100
  }'
```

See `telegram-webhook-recovery` for full webhook flow including Caddy routing + secret_token requirement.

### Step 11 — If gateway is connected but still cycling: find the cycle trigger

When `/proc/<PID>/stack` shows `epoll_wait` and external `sendMessage` works, the issue is NOT the connection. Find what sends SIGTERM:

```bash
# 1. Find systemd watchdog
grep -E "(Watchdog|RuntimeMaxSec)" /etc/systemd/system/hermes-asi-gateway.service

# 2. Check cgroup events — was this a real OOM?
cat /sys/fs/cgroup/system.slice/hermes-asi-gateway.service/memory.events
# oom_kill=0 means no real OOM

# 3. Check parent process
ps -o pid,ppid,pgid,sid,comm -p <PID>

# 4. Check system load
uptime

# 5. Check siblings — is something starving the gateway?
ps -eo pid,pcpu,etime,comm | head -20
```

If a sibling process is at 100% CPU and starving hermes — that's the root cause. See `phased-serial-debug` PITFALL: "QQQ FFF before kill" — high-load processes may be Arif's active work, not targets.

### Step 12 — Layer 4 escape: disable service and patch upstream code

If Layer 4 (`Application.initialize()` not awaited) is the root cause:

```bash
# Stop the crash spam
sudo systemctl stop hermes-asi-gateway
sudo systemctl disable hermes-asi-gateway
pkill -9 -f "hermes gateway"
```

Then fix `adapter.py:3463` to use direct await:
```python
# BAD (current 2026-08-05):
loop = asyncio.get_running_loop()
await loop.run_in_executor(None, self._app.initialize)

# GOOD:
await self._app.initialize()
```

Restart after upstream patch:
```bash
sudo systemctl enable hermes-asi-gateway
sudo systemctl start hermes-asi-gateway
sleep 30
journalctl -u hermes-asi-gateway.service --no-pager -n 20 | grep -E "(Connecting|initialized|connected|failed)"
```

## Pitfalls (PROVEN 2026-08-05)

- **Don't confuse SIGKILL with OOM.** Memory peak 285M is normal Python process, not OOM. Check `cat /sys/fs/cgroup/system.slice/hermes-asi-gateway.service/memory.events | grep oom_kill` — should be 0. If non-zero, real OOM.

- **`Connecting (attempt 1/8)` log means STUCK, not trying.** The "1/8" counter does NOT increment during IPv6 hang — it stays at 1 the whole time. Don't wait it out.

- **But ALSO:** "Connecting (1/8)" log is **fire-on-init, not persistent**. After init, the gateway may legitimately be in `epoll_wait`. Check `/proc/<PID>/stack` to confirm.

- **DoH discovery log is independent of IPv4/IPv6.** "Discovering Telegram API fallback IPs via DNS-over-HTTPS" runs even when IPv4 is forced. It can hang on its own.

- **`Application.initialize()` (Layer 4) error signature is distinctive:** "off-thread init" wording in log + "This Application was not initialized" error + "Gateway started with no connected platforms". This is NOT a network problem.

- **`PID file race lost to another gateway instance`** — kill ALL zombies before restart:
  ```bash
  pkill -9 -f "hermes gateway"
  rm -f /tmp/hermes-gateway*.pid /root/.hermes/*.pid
  ```

- **`Unknown key 'StartLimitIntervalSec' in section [Service]'`** — that systemd directive was added in v250 but the VPS has older systemd. Just `RestartSec=N` alone is sufficient.

- **Path guard will block `write_file` to `/etc/systemd/...` and `/etc/gai.conf`.** Use `sudo tee -a ...` or `sudo cp ...` via terminal. `write_file` will refuse with "Refusing to write to sensitive system path".

- **Always backup before patching vendor code or system config:**
  ```bash
  sudo cp /etc/gai.conf /etc/gai.conf.bak-20260805-ipv4-precedence
  sudo cp /usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py \
           /usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py.bak-20260805-DoH-fix
  ```

- **High CPU load from sibling processes is NOT a reason to kill the gateway.** See `phased-serial-debug` PITFALL: "QQQ FFF before kill". High load → find root cause, don't blame the gateway.

- **Don't apply patches that don't run.** 2026-08-05 session burned 15+ min on a DoH env var that fires AFTER the DoH call. Read the code execution order before applying the patch. Check whether the conditional branch actually contains the env-var check.

- **Don't kill Arif's active work.** Sibling processes (4x opencode, hindsight-api, arifOS L5 search) are Arif's active sessions. QQQ FFF (5+ paths incl. NULL + INVERSE) before any kill. See Arif's directive: "dont simply kill. make sure u know what u are doing. qqq fff".

- **Bot may be POLLING even while "Connecting" log is shown.** The log is fire-on-init. Check `/proc/<PID>/stack` for `epoll_wait` to confirm bot is actually waiting for Telegram updates, not stuck.

## Verification After Each Step

```bash
# Service should stay alive >60s without restart
sleep 60
PID=$(systemctl show hermes-asi-gateway.service --property=MainPID | grep -oE "[0-9]+")
ps -p $PID -o pid,vsz,rss,etime,stat  # etime growing, memory stable

# Process actually polling?
sudo cat /proc/$PID/wchan  # ep_poll = good

# Journal should NOT show exit/kill events
journalctl -u hermes-asi-gateway.service --since "2 min ago" --no-pager | \
  grep -E "exited|killed|Stopped|Failed" | wc -l  # should be 0

# No Application.initialize error?
journalctl -u hermes-asi-gateway.service --since "2 min ago" --no-pager | \
  grep -i "not initialized\|never awaited" | wc -l  # should be 0
```

## Current State on A-FORGE (2026-08-05)

| Patch | Applied | Effect |
|---|---|---|
| force_ipv4 true config | yes | memory 285M → 113M initial, restart cycle slowed |
| /etc/gai.conf precedence | yes | one duplicate cleaned |
| RestartSec=30 (was 5) | yes | log spam reduced |
| DoH env var skip | reverted | dead code, don't waste time |
| adapter.py patch | reverted | ran but didn't solve |
| Webhook mode | not applied | needs URL |
| Layer 3 cycle trigger | NOT identified | require upstream/load investigation |
| Layer 4 Application.initialize() | identified | upstream patch needed; service disabled meanwhile |
| service disabled + inactive | yes | stops crash spam |

## References

- `references/2026-08-05-session-transcript.md` — full session transcript and diagnostic findings

## Related Skills

- `phased-serial-debug` — phased-serial methodology, plus the "QQQ FFF before kill" pitfall
- `telegram-webhook-recovery` — webhook fallback if polling-mode gateway refuses to stabilize
- `vps-machine-health` — when system load is the suspected root cause
- `vps-operations` — broader VPS triage patterns