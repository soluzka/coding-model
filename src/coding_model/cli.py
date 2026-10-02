from __future__ import annotations
from pathlib import Path
import typer
from rich.console import Console
from rich.markdown import Markdown
from .agent import CodingAgent
from .config import Config
from .model import ModelRuntime
from .tools import Workspace

app=typer.Typer(name="coding-model",help="Full-purpose local AI coding assistant powered by assistant.gguf.")
console=Console()

@app.command()
def main(workspace:Path=typer.Option(Path("."),"--workspace","-w"),task:str|None=typer.Option(None,"--task","-t"))->None:
    config=Config.from_env(); root=workspace.resolve()
    console.print(f"[bold]Coding Model[/bold] — {root}")
    console.print(f"Model: {config.model_path}")
    try: runtime=ModelRuntime(config)
    except Exception as exc: raise typer.ClickException(str(exc)) from exc
    agent=CodingAgent(runtime,Workspace(root))
    if task:
        console.print(Markdown(agent.ask(task))); return
    console.print("Type 'exit' or 'quit' to leave.")
    while True:
        try: prompt=typer.prompt("\nYou")
        except (EOFError,KeyboardInterrupt): console.print(); break
        if prompt.strip().lower() in {"exit","quit"}: break
        if not prompt.strip(): continue
        try: console.print(Markdown(agent.ask(prompt)))
        except Exception as exc: console.print(f"[red]Error:[/red] {exc}")

if __name__=="__main__": app()
