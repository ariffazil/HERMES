# Cross-System Telegram Group Audit

When the bot is in multiple groups, Hermes `config.yaml` and OpenClaw `openclaw.json` can drift apart. This reference documents the comprehensive audit technique.

## 5-Surface Audit (comprehensive)

Every group/user ID lives in multiple config surfaces. An audit must check ALL of them:

### OpenClaw surfaces (openclaw.json)
| Surface | Path | Purpose |
|---------|------|---------|
| `groups` | `channels.telegram.groups` | Group allowlist (bot accepts messages) |
| `bindings` | `bindings[].match.peer.id` | Agent routing (which agent processes messages) |
| `unmentionedInbound` | `messages.groupChat.unmentionedInbound` OR per-group `groups[id].unmentionedInbound` | `respond` = reply to all; `room_event` = only @mentioned. Per-group overrides global. |
| `allowFrom` | `channels.telegram.allowFrom` | DM user allowlist |
| `groupAllowFrom` | `channels.telegram.groupAllowFrom` | Users who bypass @mention in groups |

### Hermes surfaces (config.yaml)
| Surface | Path | Purpose |
|---------|------|---------|
| `allowed_chats` | `telegram.allowed_chats` | Group allowlist (bot accepts messages) |
| `free_response_chats` | `telegram.free_response_chats` | Groups/users where bot responds without @mention |

## Audit Script

```python
import json, yaml, subprocess, os

# Load configs
with open('/root/.openclaw/openclaw.json') as f:
    oc = json.load(f)
with open('/root/.hermes/config.yaml') as f:
    hm = yaml.safe_load(f)

# Extract all surfaces
oc_groups = set(oc.get('channels',{}).get('telegram',{}).get('groups',{}).keys())
oc_binding_ids = {
    b['match']['peer']['id']
    for b in oc.get('bindings',[])
    if 'peer' in b.get('match',{})
}
oc_allow_from = set(oc.get('channels',{}).get('telegram',{}).get('allowFrom',[]))
oc_group_allow = set(oc.get('channels',{}).get('telegram',{}).get('groupAllowFrom',[]))

hm_chats = hm.get('telegram',{}).get('allowed_chats',[])
if isinstance(hm_chats, str):
    hm_chats = [c.strip() for c in hm_chats.split(',') if c.strip()]
hm_allowed = set(str(c) for c in (hm_chats or []))

hm_free = hm.get('telegram',{}).get('free_response_chats',[])
if isinstance(hm_free, str):
    hm_free = [c.strip() for c in hm_free.split(',') if c.strip()]
hm_free_set = set(str(c) for c in (hm_free or []))

# Find all unique group IDs
all_groups = oc_groups | oc_binding_ids | hm_allowed

print("=" * 60)
print("CROSS-SYSTEM TELEGRAM GROUP AUDIT")
print("=" * 60)

for gid in sorted(all_groups):
    is_group = gid.startswith('-')
    if not is_group:
        continue  # skip user IDs for group table

    in_oc_groups = gid in oc_groups
    in_oc_bindings = gid in oc_binding_ids
    in_hm_allowed = gid in hm_allowed
    in_hm_free = gid in hm_free_set

    gaps = []
    if in_oc_groups and not in_oc_bindings:
        gaps.append("⚠️ OC groups but NO binding — messages silently dropped")
    if in_oc_groups and not in_hm_allowed:
        gaps.append("⚠️ OC only (not in Hermes allowed_chats)")
    if in_hm_allowed and not in_oc_groups:
        gaps.append("⚠️ Hermes only (not in OC groups)")
    if in_hm_allowed and not in_oc_bindings:
        gaps.append("⚠️ Hermes but no OC binding")

# Also check unmentionedInbound globally AND per-group
unmentioned_global = oc.get('messages',{}).get('groupChat',{}).get('unmentionedInbound','NOT SET')
oc_group_configs = oc.get('channels',{}).get('telegram',{}).get('groups',{})
print(f"\n⚙️  unmentionedInbound (global): {unmentioned_global}")
if unmentioned_global == 'room_event':
    print("   ⚠️ Bot only responds to @mentioned messages (set to 'respond' to reply to all)")
elif unmentioned_global == 'respond':
    print("   ✅ Bot responds to ALL messages in allowed groups")

# Check per-group overrides
for gid in sorted(oc_groups):
    gcfg = oc_group_configs.get(gid, {})
    per_group = gcfg.get('unmentionedInbound', 'inherit')
    if per_group != 'inherit':
        print(f"   {gid}: per-group unmentionedInbound = {per_group}")

    status = "✅" if not gaps else "🔴"
    print(f"\n{status} {gid}")
    print(f"   OC groups: {'✅' if in_oc_groups else '❌'}  OC bindings: {'✅' if in_oc_bindings else '❌'}  Hermes allowed: {'✅' if in_hm_allowed else '❌'}  Hermes free: {'✅' if in_hm_free else '❌'}")
    for g in gaps:
        print(f"   {g}")

# DM users
print("\n" + "=" * 60)
print("DM USERS")
print("=" * 60)
all_users = oc_allow_from | hm_free_set
for uid in sorted(all_users):
    in_oc = uid in oc_allow_from
    in_hm_free = uid in hm_free_set
    in_hm_allowed = uid in hm_allowed
    print(f"  {uid}: OC allowFrom={'✅' if in_oc else '❌'}  Hermes free={'✅' if in_hm_free else '❌'}")

# Summary
only_in_groups = oc_groups - oc_binding_ids
unmentioned = oc.get('messages',{}).get('groupChat',{}).get('unmentionedInbound','NOT SET')
print(f"\n🔴 Groups WITHOUT bindings: {only_in_groups or 'none'}")
print(f"🔴 In Hermes but not OC: {(hm_allowed - oc_groups) or 'none'}")
print(f"🔴 In OC but not Hermes: {(oc_groups - hm_allowed) or 'none'}")
print(f"⚙️  unmentionedInbound: {unmentioned}")
if unmentioned == 'room_event':
    print(f"   ⚠️ Bot silent unless @mentioned — change to 'respond' for free-reply groups")
print(f"\nFull fix requires 5 layers: OC groups + OC bindings + unmentionedInbound=respond + Hermes allowed_chats + Hermes free_response_chats")
```

## Telegram Bot API Name Resolution

After extracting IDs, resolve them to human-readable names:

```bash
source /root/.secrets/vault.env 2>/dev/null

for gid in <group_ids>; do
    echo "=== $gid ==="
    curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChat?chat_id=$gid" | \
        python3 -c "
import json,sys
d=json.load(sys.stdin)
if d.get('ok'):
    r=d['result']
    print(f'  Title: {r.get(\"title\",\"N/A\")}')
    print(f'  Type: {r.get(\"type\",\"N/A\")}')
    print(f'  Forum: {r.get(\"is_forum\",False)}')
else:
    print(f'  ERROR: {d.get(\"description\",\"unknown\")}')
"
    curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChatMemberCount?chat_id=$gid" | \
        python3 -c "import json,sys; d=json.load(sys.stdin); print(f'  Members: {d[\"result\"]}') if d.get('ok') else None"
    echo
done
```

## Gap Types and Fixes

| Gap | Symptom | Fix |
|-----|---------|-----|
| Group in OC `groups` but no `binding` | Messages accepted but unrouted (silent) | Add binding entry to `bindings[]` |
| OC `unmentionedInbound: room_event` | Bot only processes @mentioned messages | Set to `respond` (global or per-group) if bot should reply to all |
| OC per-group `unmentionedInbound` unset | Group inherits global setting | Set per-group `unmentionedInbound: "respond"` in `groups[id]` for selective control |
| Group in OC but not Hermes | Bot responds via OC only, not Hermes | Add to `telegram.allowed_chats` in config.yaml |
| Group in Hermes but not OC | Bot responds via Hermes only, not OC | Add to `channels.telegram.groups` + `bindings` in openclaw.json |
| Group in Hermes `allowed_chats` but not `free_response_chats` | Bot needs @mention (if `require_mention: true`) | Add to `telegram.free_response_chats` |
| User in OC `allowFrom` but not Hermes `free_response` | OC allows DM, Hermes needs @mention | Add to `telegram.free_response_chats` |
| User in Hermes `free_response` but not OC `allowFrom` | Hermes allows DM, OC blocks | Add to `channels.telegram.allowFrom` |

## Three-Level Verification (after adding groups)

| Level | Command | Pass condition |
|-------|---------|---------------|
| Config present | `grep <group_id> ~/.hermes/config.yaml` | ID appears in `allowed_chats` |
| Bot membership | `curl -s "https://api.telegram.org/bot${TOKEN}/getChat?chat_id=<id>" \| jq .ok` | `true` |
| Can send | `curl -s "https://api.telegram.org/bot${TOKEN}/sendMessage" -d chat_id=<id> -d text="🟢 test" \| jq .ok` | `true` |

## Key Facts

- Both Hermes and OpenClaw use the **same bot token** (`ASI_ARIFOS_BOT_TOKEN` / `@AGI_ASI_bot`)
- Bot membership is per-token, not per-config — if the bot is in a group, both systems can reach it
- The gap is always in **config allowlists**, not bot membership
- **5 layers required for "bot replies to everything, no @mention":**
  1. OC `channels.telegram.groups` — group allowlist
  2. OC `bindings[]` — agent routing
  3. OC `unmentionedInbound` = `respond` (per-group or global)
  4. Hermes `telegram.allowed_chats` — group allowlist
  5. Hermes `telegram.free_response_chats` OR `require_mention: false` — bypass @mention
- Hermes controls access via `allowed_chats` (YAML list or comma-separated string)
- OpenClaw controls access via `channels.telegram.groups` (JSON object of group IDs)
- `free_response_chats` in Hermes = bot responds without @mention (same as `groupAllowFrom` in OC)
- `bindings` in OpenClaw = agent routing — without it, accepted messages have no agent to process them
- `unmentionedInbound` = `room_event` means bot only processes @mentioned messages; `respond` means bot replies to ALL messages in allowed groups

## Decision Framework: Should a group be `free_response`?

**`free_response` = bot responds to ALL messages without @mention.** Use sparingly:

| Group type | `free_response`? | Reason |
|-----------|-----------------|--------|
| Arif's DM | ✅ Always | Sovereign — bot should always respond |
| AAA (tech ops) | ✅ Recommended | Arif talks freely, agents @mention each other |
| Family groups | ⚠️ Ask first | Bot responding to every family message is noisy |
| Large groups | ❌ No | Bot would respond to everyone — use @mention |

**Always present the gap analysis and ask before enabling `free_response` on new groups.**
