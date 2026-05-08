import typer
from rich.console import Console

from repomind.config.settings import settings
from repomind.runtime.service import ask as runtime_ask
from pathlib import Path

app = typer.Typer()
console = Console()

@app.callback()
def main():
    pass

@app.command()
def ask(repo_path: str, question : str):
    repo = Path(repo_path)

    if not repo.exists():
        raise typer.BadParameter("Repository path does not exist")

    if not repo.is_dir():
        raise typer.BadParameter("Repository path must be a directory")

    if not question.strip():
        raise typer.BadParameter("Question must not be empty")

    answer = runtime_ask(repo_path, question, settings)
    console.print(answer)
