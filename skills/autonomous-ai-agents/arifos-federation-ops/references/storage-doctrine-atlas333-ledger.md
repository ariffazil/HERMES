# Storage Doctrine & ATLAS333 Ledger — detail (2026-08-05)

## The 3-layer storage doctrine (Arif's words, ratified in AAA session)

1. **Hardware & Filesystem Layer (Substrate)** — verdict: DO NOT FORK, DO NOT TOUCH.
   Block storage, disk management, core FS protocols = pure infrastructure, like the Linux kernel.
   "Jangan cari penyakit fork Linux kernel." ΔS ≤ 0. Never build a sovereign file system.
2. **The Agent Boundary (OpenClaw / OpenCode access)** — verdict: SANDBOX & GATE.
   - Read (ro): free — agents metabolize context.
   - Write (rw): restricted to a designated scratchpad (e.g. `/tmp/federation_workspace`).
   - Permanent-dir writes / config changes / file deletes: cannot be direct — the execution
     shell must catch the write, proxy to the arifOS kernel, trigger explicit 888_HOLD for Arif.
3. **The ATLAS333 Ledger (Persistent State)** — verdict: PERMANENT, NON-EPHEMERAL.
   Long-term cognitive memory of the federation. Not `/tmp`. Persistent + backed up.
   Append-only from agent perspective; only kernel or Arif may drop tables / alter schema.

## ATLAS333 ledger — canonical facts

- **DB:** `/root/.local/share/arifos/atlas333/atlas_ledger.db`
- **Schema:** SQLite, table `paradox_events` — id AUTOINCREMENT, timestamp, session_id,
  query_hash, lane, tau, kappa, rho, paradox_id, tension_score, catalyst, zone, verdict.
  Indexes on timestamp DESC, session_id, paradox_id.
- **State (2026-08-05):** 120 rows, live (writes same-day from sibling sessions).
- **Perms:** `640 root:arifos` (was `644 root:root` world-readable — fixed 2026-08-05;
  verify with `stat -c "%a %U:%G"`).
- **Integrity:** `sqlite3 <db> "PRAGMA integrity_check;"` → ok.
- **Contract documented at:** `arifOS/docs/ATLAS333_INTELLIGENCE_FLOW.md` §8.1
  (added + committed `4d7f4b0c4`; commit passed the SURFACE-GATE hook).
- **Amnesia rule:** the ledger cures ATLAS333 amnesia — persistence is the point;
  never point it at an ephemeral path.

## Doc-edit conventions for sealed canonical docs (EVERGREEN rule)

- Header says: "Status: EVERGREEN — update as the earth updates its map: continuously, never finished."
- Update rule: "Change the code first, then update this document. Never the reverse."
- Seal rule: "Every update requires ARIF signature: `sealed_by: ARIF :: <date>`" —
  when Arif ratified the change in chat, record his ratification that way.

## SURFACE-GATE pre-commit hook (arifOS repo)

- Runs on `git commit` in `/root/arifOS`; STRICT mode (FORGE_SURFACE_GATE_STRICT=1).
- Probes live MCP surface: expects the 8 kernel tools (arif_init, arif_observe, arif_think,
  arif_route, arif_memory, arif_judge, arif_forge, arif_seal) + /health.
- Success output: "✅ SURFACE PINNED — Live tools match surface-map declarations." → commit allowed.
- A commit failing the gate = live MCP surface drifted from the declared surface-map — fix the
  surface/declaration before committing, don't bypass the hook.
