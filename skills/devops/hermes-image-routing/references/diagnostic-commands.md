# Image Routing Diagnostic Commands

## Quick probe

```bash
# Find all image/vision-related config keys
grep -n 'supports_vision\|image_input_mode\|auxiliary.*vision' /root/HERMES/config.yaml

# Find the ghost key trap
# Line 14: agent.image_input_mode ← actually read by decide_image_input_mode()
# Line ~740: image_input_mode ← GHOST KEY (top-level, never read)

# Check what routing mode is configured
python3 -c "
from hermes_cli.config import load_config, cfg_get
cfg = load_config()
print('supports_vision:', cfg_get(cfg, 'model', 'supports_vision'))
print('agent.image_input_mode:', cfg_get(cfg, 'agent', 'image_input_mode'))
vc = cfg_get(cfg, 'auxiliary', 'vision', default={})
print('auxiliary.vision.provider:', vc.get('provider'))
print('auxiliary.vision.model:', vc.get('model'))
print('auxiliary.vision.base_url:', repr(vc.get('base_url', '')))
"

# Verify inherits from main provider config
python3 -c "
from hermes_cli.config import load_config, cfg_get
cfg = load_config()
p = cfg_get(cfg, 'providers', 'minimax', default={})
print('providers.minimax.api:', p.get('api'))
print('providers.minimax.key_env:', p.get('key_env'))
"
```

## Tracing the decision function

```bash
# Where decide_image_input_mode lives
grep -n 'def decide_image_input_mode\|def _supports_vision_override\|def _lookup_supports_vision\|def _explicit_aux_vision_override' /usr/local/lib/hermes-agent/agent/image_routing.py

# Gateway's wrapper
grep -n 'def _decide_image_input_mode\|def _enrich_message_with_vision' /usr/local/lib/hermes-agent/gateway/run.py

# vision_analyze_tool
grep -n 'def vision_analyze_tool' /usr/local/lib/hermes-agent/tools/vision_tools.py

# Task routing in auxiliary client
grep -n 'def async_call_llm\|def _resolve_task_provider_model' /usr/local/lib/hermes-agent/agent/auxiliary_client.py
```

## Verifying the active code path (text-mode routing)

```bash
grep -A3 'Text-mode routing' /usr/local/lib/hermes-agent/gateway/run.py
# Expected: calls _enrich_message_with_vision
# NOT expected: _pending_vision_model_overrides, _pending_native_image_paths
```

## Reading the config at runtime

The function at `agent/image_routing.py:432-434`:
```python
agent_cfg = cfg.get("agent") or {}
mode_cfg = _coerce_mode(agent_cfg.get("image_input_mode"))
```

Only `cfg["agent"]["image_input_mode"]` is read. Top-level `cfg["image_input_mode"]` is ignored.

## The override shortcut

`_supports_vision_override()` at line 180-207 checks `cfg["model"]["supports_vision"]` first. If present (true or false), it returns immediately — no provider metadata consulted.

## Log diagnostics on image failure

```bash
# Tail the gateway log for vision-related errors
journalctl -u hermes-asi-gateway -n 100 --no-pager | grep -i 'vision_analyze\|vision_tools\|enrich_message_with_vision\|auxiliary.*vision\|image routing\|IMAGE TRANSCRIPT\|Image routing'

# Watch live
journalctl -u hermes-asi-gateway -f --no-pager | grep -i 'vision\|image\|transcript'
```

## Verified on

- Hermes Agent commit: (insert current SHA)
- Config file: `/root/HERMES/config.yaml`
- Source root: `/usr/local/lib/hermes-agent/`
