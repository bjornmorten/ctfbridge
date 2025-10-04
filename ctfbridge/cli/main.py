from typing import Optional

import typer

from ctfbridge.cli.commands import cache, platforms, probe
from ctfbridge.cli.ui import console

app = typer.Typer(
    name="ctfbridge-cli",
    help="A utility for managing and diagnosing the ctfbridge library.",
    add_completion=False,
    no_args_is_help=True,
)

app.command(name="platforms")(platforms.platforms)
app.command(name="probe")(probe.probe)
app.add_typer(cache.app)


def version_callback(value: bool):
    """Callback function to handle the --version flag."""
    if value:
        try:
            from importlib.metadata import version

            pkg_version = version("ctfbridge")
        except Exception:
            pkg_version = "unknown (is the package installed?)"
        console.print(f"ctfbridge library version: {pkg_version}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the library version and exit.",
    ),
):
    """
    CTFBridge CLI: A utility for library diagnostics and management.
    """
    pass


if __name__ == "__main__":
    app()
