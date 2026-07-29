---
name: irreversible-consent-protocol
description: F1 AMANAH consent pattern for irreversible actions across multi-user Telegram DM. Consent-before-execute protocol with VAULT999 receipt sealing, identity attribution, and Telegram inline button UX.
layer: knowledge
invariants:
  authority: Every irreversible action requires explicit user consent before execution.
  evidence_schema: OBS (action identified) → INT (irreversibility assessment) → DER (consent received) → OBS (execution result)
  reversibility: false — this protocol governs irreversible actions
  lineage: Every receipt links to consent event + user identity + tool call
  trigger_semantics: Boolean predicate — tool call with ack_irreversible=true OR action classified as irreversible by the agent
  failure_contract: Denied consent → abort cleanly. No partial execution. No orphan side effects.
  resource_budget: {cpu: low, time_ms: < 30000, entropy: 0}
  audit_surface: [consent_request, consent_response, tool_call, vault_receipt]
bridge_connections:
  kernel_verbs: [arif_seal, arif_forge, arif_think]
  skills: [cognitive-commands, federated-skill-architecture, telegram-bot-routing-doctrine, federation-secret-vault]
  knowledge: [F1 AMANAH, F11 AUDITABILITY, F13 SOVEREIGN]
  protocol: async_consent → synchronous_execute
  inputs: {action_description: string, target: string, chat_id: string, user_id: string, user_name: string}
  outputs: {consent_granted: bool, receipt_id: string, vault_path: string}
contrast:
  not: [exec-approval-system, tirth-dangerous-command-filter]
  distinction: Exec approval intercepts SHELL commands by pattern. Irreversible consent applies to MCP TOOL calls by semantic classification (the agent judges irreversibility, not pattern matching).
  trigger_conflicts: Do NOT fire for shell commands already covered by exec approval. Only fire for MCP tools (arif_forge, arif_seal, arif_judge) with ack_irreversible=true or agent-classified irreversible side effects.
---
# Irreversible Consent Protocol

> **Core:** F1 AMANAH — reversible-first. Irreversible → explicit consent → receipt.

## Trigger

Fire this protocol when ANY of these conditions is true:

1. You call an MCP tool with `ack_irreversible=true`
2. You are about to execute an action with irreversible side effects (delete, overwrite, deploy, transfer, publish, sign)
3. The action affects shared state (federation config, secrets, production services, vault entries)

## Protocol Steps

### Step 1 — Classify

Label the action with one of:

| Classification | Meaning | Action |
|---|---|---|
| IRREVERSIBLE | Cannot be undone. Destructive write. | MUST fire consent protocol |
| SEMI-REVERSIBLE | Can be undone with effort (git revert, restore from backup) | Fire consent protocol, label "reversible-with-effort" |
| REVERSIBLE | git checkout, undo, rollback available | T1 auto-do, no consent needed |

Use `arif_think(mode="reason")` if uncertain about reversibility.

### Step 2 — Send Consent Prompt (Inline Button Preferred)

Send to the user in their original chat:

```
⚠️ IRREVERSIBLE ACTION
Arahan: [clear description of what will happen]
Target: [what will be affected]
Siapa: [user display name]

[Confirm IRREVERSIBLE] [Cancel]
```

The inline button callback uses the gateway `ic:` prefix mechanism (see gateway patch).

### Step 3 — Handle Response

| User says | Then |
|---|---|
| Confirm | Proceed to Step 4 |
| Cancel | Abort. Log to forge_work: `CONSENT_DENIED - [action] - [user_id] - [timestamp]` |
| Timeout (>60s) | Treat as cancel. Log: `CONSENT_TIMEOUT - [action]` |

### Step 4 — Execute

Call the tool with `ack_irreversible=true`. Log execution start to forge_work.

### Step 5 — Seal Receipt to VAULT999

Call `arif_seal` with payload containing:

```json
{
  "action": "ack_irreversible",
  "consent_receipt": {
    "granted_by": {
      "user_id": "<Telegram user_id>",
      "chat_id": "<Telegram chat_id>",
      "username": "<@username or display_name>"
    },
    "granted_at": "<ISO8601 timestamp>",
    "action_class": "<IRREVERSIBLE|SEMI-REVERSIBLE>"
  },
  "target": "<what was acted upon>",
  "outcome": "<success|failed>",
  "tool_call": "<the MCP tool name and key params>"
}
```

### Step 6 — Report

Respond to the user with the outcome + receipt reference:

```
✅ Done. Receipt: SEAL-<id>
Identity terikat: <user_id>
F11 audit: VAULT999/outcomes.jsonl
```

## Consent Without Inline Buttons (Fallback)

If the gateway patch isn't applied, use text-based consent:

1. Send descriptive message with clear IRREVERSIBLE warning
2. Ask user to type: `confirm` or `ya, saya sahkan`
3. Accept: `sah`, `confirm`, `ya`, `ok`, `yes` (case-insensitive, BM + EN)
4. Reject: anything else or timeout > 60s

## Tool Classification

### Tools that ALWAYS need consent

| Tool | Why |
|---|---|
| `arif_forge` (mode=engineer/write/commit) | Mutates filesystem, git, deploy |
| `arif_seal` | Immutable vault write |
| Terminal with destructive command | Covered by exec approval system |
| `write_file` to production paths | Overwrites config |
| `patch` with replace_all=true | Bulk irreversible edit |
| `skill_manage` (delete) | Removes procedural knowledge |
| `cronjob` (remove) | Removes scheduled work |

### Tools that NEVER need consent (T1 auto)

- Read-only: read_file, search_files, web_search, web_extract
- Immutable append-only: arif_seal with carry_forward context
- Skills: skill_view, skills_list
- Session housekeeping: todo, memory (writes controlled by config)

### Tools that need judgment (agent decides)

- `cronjob` (create/update) — depends on scope
- `arif_forge` (dry_run) — no side effects, T1
- `terminal` (read-only commands like ls, curl to /health) — T1
- `memory` (add/replace) — depends on char budget, injection risk

## Receipt Format (Standardised)

Every irreversible action MUST produce a VAULT999 receipt via `arif_seal` or the helper script at `/root/.hermes/scripts/irreversible_receipt.py`.

Required identity fields:

| Field | Source | Example |
|---|---|---|
| `actor` | Telegram user_id | `267378578` |
| `actor_name` | Telegram username or first_name | `Arif` |
| `source_chat` | Telegram chat_id | `267378578` (DM) or `-1003753855708` (group) |
| `action_class` | Agent classification | `IRREVERSIBLE` or `SEMI-REVERSIBLE` |
| `consent_method` | How consent was obtained | `inline_button` or `text_confirm` or `f13_override` |
| `target` | What was acted upon | File path, organ, tool name |
| `tool` | The MCP tool or shell command | `arif_forge` |
| `outcome` | Result | `success` or `failure` or `cancelled` |

## Gateway Patch Reference

For inline button support, the `ic:` callback prefix is added to:
- `/usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py` — `_handle_callback_query()` method
- Adds `ic:confirm:{receipt_id}` and `ic:cancel:{receipt_id}` callback data patterns

## Example Flow (Telegram DM)

```
User: Delete file /tmp/test.txt
Agent: ⚠️ IRREVERSIBLE ACTION
       Arahan: Delete file /tmp/test.txt
       Target: /tmp/test.txt
       [Confirm IRREVERSIBLE] [Cancel]
User: [clicks Confirm]
Agent: [executes rm /tmp/test.txt]
       [calls arif_seal with identity]
       ✅ Done. File deleted.
       Receipt: SEAL-2026-07-29-irreversible-delete
       Identity: user_id=267378578, actor=Arif
```

*DITEMPA BUKAN DIBERI — F1 AMANAH enforced at protocol level, not just prompt.*
