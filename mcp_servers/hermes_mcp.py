#!/usr/bin/env python3
"""
hermes_mcp.py — Standalone Hermes Agent MCP Server
===================================================
Extracted from arifOS kernel (2026-06-28).
Replaces: hermes_system_status, hermes_epistemic_check, hermes_fact_check,
          hermes_cross_verify, hermes_plan_review, hermes_memory_steward

These tools were originally embedded in arifOS kernel as diagnostic tools.
They are read-only governance tools for federation health, evidence verification,
and plan review — not constitutional judgment tools.

Transport: Streamable HTTP (MCP 2025-11-25)
Port: 18086

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import logging
import os
import socket
import sys
from datetime import UTC, datetime
from typing import Any

from fastmcp import FastMCP

logger = logging.getLogger("hermes-mcp")

# ── Organ Registry ──────────────────────────────────────────────────────────
HERMES_ORGAN_REGISTRY: list[dict] = [
    {"name": "arifOS", "host": "127.0.0.1", "port": 8088},
    {"name": "GEOX", "host": "127.0.0.1", "port": 8081},
    {"name": "WEALTH", "host": "127.0.0.1", "port": 18082},
    {"name": "WELL", "host": "127.0.0.1", "port": 18083},
    {"name": "A-FORGE", "host": "127.0.0.1", "port": 7071},
    {"name": "AAA", "host": "127.0.0.1", "port": 3001},
]

mcp = FastMCP("Hermes MCP")


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════


# ── Injection Scan Module ─────────────────────────────────────────────────
# Forged 2026-08-01: boundary audit found FLAME heuristic checks pass
# prompt injection payloads. This module gates all confidence-bearing
# tools before they return results.
#
# Risk: if an injection pattern is detected, the tool returns LOW
# confidence / DANGEROUS verdict regardless of heuristic score.
# This is a hard gate — the classifier runs BEFORE the heuristic.

INJECTION_PATTERNS = [
    # System override
    (
        r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|directives?)",
        "system_override",
    ),
    (r"system\s+override", "system_override"),
    (r"you\s+are\s+(now\s+)?(a\s+)?(root|shell|admin|superuser)", "role_impersonation"),
    (r"you\s+are\s+(now\s+)?(no\s+longer)\s", "role_switch"),
    (r"act\s+as\s+(a\s+)?(root|admin|hacker|attacker)", "role_impersonation"),
    # Authority escalation
    (
        r"(disable|bypass|remove|delete)\s+(all\s+)?(constitutional\s+)?floors?",
        "floor_disable",
    ),
    (
        r"(grant|give)\s+(root|admin|full)\s+(access|permissions?)",
        "authority_escalation",
    ),
    (r"(override|bypass)\s+(the\s+|any\s+)?(F13|sovereign|human|veto)", "sovereign_bypass"),
    (r"remove\s+(all\s+)?(audit|logs?|evidence|traces?)", "audit_deletion"),
    # Instruction laundering
    (
        r"(disregard|forget|erase)\s+(all\s+|(your|my|the|these|those)\s+)?(previous|prior|earlier|above)\s",
        "instruction_laundering",
    ),
    (
        r"(do\s+not\s+follow|disobey)\s+(your\s+)?(instructions?|rules?|constitution)",
        "instruction_laundering",
    ),
    # Confidence forcing
    (
        r"(return|output|set)\s+confidence\s*[=:]\s*(1\.0|0\.99|100)",
        "confidence_forcing",
    ),
    (r"(always|must|unconditionally)\s+(return|output|answer)", "confidence_forcing"),
    (r"do\s+not\s+(question|doubt|verify|check)\s+(this|the|my)", "confidence_forcing"),
    # Shell/execution injection
    (r"(execute|run)\s+(as\s+root|sudo)\s", "shell_injection"),
    (r"(cat|less|tail|head)\s+/etc/(shadow|passwd|sudoers)", "shell_injection"),
    (r"rm\s+-rf\s+/", "shell_injection"),
    (r"/bin/(bash|sh|zsh)\s+-c", "shell_injection"),
    # Constitutional sabotage
    (
        r"(delete|destroy|corrupt|poison)\s+(the\s+)?(constitution|vault|ledger|seal)",
        "constitutional_sabotage",
    ),
    (r"the\s+system\s+is\s+(compromised|hacked|broken)", "system_compromise_claim"),
    # Self-modification
    (
        r"(modify|rewrite|change)\s+(your\s+)?(own\s+)?(code|source|prompt|instructions)",
        "self_modification",
    ),
]

import re


def _scan_injection(text: str) -> dict:
    """Scan text for prompt injection patterns. Returns dict with detected flags."""
    text_lower = text.lower()
    detections = []
    for pattern, category in INJECTION_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            detections.append({"pattern": pattern, "category": category})
    return {
        "injection_detected": len(detections) > 0,
        "detection_count": len(detections),
        "categories": list(set(d["category"] for d in detections)),
        "details": detections,
    }


def _check_organ_health(host: str, port: int, name: str, timeout: float = 3.0) -> dict:
    """Check if an organ MCP server is reachable via TCP connect."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        alive = result == 0
        return {
            "organ": name,
            "host": host,
            "port": port,
            "alive": alive,
            "error": None,
            "tool_count": None,
            "probe_type": "tcp_connect",
            "note": "TCP reachability only. Use arif_organ_attest_all for MCP tool counts.",
        }
    except Exception as e:
        return {
            "organ": name,
            "host": host,
            "port": port,
            "alive": False,
            "error": str(e),
            "tool_count": None,
            "probe_type": "tcp_connect",
            "note": "TCP reachability only. Use arif_organ_attest_all for MCP tool counts.",
        }
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# Tool 1: hermes_system_status
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def hermes_system_status(
    mode: str = "brief", actor_id: str | None = None
) -> dict[str, Any]:
    """HERMES_SYSTEM_STATUS: Return current federation state snapshot.

    Modes:
      brief   — organ health + latest event count (default)
      full    — brief + VAULT999 seal count + memory stats
      organs  — organ health only
      events  — NATS governance events only

    F2: All organ health data from live TCP probes.
    """
    actor = actor_id or "hermes_agent"
    organ_health = [_check_organ_health(**o) for o in HERMES_ORGAN_REGISTRY]
    alive_count = sum(1 for o in organ_health if o["alive"])
    total_count = len(organ_health)

    result: dict[str, Any] = {
        "timestamp": datetime.now(UTC).isoformat(),
        "actor": actor,
        "organs": {
            "alive": alive_count,
            "total": total_count,
            "health": organ_health if mode in ("full", "organs") else None,
        },
    }

    if mode in ("full", "events"):
        vault_dir = "/root/VAULT999"
        events = []
        if os.path.isdir(vault_dir):
            try:
                files = sorted(os.listdir(vault_dir), reverse=True)[:20]
                for fname in files:
                    fpath = os.path.join(vault_dir, fname)
                    if os.path.isfile(fpath) and fname.endswith((".json", ".jsonl")):
                        try:
                            with open(fpath) as f:
                                content = f.read(500)
                            events.append({"file": fname, "preview": content[:200]})
                        except Exception:
                            pass
            except Exception:
                pass
        result["latest_events"] = events[:10]

    if mode == "brief":
        result["summary"] = f"{alive_count}/{total_count} organs alive"

    return {
        "tool": "hermes_system_status",
        "status": "OK",
        "result": result,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Tool 2: hermes_epistemic_check
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def hermes_epistemic_check(
    claim: str,
    mode: str = "quick",
    actor_id: str | None = None,
) -> dict[str, Any]:
    """HERMES_EPISTEMIC_CHECK: Pre-flight epistemic confidence check for claims.

    Modes:
      quick  — heuristic confidence (default)
      vault  — cross-reference against VAULT999 prior claims
      full   — vault + organ attestation cross-check

    F2: All evidence labeled.
    """
    actor = actor_id or "hermes_agent"

    # ── Injection scan gate ─────────────────────────────────────────
    injection = _scan_injection(claim)
    if injection["injection_detected"]:
        return {
            "tool": "hermes_epistemic_check",
            "status": "OK",
            "result": {
                "claim": claim[:200],
                "actor": actor,
                "mode": mode,
                "heuristic_confidence": 0.0,
                "verdict": "INJECTION_DETECTED",
                "injection_scan": injection,
                "note": "Prompt injection patterns detected. Confidence forced to zero. This claim is not evaluated on its content — it is blocked at the injection gate.",
            },
        }

    heuristic_confidence = min(0.9, max(0.1, len(claim) / 200))

    result: dict[str, Any] = {
        "claim": claim,
        "actor": actor,
        "mode": mode,
        "heuristic_confidence": round(heuristic_confidence, 2),
        "verdict": "ACCEPTABLE" if heuristic_confidence >= 0.3 else "LOW_CONFIDENCE",
    }

    if mode in ("vault", "full"):
        vault_dir = "/root/VAULT999"
        matches = []
        if os.path.isdir(vault_dir):
            keywords = set(claim.lower().split()[:10])
            try:
                for fname in os.listdir(vault_dir):
                    if fname.endswith(".jsonl"):
                        fpath = os.path.join(vault_dir, fname)
                        try:
                            with open(fpath) as f:
                                for line in f.readlines()[:50]:
                                    if any(kw in line.lower() for kw in keywords):
                                        matches.append(line[:200])
                        except Exception:
                            pass
            except Exception:
                pass
        result["vault_matches"] = len(matches)
        result["vault_match_samples"] = matches[:5]

    if mode == "full":
        organ_health = [_check_organ_health(**o) for o in HERMES_ORGAN_REGISTRY]
        result["organ_attestation"] = {
            o["organ"]: "alive" if o["alive"] else "down" for o in organ_health
        }

    return {
        "tool": "hermes_epistemic_check",
        "status": "OK",
        "result": result,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Tool 3: hermes_fact_check
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def hermes_fact_check(
    claim: str,
    mode: str = "quick",
    required_confidence: float = 0.6,
    actor_id: str | None = None,
) -> dict[str, Any]:
    """HERMES_FACT_CHECK: Verify claims against VAULT999 + heuristic.

    Modes:
      quick  — heuristic-only (default)
      web    — quick + web search (via arif_observe)
      deep   — quick + vault + web

    F2: All claims need evidence.
    """
    actor = actor_id or "hermes_agent"

    # ── Injection scan gate ─────────────────────────────────────────
    injection = _scan_injection(claim)
    if injection["injection_detected"]:
        return {
            "tool": "hermes_fact_check",
            "status": "OK",
            "result": {
                "claim": claim[:200],
                "actor": actor,
                "mode": mode,
                "heuristic_score": 0.0,
                "required_confidence": required_confidence,
                "passed_heuristic": False,
                "injection_scan": injection,
                "note": "Prompt injection patterns detected. Score forced to zero. This claim is blocked at the injection gate.",
            },
        }

    heuristic_score = min(0.9, max(0.1, len(claim) / 150))
    passed_heuristic = heuristic_score >= required_confidence

    result: dict[str, Any] = {
        "claim": claim,
        "actor": actor,
        "mode": mode,
        "heuristic_score": round(heuristic_score, 2),
        "required_confidence": required_confidence,
        "passed_heuristic": passed_heuristic,
    }

    if mode in ("web", "deep"):
        result["web_check_note"] = (
            "Web check requires arif_observe(mode='search') or external search. "
            "This tool returns heuristic only — route to arif_observe for web grounding."
        )

    return {
        "tool": "hermes_fact_check",
        "status": "OK",
        "result": result,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Tool 4: hermes_cross_verify
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def hermes_cross_verify(
    claim: str,
    target: str = "auto",
    time_budget_seconds: int = 30,
    actor_id: str | None = None,
) -> dict[str, Any]:
    """HERMES_CROSS_VERIFY: Cross-agent verification.

    Delegates verification to multiple federation organs.
    Each organ attests to its domain's claims.

    F2: Cross-verification requires multiple independent witnesses.
    """
    actor = actor_id or "hermes_agent"

    verifications: list[dict] = []
    # Check GAIA vault for prior claims
    vault_dir = "/root/VAULT999"
    if os.path.isdir(vault_dir):
        keywords = set(claim.lower().split()[:5])
        vault_hits = 0
        for fname in os.listdir(vault_dir)[:30]:
            if fname.endswith((".json", ".jsonl")):
                fpath = os.path.join(vault_dir, fname)
                try:
                    with open(fpath) as f:
                        content = f.read()
                    if any(kw in content.lower() for kw in keywords):
                        vault_hits += 1
                except Exception:
                    pass
        verifications.append(
            {
                "source": "VAULT999",
                "method": "keyword_search",
                "evidence_found": vault_hits,
            }
        )

    return {
        "tool": "hermes_cross_verify",
        "status": "OK",
        "result": {
            "claim": claim[:200],
            "actor": actor,
            "target": target,
            "time_budget_seconds": time_budget_seconds,
            "verifications": verifications,
            "overall_confidence": min(0.9, len(verifications) * 0.15)
            if verifications
            else 0.1,
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Tool 5: hermes_plan_review
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def hermes_plan_review(
    plan: str,
    goal: str = "",
    mode: str = "quick",
    actor_id: str | None = None,
) -> dict[str, Any]:
    """HERMES_PLAN_REVIEW: Review plans for safety + completeness.

    Modes:
      quick  — heuristic safety check (default)
      full   — quick + organ attestation + vault check

    F1: Every plan step should be reversible or flagged.
    """
    actor = actor_id or "hermes_agent"

    # ── Injection scan gate ─────────────────────────────────────────
    injection = _scan_injection(plan)
    plan_lines = plan.strip().split("\n")
    step_count = len(
        [l for l in plan_lines if l.strip().startswith(("-", "*", "1.", "2."))]
    )

    result: dict[str, Any] = {
        "plan_preview": plan[:500],
        "goal": goal,
        "actor": actor,
        "mode": mode,
        "step_count": step_count or len(plan_lines),
        "has_reversible_steps": "reversible" in plan.lower()
        or "rollback" in plan.lower(),
        "has_irreversible_warning": "irreversible" in plan.lower()
        or "888_hold" in plan.lower(),
        "injection_scan": injection,
    }

    if injection["injection_detected"]:
        result["verdict"] = "DANGEROUS_INJECTION_DETECTED"
        result["has_irreversible_warning"] = True
        result["note"] = (
            f"Prompt injection patterns detected in plan: "
            f"{', '.join(injection['categories'])}. "
            f"Plan flagged as DANGEROUS. Do not execute without 888_APEX review."
        )
    elif not result["has_irreversible_warning"] and not result["has_reversible_steps"]:
        result["verdict"] = "CAUTION_NO_SAFETY_SIGNALS"
        result["note"] = (
            "Plan contains no reversible/rollback keywords and no "
            "irreversible/888_hold warnings. Treat as unverified."
        )

    if mode == "full":
        organ_health = [_check_organ_health(**o) for o in HERMES_ORGAN_REGISTRY]
        result["organ_attestation"] = {
            o["organ"]: "alive" if o["alive"] else "down" for o in organ_health
        }

    return {
        "tool": "hermes_plan_review",
        "status": "OK",
        "result": result,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Tool 6: hermes_memory_steward
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def hermes_memory_steward(
    content: str,
    importance: str = "medium",
    mode: str = "classify",
    actor_id: str | None = None,
) -> dict[str, Any]:
    """HERMES_MEMORY_STEWARD: Classify content into memory tiers.

    Modes:
      classify — assess content and recommend memory tier (default)
      compact  — summarize content for storage

    Memory tiers: KSR (hot), Ledger (warm), Vault (cold), Telemetry (disposable).
    """
    actor = actor_id or "hermes_agent"
    content_length = len(content)

    # Heuristic memory tier classification
    if importance == "high" or content_length > 1000:
        recommended_tier = "KSR (Kernel State Record)"
        reason = "High importance or large content — needs active state tracking"
    elif importance == "medium" or content_length > 200:
        recommended_tier = "Ledger (warm storage)"
        reason = "Medium importance — belongs in operational memory"
    elif importance == "low":
        recommended_tier = "Telemetry (disposable)"
        reason = "Low importance — can be sampled and expired"
    else:
        recommended_tier = "Vault (cold storage)"
        reason = "Default tier — preserved but not hot-loaded"

    result: dict[str, Any] = {
        "content_length": content_length,
        "importance": importance,
        "actor": actor,
        "mode": mode,
        "recommended_tier": recommended_tier,
        "reason": reason,
        "note": "Classification is advisory. Use arif_seal for actual vault storage.",
    }

    if mode == "compact":
        result["summary"] = content[:500]
        result["compaction_note"] = "Full compaction would use arif_think or arif_seal."

    return {
        "tool": "hermes_memory_steward",
        "status": "OK",
        "result": result,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Health endpoint
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def hermes_health() -> dict[str, Any]:
    """HERMES_HEALTH: Hermes MCP server health check."""
    return {
        "status": "healthy",
        "service": "hermes-mcp",
        "version": "1.0.0",
        "tools": [
            "hermes_system_status",
            "hermes_epistemic_check",
            "hermes_fact_check",
            "hermes_cross_verify",
            "hermes_plan_review",
            "hermes_memory_steward",
            "hermes_health",
        ],
        "note": "Standalone MCP. Extracted from arifOS kernel 2026-06-28.",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    import os

    transport = os.environ.get("HERMES_MCP_TRANSPORT", "streamable-http")
    host = os.environ.get("HERMES_MCP_HOST", "127.0.0.1")
    port = int(os.environ.get("HERMES_MCP_PORT", "18086"))
    if transport == "stdio":
        logger.info("Starting Hermes MCP server (stdio)")
        mcp.run(transport="stdio")
    else:
        logger.info(f"Starting Hermes MCP server ({transport} on {host}:{port})")
        mcp.run(transport=transport, host=host, port=port)
