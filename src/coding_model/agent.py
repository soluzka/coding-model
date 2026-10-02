import json
from .model import ModelRuntime, SYSTEM_PROMPT
from .tools import Workspace

class CodingAgent:
    def __init__(self,model:ModelRuntime,workspace:Workspace):
        self.model=model; self.workspace=workspace
        self.messages=[{"role":"system","content":SYSTEM_PROMPT}]
    def ask(self,prompt):
        context=json.dumps({"workspace":str(self.workspace.root),"git_status":self.workspace.git_status()},indent=2)
        self.messages.append({"role":"user","content":f"Repository context:\n{context}\n\nTask:\n{prompt}"})
        answer=self.model.complete(self.messages)
        self.messages.append({"role":"assistant","content":answer})
        return answer
