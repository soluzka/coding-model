from pathlib import Path
import os, subprocess

class Workspace:
    def __init__(self, root: Path): self.root=root.resolve()
    def _path(self, relative):
        path=(self.root/relative).resolve()
        if path != self.root and self.root not in path.parents: raise ValueError("Path escapes the workspace")
        return path
    def read_file(self,path): return self._path(path).read_text(encoding="utf-8",errors="replace")
    def write_file(self,path,content):
        target=self._path(path); target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content,encoding="utf-8"); return str(target.relative_to(self.root))
    def search(self,pattern,max_results=100):
        out=[]; ignored={".git",".venv","venv","node_modules","__pycache__"}
        for p in self.root.rglob("*"):
            if len(out)>=max_results: break
            if not p.is_file() or any(x in ignored for x in p.parts): continue
            try: text=p.read_text(encoding="utf-8",errors="ignore")
            except OSError: continue
            if pattern.lower() in text.lower(): out.append(str(p.relative_to(self.root)))
        return out
    def git_status(self): return self._git(["status","--short"])
    def git_diff(self): return self._git(["diff","--"])
    def shell(self,command,allow=False):
        if not allow: return "Shell execution is disabled; set CODING_MODEL_ALLOW_SHELL=1 to enable it."
        r=subprocess.run(command,cwd=self.root,shell=True,text=True,capture_output=True,timeout=120,env=os.environ.copy())
        return r.stdout+r.stderr+f"\n[exit code: {r.returncode}]"
    def _git(self,args):
        r=subprocess.run(["git",*args],cwd=self.root,text=True,capture_output=True,timeout=30); return r.stdout+r.stderr
