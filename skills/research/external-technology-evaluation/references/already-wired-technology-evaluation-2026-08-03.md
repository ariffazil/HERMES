# Already-Wired Technology Evaluation — Mode 1 variant (forged 2026-08-03, qwen3.8-max case)

When the subject of evaluation is ALREADY deployed (e.g. a model already set as
`model.default` in Hermes config), the question shifts from "should we integrate?"
to **"is the live wiring healthy?"** Run the evaluation in reverse.

## Trigger

Arif asks "tell me everything about X and contrast fit with my Hermes agent" while X
is already the live primary. The honest answer starts with: *"Kau tak perlu integrate
apa-apa — X dah jadi otak aku sekarang."* Then prove the wiring.

## Reverse-evaluation procedure

1. **Confirm what's actually wired** (config, not docs):
   ```bash
   python3 -c "
   import yaml; cfg=yaml.safe_load(open('/root/.hermes/config.yaml'))
   print(yaml.dump(cfg.get('model',{})))
   for n,p in (cfg.get('providers') or {}).items():
       print(n, p.get('key_env'), [m['id'] for m in (p.get('models') or [])][:8])
   print(cfg.get('fallback_providers'))"
   ```
   Check model block (provider, default, context_length, max_tokens, supports_vision),
   provider key_env per provider, fallback chain, and auxiliary blocks (vision,
   compression).

2. **Live-probe the endpoint per key/seat SEPARATELY** — seats exhaust independently.
   Proven 2026-08-03: `qwen3.8-max` ALIVE on the Standard seat (`QWEN_HERMES_API_KEY`)
   while the Pro seat (`QWEN_OPENCODE_API_KEY`) returned `insufficient_quota` for the
   same model. A models-list 200 does not mean the seat can infer. Probe:
   ```bash
   curl -s -m 60 -X POST "$BASE/chat/completions" -H "Authorization: Bearer $KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"<model>","messages":[{"role":"user","content":"Reply with exactly: OK"}],"max_tokens":20}'
   ```
   Check `choices` present + `reasoning_tokens` in usage.

3. **Verify harness-critical capabilities with real payloads:**
   - Structured tool call (function schema) — watch for `content:null` disease
     (Kimi K3, DeepSeek-V4-Pro known carriers; qwen3.8-max clean, probed).
   - Base64 vision via `data:` URI — this kills the PRMT hallucination class if native.
   - `reasoning_effort` param (`low`/`high`/`xhigh`) if always-on reasoning —
     measure the token/latency delta (probed: low ≈ 40% fewer reasoning tokens,
     ≈25% faster).

4. **Verdict format:** FORGE-already-executed (wiring confirmed live) + SABAR for
   pending events (open-weights release, preview-model retirement dates, seat quota
   rollover). Deliverable = wiring-health report + loose-ends list, NOT an
   integration proposal.

## Loose-ends checklist (qwen3.8-max case, 2026-08-03)

| Loose end | Why it matters |
|---|---|
| Pro seat `insufficient_quota` | Any agent still riding that key will 401 |
| Fallback chain thickness | Live chain was 2 entries (opencode-go/dsv4-pro → minimax) vs historical 11-tier; primary-down recovery is thin |
| Stale `-preview` model refs | Preview endpoints retire (~5 days after GA); provider lists still naming them |
| Always-on reasoning burn | Higher tokens/turn than predecessor — watch monthly seat quota |

## Benchmark honesty rule

Vendor-published benchmark tables are [INT], not [OBS]. One independent head-to-head
(proven: Trilogy StackPerf, Qwen 80 vs Kimi K3 83) is a data point, not a verdict.
Always separate: live-probed capabilities (measured) vs vendor claims (reported) vs
independent evals (if any exist).
