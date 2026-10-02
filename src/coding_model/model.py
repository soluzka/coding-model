from llama_cpp import Llama
from .config import Config

SYSTEM_PROMPT = "You are Coding Model, a full-purpose repository coding agent. Help with programming, debugging, architecture, refactoring, tests, documentation, builds and code review. Never invent repository facts. Prefer small, reviewable changes and verification."

class ModelRuntime:
    def __init__(self, config: Config):
        if not config.model_path.exists():
            raise FileNotFoundError(f"GGUF model not found: {config.model_path}")
        self.config=config
        self.llm=Llama(model_path=str(config.model_path), n_ctx=config.context_size, n_threads=config.threads, n_gpu_layers=config.gpu_layers, verbose=False)

    def complete(self, messages):
        result=self.llm.create_chat_completion(messages=messages, temperature=self.config.temperature, max_tokens=self.config.max_tokens)
        return result["choices"][0]["message"]["content"]
