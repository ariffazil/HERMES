---
name: ariflow-component-forging
description: Build, instrument, and deploy new governed components for the arifFlow Rust engine — from spec to struct to Kabarkan integration to systemd deploy.
category: software-development
---

# ariflow-component-forging

> Build and deploy governed components for the arifFlow Rust execution engine.
> Part of the arifOS Federation — FLOW layer between arifOS (LAW/Python) and A-FORGE (HANDS/TS).

## Trigger

Use this skill when you need to:
- Add a new data type, struct, or module to the arifFlow Rust codebase
- Define a spec for a new arifFlow capability
- Wire a new component into Kabarkan observability (FQ snapshots, events)
- Deploy the arifFlow binary via systemd
- Compute or emit Flow Quotient (FQ) metrics
- Integrate with the A-FORGE adapter (`/root/A-FORGE/domain/orchestration/arifFlow_adapter.py`)

## Repo Canonical

```
repo:   https://github.com/ariffazil/arifFlow
local:  /root/arifFlow/
deploy: /opt/ariflow/app/
binary: /usr/local/bin/ariflow
unit:   /etc/systemd/system/arifflow.service
```

## Workflow: Spec → Struct → Test → Integrate → Deploy

### 1. Spec (`spec/`)
Write a canonical spec document first. Cover:
- Purpose and design rationale
- Field definitions with types
- Validation rules
- Serialization format (JSON for Kabarkan/VAULT999, bincode for internal channels)
- Example JSON
- Related specs (Kabarkan, VAULT999, cooling, FQ)
- Flow Quotient thresholds and alert levels

### 2. Rust Struct (`src/`)
- Derive `Serialize, Deserialize` for all types
- Implement builder pattern (`.with_*()` methods) for ergonomic construction
- Import cross-module types: `use crate::merkle::MerkleRoot`, `use crate::channel::*`
- Register `pub mod <module>;` in `src/lib.rs` (alphabetical order with existing mods)
- Add new crate deps to `Cargo.toml` (e.g. `sha3`, `hex`, `bincode`)

### 3. Tests
- 15–20 unit tests minimum for a new module surface
- Cover: creation, chaining/sequencing, validation error paths, edge cases, builder patterns, display traits
- Use `#[cfg(test)] mod tests { ... }` inline
- Test downstream consumers still compile: `cargo test`

### 4. Integration
- Wire into `SuperStepScheduler` for automated receipts
- For Kabarkan: add `KabarkanEvent` variant + emission in `kabarkan.rs`
- For FQ: compute from `ReceiptStore` via `store.flow_quotient(window)`
- **Backward compat:** sibling subagents may modify same files in parallel with old API. Add legacy types:
  - `AFQMetric` — struct with `::new(exec_steps, gov_steps)`, `diagnosis()`, `Default`
  - `EpistemicTag` — enum with `From<Tag> for EpistemicLabel`
  - `GovernanceOverlay` — struct with `none()`
  - `ReceiptChain` — `Vec<FlowReceipt>` alias
  - `FlowReceipt::new(...)` — legacy constructor bridging old call sites

### 5. Deploy (Daemon Mode)

The arifFlow binary runs in **two modes**:

1. **stdin/stdout protocol** (default) — reads JSON-L from stdin, writes to stdout. Used by the A-FORGE adapter as a subprocess.
2. **`--daemon` mode** — TCP listener on `ARIFLOW_PORT` (default 7073). Serves health, receipt ingest, and flow command endpoints.

**Daemon endpoints:**

| Method | Path | Returns |
|--------|------|---------|
| GET | `/health` | `{"status":"ok","fq":{...},"receipts":N,"uptime_ms":...}` |
| POST | `/ingest` | Push a `FlowReceipt` JSON → daemon's `ReceiptStore` → updated FQ gauge |
| POST | `/flow` | JSON-L command passthrough (configure/seed/step/verdict/stop) |

**Deploy sequence:**
```bash
cargo build --release
cp target/release/ariflow /usr/local/bin/

# Write systemd unit
cat > /etc/systemd/system/ariflow.service << 'UNIT'
[Unit]
Description=arifFlow — Governed Parallel Execution Engine
Documentation=https://github.com/ariffazil/arifFlow
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ariflow
ExecStart=/usr/local/bin/ariflow --daemon
Restart=on-failure
RestartSec=5
Environment=RUST_LOG=info
Environment=ARIFLOW_PORT=7073
StandardOutput=journal
StandardError=journal
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=read-only
PrivateTmp=true

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload && systemctl restart arifflow
systemctl status arifflow.service --no-pager

# Verify health endpoint
curl -s http://127.0.0.1:7073/health | python3 -m json.tool

# Federation-wide probe:
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083 ariflow:7073; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅ $name :$port" || echo "❌ $name :$port"
done
```

### 6. A-FORGE Adapter Integration

After deploying the daemon, wire the A-FORGE adapter to push receipts to `/ingest`:

```python
# In /root/A-FORGE/domain/orchestration/arifFlow_adapter.py
ARIFLOW_DAEMON_URL = os.environ.get("ARIFLOW_DAEMON_URL", "http://127.0.0.1:7073")

# Call in run_step() after verdict processing:
step_type = "Execute" if verdict == "SEAL" else "Verify"
epistemic = "OBS" if verdict == "SEAL" else "DER"
self._push_receipt(step_type, cost_ns, verdict, epistemic)
```

The `_push_receipt()` method sends a `FlowReceipt`-compatible JSON to `POST /ingest`. This feeds the daemon's `ReceiptStore`, updating the live FQ gauge at `GET /health`. Failures are logged but never block execution (fire-and-forget).

The daemon uses `KabarkanTracer` (wired into `SuperStepScheduler`) to emit FQ snapshots per super-step and cooling cross-references directly into the Kabarkan observability plane.

### 7. Gitwrap
```bash
git status --short          # check for unstaged/modified files
git add -A                  # stage all
git commit -m "feat: <description>"
git push origin main
git tag vYYYY.M.DD && git push origin vYYYY.M.DD
```

After gitwrap, if the change affects the running binary:
```bash
systemctl restart ariflow && systemctl status ariflow --no-pager
curl -s http://127.0.0.1:7073/health | python3 -m json.tool
```

### 8. Reference Files

| File | Content |
|------|---------|
| `references/fq-kabarkan-instrumentation.md` | FQ thresholds, alert protocol, Kabarkan event schema, cooling correlation |
| `references/daemon-endpoints.md` | HTTP endpoint docs for GET /health, POST /ingest, POST /flow |

## Canonical Spec Documents

The following documents form the arifFlow canon at `/root/arifFlow/`:

| File | Content |
|------|---------|
| `spec/FLOW_RECEIPT_v1.md` | The atom — receipt schema, chain integrity, FQ thresholds |
| `doc/KABARKAN_FQ_MONITORING.md` | The eye — real-time FQ dashboard, alert protocol, correlation engine |
| `doc/SOMATIC_AGENTIC_FLOW_EQUIVALENCE.md` | The map — 11 isomorphic mappings, human to agentic |
| `doc/LANGCHAIN_LANGGRAPH_ANATOMICAL_CONTRAST.md` | The perimeter — phantom limb vs autonomic organism |
| `doc/REALITY_ENGINEERING_PRIMER.md` | The capstone — governance becomes physics, not policy |
| `src/receipt.rs` | Rust impl — 79 tests, FlowReceipt, FlowQuotient, ReceiptStore |

## Flow Quotient (FQ) — Domain Reference

| FQ Range | Verdict | Meaning |
|----------|---------|---------|
| > 3.0 | Optimal | Agent in flow. Governance in the architecture. |
| 1.0 – 3.0 | Balanced | Healthy verification. Self-monitoring supports execution. |
| 0.5 – 1.0 | Watching | Verification cost ≈ execution cost. Caution. |
| < 0.5 | Stuck | mPFC takeover. Self-monitoring has become the task. |

**Formula:** `FQ = Σ(Execute.cost_ns) / Σ(Verify.cost_ns + preceding_verify_cost_ns)`

**Window:** Default N=20 receipts sliding window.

### FQ Alert Levels (Kabarkan)

| Trigger | Alert | Meaning | Action |
|---------|-------|---------|--------|
| FQ < 1.0 | WARNING | Verification starting to dominate | Route more through FLAME |
| FQ < 0.5 | CRITICAL | mPFC takeover confirmed | Recommended 888_HOLD |
| FQ recovers > 1.5 | RECOVERED | Flow restored | Clear hold, resume |

## Key Types (`src/receipt.rs`)

- `FlowReceipt` — UUID v4, previous SHA3-256 hash chain, DateTime timestamp, actor/session binding
- `StepType` — Execute, Verify, Cool, Seal, Barrier, Merge, Route
- `EpistemicLabel` — OBS, DER, INT, SPEC, SEAL (Display: OBS/DER/INT/SPEC/SEAL)
- `FloorVerdict` — Pass, Caution, Hold, Void
- `CoolingDecision` — None, Hold, Clamp, Bypass
- `TriWitnessVotes` — human/ai/earth f64 scores + `nash_score()` + `meets_f3_threshold()`
- `FlowQuotient` — computed from receipt slice, carries verdict (Optimal/Balanced/Watching/Stuck)
- `FlowVerdict` — Optimal, Balanced, Watching, Stuck
- `ReceiptStore` — Vec-based, max_capacity, push validates chain continuity, `flow_quotient(window)`
- `verify_chain(receipts)` — standalone function, validates hash chain integrity

## Pitfalls

- **Cargo version format:** `"2026.7.25"` not `"2026.07.25"` — Cargo rejects leading zeros in minor version
- **Sibling subagent collisions:** always re-read files before writing; sibling may have modified the same lines
- **Duplicate `pub mod` lines:** after adding a new module to `lib.rs`, check for accidental duplicates from parallel edits
- **Systemd EXEC failures:** `ProtectSystem=full` + `NoNewPrivileges=true` can prevent binary execution. Use `/usr/local/bin/` path and minimal unit hardening for arifFlow
- **Binary lifecycle (RESOLVED):** arifFlow's stdin/stdout protocol mode exits immediately under systemd. **Use `--daemon` flag** for long-running service mode — TCP listener with health endpoint. See §5 Deploy (Daemon Mode).
- **Dependency resolution:** `cargo build --release` may skip binary linking if nothing changed. Use `cargo clean --release` then rebuild if binary isn't produced
- **Backward compat:** always add legacy types when replacing an API that sibling subagents already depend on
- **`/ingest` uses push_force, not push:** The HTTP monitoring endpoint calls `store.push_force()` which skips chain validation. This is intentional — monitoring/observability must never block on chain integrity. Core execution (stdin/stdout) still uses `store.push()` with strict chain validation. If you change `/ingest` to use `push()`, monitoring receipts from the A-FORGE adapter will be rejected when chain continuity is broken (e.g. after daemon restart). Two data paths: core = chain-verified governance, monitoring = live FQ gauge.
- **Daemon restart loses state:** The daemon's ReceiptStore is in-memory (Vec-backed, max 1000 entries). A restart resets the store to 0 receipts. FQ shows STUCK (0/0=0.0) until adapter pushes new receipts. Correct — daemon is an observability relay, not a truth ledger. VAULT999 is the truth ledger.
- **JSON enum variants match Rust Discriminants:** POST /ingest expects Rust enum variant names: `"Observation"` not `"OBS"`, `"Execute"` not `"exec"`, `"Pass"` not `"pass"`. Must use Rust naming, not Display format.
