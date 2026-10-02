# Coding Model

Coding Model is a full-purpose local AI coding assistant built around a GGUF model such as `assistant.gguf`.

## Vision

This is intended to become a repository-level coding agent, not just autocomplete. It will understand projects, inspect source, search symbols, edit files, run tests, diagnose failures, review diffs, and iterate on coding tasks.

## Architecture

Model runtime -> Coding agent -> Workspace tools -> CLI / API / IDE interfaces

The model runtime uses llama.cpp through `llama-cpp-python`. The first release keeps orchestration explicit so the runtime is predictable; structured model tool calling will be added next.

## Model

Place `assistant.gguf` at `models/assistant.gguf`, or set `CODING_MODEL_PATH` to another GGUF file. Model weights are ignored by Git.

## Install

Python 3.11+ is recommended.

    python -m venv .venv
    .venv\\Scripts\\activate
    pip install -e .

## Run

    coding-model
    coding-model --workspace C:\\path\\to\\project
    coding-model --workspace . --task "Analyze the authentication system and identify likely bugs"

## Configuration

`CODING_MODEL_CONTEXT` controls context size, `CODING_MODEL_THREADS` controls CPU threads, `CODING_MODEL_GPU_LAYERS` controls llama.cpp GPU offload, `CODING_MODEL_TEMPERATURE` controls generation temperature, and `CODING_MODEL_MAX_TOKENS` controls output length.

Shell execution is disabled by default. Enable it explicitly with `CODING_MODEL_ALLOW_SHELL=1`.

## Roadmap

- Structured GGUF tool calling
- Streaming responses
- File-aware context retrieval
- Repository indexing and symbol search
- Automatic test/run/fix loops
- Patch-based editing
- Persistent project memory
- MCP support
- REST/WebSocket API
- VS Code integration
- Multiple local model profiles
- GPU backend auto-detection
