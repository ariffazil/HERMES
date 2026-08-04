# FED Wire Architecture & Gap Audit — 2026-08-04

## Context

Wawabot (Hermes on azwaos, srv164254, Tailscale 100.64.0.4) was configured to route through `af-forge-fed` provider at `http://100.64.0.2:4000/v1`. End-to-end wire was verified: wawabot Telegram → azwaos Hermes → Tailscale → af-forge:4000 → model (hermes-asi/MiniMax) → reply back.

## Architecture: What Is af-forge:4000?

**Key question**: What process binds `100.64.0.2:4000` on af-forge?

| Hypothesis | Evidence |
|---|---|
| LiteLLM proxy | `/v1/chat/completions` works, `/health` returns status |
| Hermes federation router | `/v1/models` returns model list including `hermes-asi` |
| ArifOS kernel bridge | Tool calls route through constitutional membrane |

**Not yet confirmed**: Whether af-forge:4000 is a pure LiteLLM proxy or a custom Hermes federation router that wraps LiteLLM + adds governance layers. The `hermes-asi` model name suggests it's not a raw LiteLLM passthrough.

## Confirmed Working

- `HEAD /health` returns `200 OK` on af-forge:4000 via Tailscale
- `POST /v1/chat/completions` with model `hermes-asi` returns Malay reply
- Model `hermes-asi` routes to MiniMax-M3 through af-forge

## Gaps Identified (Not All Probed)

### GAP-1: `GET /v1/models` returns empty
```json
{"data": [], "object": "list"}
```
Models exist (we can call them), but the listing endpoint returns nothing. Either model discovery is disabled or models are registered at a different layer.

### GAP-2: FED ecosystem skill missing
The `fed` skill (Rust, Tailscale-native LLM load balancer) was designed but no source code or binary found at:
- `/root/fed/`
- `/root/A-FORGE/fed/`
- No `fed` systemd service or Docker container
- Not in `rustup toolchain list` (no Rust toolchain on VPS)

### GAP-3: Probe failed — Multi-agent consensus (SOUL)
- 5 agents dispatched to probe af-forge:4000
- 3 terminated with UNKNOWN
- 1 in UNKNOWN state
- Only 1 reached the service (returned health data)
- Suggests network path instability or agent timeout issues when routing through A2A mesh

### GAP-4: TLS posture unverified
- af-forge:4000 served over plain HTTP
- Tailscale provides transport encryption (WireGuard), but application-layer TLS not confirmed
- No `mTLS` or bearer token auth observed on probe requests

### GAP-5: No latency tracking on af-forge route
- `fed_report_latency` tool exists but no baseline data for the af-forge:4000 → hermes-asi route
- Need `POST /v1/chat/completions` with `stream=false` to measure TTFB

### GAP-6: Auth posture unknown
- No API key observed on successful requests
- Either: (a) Tailscale IP allowlist only, or (b) auth disabled
- If (b): any Tailscale node can call any model without auth

## Recommended Next Steps

1. `ssh af-forge` → `ss -tlnp | grep 4000` → identify the actual process
2. `systemctl list-units --type=service | grep -i 'litellm\|fed\|hermes'` → find the service
3. `cat /etc/systemd/system/<service>.service` → get the ExecStart command
4. Check if af-forge has its own `~/.hermes/config.yaml` with provider definitions
5. Benchmark: `curl -w '%{time_total}' -o /dev/null -s http://100.64.0.2:4000/v1/chat/completions` with a simple prompt
