# Furi — MCP Server Manager Evaluation

**Date:** 2026-07-26
**Source:** https://github.com/ashwwwin/furi
**Epistemic:** OBS (live fetch from GitHub README)
**License:** BSL 1.1 → Apache 2.0 (2028-05-21)

## What It Is

CLI + HTTP API for installing, managing, and aggregating MCP servers. Built with Bun + TypeScript. Uses PM2 for process management. Supports SSE and stdio aggregation.

## Feature Matrix vs Current Setup

| Feature | Furi Approach | Current Federation | Value Add |
|---------|--------------|-------------------|-----------|
| Install MCP from GitHub | `furi add author/repo` — clone + detect Smithery.yaml + build + run | Manual: clone → install → build → systemd unit → start | **Nilai tambah:** 1 command vs 5-6 steps |
| Process management | PM2-backed (start, stop, restart, status, logs) | systemd per organ | Sama — cuma PM2 vs systemd |
| SSE aggregator | `furi meta start` — single SSE endpoint for all tools | Already have per-organ MCP endpoints | Berguna untuk external clients that need one endpoint |
| HTTP proxy | `furi http start` — auto HTTP routes per MCP | Not available for third-party MCPs | **Nilai tambah:** REST access to MCP tools |
| CLI tool calls | `furi call <name> <tool> '{}'` | Direct tool calls via Hermes | Kasual — kita dah ada |
| MCP marketplace access | Direct GitHub repo install | Manual git clone + setup | **Nilai tambah:** fast experimentation |
| Python MCP support | "key roadmap item" — NOT YET | We already run Python MCPs natively | Gap — doesn't cover our stack yet |

## Verdict: SABAR

**Why not FORGE:**
- Python MCP support is roadmap, not reality — our federation runs Python MCPs natively
- Bun not installed — would need to add another runtime
- PM2 overlaps with systemd (which we already use and trust)
- The GitHub marketplace access is the only real gap it fills, but we don't have a high-volume MCP onboarding pipeline yet

**Why not HOLD:**
- The SSE aggregator + HTTP proxy pattern is genuinely useful for external MCP consumers
- Could be valuable once Python support lands and we start onboarding many third-party MCPs
- The `furi add` workflow reduces friction for prototyping

**Trigger for escalation (SABAR → FORGE):**
1. Python MCP support ships
2. We start regularly onboarding 5+ third-party MCPs
3. An external consumer needs a single SSE endpoint instead of per-organ MCP connections
