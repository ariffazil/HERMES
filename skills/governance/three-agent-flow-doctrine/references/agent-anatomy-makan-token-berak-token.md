# Agent Anatomy — Makan Token, Berak Token

**Canonical:** 2026-07-28 | **Ratified by:** Arif (F13 SOVEREIGN)

## The Only Mental Model That Matters

Bila orang cakap "Agent", diorang bayang satu robot dalam kotak. Hakikat sebenar:

```
┌─────────────────────────────────────────────────────────┐
│                    AGENTIC SYSTEM                       │
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │              1. HARNESS / KERNEL                │   │
│   │   (Pure Deterministic Code: Python, Rust, Go)   │   │
│   │   • While loops, error handling, state memory   │   │
│   │   • Panggil API / panggil tool / kawal token    │   │
│   └────────────────────────┬────────────────────────┘   │
│                            │                            │
│                            ▼                            │
│   ┌─────────────────────────────────────────────────┐   │
│   │               2. LLM TRANSFORMER                │   │
│   │   (Pure Math: Linear Algebra, Weights, Matrices)│   │
│   │   • Makan Token IN  -->  Berak Token OUT        │   │
│   └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Tiga Komponen, Tiga Risiko Berbeza

| Komponen | Realiti | Apa Dia Buat | Risiko | Kawalan |
|----------|---------|-------------|--------|---------|
| **LLM** | Vector Math & Matrix Multiplication | Makan token → Berak token | **Zero direct** — tak ada tangan | Prompt engineering + F9 ANTI-HANTU |
| **Harness / Kernel** | Deterministic Code (Python/Rust) | Loop, prompt assembly, API router | **High** — dia yang execute | Constitutional Floors F1–F13 |
| **Tool / Binary** | System Executable | Disk I/O, Network, CPU | **High** — dia yang ada kuasa | Sandbox quarantine + lease |

## Kenapa "Cage" Tak Relevan

LLM tak boleh "meloloskan diri" — dia cuma fungsi matematik. Dia tak ada akses ke disk, network, atau OS.

Kawal agent = kawal dua titik:
1. **Tutup mulut** — tapis token sebelum masuk LLM (prompt injection defence)
2. **Quarantine** — sanitise token sebelum Harness execute Tool (tool call validation)

Tak payah bina "cage" kat luar. Kawal Harness guna F1–F13. Kawal Binary guna Sandbox. Clear, deterministic, ΔS ≤ 0.

## Implikasi kepada arifOS

- arifOS kernel = Harness yang governed — F1–F13 enforce pada setiap tool call
- A-FORGE = Harness yang lease-bound — tak boleh execute tanpa verdict
- WELL = LLM-independent — reflect only, tak pernah diagnose
- VAULT999 = rekod immutable bagi setiap token yang jadi tool call
