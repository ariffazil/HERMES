# Langfuse Cutover Decision Pattern

## Trigger

Langfuse free tier quota exhausted (50k events/month) or billing upgrade prompt appears.

## Diagnostics

```bash
# Check Langfuse usage
# Email alert to arifbfazil@gmail.com: "Usage Threshold Reached — X events out of Y limit"

# Check current Kabarkan state
PGPASSWORD="$POSTGRES_PASSWORD" psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -c "SELECT count(*) FROM observability.observations;"
nats stream info kabarkan-ingest 2>&1 | grep -E "Messages|Last Message"
systemctl is-active kabarkan-worker
```

## Decision

Kabarkan must be sovereign FIRST (all 3 layers verified) before cutting Langfuse.

### Prerequisites
- [ ] Layer 1 (kernel Postgres direct): observations growing
- [ ] Layer 2 (NATS stream): messages flowing
- [ ] Layer 3 (worker): active, no write failures
- [ ] ATLAS333 hooks: all dispatch paths covered (Airlock + _wrap_handler + _wrap_with_canonical_normalization)
- [ ] VAULT999 seal written: kabarkan-atlas333-hook-sealed

### Decision Matrix

| Kabarkan State | Langfuse State | Action |
|---|---|---|
| ✅ Sovereign | ❌ Quota exhausted | Cut Langfuse. Flip `OBSERVABILITY_BACKEND=arifos` |
| ✅ Sovereign | ✅ Available | Keep dual-write until AAA UI is ready |
| ❌ Not verified | ❌ Quota exhausted | Emergency: budget revert to dual-write, add $29/mo Langfuse Core |
| ❌ Not verified | ✅ Available | Keep Langfuse, fix Kabarkan gaps |

## Cutover Steps

### 1. Flip backend
```python
# In telemetry.py or env:
_OBSERVABILITY_BACKEND = "arifos"  # was "dual"
```

### 2. Remove Langfuse SDK dependency
```bash
cd /root/arifOS
uv remove langfuse  # if listed as dependency
```

### 3. Decommission Langfuse containers
```bash
cd /root/compose
docker compose -p langfuse -f docker-compose.langfuse.yml down
```

### 4. Remove Langfuse env vars from vault.env
Keys to remove:
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_BASE_URL`

### 5. Restart arifOS kernel
```bash
systemctl restart arifos
```

### 6. Verify no Langfuse traffic
```bash
journalctl -u arifos --no-pager -n 50 | grep -i langfuse
# Should show zero Langfuse references
```

## Pitfalls

1. **Don't cut Langfuse before Kabarkan is verified sovereign.** The in-process backend (Layer 1) can work while the standalone worker (Layer 3) silently fails. If you cut Langfuse while only Layer 1 works, you lose observability when the kernel restarts without the in-process backend configured.

2. **Langfuse reset date:** Free tier resets monthly. If cutover happens mid-cycle and fails, you can't fall back to Langfuse until the reset. Always verify Kabarkan is fully sovereign before cutting.

3. **Langfuse Cloud vs self-host:** This pattern assumes Langfuse Cloud (external SaaS). Self-hosted Langfuse has no quota issue but still adds operational cost. Same cutover pattern applies.

## Confirmed Events

| Date | Langfuse Usage | Action | Outcome |
|---|---|---|---|
| 2026-07-24 | 50,381/50k (exhausted) | Kabarkan verified sovereign (240+ obs, all 3 layers). Cutover deferred until AAA UI is built. Grace period active. | Kabarkan = canonical. Langfuse dead unless $29/mo upgrade. |
