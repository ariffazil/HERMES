# Langfuse Zero-Trace Forensic — The "White Box Isn't Working" Diagnosis

*Reusable pattern for debugging any observability pipeline that is configured, running, and healthy — but producing zero traces.*

## The Trap

A backend can be in all of these states simultaneously:

| State | How to check | Langfuse self-host example |
|-------|-------------|---------------------------|
| **Configured** | `grep LANGFUSE vault.env` | ✅ `LANGFUSE_BASE_URL`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` all set |
| **Running** | `systemctl is-active <unit>` / Docker status | ✅ Container `langfuse-web` up, v3.224.1 |
| **Healthy** | `curl /api/public/health` | ✅ `{"status":"OK"}` |
| **Producing traces** | `curl /api/public/traces \| jq '.data \| length'` | ❌ **0 traces** |
| **Auth valid** | `curl -u pk:sk /api/public/traces` | ❌ Silently 401'd? No — auth passed but no data |

## Root Cause Categories

### 1. Silent backend failure (Langfuse self-host case)

The `_get_langfuse()` REST emitter in `telemetry.py`:

```python
with httpx.Client(timeout=5.0) as client:
    client.post(
        f"{base_url}/api/public/ingestion",
        json=payload,
        auth=(public_key, secret_key),
    )
# except Exception: pass  ← SILENT FAILURE
```

Every failure is swallowed by `except Exception: pass` (line 94). No log, no metric, no retry. This is by design — the telemetry shim must never block the kernel tool path. But it makes debugging nearly impossible.

**Diagnostic:** Add a debug log or test the REST call directly:
```python
import httpx
public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
secret_key = os.getenv("LANGFUSE_SECRET_KEY")
base_url = os.getenv("LANGFUSE_BASE_URL")
r = httpx.post(
    f"{base_url}/api/public/ingestion",
    json={"batch": [{"id": "test", "type": "trace-create", "body": {"name": "test"}}]},
    auth=(public_key, secret_key),
)
print(r.status_code, r.text)
```

### 2. OTEL_SDK_DISABLED (Langfuse v4 SDK path)

Langfuse v4 Python SDK uses OpenTelemetry (OTLP) export. The `OTEL_SDK_DISABLED` env var suppresses all OTLP traces. If the SDK is configured to use OTLP (modern path), it produces zero output even when the REST credentials are valid.

**Check:** `echo $OTEL_SDK_DISABLED` or `grep OTEL_SDK vault.env`

**Fix:** Either unset `OTEL_SDK_DISABLED`, or use the REST ingestion API directly (as `_get_langfuse()` does).

### 3. Backend not selected

The `_get_langfuse()` function returns `None` early if `OBSERVABILITY_BACKEND == "arifos"`:

```python
if _OBSERVABILITY_BACKEND == "arifos":
    return None
```

If the backend is set to `"dual"`, BOTH Langfuse AND Kabarkan try to initialize. But if set to `"arifos"` only, Langfuse is entirely skipped — even with valid keys and a running server.

**Check:** `echo $OBSERVABILITY_BACKEND`

### 4. Key mismatch (cloud vs self-host)

The Langfuse REST API requires `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`. These are DIFFERENT between cloud and self-host instances. If you migrated from cloud to self-host and kept the old keys, REST calls to `localhost:4000` will 401 silently.

**Fix:** Generate new API keys from the self-host admin UI at `http://localhost:4000/auth` (default: admin/langfuse)

## The General Pattern

When an observability pipeline shows **healthy but zero data**:

1. **Check the data store directly** — not the service health endpoint
   - Postgres: `SELECT count(*) FROM ...`
   - Langfuse: `GET /api/public/traces`
   - Kabarkan: `SELECT count(*) FROM observability.observations`
   - NATS: `nats stream info` (message count)

2. **Trace the full data path** — from source to sink
   - Source: Is `trace_tool_call()` being called? (Add a temporary `logger.info` or check file timestamps)
   - Transport: Is NATS receiving messages? (`nats stream info`)
   - Consumer: Is the worker reading them? (`journalctl`)
   - Storage: Are they being written? (`SELECT count(*)` before and after)

3. **Check every component's actual output**, not its status
   - `systemctl is-active` tells you the process is running
   - `journalctl` tells you what it's actually doing
   - The data store tells you what made it through

4. **Beware of fire-and-forget**: Any `except Exception: pass` in the pipeline silences the failure. Add temporary debug logging to isolate where data stops flowing.

## Verification Commands

```bash
# Langfuse self-host — check actual traces
curl -s http://localhost:4000/api/public/traces | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'Traces: {len(d.get(\"data\", []))}')
for t in d.get('data', [])[:3]:
    print(f'  {t.get(\"name\",\"?\")} — {t.get(\"sessionId\",\"no-session\")}')
" 2>/dev/null

# Kabarkan — check actual observations
PGPASSWORD="ArifPostgres2026!" psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -c "SELECT count(*) FROM observability.observations;"

# NATS JetStream message count
nats stream info kabarkan-ingest 2>/dev/null | grep -E "Messages|Last Sequence"

# Worker journal for silent failures
journalctl -u kabarkan-worker --no-pager -n 20 | grep -E "WARNING|ERROR|Nak|failed"
```

## 2026-07-24 Case Summary

| Backend | Health endpoint | Actual traces | Root cause |
|---------|----------------|---------------|------------|
| Langfuse Cloud | ✅ OK | 50,381 (quota exhausted, historical) | N/A — was working until quota hit |
| Langfuse self-host | ✅ OK | **0** | REST emitter `except Exception: pass`; no auth failure surfaced |
| Kabarkan PG local | ✅ OK | **240+** | Sovereign path — working |
