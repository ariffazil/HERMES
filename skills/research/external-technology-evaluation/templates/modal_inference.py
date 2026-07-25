"""
Modal Inference Scaffold Template
===================================
5 Modal primitives: Image · Volume · Secret · @app.cls · @enter() · @web_endpoint

Copy this file to /root/forge_work/references/<name>/ and customise:
  1. Image — Python deps, CUDA version, model-specific packages
  2. Model name — HuggingFace model ID
  3. GPU spec — adjust based on model VRAM requirements
  4. Request/Response schemas — align with model input/output

Usage:
  modal deploy <name>_modal.py    # → production endpoint
  modal run <name>_modal.py       # → dev test
"""

from __future__ import annotations

import io
import base64
import time
from pathlib import Path
from typing import Optional

import modal
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# 1. IMAGE — container definition
# ---------------------------------------------------------------------------

_image = (
    modal.Image.micromamba(python_version="3.11")
    .env({
        "HF_HOME": "/cache/huggingface",
        "HF_HUB_CACHE": "/cache/huggingface/hub",
        "TORCH_HOME": "/cache/torch",
        "XDG_CACHE_HOME": "/cache",
    })
    .micromamba_install(
        "cudatoolkit=12.4", "cudnn=9", channels=["conda-forge", "nvidia"]
    )
    .pip_install(
        "torch>=2.13.0",
        "torchvision>=0.28.0",
        "diffusers>=0.37.0",
        "transformers>=5.3.0,<5.6",
        "accelerate>=1.0.0",
        "einops>=0.8.0",
        "pydantic>=2.0",
        "pillow>=10.0",
        "safetensors>=0.4.0",
        "huggingface_hub>=0.20",
    )
    # flash-attn: build against installed torch, isolation OFF
    .run_commands(
        "pip install --no-build-isolation flash-attn==2.8.3",
        gpu="any",
    )
)

# ---------------------------------------------------------------------------
# 2. VOLUME — persistent model weight cache
# ---------------------------------------------------------------------------

_volume = modal.Volume.from_name(
    "<name>-weights", create_if_missing=True
)

# ---------------------------------------------------------------------------
# 3. SECRET — API keys
# ---------------------------------------------------------------------------

_secret = modal.Secret.from_name(
    "huggingface",  # create: modal secret create huggingface HF_TOKEN=...
    required=False,
)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = modal.App(
    name="<name>",
    image=_image,
    secrets=[_secret] if _secret else [],
)


# ---------------------------------------------------------------------------
# Request/Response schemas — CUSTOMISE per model
# ---------------------------------------------------------------------------

class Request(BaseModel):
    prompt: str
    # Add model-specific fields here


class Response(BaseModel):
    output_b64: str
    format: str = "png"
    inference_ms: int


# ---------------------------------------------------------------------------
# 4. @app.cls — Modal class with GPU
# ---------------------------------------------------------------------------

@app.cls(
    gpu="A100-40GB",           # adjust based on model VRAM
    container_idle_timeout=300, # 5 min → scale-to-zero (F1 AMANAH)
    volumes={"/cache": _volume},
    timeout=600,
    allow_concurrent_inputs=4,
)
class Inference:
    """
    Modal-deployed model inference.
    Primitives: @app.cls, @modal.enter(), @modal.web_endpoint
    """

    @modal.enter()
    def load(self):
        """
        Called ONCE per cold start.
        Weights auto-cached to /cache/huggingface via HF_HOME.
        """
        import sys
        sys.path.insert(0, "/root")

        t0 = time.perf_counter()
        # TODO: load your model here
        # self._pipe = YourPipeline.from_pretrained("model-id", device="cuda")
        self._model_id = "<model-id>"
        dt = time.perf_counter() - t0
        print(f"[{self._model_id}] Loaded in {dt:.1f}s")

    @modal.web_endpoint(method="POST", label="generate", docs=True)
    def generate(self, req: Request) -> Response:
        """Run inference and return base64-encoded output."""
        t0 = time.perf_counter()

        # TODO: run inference
        # output = self._pipe(req.prompt)

        dt = int((time.perf_counter() - t0) * 1000)
        # TODO: encode output to base64
        # buf = io.BytesIO(); output.save(buf, format="PNG")
        # b64 = base64.b64encode(buf.getvalue()).decode()

        return Response(
            output_b64="",  # replace with actual b64
            inference_ms=dt,
        )


# ---------------------------------------------------------------------------
# CLI entry point for `modal run`
# ---------------------------------------------------------------------------

@app.local_entrypoint()
def main():
    """modal run <name>_modal.py"""
    # TODO: Add test invocation
    pass
