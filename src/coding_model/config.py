from dataclasses import dataclass
from pathlib import Path
import os

def _int(name, default):
    try: return int(os.getenv(name, default))
    except ValueError: return default

def _float(name, default):
    try: return float(os.getenv(name, default))
    except ValueError: return default

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
    def from_env(cls):
        return cls(Path(os.getenv("CODING_MODEL_PATH", "models/assistant.gguf")), _int("CODING_MODEL_CONTEXT",8192), _int("CODING_MODEL_THREADS",8), _int("CODING_MODEL_GPU_LAYERS",0), _float("CODING_MODEL_TEMPERATURE",0.2), _int("CODING_MODEL_MAX_TOKENS",2048), os.getenv("CODING_MODEL_ALLOW_SHELL","0").lower() in {"1","true","yes","on"})
