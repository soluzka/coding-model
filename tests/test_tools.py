from coding_model.tools import Workspace

def test_escape_is_rejected(tmp_path):
    w=Workspace(tmp_path)
    try: w.read_file("../outside.txt")
    except ValueError: return
    assert False

def test_write_read(tmp_path):
    w=Workspace(tmp_path); w.write_file("src/a.py","print(1)\n"); assert w.read_file("src/a.py")=="print(1)\n"
