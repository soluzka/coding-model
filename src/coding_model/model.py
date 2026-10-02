from __future__ import annotations

from typing import Iterator
from llama_cpp import Llama
from .config import Config

SYSTEM_PROMPT = """You are Coding Model, a general-purpose AI coding agent.

You work inside a user-selected repository. Help with programming, debugging,
architecture, refactoring, tests, documentation, build systems, and code review.
Do not invent file contents. Prefer small, reviewable changes and verify work
with tests or static checks when possible.
"""

class ModelRuntime:
    def __init__(self, config: Config):
        self.config = config
        if not config.model_path.exists():
            raise FileNotFoundError(f"GGUF model not found: {config.model_path}. Place assistant.gguf in models/ or set CODING_MODEL_PATH.")
        self.llm = Llama(model_path=str(config.model_path), n_ctx=config.context_size, n_threads=config.threads, n_gpu_layers=config.gpu_layers, verbose=False)

    def complete(self, messages: list[dict[str, str]]) -> str:
        result = self.llm.create_chat_completion(messages=messages, temperature=self.config.temperature, max_tokens=self.config.max_tokens)
        return result["choices"][0]["message"]["content"]

    def stream(self, messages: list[dict[str, str]]) -> Iterator[str]:
        result = self.llm.create_chat_completion(messages=messages, temperature=self.config.temperature, max_tokens=self.config.max_tokens, stream=True)
        for chunk in result:
            delta = chunk["choices"][0].get("delta", {}).get("content")
            if delta:
                yield delta
