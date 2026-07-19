# 2026-07-13 EUREKA Runtime Convergence — Deployment Incident

## Context

Arif's mandate for the EUREKA session stated:

> Deploy the current approved branch through the normal A-FORGE release
> path. Do not manually copy files. Build and hash the wheel, install it
> into the authoritative virtual environment, restart arifos.service,
> and run the five-layer runtime convergence check.

He predicted: "the only remaining path is: build immutable wheel →
install into /opt/arifos/venv → restart arifos.service → run runtime_verify
→ run ceremony canary → verify VAULT chain → promote or rollback."

What actually happened: deployment landed cleanly through step 5
(runtime_verify). The vault chain step then "blocked" promotion —
but the block was a probe artifact, not a chain break.

## Sequence Executed

| Step | Command | Outcome |
|---|---|---|
| 1. Build wheel | `cd /root/arifOS && python3 -m build --wheel` | ✅ `arifos-1!2026.7.11-py3-none-any.whl` |
| 2. Hash wheel | `sha256sum dist/arifos-*.whl` | ✅ `485b92a2afaac6d6d1ec51ecb219ac9159773fefd99f7efbc4226f0b1d04873f` |
| 3. Install venv | `/opt/arifos/venv/bin/pip install --force-reinstall --no-deps dist/arifos-*.whl` | ✅ replaced editable with immutable |
| 4. Restart | `systemctl daemon-reload && systemctl restart arifos` | ✅ active, new PID 1322638 → auto-restart 1338455 |
| 5. Health | `curl :8088/health` | ✅ `status=healthy`, 8 tools, 13 floors |
| 6. Convergence receipt | `from arifosmcp.runtime.convergence_tracker import build_convergence_receipt` | ✅ state=CONVERGED, readiness=PASS |
| 7. Ceremony canary | (BLOCKED by 8) | ⛔ not run |
| 8. Vault chain verify | `node /root/AAA/a2a-server/seal_chain.js verify` | ❌ `ok=false, prev_hash mismatch` |

## The Two False-Positive Failures

### False Positive 1: Module Path Mismatch (probe artifact)

Initial `runtime_verify` probe returned `module_path: FAIL` because
the probe ran from CWD=`/root/arifOS`, where `import arifosmcp`
resolved to the source tree at `sys.path[0]`. The running systemd
service was actually importing from `/opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/__init__.py`
correctly.

Diagnostic that proved this:
```bash
cd /tmp && /opt/arifos/venv/bin/python3 -c \
  "import arifosmcp; print(arifosmcp.__file__)"
# → /opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/__init__.py  ✅
```

vs. from `/root/arifOS`:
```bash
cd /root/arifOS && /opt/arifos/venv/bin/python3 -c \
  "import arifosmcp; print(arifosmcp.__file__)"
# → /root/arifOS/arifosmcp/__init__.py  ❌ (CWD shadow)
```

**Lesson:** every convergence probe must defensively chdir to /tmp
and strip the empty-string CWD entry from sys.path inside the spawned
interpreter. See SKILL.md "Pitfalls" section for the canonical fix
applied to `scripts/convergence_check.py`.

### False Positive 2: VAULT Chain Integrity (writer-tooling artifact)

`node seal_chain.js verify` returned:
```json
{
  "ok": false,
  "broken_at_seq": null,
  "reason": "prev_hash mismatch",
  "expected": "sha256:15acd447ad4e4bbc3e4b4d712e343477...",
  "actual": "fb9f73b98be46e9a137b8d07b4b1f906d4b613949fbfeb46a291a3683dd0bd45"
}
```

Investigation showed:
- `seal_chain.jsonl` (282KB, 162 entries) contains 3-4 duplicate forks per seq 50-63
- `receipts_v2.jsonl` (9.3MB) is the canonical writer's ledger
- `seal_chain_head.json` references seq 9907 in the receipts_v2 file, not in the stub
- The verifier was reading the wrong file — a pre-existing writer routing bug from earlier this year

**Lesson:** verify which ledger file is canonical before declaring
chain integrity failure. The seal-chain-verifier's pointer never
moved when the canonical writer did. See the new
"seal_chain.jsonl is not the canonical chain" pitfall in
`vault999-chain-governance/SKILL.md`.

## Production State After This Session

- New wheel installed: `arifos-1!2026.7.11` SHA `485b92a2...487d`
- Service active: PID 1338455, running from venv
- Module imports: `/opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/__init__.py`
- Source commit: `cb922b9c7cf0`
- 8 tools on public MCP surface, 13 floors active
- Vault seal count: 153 (writer `seal_chain.js` v2.0.0)
- Convergence state: **CONVERGED** per `build_convergence_receipt`

## What Was NOT Done (Pending F13)

- Ceremony canary (challenge, signature, narrow capability, replay denial) — held by chain verify artifact
- VAULT999 chain verify path unification (seal_chain.js → receipts_v2.jsonl)

These remain governance-flagged for F13 because:
1. Ceremony canary touches irreversible capability issuance (888_HOLD class)
2. Chain writer routing is a constitutional surface change (F13 ratifies routing changes to VAULT999)
