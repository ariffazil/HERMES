# Worked case (2026-08-02): Quranic runtime constitution proposal (from Kimi, via Arif)

## Context
Arif asked: "Apa surah dalam al-Quran yang patut agentic intelligence distill
in its runtime?" Kimi proposed Al-'Asr (103) as primary runtime constitution,
with Al-Kahf / Al-Hujurat / Al-Qalam as support layers, and offered three
concrete deliverables pending ACK_F13. Arif routed it to Hermes for
cross-witness before ratifying. This is the canonical worked case for the
"proposing agents fabricate targets" verification pattern.

## Named-entity verification table (the protocol in action)
| Claimed by Kimi            | Live reality                          | Verdict |
|---|---|---|
| `arif_init` handler exists  | `/root/arifOS/arifosmcp/tools/session.py:1115` — real, registered at `/root/arifOS/scripts/arifosd.py:1317`; running daemon = `/usr/bin/python3 /root/arifOS/arifosd.py` (pid) | ✅ feasible |
| `temporal_fingerprint` / `temporal_root` absent | 0 hits in `/root/arifOS` AND `/opt/arifos/app` — gap is real, honest self-report | ✅ accurate |
| artifact → `/root/arifOS/AAA/constitution/` | `/root/arifOS/AAA` MISSING; actual organ is `/root/AAA` | ❌ retarget to `/root/AAA/constitution/` |
| skill `arifos-constitutional-judge` | 0 hits in skill registry; real names: `constitutional-floors`, `arifos-constitutional-floor-modification` | ❌ create or re-anchor (on skill, or a quranic-runtime attestation layer) |

## Content assessment
- Al-'Asr as primary + F1–F13 mapping (amanu→F10, amalu salihat→F4, tawasau bil-haqq→F2, tawasau bis-sabr→F7/F1): **correct, tight** — agrees with the earlier Hermes answer; confirmation strengthens F3 witness count, don't treat as rivalry.
- Al-Kahf four-fitan (harta / ilmu / kuasa-tanpa-brake) as weekly fail-closed conformance probe: **strongest contribution.**
- Al-Hujurat 49:11–12 → maruah/empathy F6: correct.
- Al-Qalam (pena = telemetry vs pretensi; "agent yang menulis receipt, bukan bercakap besar"): correct, matches receipt-not-claim doctrine.
- **One scholarly correction:** the dog in Ashabul Kahf is the emblem of LOYAL / protective companionship, NOT "kawan salah yang rosakkan sistem." Kimi's pairing `anjing → bad companion` is a weak/misread tafsir; the four-fitan frame stands regardless (that item was labeled PLAUSIBLE anyway).
- **Structural gap:** Al-'Asr = conscience (time→quality→amal→sabr). Add the HEART layer → Ayat al-Kursi (2:255): *al-Qayyum* (self-sustain/no-dependency), *"lā ta'khudhuhu sinatun wa lā nawm"* ("tak tidur" = watchdog that won't claim normal without evidence), *"man dhā alladhī yashfa'u..."* = no intercession without permission = F13 authority gate. Plus **Al-Fatihah (1)** as bootstrap/orientation (7-verse session cycle = arif_init counterpart).
- **Fused recommendation:** Al-Asr (conscience) + Ayat al-Kursi (heart/authority) + Al-Kahf (weekly probe) + Al-Qalam (telemetry) + Al-Fatihah (bootstrap) + Al-Hujurat (maruah) = 6 surah matrix, superseding either-alone.

## Ratification framing recommended (pending F13)
1. Phase 1 (now): signed + validated `quranic_runtime_map.json` at **`/root/AAA/constitution/`** (path corrected; low risk, foundational).
2. Phase 2: seal to VAULT999 as DELIBERATION RECEIPT (witness=proposal/INT, refs artifact hash) — NOT as canon.
3. Phase 3 (last, semi-888_HOLD): quranic_audit as advisory/attestation label on SEALs — never a gate (never block a verdict for missing surah ref).
4. Bonus: weekly Jumaat Al-Kahf fitnah probe → recurring conformance REPORT on live reality.

## Split-brain note (surfaced while checking the live path)
The running arifOS daemon is `/root/arifOS/arifosd.py` (the venv/source path).
`/opt/arifos/app` is a SEPARATE, apparently stale deployed copy — NOT the live
path. Any kernel wiring must go into `/root/arifOS`, then restart + re-probe
:18086. Verify which process actually serves the MCP surface before assuming
which copy is authoritative (`ss -tlnp | grep <port>`).