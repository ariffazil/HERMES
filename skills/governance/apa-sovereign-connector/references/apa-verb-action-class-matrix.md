# APA Verb × Action-Class × Reflex Matrix

> Source: `APA-GITHUB-SOVEREIGN-CONNECTOR.md` (canonical compile target).
> Every future APA connector (Slack, Drive, Notion, Sheets, any SaaS) is an isomorphic copy of this matrix. Only the protocol adapter and verb names change.

## 1.1 OBSERVE Verbs (no lease required, session may apply)

| Verb | Action Class | Lease Scope | Blast | ART Classifies | Kernel Checks | APA Expresses | ACT Phases | VAULT999 |
|------|-------------|-------------|-------|----------------|---------------|---------------|------------|----------|
| `search_repos` | OBSERVE | `github.read` (opt) | LOW | Tool call = observer. No mutation. | F2 (truth), F4 (clarity), F12 (injection) | Manifest resolve. No lease gate. | DRY_RUN (validate query) → EXECUTE (GET search) → VERIFY (items is array) | Optional |
| `get_repo` | OBSERVE | `github.read` (opt) | LOW | Observer. | F2, F4, F12 | Same. | DRY_RUN → EXECUTE (GET) → VERIFY (has `full_name`) | Optional |
| `list_issues` | OBSERVE | `github.read` (opt) | LOW | Observer. | F2, F4, F12 | Same. | DRY_RUN → EXECUTE (GET) → VERIFY (items is array) | Optional |
| `list_pull_requests` | OBSERVE | `github.read` (opt) | LOW | Observer. | F2, F4, F12 | Same. | DRY_RUN → EXECUTE (GET) → VERIFY (items is array) | Optional |

**OBSERVE rule:** No lease gate at APA layer. Bridge may still apply session/transport checks from A-FORGE MCP. RECEIPT is optional — but RECOMMENDED for any external API call (F11 audit continuity).

## 1.2 MUTATE Verbs (lease REQUIRED)

| Verb | Action Class | Lease Scope | Blast | ART Classifies | Kernel Checks | APA Expresses | ACT Phases | VAULT999 |
|------|-------------|-------------|-------|----------------|---------------|---------------|------------|----------|
| `create_issue` | MUTATE | `github.mutate` | MEDIUM | Mutator. External side effect (public if repo public). Reversible via close_issue (compensating). Requires lease. | **All 13 floors applied.** F1 (reversible-enough), F2 (not fabricated), F3 (witness if HIGH stakes), F4 (thin verb), F5 (no harassment), F7 (Ω₀ ≤ 0.85), F11 (receipt), F12 (body is data), F13 (888 can HOLD) | ① manifest resolve ② verify lease `github.mutate` ③ TTL alive ④ bind session+actor ⑤ dispatch to bridge | DRY_RUN (GET repo exists) → SIMULATE (hash title+body) → EXECUTE (POST issue) → VERIFY (GET issue, state=open) → ROLLBACK (close_issue compensating) → RECEIPT | **REQUIRED** |
| `close_issue` | MUTATE | `github.mutate` | MEDIUM | Mutator. Reversible (reopen possible). Requires lease. | Same as create_issue. | Same. | DRY_RUN → SIMULATE → EXECUTE (PATCH state=closed) → VERIFY (GET state=closed) → ROLLBACK (reopen) → RECEIPT | **REQUIRED** |
| `add_issue_comment` | MUTATE | `github.mutate` | MEDIUM | Mutator. Requires lease. | Same. | Same. | DRY_RUN → SIMULATE → EXECUTE (POST comment) → VERIFY → ROLLBACK (delete comment if possible) → RECEIPT | **REQUIRED** |
| `create_pr` | MUTATE | `github.mutate` | MEDIUM | Mutator. Default draft=true (lower blast). Requires lease. | Same + F1 (draft first, never force-push). | Same. | DRY_RUN (GET branches exist) → SIMULATE (show diff summary) → EXECUTE (POST pulls, draft=true) → VERIFY (GET pr) → ROLLBACK (close PR) → RECEIPT | **REQUIRED** |
| `create_or_update_file` | MUTATE | `github.mutate` | MEDIUM | Mutator. External side effect. Requires lease. | Same + F1 (get sha first for update; backup content). | Same. | DRY_RUN → SIMULATE → EXECUTE (PUT file) → VERIFY (GET file, content matches) → ROLLBACK (revert commit) → RECEIPT | **REQUIRED** |
| `push_files` | MUTATE | `github.mutate` | MEDIUM | Mutator. Multi-file commit. Requires lease. | Same + F1 (commit-to-branch only, never force-push main). | Same. | DRY_RUN → SIMULATE → EXECUTE → VERIFY → ROLLBACK (revert) → RECEIPT | **REQUIRED** |

**MUTATE rule:** No lease → no dispatch. Bridge returns `403 lease_required`. RECEIPT mandatory.

## 1.3 IRREVERSIBLE Verbs (short-TTL lease + ACK REQUIRED)

| Verb | Action Class | Lease Scope | Blast | ART Classifies | Kernel Checks | APA Expresses | ACT Phases | VAULT999 |
|------|-------------|-------------|-------|----------------|---------------|---------------|------------|----------|
| `delete_repo` | IRREVERSIBLE | `github.admin` | HIGH | Destructor. CANNOT be compensated. Requires short-TTL lease + explicit ACK. | All 13 + F1 AMANAH confirm: paired irreversible gate + `ack_irreversible=true` | ① short-TTL lease (5 min max) ② explicit `ack_irreversible` ③ sovereign countersign if repo is main | DRY_RUN (validate ownership) → SIMULATE (list repos to delete) → **HUMAN GATE** → EXECUTE (DELETE) → VERIFY (GET 404) → RECEIPT (no rollback possible) | **REQUIRED** + SEAL entry type=IRREVERSIBLE |
| `force_push_main` | IRREVERSIBLE | `github.admin` | HIGH | Destructor. Rewrites history. Cannot be compensated. | Same as delete_repo + F8 (real need vs rage). | Same. | DRY_RUN → SIMULATE → **888_HOLD** → EXECUTE if cleared → VERIFY (HEAD matches) → RECEIPT | **REQUIRED** + SEAL |

**IRREVERSIBLE rule:** Short lease. Explicit ack. 888_HOLD gate at SIMULATE stage. Rollback column says N/A. SEAL block in VAULT999 marks entry type=IRREVERSIBLE for future auditors.

## 2. Dispatched Execution Phases (ACT)

Every verb passes through these phases in order. No phase may be skipped.

```
DRY_RUN → SIMULATE → EXECUTE → VERIFY → ROLLBACK → RECEIPT
```

| Phase | Job | Exit Condition |
|-------|-----|----------------|
| **DRY_RUN** | Validate that the target exists and is reachable. No side effects. | 200 OK + target identity confirmed |
| **SIMULATE** | Compute what would change. Hash of new state. Show diff to caller. | Confirmation hash + diff text |
| **EXECUTE** | Apply the mutation. | API 2xx + idempotency key logged |
| **VERIFY** | Read back the new state and assert it matches SIMULATE pre-image. | GET matches expected state |
| **ROLLBACK** | If VERIFY fails: apply compensating action. If none exists, log IRRECOVERABLE. | Compensating 2xx or IRRECOVERABLE flag |
| **RECEIPT** | Write immutable receipt to VAULT999. | Seal chain entry appended |

## 3. APA Connector Clone Checklist

Any new connector that does not pass all 7 gates is NOT APA:
1. Manifest YAML exists under `connectors/<name>/manifest.yaml`
2. Verb × action-class table fully populated (OBSERVE/MUTATE/IRREVERSIBLE rows)
3. ACT 6-phase execution implemented in bridge
4. Lease required for MUTATE/IRREVERSIBLE verbs
5. VAULT999 RECEIPT wired for MUTATE+ verbs
6. systemd unit registered
7. Port assigned in the 18093-18096 range
