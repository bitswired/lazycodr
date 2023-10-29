import pyfiglet
import typer
from rich.console import Console

from .config import app as config
from .pr import app as pr
from .readme import app as readme

console = Console()

app = typer.Typer()
app.add_typer(config, name="config")
app.add_typer(pr, name="pr")
app.add_typer(readme, name="readme")


def main():
    console.print(pyfiglet.figlet_format("LazyCodr", font="small"), style="bold green")
    console.print("💻 Welcome Lazy Coder 🚀", style="bold green")
    app()


if __name__ == "__main__":
    main()
