# Vitals Narrative Audit — PETRONAS vitals page (2026-08-04)

**Class:** narrative-vs-live-state audit of a WEALTH dashboard + its sealed data.
**Input:** prose narrative ("time-asymmetric early-warning engine...") + URL `https://arif-fazil.com/wealth/vitals/`.

## Verdict table (narrative claim → probe)

| Claim | Probe | Status | Tag |
|---|---|---|---|
| 48 HOLD composite | JSON pulse 47.5 HOLD; recompute 0.40×75.5 + 0.35×33.6 + 0.25×22.2 = 47.51 | ✅ computed, not asserted | OBS+DER |
| Financials alone → SABAR | BODY layer 75.5 SABAR; SPINE 33.6 + SOUL 22.2 both VOID drag it down | ✅ | OBS |
| Sovereign extraction 0/100 breached | Tripwire #9 score 0.0 VOID (now 70.5% PAT, trip 60) | ✅ | OBS |
| Capital recycling 20/100 | Tripwire #5 score 20.0 VOID (1.2× vs trip 1.0×) | ✅ | OBS |
| "Governance 22/100" | 22 = SOUL **layer** score; governance **tripwire** = 33.3 | ⚠️ layer/tripwire conflation | OBS |
| Gearing 20.7%, CFFO RM85.2B | Match sealed IFR FY2025 anchors | ✅ | OBS |
| Brent/FCF crossover $71.60 | Arithmetic not self-consistent (see below) | ⚠️ | DER |
| "Live proxies computing now" | Panel shows "Proxies unavailable" — live feed dead | ❌ | OBS |

## Finding 1 — SPA catch-all swallowed the API endpoint (the headline finding)

Page fetches `const API = origin + '/wealth/gold/api/proxies'`; live endpoint is `/gold/api/proxies`.
Wrong path → SPA catch-all returns **200 + HTML** → JSON.parse throws → page falls back to
"Proxies unavailable · sealed inputs remain authoritative." Live-monitoring layer dead while page looks intact.

- Correct endpoint probe: fresh JSON, timestamp same minute as probe, Brent $83.49, USD/MYR 4.093 [OBS].
- Fix: one line in `index.html:599` (source + webroot), then verify panel renders + `make verify-pages`.
- **Held at F13** — proposed the one-liner, did not deploy. This is the correct posture for arif-fazil.com.

## Finding 2 — back-solved sensitivity contradiction

Static transmission text pairs a coefficient with derived prices:

- Stated: ±$10 Brent ≈ ±RM6.0B FCF/CFFO
- Crossover claims: FCF-zero $71.60, CFFO-trip $47.40, reference $84.10
- Back-solve: $12.50 drop vs RM11.6B ⇒ **RM9.3B/$10** implied; $36.70 drop vs RM25.2B ⇒ **RM6.9B/$10** implied
- Both contradict stated RM6.0B. At RM6.0B the crossovers would be ~$64.8 / ~$42.1 instead.

Reported both readings; sealed JSON anchors are authoritative, static HTML text is the stale side.

## Finding 3 — source == webroot integrity

`diff` of `public/data/wealth/petronas_vitals.json` (source) vs `/var/www/html/arif/data/wealth/` copy → IDENTICAL.
Deploy mtime 2026-08-03 23:43 MYT. `f2_audit` field carries honest provenance (what changed 2026-07-24,
what remains INTERPRET, thresholds sovereign-sealed). Authority label `COMPUTE_ONLY` correct.

## Finding 4 — canonical-vs-legacy route divergence

`/wealth/vitals/` (URL the narrative cited) serves the OLD generation: 54,390B, pulse 48 HOLD, narrative
section "INSTITUTIONAL PHYSICS" duplicated 2×, zero occurrences of `EXTRACTION_LOCK_ACTIVE`.
Canonical `/vitals/` serves the NEW generation: 57,624B (later mtime 2026-08-03 16:49 UTC), VOID override
logic (18 hits), crisis banner, pacemaker panel. Ground truth that `/vitals/` is canonical: JSON `public_url`
field AND `/wealth/` nav's "PETRONAS health" href. No 301 from legacy route → two surfaces contradicting
each other about the same institution (F2). Fix: Caddy `redir /wealth/vitals* /vitals/ 301`. Held at F13.

## Finding 5 — computed-but-unused override: hero rendered "0 HOLD"

`/vitals/` computes `PULSE_VERDICT_OVERRIDE = EXTRACTION_LOCK_ACTIVE ? "VOID" : null` but the render block
(`pulseval.textContent = PULSE.toFixed(0); pulseverdict.textContent = pv.w` where `pv = verdict(PULSE)`)
never consumes the override. `verdict(0)` → HOLD (0 < 60). So the hero badge said HOLD while the 0-band
legend AND the top crisis banner both said VOID — three states on one screen. Fix: use the override constant
in the badge render. Held at F13.

## Finding 6 — narrative was stale one constitutional amendment

The essay's "48 HOLD" was TRUE for seal 2026-07-24 but the engine resealed 2026-08-03
(`AMEND-2026-08-03-001`): extraction 70.5% PAT > 65% pacemaker → BODY override 0 → composite VOID,
dividend-stop advisory lock ENGAGED, exit only via reseal (< 55% PAT × 2 audits AND governance_capacity ≥ 2.0/3).
Classified "stale one amendment", not fabrication. Note the JSON's `pulse` field still held 47.5 — the
override lives in page JS + `f2_audit` fields, so `f2_audit` must be read, not just `pulse`.

## Finding 7 — unified-header clock frozen site-wide (chrome defect)

Header shows `UTC --:--:--` / `EPOCH ----------` on every unified-loader page. Root cause: loader injects
`unified-header.html` via `insertAdjacentHTML`; per spec, scripts inserted via innerHTML never execute, so
the header's inline `setInterval(update,1000)` clock never runs. Not CSP, not Caddy. Fix options captured in
`caddy-reverse-proxy` skill → `references/unified-header-pattern.md` § pitfall 5.

## Reusable recipe (this class of audit)

1. HTTP probe the page (status, bytes, last-modified).
2. Find the sealed data JSON (webroot + source), diff them, read `pulse`/layers/tripwires.
3. For each narrative number: locate the exact source field; recompute composites from weights.
4. `grep -oE 'const API[^;]*;|fetch\(...'` the deployed HTML → curl every endpoint → assert content-type JSON + timestamp freshness.
5. Back-solve any stated coefficient from its derived prices against sealed anchors.
6. Report verdict table with OBS/DER/INT tags; propose fixes at F13, never deploy.
