import typer

app = typer.Typer()


@app.command(help="Generate a benchmark dataset from raw data")  # type: ignore
def generate() -> None:
    """
    Generate a benchmark dataset from raw data.
    """
    typer.echo("Generating datasets...")
