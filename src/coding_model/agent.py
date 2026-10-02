from __future__ import annotations
import json
from .model import ModelRuntime, SYSTEM_PROMPT
from .tools import Workspace

class CodingAgent:
    """Repository-aware coding assistant."""
    def __init__(self, model: ModelRuntime, workspace: Workspace):
        self.model=model
        self.workspace=workspace
        self.messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"system","content":f"Current workspace: {workspace.root}"}]

    def context_snapshot(self) -> str:
        return json.dumps({"workspace":str(self.workspace.root),"git_status":self.workspace.git_status()},indent=2)

    def ask(self,prompt:str)->str:
        enriched=f"Repository context:\n{self.context_snapshot()}\n\nUser task:\n{prompt}"
        self.messages.append({"role":"user","content":enriched})
        answer=self.model.complete(self.messages)
        self.messages.append({"role":"assistant","content":answer})
        return answer
