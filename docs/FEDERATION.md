# FEDERATION.md — HERMES

```yaml
role: DOMAIN
organ: hermes
layer: L3
citizenship: warga-aaa
canon: ariffazil/ariffazil

depends_on:
  - repo: ariffazil/arifOS
    reason: Governance gates, constitutional compliance
  - repo: ariffazil/AAA
    reason: A2A state, cockpit triggers

mcp:
  port: 8644 (internal)
  endpoint: N/A (Telegram bridge, not public MCP)
  tools_count: 0 (operator edge only)
  protocol: Telegram Bot API + internal bridge

governance:
  judge: arifOS
  seal: VAULT999
  floors: F1-F13
  mutation_rule: NEVER mutate. Route and bridge only. arifOS judges.

stack_role: |
  HERMES is the multi-modal bridge organ — L3 DOMAIN.
  It handles Telegram operator edge, creative/media surface routing,
  and visual/audio signal ingestion.
  It bridges external signals into the federation's reasoning layer.
  HERMES speaks to the outside. arifOS governs what gets through.

entrypoints:
  - Telegram: operator edge (port 8644)
  - Code: https://github.com/ariffazil/HERMES
```

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**
**Part of the arifOS Federation. See `/root/AAA/docs/FEDERATION_MAP.md` for canonical topology.**
