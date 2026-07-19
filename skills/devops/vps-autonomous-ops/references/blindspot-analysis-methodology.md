# Blindspot Analysis for Autonomous Systems

> Structured review pattern for identifying failure modes in self-healing infrastructure. Use after building any autonomous control loop.

## The 4 Blindspot Categories

### 1. Observer's Dilemma (F2 - Truth)

**Question:** What happens when the sensor itself cannot see?

- Smoketest depends on localhost + curl. If kernel panic or network stack failure occurs, smoketest reports "Critical" but the real problem is deeper than shell scripts can detect.
- **Risk:** False negative on system-wide freeze.
- **Mitigation:** Acceptable for single-VPS. For multi-node: external probe from different network/location.

### 2. Feedback Loop Contagion

**Question:** Can the fix create a worse problem than the original failure?

- Watchdog (systemd) + watchdog (smoketest) + rollback = three actors that can compound.
- If rolled-back config is also buggy: restart-rollback-restart loop. Exhausts disk write cycles, fills /var/log.
- **Risk:** Cascading restart, log storm, disk death spiral.
- **Mitigation:** Circuit breaker (RETRY_BUDGET). Max N rollbacks per time window → hard stop.

### 3. Semantic Gap

**Question:** Does "healthy" actually mean "working correctly"?

- HTTP 200 with corrupted response body = smoketest says HEALTHY, system is delivering garbage data.
- Status code is necessary but not sufficient.
- **Risk:** System reports healthy while producing broken output.
- **Mitigation:** Validate response BODY content (grep for expected strings), not just HTTP status.

### 4. State Persistence Gap

**Question:** What happens to control state across reboots?

- Flags in tmpfs (/run/) vanish on reboot. System boots into default state (potentially unsafe).
- If default is UNLOCKED and monitoring isn't ready yet → AGI can execute unwanted mutations.
- **Risk:** Initial state drift after reboot.
- **Mitigation:** Persistent storage for flags (/var/lib/). Default boot to safe state (LOCKED).

## Review Protocol

After building any autonomous system, run through these 4 categories:

1. **What can the sensor NOT see?** (Observer's Dilemma)
2. **Can the fix make things worse?** (Feedback Loop Contagion)
3. **Does healthy mean functional?** (Semantic Gap)
4. **What happens after reboot?** (State Persistence Gap)

Each category should produce at least one concrete mitigation. If you cannot mitigate, document the accepted risk.

## Source

Developed during arifOS Tier 1 Active Response implementation (2026-07-12). Applied to VPS watchdog architecture with smoketest + state machine + rollback + circuit breaker + dead-man switch.
