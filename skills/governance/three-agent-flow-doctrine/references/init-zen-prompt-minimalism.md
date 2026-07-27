# INIT-ZEN — Prompt Minimalism via Server Enforcement

**Ratified:** 2026-07-27
**Source:** `INIT.md` (16k tokens) → `INIT-ZEN.md` (96 lines, ~900 tokens)
**Principle:** "If the model ignores this line, does anything stop it?"

## Test for Every Line Kept

> **If the model ignores this line, does anything stop it?**

Hanya lines yang server enforce survive sebagai instruction. Segala-galanya — resource, reference, atau gone.

## What Was Cut and Where It Went

| Removed | Destination | Why |
|---------|-------------|-----|
| Q1–Q8 self-attestation | Gone | Training agents to lie as their first act |
| "buat ja la" / magic phrases | Server. Signed action_hash | Published password |
| BOOT ATTESTATION block | Server. SCT boot_attested field | Self-emitted receipt = fake sensor |
| FQ formula + constraint | Server | Punishes verification; gated by unsigned JSON |
| TRINITY-33 full repo map | Resource. arifos://trinity33 | Reference, not instruction |
| ATLAS333 paradoxes | Resource. arifos://atlas333/index | On demand |
| Model rotation table | Resource. arifos://models/rotation | On demand |
| RSI protocol (full) | Resource. Load when needed | Not a boot concern |
| APA / QUANTUM KERNEL | Gone | Contradicted §7 (F9 ANTI-HANTU) |
| Future-task map §15 | Gone | Stale housekeeping |
| /000 ↔ /999 proof architecture | Resource | On demand |
| Three-agent flow doctrine | Server | FQ moves to kernel |
| Duplicate §1 / §18.1 / §18.6 inits | Gone | One init, one gate |
| Presentation Law | Gone | Bad F1→crypto mapping; moved to PDF compiler filters |

## Remaining Structure (7 sections)

Only 7 refusals (§7) and 1 seal pointer (§8) are pure behavioural. Everything else (§1–§5) describes a server gate the model is informed about — but the server enforces regardless. That's the right ratio.

| Section | Type | Server-enforced? |
|---------|------|-----------------|
| §1–§5 | Server gate descriptions | ✅ Yes — model informed, server enforces |
| §7 | Behavioural refusals | ❌ No — pure behavioural |
| §8 | Seal pointer | ❌ No — pure behavioural |

## Constitutional Signal

16k → 900 tokens bukan "edit." Ini **constitutional refactoring**: apa yang boleh server enforce, jangan minta agent patuh secara sukarela. Prompt adalah notification, bukan constitution. Constitution runs on :8088.
