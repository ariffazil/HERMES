# Turso / libSQL — Architecture Reference (2026-07-30)

**Source:** The Register (Joab Jackson, 29 Jul 2026) + daily.dev summary + Turso announcement
**URL:** https://www.theregister.com/databases/2026/07/29/after-rewriting-sqlite-in-rust-turso-turns-its-sights-on-postgres/5279835

## What It Is

Turso rewrote SQLite from scratch in Rust (NOT a fork — a full reimplementation called libSQL). Now they're adding a Postgres-compatible wire protocol frontend on the same core engine.

## Architecture: "LLVM of Databases"

```
┌─────────────────────────────────────────┐
│  SQLite frontend  │  Postgres frontend   │  ← multiple SQL frontends
├─────────────────────────────────────────┤
│      VDBE Bytecode VM (Rust core)       │  ← single engine (like LLVM IR)
├─────────────────────────────────────────┤
│        Storage engine (page-based)      │  ← single storage
└─────────────────────────────────────────┘
```

Analogy: same way LLVM takes C/C++/Rust → IR → native code, Turso takes SQLite SQL and Postgres SQL → compile to VDBE bytecode on the same engine.

## Key Features

| Feature | Detail |
|---------|--------|
| Language | Rust (from scratch, not a C fork) |
| License | MIT |
| SQLite compat | File-format compatible |
| Postgres compat | Wire protocol level (alpha, runnable from source) |
| Concurrency | MVCC concurrent writes (SQLite original uses reader-writer lock) |
| Async | Fully asynchronous — runs in browser via WASM |
| Materialized views | Auto-updating |
| Testing | Deterministic simulation testing, Antithesis, Oracle testing, fuzzing, formal methods |
| Connection model | NOT process-per-connection (unlike Postgres) |
| Contributors | 260+ |
| Extensions | Via WASM containers |

## Postgres Compatibility Approach

- Goal is **broad compatibility**, NOT 100% SQL parity
- Multi-year effort prioritizing correctness over speed
- MIT-licensed, open to community contributions
- Turso positions this as "the LLVM of databases"

## Key Differences from arifOS Federation (summarised)

| Axis | Turso | arifOS |
|------|-------|--------|
| Philosophy | One engine, many SQL frontends | Polyglot persistence — 6 specialised engines |
| Data models | Relational only (SQLite + Postgres) | Relational + Vector + Graph + KV + Event Stream + Append Chain |
| Security | Traditional auth (API keys, managed) | LOCALHOST_IS_PASSWORD — zero passwords |
| Deployment | Cloud-native, edge/WASM, async | Bare-metal systemd + Docker, single VPS |
| Extensions | WASM containers inside DB engine | MCP tools via NATS + F1-F13 governance |
| Governance | None (standard DB) | F1-F13 constitutional floors on every tool call |

## Verdict

Different solution to a different problem. Turso solves "one reliable engine speaking multiple SQL dialects at the edge." arifOS solves "right storage engine for every data class, governed by constitution, zero cloud lock-in."
