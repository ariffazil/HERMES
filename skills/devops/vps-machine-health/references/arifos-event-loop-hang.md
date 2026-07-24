# arifOS Event-Loop Hang Diagnosis

When arifOS is `active (running)` per systemd but `/health` endpoint times out.

## The Pattern

```
curl --max-time 5 http://localhost:8088/health
→ empty response (exit 0) or timeout

curl -v http://localhost:8088/health
→ TCP connected (127.0.0.1:8088)
→ GET /health HTTP/1.1 sent
→ 0 bytes received
→ Operation timed out after N ms
```

The socket accepts connections but the async event loop never reads from it.

## Differential: OOM vs Event-Loop Hang

| Signal | OOM (memory cap) | Event-Loop Hang |
|--------|------------------|-----------------|
| systemd status | `deactivating (stop-sigterm)` | `active (running)` |
| Memory | At or near 1.5GB cap, swapping | Normal (200-400MB) |
| TCP socket | Closed (port not listening) | Open, accepts, never reads |
| Fix | Auto-restarts (systemd kills it) | Manual `systemctl restart` required |

## Diagnosis Steps

```bash
# 1. Quick check
curl -sf --max-time 5 http://localhost:8088/health

# 2. Confirm alive
systemctl status arifos --no-pager | grep Active

# 3. Check memory
systemctl status arifos --no-pager | grep Memory

# 4. Visual TCP confirmation
curl -v --max-time 5 http://localhost:8088/health 2>&1
# Look for: "Connected to localhost" then "0 bytes received"
```

## Fix

```bash
systemctl restart arifos
sleep 12
curl -sf http://localhost:8088/health  # expect {"status":"healthy"}
```

arifOS takes ~10-12s to initialize (ATLAS333 wrappers). Don't probe before 10s.

## Proven

- 2026-07-19 09:23 UTC — event-loop hang, memory normal at 289MB
- Multiple earlier instances: "8 crashes in 8d" same signature
