import pyfiglet
import typer

from lazycodr.utils import console

from .config import app as config
from .pr import app as pr

app = typer.Typer()
app.add_typer(config, name="config")
app.add_typer(pr, name="pr")


def main():
    console.print(pyfiglet.figlet_format("LazyCodr", font="small"), style="bold green")
    console.print("💻 Welcome Lazy Coder 🚀", style="bold green")
    app()


if __name__ == "__main__":
    main()
