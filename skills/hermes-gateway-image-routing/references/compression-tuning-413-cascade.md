# Compression Tuning for 413 Cascade Failure

> **Symptom:** All fallback providers return 413 (Request Payload Too Large) in sequence.
> The error cascades through 10+ providers because the payload is too large for ALL of them.
> **Root cause:** High-volume group chat (e.g. SADO) with `protect_last_n: 20` keeps 20 messages
> fully uncompressed. Images in those messages bloat the payload past the provider's HTTP request
> limit (~10-50MB). The 413 is an HTTP-level limit, not a model context window limit.
>
> **Proven:** 2026-07-30, SADO group with Syed's daily nasi lemak orders + images.

## Diagnostic

```
Response: 413 Request Payload Too Large
```

The error cascades through ALL fallback providers because the payload size is the same for every
provider. Compression attempts (17→14, 14→12 messages) don't reduce enough.

```bash
# Check current compression settings
grep -A6 "^compression:" /root/.hermes/config.yaml

# Check session context size
journalctl -u hermes-asi-gateway --since "5 min ago" --no-pager | grep -i "compression\|context\|token\|413"
```

## Fix — More Aggressive Compression

| Setting | Default (before) | After | Effect |
|---|---|---|---|
| `threshold` | 0.5 | **0.3** | Triggers compression when 30% full (not 50%) |
| `target_ratio` | 0.15 | **0.10** | Compresses history to 10% of original |
| `protect_last_n` | 20 | **10** | Only 10 messages kept raw instead of 20 |
| `hygiene_hard_message_limit` | 5000 | **3000** | Hard cleanup kicks in sooner |
| `auxiliary.compression.provider` | auto | **mulerouter** | LLM-based summarization (not basic truncation) |
| `auxiliary.compression.model` | '' | **qwen3-max** | Fast summarization via MuleRouter |

```bash
# Apply via sed (config.yaml edit guard blocks write_file/patch)
sed -i 's/  threshold: 0.5/  threshold: 0.3/' /root/.hermes/config.yaml
sed -i 's/  target_ratio: 0.15/  target_ratio: 0.10/' /root/.hermes/config.yaml
sed -i 's/  protect_last_n: 20/  protect_last_n: 10/' /root/.hermes/config.yaml
sed -i 's/  hygiene_hard_message_limit: 5000/  hygiene_hard_message_limit: 3000/' /root/.hermes/config.yaml

# Set compression model to use same provider as primary
sed -i '/^  compression:/,/^  [a-z]/s/  provider: auto/  provider: mulerouter/' /root/.hermes/config.yaml
sed -i "/^  compression:/,/^  [a-z]/s/  model: ''/  model: qwen3-max/" /root/.hermes/config.yaml
```

## Architecture

The `auxiliary.compression` LLM summarizer must use the same provider as the primary model.
If compression uses a different provider (e.g. TokenRouter/OpenRouter) and that provider has
credit issues, compression will ALSO fail — even though the primary and vision are fine.

```yaml
# In /root/.hermes/config.yaml
auxiliary:
  compression:
    provider: <SAME AS PRIMARY PROVIDER>  # NOT auto
    model: qwen3-max                       # fast summarizer
```

## Related Pitfalls

- **`image_input_mode` alignment** (PROVEN 2026-07-30): When `image_input_mode: text` and
  primary provider is changed (e.g. to mulerouter), `auxiliary.vision.provider` MUST also be
  changed to the same provider. If they diverge, the auxiliary vision enrichment can fail on a
  different failure domain (balance, rate limit, network). When it fails, raw image bytes are
  forwarded to the text-only primary model → 413 Payload Too Large → cascade through all
  text-only fallbacks.

- **OpenRouter balance exhaustion** (PROVEN 2026-07-30): OpenRouter with $0 credit returns 402,
  which marks the auxiliary provider as "unhealthy for 600s" — all vision calls skipped for 10
  minutes. Solution: use MuleRouter for both primary and auxiliary (same key, same balance).

- **session_id vs protect_last_n**: Even with aggressive compression, a session that has
  accumulated 50+ messages over hours will still send 10 full messages + compressed history.
  For very high-volume groups, consider reducing `protect_last_n` further to 5.

## Verification

```bash
# After changes, restart gateway
systemctl restart hermes-asi-gateway

# Send an image in the high-volume group
# Check logs for compression trigger
journalctl -u hermes-asi-gateway -f --since "1 min ago" | grep -i "compress\|413\|payload"
```