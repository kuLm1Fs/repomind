import typer
from rich.console import Console

from repomind.config.settings import settings
from repomind.runtime.service import ask as runtime_ask

app = typer.Typer()
console = Console()

@app.callback()
def main():
    pass

@app.command()
def ask(repo_path: str, question : str):
    answer = runtime_ask(repo_path, question, settings)
    console.print(answer)
