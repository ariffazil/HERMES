# ZEN-WIRE seal transcript — 2026-07-04 (third concrete instance)

## Context

This is a **third instance** of the arifOS constitutional floor working in practice, distinct from the lifecycle kernel HOLD (which is mutation-class) and the v4 Kinabalu audit (which is evidence-class). The ZEN-WIRE forge is **config-class**: an additive wire of two LLM providers + a fallback chain into `~/.hermes/config.yaml`. No code mutations, no organ routing changes, no skill surface edits. Just YAML additions.

The transcript below is the **full MCP JSON-RPC exchange** with arifOS at `:8088`, including the kernel's refusal. It demonstrates that the floor works **regardless of mutation class** — even a config-only forge requires external evidence anchor to SEAL.

## The forge attempt

```
SEAL_ID:    AF-2026-07-04-002-ZEN-WIRE
CLASS:      6 (External Integration — third-party billing boundary)
MUTATIONS:  /root/.hermes/config.yaml  (additive — providers + fallback_providers block)
            /root/.hermes/.env         (additive — placeholder key + canonical aliases)
            /root/forge_work/          (new — receipt + mapping markdown)
```

## The transcript (raw, MCP JSON-RPC over :8088/mcp)

### Step 0 — Initialize handshake

```json
POST http://localhost:8088/mcp
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{
  "protocolVersion":"2024-11-05",
  "capabilities":{},
  "clientInfo":{"name":"zen-wire-forge","version":"1.0"}
}}

→ 200 OK
{"jsonrpc":"2.0","id":1,"result":{
  "protocolVersion":"2024-11-05",
  "capabilities":{...},
  "serverInfo":{"name":"ARIFOS MCP","version":"kanon-2026.07.03+accd416"}
}}
```

### Step 1 — `arif_init` (first attempt, missing actor_id)

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{
  "name":"arif_init",
  "arguments":{"intent":"Seal ZEN-WIRE forge...","session_id":"..."}
}}

→ 200 OK
{"status":"HOLD","tool":"arif_init","verdict":"HOLD",
 "meta":{"reason":"actor_id required — null not coerced to anonymous",
         "violated_laws":["L11"],
         "hint":"Provide actor_id for non-anonymous session."}}
```

**Lesson:** L11 AUTH (actor verification) is enforced even for read-only sessions. The hint names the floor.

### Step 2 — `arif_init` (corrected, actor_id="arif-arif")

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{
  "name":"arif_init",
  "arguments":{
    "actor_id":"arif-arif",
    "actor":"arif-arif",
    "intent":"Seal ZEN-WIRE forge (MiMo + OpenCode Go providers + fallback chain)",
    "session_id":"a8ff3476-7254-41e9-9e2e-901deb99dedc"
  }
}}

→ 200 OK
{"status":"OK","tool":"arif_init","verdict":"SEAL","result":{
  "session_id":"SEAL-be412e5a866040b9",
  "actor_verified":false,
  "authority":"OBSERVE_ONLY",
  "verdict":"SEAL",
  "constitution_hash":"arifos-..."
}}
```

**Note:** `actor_verified:false` even with a known actor string. The kernel still considers verification pending until F13 SOVEREIGN downstream action. `authority: OBSERVE_ONLY` confirms the engine boundary — observe is permitted, mutation is not.

### Step 3 — `arif_observe` (records the mutation footprint)

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{
  "name":"arif_observe",
  "arguments":{
    "actor_id":"arif-arif",
    "subject":"ZEN-WIRE forge mutations",
    "observation":"providers.xiaomi-mimo + providers.opencode-go registered with 50+2 models; fallback_providers chain (3 entries); hermes config check OK",
    "session_id":"a8ff3476-..."
  }
}}

→ 200 OK (recorded)
```

### Step 4 — `arif_judge` (Pydantic rejection on schema)

```json
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{
  "name":"arif_judge",
  "arguments":{
    "actor_id":"arif-arif",
    "session_id":"a8ff3476-...",
    "claim":"ZEN-WIRE forge is constitutional-compliant",
    "evidence_paths":["...","...","..."],
    "floors_checked":["L01","L02","L04","L08","L11","L13"]
  }
}}

→ 200 OK (Pydantic validation error INSIDE the tool call)
6 validation errors for call[arif_judge]
actor
  Missing required argument [type=missing_argument, ...]
intent
  Missing required argument [type=missing_argument, ...]
```

**Lesson:** `arif_judge` does NOT take `actor_id` — it takes `actor` + `intent` + the 5 floor fields (requested_capability, domain, reversibility_level, blast_radius). The first attempt was schema-incorrect; the kernel did not interpret or coerce — it failed validation and refused to render a verdict.

**This matches the canonical schema discovery pattern:** call with `{}`, read the Pydantic error, retry with corrected field names. (Documented in `geox-federation-mcp-driver` pitfall 1b.)

### Step 5 — `arif_seal` (KERNEL_DENY — strange loop blocked)

```json
{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{
  "name":"arif_seal",
  "arguments":{
    "actor_id":"arif-arif",
    "session_id":"a8ff3476-...",
    "seal_id":"AF-2026-07-04-002-ZEN-WIRE",
    "verdict":"SEAL_READY",
    "artifact_paths":["...","...","..."]
  }
}}

→ 200 OK
{
  "KERNEL_DENY": "Strange loop blocked: capability 'kernel.seal' requires
                  an external anchor for mutations, but no EXTERNAL_*
                  evidence source was provided.
                  Evidence sources received: [].
                  Supply at least one external evidence source
                  (EXTERNAL_DB, EXTERNAL_API, EXTERNAL_HUMAN,
                   EXTERNAL_SENSOR, EXTERNAL_LAW, EXTERNAL_VAULT).",
  "Capability": "kernel.seal",
  "Actor": "arif-arif",
  "Authority": "SOVEREIGN"
}
```

**This is the canonical floor in action.** Even with `actor_id`, `session_id`, `verdict`, and `artifact_paths` all populated, the kernel REFUSED to seal because:
1. No external evidence source was supplied
2. The forge is config-class (mutation-class by the kernel's taxonomy — any filesystem write counts)
3. The `actor_id` is self-declared, not externally verified

The refusal message names the floor (`Strange loop blocked`), the required evidence types (`EXTERNAL_DB | EXTERNAL_API | EXTERNAL_HUMAN | EXTERNAL_SENSOR | EXTERNAL_LAW | EXTERNAL_VAULT`), and confirms the actor's `Authority: SOVEREIGN` — meaning the path to proceed is via an external anchor, not via algorithmic escalation.

## The 6 lessons from this transcript

1. **L11 AUTH is enforced at `arif_init` entry, not at seal.** Don't try to bypass by skipping init — the kernel reads `actor_id` from the first call. If you skip init entirely, every subsequent call gets SYUBHAH (DOUBTFUL) verdict.

2. **`actor_verified:false` is the correct post-init state.** Verification happens downstream (typically at `arif_judge` or via an external signature). A SEAL at init does NOT mean a SEAL at seal.

3. **`authority: OBSERVE_ONLY` is the engine boundary in action.** The init call permits observation; it does not grant mutation authority. This matches `cannot_apply_patch` from the lifecycle kernel hard rules.

4. **Pydantic validation errors leak the full input schema.** This is the fastest way to discover correct field names — call with `{}`, read the error, retry. Works for `arif_init`, `arif_judge`, `arif_seal`, and any other constitutional tool. Documented in `geox-federation-mcp-driver` pitfall 1b.

5. **`KERNEL_DENY: Strange loop blocked` is the right answer for self-sealing.** The kernel refuses to seal a config mutation using only internal evidence (its own observation, its own session, its own verdict). The external anchor is the human's gateway-restart confirmation — that's F13 SOVEREIGN exercising F1 AMANAH (reversible-first).

6. **`Authority: SOVEREIGN` in the denial means: the path forward is not via algorithm.** Even with `actor_id="arif-arif"` (which would normally be the sovereign actor), the kernel still requires an external anchor — because the only "external" anchor the kernel trusts for SOVEREIGN-class actions is something outside its own process boundary (a gateway restart, an Arif-signed message, a Cron receipt, etc.).

## What "external anchor" means in practice for arifOS config-class forges

For a forge like ZEN-WIRE (config-only, no organ routing change, no tool surface change), the external anchor is **Arif's confirmation that the runtime side-effects are in place**. That is:

| External anchor | What it proves |
|---|---|
| `EXTERNAL_HUMAN` — Arif runs `hermes gateway restart` and confirms `/model` shows MiMo + OpenCode Go in picker | The provider wire is live in the runtime; not just on disk |
| `EXTERNAL_API` — `curl https://token-plan-sgp.xiaomimimo.com/v1/models` returns 200 with real model list | The key resolves; the upstream is reachable |
| `EXTERNAL_VAULT` — a sealed receipt from a prior `arif_seal` (different session, different seal_id) references the same provider | The wire has prior precedent; not a one-off experiment |

In the ZEN-WIRE transcript, the forge stopped at `arif_seal` because none of these had been recorded yet. Arif's three actions (paste OPENCODE_GO_API_KEY → `hermes gateway restart` → Telegram `/model` pick) supply the `EXTERNAL_HUMAN` anchor that would unlock the seal.

## Why this transcript belongs in `non-mutating-review-harness`

The transcript demonstrates the **engine boundary at the seam between proposal and apply**. The lifecycle kernel transcript (`references/arifos-hold-correction-2026-07-04.md`) shows the boundary for **mutation-class** proposals (skill regeneration). The ZEN-WIRE transcript shows the boundary for **config-class** proposals (provider registration). Both share the same structural pattern:

```
proposal → init → observe → judge → seal
                ↓         ↓       ↓       ↓
              L11 AUTH  L11+L04  schema  Strange loop check
              required  intact   OK?     → external anchor?
                                          ↓
                                       DENY or SEAL
```

The skill's prime law applies regardless of mutation class:

```yaml
trigger:
  rule: any_proposal_with_side_effects
  must_trigger: review_chain            # always (init → observe → judge → seal)
  may_trigger: artifact_persist         # sometimes (after external anchor)
  must_not_trigger: autonomous_apply_without_anchor   # never
```

## Cross-reference

- `references/arifos-hold-correction-2026-07-04.md` — the original HOLD (mutation-class)
- `references/zen-wire-seal-transcript-2026-07-04.md` — this transcript (config-class)
- `/root/forge_work/AF-2026-07-04-002-ZEN-WIRE-FINAL.md` — the forge receipt the seal was attempted against
- `/tmp/seal_v2.py` — rerunnable seal script (will reproduce the transcript on the live kernel)