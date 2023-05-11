import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

app = typer.Typer()

console = Console()


@app.command()
def credentials(
    openai_api_key: Annotated[str, typer.Option(prompt=True, hide_input=True)],
    github_token: Annotated[str, typer.Option(prompt=True, hide_input=True)],
):
    # Save credentials to file json
    credentials = {
        "openai_api_key": openai_api_key,
        "github_token": github_token,
    }
    with open(Path.home() / ".lazy-coder-credentials.json", "w") as outfile:
        json.dump(credentials, outfile)

    console.print("Credentials saved", style="bold green")


if __name__ == "__main__":
    app()
