from pathlib import Path
import typer
from rich.console import Console
from rich.markdown import Markdown
from .config import Config
from .model import ModelRuntime
from .agent import CodingAgent
from .tools import Workspace

app=typer.Typer(name="coding-model")
console=Console()

@app.command()
def main(workspace:Path=typer.Option(Path("."),"--workspace","-w"),task:str|None=typer.Option(None,"--task","-t")):
    config=Config.from_env(); root=workspace.resolve()
    console.print(f"[bold]Coding Model[/bold] {root}")
    try: agent=CodingAgent(ModelRuntime(config),Workspace(root))
    except Exception as exc: raise typer.ClickException(str(exc)) from exc
    if task: console.print(Markdown(agent.ask(task))); return
    while True:
        try: prompt=typer.prompt("You")
        except (EOFError,KeyboardInterrupt): break
        if prompt.strip().lower() in {"exit","quit"}: break
        if prompt.strip(): console.print(Markdown(agent.ask(prompt)))

if __name__=="__main__": app()
