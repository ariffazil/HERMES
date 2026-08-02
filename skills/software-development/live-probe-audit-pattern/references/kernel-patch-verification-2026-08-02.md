# Kernel Patch Verification — Editable Install + MCP Trimming

Proven 2026-08-02 during Z5 reality anchor injection into arifOS kernel.

## Context

Patched 4 kernel tools (session.py, sense.py, judge.py, vault.py) with reality anchors.
Service runs from `/opt/arifos/venv` with `PYTHONPATH=/opt/arifos/app` but uses an
editable install pointing at `/root/arifOS`. Three hazards discovered during verification.

## Hazard 1: Editable Install + PYTHONPATH Shadow

The service unit sets `PYTHONPATH=/opt/arifos/app` which contains a STALE Jul-27 copy
of arifosmcp. But `pip install -e /root/arifOS` registers a path finder that intercepts
the `arifosmcp` import before PYTHONPATH resolution.

**Verification (before restart):**
```bash
# Simulate the service's exact env
PYTHONPATH=/opt/arifos/app /opt/arifos/venv/bin/python -c \
  "import arifosmcp; print(arifosmcp.__file__)"
# MUST print: /root/arifOS/arifosmcp/__init__.py
# If it prints /opt/arifos/app/... → patches won't load, editable install is broken
```

Also check: `pip show arifos | grep -i editable` → should show "Editable project location: /root/arifOS"

## Hazard 2: MCP Transport Trims Output for OBSERVE_ONLY Sessions

After restart, calling `arif_init` or `arif_observe` via MCP returns a governance
envelope (`status: "pending"`, `verdict: "pending"`) that strips the tool body output.
New fields (like `vps_snapshot` or `evidence_receipt`) are NOT visible in the MCP response.

This is NOT a bug in the patch. The interceptor gates unverified sessions (no Ed25519
signature) and returns a trimmed envelope. The tool body DID execute — the MCP layer
just doesn't surface the full output.

**Verification (bypass MCP):**
```bash
cd /root/arifOS && python3 -c "
from arifosmcp.tools.sense import arif_observe
result = arif_observe(mode='vitals', actor_id='HERMES', session_id='TEST')
meta = result.get('meta', {})
print('evidence_receipt:', meta.get('evidence_receipt', 'ABSENT'))
"
```

**Also confirm code is loaded (not stale .pyc):**
```bash
python3 -c "
import inspect
from arifosmcp.tools.session import _project_light
print('vps_snapshot' in inspect.getsource(_project_light))  # True = loaded
"
```

## Hazard 3: Multiple Return Paths

Kernel tools have 20+ return paths. session.py alone has returns at lines 424, 453,
484, 559, 612, 781, 847, 1498, plus the _project_light builder. Patching ONE path
(e.g., the `_ok` wrapper in sense.py) covers the success path but not error holds,
mode-specific early returns, or the light-vs-full init split.

**Detection:**
```bash
grep -c "return " /root/arifOS/arifosmcp/tools/session.py
# 20+ returns — a single patch covers ~5% of paths
```

**Strategy:** Patch the most common path first (the `_ok` wrapper or the main return
dict). Then verify the SPECIFIC mode you care about via direct call. Don't assume
"patched the function" means "all modes covered."

## Ground-Truth Hierarchy for Patch Verification

| Priority | Method | What it proves |
|----------|--------|----------------|
| 1 | Direct function call | Tool body executes, output correct |
| 2 | Disk artifacts | Side effects land (evidence files, ledger entries) |
| 3 | `inspect.getsource()` | Code is loaded in the running interpreter |
| 4 | MCP call | Full pipeline works (but may be trimmed by governance) |

**Rule:** Never trust MCP call alone for patch verification. It's the WEAKEST signal
because the governance layer can strip your output. Direct call + disk artifact is
the strongest proof.

## Disk Artifact Verification

For anchors that write to disk (evidence files, ledger entries):
```bash
# Check evidence files landed
ls -la /root/reality_ledger/evidence/
# Verify hash integrity of a written file
python3 -c "
import json, hashlib
with open('/root/reality_ledger/evidence/<file>.json') as f:
    d = json.load(f)
stored = d.pop('sha256')
recomputed = hashlib.sha256(json.dumps(d, sort_keys=True, default=str).encode()).hexdigest()
print(f'HASH VERIFIES: {stored == recomputed}')
"
```

## Service Restart Protocol

```bash
systemctl restart arifos.service
sleep 6  # kernel takes ~5s to boot
systemctl is-active arifos.service  # must be "active"
# Verify new PID
systemctl show arifos.service -p MainPID --value
# Health check
curl -sf http://127.0.0.1:8088/health | python3 -c "import json,sys; print(json.load(sys.stdin).get('status'))"
```
