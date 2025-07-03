import typer

# Import commands & sub-commands
from .generate import app as generate_cmd

app = typer.Typer()

# Directly add sub-commands to the main app
app.add_typer(generate_cmd)


# Entry point function needed by the package installation
def main() -> None:
    """
    SATPLAN CLI - A command line interface for the SATPLAN toolbox.
    """
    app()
