from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


def _float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return default


@dataclass(slots=True)
class Config:
    model_path: Path = Path("models/assistant.gguf")
    context_size: int = 8192
    threads: int = 8
    gpu_layers: int = 0
    temperature: float = 0.2
    max_tokens: int = 2048
    allow_shell: bool = False

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            model_path=Path(os.getenv("CODING_MODEL_PATH", "models/assistant.gguf")),
            context_size=_int("CODING_MODEL_CONTEXT", 8192),
            threads=_int("CODING_MODEL_THREADS", 8),
            gpu_layers=_int("CODING_MODEL_GPU_LAYERS", 0),
            temperature=_float("CODING_MODEL_TEMPERATURE", 0.2),
            max_tokens=_int("CODING_MODEL_MAX_TOKENS", 2048),
            allow_shell=os.getenv("CODING_MODEL_ALLOW_SHELL", "0").lower() in {"1", "true", "yes", "on"},
        )
