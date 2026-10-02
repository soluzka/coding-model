from pathlib import Path
from coding_model.tools import Workspace

def test_workspace_rejects_path_escape(tmp_path: Path):
    workspace=Workspace(tmp_path)
    try: workspace.read_file("../outside.txt")
    except ValueError: pass
    else: raise AssertionError("workspace escape was not rejected")

def test_workspace_can_write_and_read(tmp_path: Path):
    workspace=Workspace(tmp_path)
    workspace.write_file("src/example.py","print('hello')\n")
    assert workspace.read_file("src/example.py")=="print('hello')\n"
