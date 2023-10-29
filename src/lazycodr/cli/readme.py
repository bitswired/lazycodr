from pathlib import Path

import typer
from rich.console import Console

from lazycodr.utils.readme import generate_readme

console = Console()


app = typer.Typer()


@app.command()
def generate(
    repo_path: Path,
    ignore: list[str] = typer.Option([]),
):
    readme = generate_readme(repo_path, ignore)
    typer.echo(readme)


if __name__ == "__main__":
    app()
