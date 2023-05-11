import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

from lazycodr.utils import generate_pr, get_pr_diff

console = Console()


app = typer.Typer()


@app.command()
def generate(repo_name: str, pr_number: int):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        pr_template = typer.edit()
        progress.add_task(description="Getting diff...", total=None)
        pr_diff = get_pr_diff(repo_name, pr_number)
        progress.add_task(description="Generating PR description...", total=None)
        res = generate_pr(pr_diff, pr_template)
        md = Markdown(res)
        console.print(md, width=90)


if __name__ == "__main__":
    app()
