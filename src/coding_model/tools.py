from __future__ import annotations

import os
import subprocess
from pathlib import Path

class Workspace:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def _path(self, relative: str) -> Path:
        path = (self.root / relative).resolve()
        if path != self.root and self.root not in path.parents:
            raise ValueError("Path escapes the workspace.")
        return path

    def read_file(self, path: str) -> str:
        return self._path(path).read_text(encoding="utf-8", errors="replace")

    def write_file(self, path: str, content: str) -> str:
        target = self._path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Wrote {target.relative_to(self.root)}"

    def search(self, pattern: str, max_results: int = 100) -> list[str]:
        results=[]
        ignored={".git",".venv","venv","node_modules","__pycache__"}
        for path in self.root.rglob("*"):
            if len(results)>=max_results: break
            if not path.is_file() or any(part in ignored for part in path.parts): continue
            try: text=path.read_text(encoding="utf-8",errors="ignore")
            except OSError: continue
            if pattern.lower() in text.lower(): results.append(str(path.relative_to(self.root)))
        return results

    def git_status(self) -> str:
        return self._git(["status","--short"])

    def git_diff(self) -> str:
        return self._git(["diff","--"])

    def shell(self, command: str, allow: bool=False) -> str:
        if not allow: return "Shell execution is disabled. Set CODING_MODEL_ALLOW_SHELL=1 to enable it."
        completed=subprocess.run(command,cwd=self.root,shell=True,text=True,capture_output=True,timeout=120,env=os.environ.copy())
        return f"{(completed.stdout+completed.stderr).strip()}\n[exit code: {completed.returncode}]"

    def _git(self,args:list[str]) -> str:
        completed=subprocess.run(["git",*args],cwd=self.root,text=True,capture_output=True,timeout=30)
        return (completed.stdout+completed.stderr).strip()
