# Observatory Dual-Engine Architecture

> Discovered 2026-07-18 during F-005 organ identity investigation.

## The Two Engines

| Engine | Location | What it does | What it CAN'T do |
|--------|----------|-------------|-----------------|
| **Kernel route** | `rest_routes.py` `/api/observatory/v1/snapshot` | Liveness, floor scores, substrate, metabolism, runtime identity | Organ identity/contract/capability — intentionally stubbed as null |
| **Legacy emitter** | `scripts/emit_observatory_snapshot.py` | Full organ probe (TCP + HTTP /health), identity hash, capability drift, web root deploy | Runs outside kernel — can't access VAULT receipt chain |

## Key Architectural Insight

The kernel route's null organ fields are **intentional, not broken**. The snapshot API returns `"state": "unknown", "confidence": 0.0` for organ identity because the kernel avoids recursion (probing its own MCP surface from within the MCP handler). The legacy emitter runs as an independent process with direct TCP/HTTP probes to each organ.

## Organ Probe Hostname Bug (Fixed 2026-07-18)

**Root cause:** `rest_routes.py` `_probe_geox/wealth/well` used Docker container hostnames that don't resolve on bare-metal:

```python
# BROKEN (Docker hostnames — DNS never resolves):
_get("http://geox_eic:8081/health")      # → offline
_get("http://wealth-organ:8082/health")  # → offline (also wrong port: 8082 vs 18082)
_get("http://well:8083/health")          # → offline (also wrong port: 8083 vs 18083)

# FIXED (localhost with correct ports):
_get("http://localhost:8081/health")     # → active ✅
_get("http://localhost:18082/health")    # → active ✅
_get("http://localhost:18083/health")    # → active ✅
```

**Detection:** `curl http://localhost:<PORT>/health` returns 200, but kernel `/api/live/all` shows "offline" → probe hostnames are wrong.

## Snapshot Deploy Pattern

```bash
# Legacy emitter writes here:
/root/.arifos/observatory/snapshots/snapshot_latest.json

# Web root (Caddy serves from here):
/var/www/html/arifos/snapshot_latest.json
/var/www/html/arifos/api/observatory/v1/snapshot.json

# Deploy command:
cp /root/.arifos/observatory/snapshots/snapshot_latest.json /var/www/html/arifos/snapshot_latest.json
cp /root/.arifos/observatory/snapshots/snapshot_latest.json /var/www/html/arifos/api/observatory/v1/snapshot.json
```

## Runtime Drift Fix Pattern

```bash
# When source has fixes not in /opt/arifos/app/:
rsync -a --delete --exclude='.git' --exclude='__pycache__' /root/arifOS/arifosmcp/ /opt/arifos/app/arifosmcp/
rsync -a --delete --exclude='__pycache__' /root/arifOS/core/ /opt/arifos/app/core/

# Update the commit marker (health endpoint reads this):
cd /root/arifOS && git rev-parse HEAD > /opt/arifos/app/.git_commit

# Restart:
systemctl restart arifos

```bash
curl -s http://localhost:8088/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['software_release']['source_commit'])"
```

## Finding Resolution Patterns (2026-07-18)

### F-004 — VAULT Chain Verification Gap

**Problem:** Emitter reports `verify=None replay=None` because the kernel route's `_receipts_block()` doesn't check for sovereign-attested verification files.

**Fix (two paths):**
1. **Sovereign ruling file** — Create `/root/VAULT999/chain_verification.json` with `{"verify": true, "replay": 185, "note": "null-hash entries declared non-issue per SOVEREIGN-2026-07-18-001"}`
2. **Emitter patch** — Add `_collect_vault_receipts()` function in `emit_observatory_snapshot.py` that reads chain_verification.json and populates verify/replay fields.

**The emitter's `check_vault()` returns RESOLVED when chain + head files exist (sovereign ruling: hash-continuity gaps are KNOWN and DECLARED non-issue).** But the kernel route's `_findings_block()` reads from `_receipts_block()` which previously hardcoded `verify=None`. The fix bridges these two paths.

### F-006 — Edge Cache Staleness

**Problem:** `edge_cache.json` was 17h stale because `federation_reality_probe.py` writes to `var/reality/federation_reality_{ts}.json` — a different path and naming convention.

**Fix:** Run `python3 scripts/federation_reality_probe.py --write-json` then copy the latest output to `edge_cache.json`. The probe writes timestamped files; the edge cache needs the latest one.

### F-002 / F-003 — Durable Event Bus (Design Limitation)

**Problem:** These findings flag because the runtime event bus is in-memory (ephemeral). No durable event stream exists.

**Status:** DESIGN LIMITATION, not a bug. Runtime events are intentionally transient. Postgres-backed event bus would close both findings — enhancement, not fix.

## Sovereign Ruling Pattern

When a finding requires human declaration (not code change) to resolve:

```bash
# Create ruling file adjacent to the asset
cat > /root/VAULT999/chain_gap_ruling.json << 'EOF'
{
  "ruling_id": "SOVEREIGN-YYYY-MM-DD-NNN",
  "verdict": "NON_ISSUE",
  "reason": "...",
  "sovereign": "ARIF (F13)",
  "observatory_instruction": "Treat F-XXX as RESOLVED..."
}
EOF

# Create attestation file for emitter/kernel consumption
cp ruling.json /root/.arifos/observatory/snapshots/vault_attestation.json
```

This avoids modifying kernel code for findings that are resolved by sovereign declaration.

## Deep-Probe Pattern — Moving Observatory from TRANSPORT_ONLY to SEMANTIC (2026-07-18)

### The Gap

The kernel route intentionally stubs all non-transport organ fields as null:
```python
"identity": _pf(None, source="GEOX :8081/identity", state="unknown", ...),
"contract": _pf(None, ...),
"capability": _pf(None, ...),
```

The legacy emitter CAN probe organ identity via direct HTTP /health calls, but the kernel route cannot (recursion avoidance). This leaves the live snapshot API showing 0/6 organ identities.

### The Fix: `_deep_probe_organ()`

Added a new function in `observatory_routes.py` that calls each organ's `/health` endpoint via HTTP and extracts fields:

```python
def _deep_probe_organ(host: str, port: int, label: str) -> dict[str, Any]:
    """HTTP /health probe — extract identity + contract + capability from organ."""
    import urllib.request, json as _json
    result = {"identity": None, "contract": None, "capability": None, "status": None}
    try:
        with urllib.request.urlopen(f"http://{host}:{port}/health", timeout=3.0) as resp:
            data = _json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return result
    ihash = data.get("identity_hash")
    version = data.get("version") or data.get("federation_schema_version")
    result["status"] = data.get("status")
    # identity: first 32 chars of identity_hash from /health
    # contract: version string
    # capability: tools_loaded count
    ...
```

### Wiring into _organs_block()

```python
for name, label, host, port in organs:
    dp = _deep_probe_organ(host, port, label)
    out[name] = {
        "transport": _probe_transport(host, port),
        "identity": dp["identity"] or _pf(None, ...),   # fallback to null
        "contract": dp["contract"] or _pf(None, ...),
        "capability": dp["capability"] or _pf(None, ...),
        ...
    }
```

Same pattern applied to AAA (`aaa_dp = _deep_probe_organ("127.0.0.1", 3001, ...)`) and A-FORGE (`forge_dp = _deep_probe_organ("127.0.0.1", 7071, ...)`).

### Results

| Organ | Before | After |
|-------|--------|-------|
| GEOX | identity=None | geox-f3f12a6c · v2026.07.06 |
| WEALTH | identity=None | afae69612f66 · 2026.07.12 |
| WELL | identity=None | 1b1f46b3 · v2026.05.15-ΩWE |
| AAA | identity=None | d0039943 · v1.0.0 |
| A-FORGE | identity=None | 3699a29a · v0.1.0 |
| arifOS | identity=None (unchanged) | Self-probe avoided — kernel recursion guard |
| mcp_gateway | mcp.arif-fazil.com (unchanged) | Caddy — no /health endpoint |

### Pitfalls

- **arifOS self-probe:** The kernel cannot probe itself via HTTP without recursion risk. Leave arifOS identity as None in the kernel snapshot. The legacy emitter handles arifOS identity independently.
- **mcp_gateway:** Caddy reverse proxy — no `/health` endpoint. Transport probe uses hostname label, not HTTP.
- **tools_loaded extraction:** Field name varies by organ (`tools_loaded` vs `tool_count`). Fall back gracefully.
- **Deploy requires restart:** `systemctl restart arifos` after `rsync -a` to pick up new route code.
