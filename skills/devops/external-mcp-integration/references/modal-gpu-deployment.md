# Modal GPU Deployment — Serverless Inference for arifOS

Deploy GPU-backed MCP tools (image generation, ML inference) on Modal when the VPS has no local GPU.

## 5 Primitives

Every Modal GPU deployment needs these five components:

| # | Primitive | Role | Canonical Example |
|---|-----------|------|-------------------|
| 1 | `modal.Image` | Build environment: Python deps, system packages, code clone | Mage-Flow: torch 2.13, diffusers 0.38, transformers 5.5, CUDA 13 |
| 2 | `modal.Volume` | Persistent cache (model weights survive deploys) | `mage-model-cache` at `/cache` |
| 3 | `modal.Secret` | API keys passed at runtime | `hf-token` with `HF_TOKEN` |
| 4 | `@app.cls` + `@modal.enter()` | Class with lifecycle: `@modal.enter()` runs model download + warm-up at container start | `MageFlowInference` class |
| 5 | `@modal.fastapi_endpoint(method="POST")` | Web endpoint that accepts JSON body, returns JSON | `generate(body: dict)` |

## Modal API Deprecations (v1.5.3)

Modal moves fast. These were caught 2026-07-25:

| Deprecated | Replacement | Error |
|------------|-------------|-------|
| `container_idle_timeout` | `scaledown_window` | `DeprecationError: renamed on 2025-02-24` |
| `@modal.web_endpoint` | `@modal.fastapi_endpoint` | `DeprecationError: renamed on 2025-03-05` |
| `allow_concurrent_inputs` | `@modal.concurrent` decorator | `DeprecationError: deprecated on 2025-04-09` |
| Custom `__init__` with params | `@modal.enter()` + `modal.parameter()` | Warning only (2025-04-15), still works |

## flash-attn on Modal

**Do NOT install flash-attn on Modal.** It requires `nvcc` (CUDA compiler) at build time, which is not available in Modal's builder environment (GPU only at runtime). Mage-Flow falls back to standard PyTorch attention — the 4-step Turbo path is fast either way (~1s/image at 1024² on A10G).

If flash-attn is required, install CUDA toolkit in the build image first:
```python
.modal.Image.debian_slim()
.apt_install("cuda-toolkit-12-8")  # or equivalent
.pip_install("flash-attn")
```

## Model Caching Pattern

```python
MODEL_CACHE = modal.Volume.from_name("mage-model-cache", create_if_missing=True)
CACHE_DIR = "/cache"

@app.cls(volumes={CACHE_DIR: CACHE_DIR}, ...)
class Inference:
    @modal.enter()
    def load(self):
        from huggingface_hub import snapshot_download
        local = Path(CACHE_DIR) / model_name.replace("/", "--")
        if not (local / "model_index.json").exists():
            snapshot_download(model_name, local_dir=str(local),
                              local_dir_use_symlinks=False)
        self.pipe = LoadFrom(str(local))
```

## Cold Start

- **Image build**: ~60-120s first deploy (torch + CUDA packages)
- **Model download**: ~3-5 min first request (4B weights from HuggingFace)
- **Subsequent requests**: ~0.5-2s (model cached in Volume + warm container)
- **GPU queue**: Free tier (L40S) may queue — no SLA

## Endpoint Wire to MCP Server

The local FastMCP server (stdio) calls the Modal web endpoint via HTTP:

```python
@mcp.tool()
def mage_generate(prompt: str) -> dict:
    import httpx
    with httpx.Client(timeout=300.0) as client:
        resp = client.post(
            MODAL_ENDPOINT,  # set via env var or hardcoded
            json={"prompt": prompt, "width": 1024, "height": 1024, "steps": 4},
        )
    data = resp.json()
    # data["image_b64"] → save to disk
    return {"image_path": path, "image_b64": b64}
```

The MCP server's timeout must be ≥300s to handle Modal cold starts.
