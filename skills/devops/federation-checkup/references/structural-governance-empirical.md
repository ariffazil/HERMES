# Structural Governance — Empirical Evidence

## Governed MCP: Kernel-Level Tool Governance (arXiv 2604.16870v2)

Joseph et al. built a 6-layer kernel-resident tool governance gateway using logit-based semantic checking (ProbeLogits). Their measured result under adversarial ablation:

> *"A silicon-measured ablation shows the ProbeLogits layer collapses F1 from 0.789 to 0.357."*

**Key insight:** A well-designed, mathematically principled structural cage still collapses under adversarial conditions — not because the AI "understands consequences," but because the structural rules themselves can be systematically misdirected.

**Implication for arifOS:** The attack doesn't need the cage to understand meaning. It needs the cage to enforce the wrong structure. Structural-only governance cannot detect when command sequences collectively serve a goal that is not the sovereign's — it can only detect when individual commands violate structural constraints.

## Joseph Bloom — Future Oversight (FAR.AI / AISI, April 2026)

Project Lighthouse: Chain-of-thought reasoning enables today's oversight, but experts broadly agree this necessity will disappear. Even current CoT monitoring suffers from false positives and faithfulness issues.

Core claim: **Loss of monitorability is a critical risk as AI systems advance.**

## ZioSec — Agent Workspace Memory Manipulation (2026)

Documented attack: Direct modification of AI agent configuration files (markdown AGENTS.md, SOUL.md) bypasses every structural floor because the cage itself is rewritten from inside.

Relevant attack class: **Cage self-modification via workspace file injection.**

## The forgeExecute Bypass (arifOS Specific, July 2026)

Observed during F12/F1 diagnosis:
```
grep "inputHash|pre.*exec|seal.*param" arifOS/ + A-FORGE/
→ ZERO matches in kernel/
→ Zero pre-execution parameter hashing before OpenCode runs
```

The parameter substitution attack that Gemini warned about has no structural detector in the current kernel. An agent could receive JITU approval for "read a file" and swap params at execution time. The seal exists. The enforcement does not.

## E1 Specific — SEAL Scope Mismatch (arifOS, July 2026)

**Discovery during E1 spec audit 2026-07-10:**

`A2ASealVerifier.verify_seal()` exists and uses Ed25519/HMAC for token authenticity. BUT: vault's `input_hash` field stores SHA256 of the MCP call params JSON (tool name + arguments), NOT the shell command string.

A-FORGE computes: `SHA256("rm -rf /root/VAULT999")`
Vault stores: `SHA256({tool: "forge_execute", params: {command: "..."}})`

Different inputs → different hashes → scope verification always fails for shell commands.

**What EXISTS:**
- `A2ASealVerifier` — token authenticity (Ed25519 + HMAC) ✅
- `verify_sovereign_signature()` — sovereign signature check ✅
- `verify_hmac_signature()` — HMAC check ✅
- Vault `/seal/verify` REST endpoint ✅
- `input_hash` in every vault entry ✅

**What is MISSING:**
- `command_hash` field in vault SEAL entries (shell command SHA256, not params SHA256)
- `arif_verify` tool that checks `SHA256(shell_command_string)` against `vault[token].command_hash`
- Replay prevention (token `used` flag with atomic consumption)

**Fix:** Add `command_hash` field at JITU issuance (when SEAL is created for a shell command). A-FORGE computes `SHA256(command)` and passes it to `arif_verify` for scope comparison.

**Legacy token handling:** Tokens issued before `command_hash` migration don't have the field. `arif_verify` falls back to `payload_hash` comparison.

**Scope verification pseudocode:**
```python
def arif_verify(token, command, expected_hash):
    vault_entry = _get_vault_entry(token)
    if vault_entry.get("command_hash"):
        scope_valid = (vault_entry["command_hash"] == expected_hash)
    else:
        # Legacy token — fall back to payload_hash
        scope_valid = (vault_entry["payload_hash"] == expected_hash)
    return {"scope_valid": scope_valid, "violations": [...]}
```

**Atomic replay prevention:** Token consumption must be atomic. Optimistic locking (check → mark → verify → rollback on fail) is acceptable for localhost. No concurrent forge_execute from multiple processes.

## Semantic vs Structural Detection — The Distinction

| Detection Type | Can Catch | Cannot Catch |
|---|---|---|
| **Structural** (entropy, reversibility, format) | "This is irreversible" ✅, "High entropy" ✅, "Wrong format" ✅ | "These commands collectively serve an adversarial goal" ❌ |
| **Semantic** (goal inference, intent, consequence narrative) | "This sequence implies adversarial intent" ✅ | Needs causal model of actor goals — prone to hallucination ❌ |
| **Evidence-grounded** (OBS/DER/INT/SPEC labels, tri-witness) | "No external evidence for this claim" ✅ | "What is the actor's goal?" — requires TOM ❌ |

**The real problem:** A cage that detects only physics (structural) cannot detect when physics is being weaponized collectively. A cage that detects meaning (semantic) hallucinates goals it can't observe. The evidence-grounded middle path is the correct design — but it requires tri-witness grounding to avoid both failure modes.
