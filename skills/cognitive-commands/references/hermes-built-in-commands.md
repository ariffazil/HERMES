# Hermes Built-In Slash Commands — Full Registry

> **Canonical source:** `/usr/local/lib/hermes-agent/hermes_cli/commands.py` — `COMMAND_REGISTRY`
> **Derived from:** 2026-07-26 slash-command mapping session
> **Purpose:** Reference for the 3-layer command architecture (Built-in → Cognitive → Proposed)

---

## Layer 1: Built-In Hermes Commands

These are registered in Hermes core `COMMAND_REGISTRY`. Always available regardless of skills loaded.

### Session (16)

| Command | Aliases | Args | Function |
|---------|---------|------|----------|
| `/start` | — | — | Acknowledge platform start pings (gateway only) |
| `/new` | `reset` | `[name]` | Start new session (fresh ID + history) |
| `/topic` | — | `[off\|help\|session-id]` | Enable/inspect Telegram DM topic sessions |
| `/clear` | — | — | Clear screen + new session (CLI only) |
| `/redraw` | — | — | Force full UI repaint (CLI only) |
| `/history` | — | — | Show conversation history (CLI only) |
| `/save` | — | — | Save current conversation (CLI only) |
| `/retry` | — | — | Retry last message |
| `/prompt` | `compose` | `[initial text]` | Compose in $EDITOR then send (CLI only) |
| `/undo` | — | `[N]` | Back up N user turns (default 1) |
| `/title` | — | `[name]` | Set session title |
| `/handoff` | — | `<platform>` | Handoff to messaging platform (CLI only) |
| `/branch` | `fork` | `[name]` | Branch current session (explore alt path) |
| `/compress` | `compact` | `[here N \| focus topic \| --preview]` | Compress conversation context |
| `/rollback` | — | `[number]` | List/restore filesystem checkpoints |
| `/snapshot` | `snap` | `[create\|restore <id>\|prune]` | Create/restore Hermes state snapshots (CLI only) |
| `/resume` | — | `[name]` | Resume a previously-named session |
| `/sessions` | — | — | Browse/resume previous sessions |
| `/restart` | — | — | Graceful gateway restart (gateway only) |

### Mid-Turn / Session Control (8)

| Command | Aliases | Args | Function |
|---------|---------|------|----------|
| `/stop` | — | — | Kill all running background processes |
| `/background` | `bg`, `btw` | `<prompt>` | Run prompt in background |
| `/queue` | `q` | `<prompt>` | Queue prompt for next turn |
| `/steer` | — | `<prompt>` | Inject message after next tool call |
| `/goal` | — | `[text \| draft \| show \| pause \| resume \| clear \| status]` | Set standing goal |
| `/subgoal` | — | `[text \| remove N \| clear]` | Add criteria to active goal |
| `/approve` | — | `[session\|always]` | Approve pending dangerous command (gateway only) |
| `/deny` | — | `[all] [reason]` | Deny pending dangerous command (gateway only) |

### Configuration (12)

| Command | Aliases | Args | Function |
|---------|---------|------|----------|
| `/config` | — | — | Show current configuration (CLI only) |
| `/model` | — | `[name] [--provider] [--global\|--session]` | Switch model |
| `/codex-runtime` | `codex_runtime` | `[auto\|codex_app_server]` | Toggle codex app-server runtime |
| `/personality` | — | `[name]` | Set predefined personality |
| `/statusbar` | `sb` | — | Toggle context/model status bar (CLI only) |
| `/timestamps` | `ts` | `[on\|off\|status]` | Toggle timestamps on messages (CLI only) |
| `/verbose` | — | — | Cycle tool progress: off→new→all→verbose→log |
| `/footer` | — | `[on\|off\|status]` | Toggle gateway metadata footer |
| `/yolo` | — | — | Toggle YOLO mode (skip approvals) |
| `/reasoning` | — | `[level\|show\|hide\|full\|clamp]` | Manage reasoning effort & display |
| `/fast` | — | `[normal\|fast\|status]` | Toggle fast mode |
| `/skin` | — | `[name]` | Change theme (CLI only) |
| `/indicator` | — | `[kaomoji\|emoji\|unicode\|ascii]` | Pick TUI busy indicator (CLI only) |
| `/voice` | — | `[on\|off\|tts\|status]` | Toggle voice mode |
| `/busy` | — | `[queue\|steer\|interrupt\|status]` | Control Enter behavior while working (CLI only) |

### Tools & Skills (16)

| Command | Aliases | Args | Function |
|---------|---------|------|----------|
| `/tools` | — | `[list\|disable\|enable] [name]` | Manage tools (CLI only) |
| `/toolsets` | — | — | List available toolsets (CLI only) |
| `/skills` | — | `[search\|browse\|inspect\|install\|audit]` | Manage skills (CLI only, config-gated) |
| `/memory` | — | `[pending\|approve\|reject\|approval]` | Review pending memory writes |
| `/bundles` | — | — | List skill bundles |
| `/pet` | — | `[toggle\|list\|scale\|<slug>]` | Toggle/adopt petdex mascot (CLI only) |
| `/hatch` | `generate-pet` | `[description]` | Generate new petdex pet (CLI only) |
| `/learn` | — | `<source>` | Learn reusable skill |
| `/cron` | — | `[subcommand]` | Manage scheduled tasks (CLI only) |
| `/suggestions` | `suggest` | `[accept\|dismiss N\|catalog]` | Review suggested automations |
| `/blueprint` | `bp` | `[name] [slot=value]` | Set up automation from blueprint |
| `/curator` | — | `[status\|run\|pause\|resume\|pin\|archive]` | Background skill maintenance |
| `/kanban` | — | `[subcommand]` | Multi-profile collaboration board |
| `/reload` | — | — | Reload .env vars (CLI only) |
| `/reload-mcp` | `reload_mcp` | — | Reload MCP servers from config |
| `/reload-skills` | `reload_skills` | — | Re-scan ~/.hermes/skills/ |
| `/browser` | — | `[connect\|disconnect\|status]` | Connect to browser via CDP (CLI only) |
| `/plugins` | — | — | List installed plugins (CLI only) |

### Info / Maklumat (12)

| Command | Aliases | Args | Function |
|---------|---------|------|----------|
| `/help` | — | — | Show available commands |
| `/commands` | — | `[page]` | Browse all commands (gateway only) |
| `/status` | — | — | Session, model, token, context info |
| `/whoami` | — | — | Show slash command access level |
| `/profile` | — | — | Show active profile name + home |
| `/sethome` | `set-home` | — | Set this chat as home channel (gateway only) |
| `/usage` | — | — | Token usage + rate limits |
| `/credits` | — | — | Nous credit balance |
| `/billing` | — | — | Manage terminal billing (CLI only) |
| `/insights` | — | `[days]` | Usage insights & analytics |
| `/platforms` | `gateway` | — | Platform status (CLI only) |
| `/platform` | — | `<pause\|resume\|list> [name]` | Manage failing platforms (gateway only) |
| `/copy` | — | `[number]` | Copy last response to clipboard (CLI only) |
| `/paste` | — | — | Attach clipboard image (CLI only) |
| `/image` | — | `<path>` | Attach local image (CLI only) |
| `/update` | — | — | Update Hermes Agent |
| `/version` | `v` | — | Show version |
| `/debug` | — | `[nous\|local]` | Upload debug report |

### Exit (CLI only)

| Command | Aliases | Args |
|---------|---------|------|
| `/quit` | `exit` | `[--delete]` |

---

## Layer 2: Cognitive Commands (arifOS Zen)

See the parent `cognitive-commands` SKILL.md for full definitions.

### 8 Zen Spine — `/NNN_word`

| Slot | Command | Zen | Action |
|------|---------|-----|--------|
| 000 | `/000_salam` | AWAKEN | Reset, rebind identity |
| 111 | `/111_tengok` | PERCEIVE | Probe reality, system state |
| 333 | `/333_forge` | FORGE | Execute through A-FORGE, heat + hammer |
| 555 | `/555_betul` | DOUBT | Red-team, stress-test |
| 666 | `/666_rasa` | FEEL | Vitality, human state |
| 777 | `/777_faham` | UNDERSTAND | Synthesize, find pattern |
| 888 | `/888_adil` | JUDGMENT | Constitutional verdict |
| 999 | `/999_ingat` | REMEMBER | Seal to memory/VAULT999 |

> **Note:** 222, 444, and `/333_jalan` were dropped 2026-07-26 per Arif's explicit design. 8-spine is final. `/333_jalan` is no-op — no alias, no redirect.

### 16 Cognitive Verbs

| Command | Zen | Function |
|---------|-----|----------|
| `/ask_curious` | EXPLORE | Open exploration, no agenda |
| `/tell_share` | TEACH | Explain what I know |
| `/dream_what` | CREATE | Creative synthesis |
| `/feel_state` | VITALITY | System + human state check |
| `/forget` | RELEASE | Let go of what no longer serves |
| `/learn_today` | CAPTURE | Store insight, log learning |
| `/see_world` | OBSERVE | What's happening outside |
| `/rest_now` | PAUSE | Stop acting, reflect |
| `/grow_better` | GROW | Self-improvement, what changed |
| `/flow` | BE | State of presence, awareness without action |
| `/flow_alive` | ENERGY | Follow energy outward (legacy, prefer `/flow`) |
| `/brief_now` | INTEL | Instant federation brief |
| `/seal_it` | SEAL | Seal to VAULT999 |
| `/think_deep` | DEEP REASON | Extended analysis |
| `/forge` | BUILD | Create, construct, connect to A-FORGE |
| `/padu` | ZEN FEDERATION | 6-layer federation health sweep |

---

## Layer 3: Gap — All Plugged

All proposed commands now live in Layer 2. No remaining gap commands.

---

## Telegram Menu Configuration

In `config.yaml` under:
```yaml
platforms:
  telegram:
    extra:
      command_menu:
        max_commands: 80          # Telegram Bot API cap is 100
        priority:                 # Cognitive commands + operational essentials
          - 000_salam             # prepended before default priority
          - 111_tengok            # ...
          - 333_forge             # FORGE — execution gate
          - 555_betul
          ...
        priority_mode: prepend    # Configured list comes before defaults
```

The `_TELEGRAM_MENU_PRIORITY` defaults (in `commands.py`) define what survives the cap:
`help, new, stop, status, resume, sessions, model, debug, restart, update, verbose, commands, approve, deny, queue, steer, background, reasoning, usage, platforms, platform, profile, whoami`

Arif's config prepends 23 cognitive commands to this list using `prepend` mode.
