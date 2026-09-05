from typer import Typer

from . import getter, runner

app = Typer()

@app.command()
def get() -> None:
    getter.get()

@app.command()
def run(debug: bool = False) -> None:
    runner.run(debug)
