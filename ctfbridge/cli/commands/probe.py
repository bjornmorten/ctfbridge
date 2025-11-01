import asyncio
import json
import logging

import typer

from ctfbridge import create_client
from ctfbridge.cli.ui import (
    STYLES,
    console,
    display_error,
    display_probe_results_as_json,
    display_probe_results_as_table,
)
from ctfbridge.exceptions import CTFBridgeError, UnknownPlatformError

app = typer.Typer(
    name="probe",
    help="Analyzes a URL to detect the CTF platform and its capabilities.",
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def probe(
    url: str = typer.Argument(..., help="The URL of the CTF platform to probe."),
    as_json: bool = typer.Option(False, "--json", help="Output the results in JSON format."),
    insecure: bool = typer.Option(
        False,
        "--insecure",
        help="Ignore TLS certificate validation errors (use with caution).",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug logging for troubleshooting.",
    ),
):
    """Analyzes a URL to detect the CTF platform and its capabilities."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    http_config = {"verify_ssl": False} if insecure else None

    with console.status(f"[bold green]Probing {url}...[/bold green]", spinner="dots"):
        try:
            client = asyncio.run(create_client(url, http_config=http_config))
        except UnknownPlatformError as e:
            if as_json:
                console.print(json.dumps({"success": False, "error": str(e)}, indent=2))
            else:
                console.print(f"❌ Error: {e}", style=STYLES["error"])
                console.print(
                    "\nThis could be because the URL is incorrect or the platform is not yet supported.",
                    style=STYLES["info"],
                )
                console.print("\n[bold]What you can do:[/bold]")
                console.print("  1. Double-check the URL and ensure the site is accessible.")
                console.print(
                    "  2. If you know the platform, you can try specifying it manually in your script."
                )
                console.print(
                    "  3. To report an error or request support for this platform, please open an issue on GitHub:",
                    style="default",
                )
                console.print(
                    "     [underline blue]https://github.com/bjornmorten/ctfbridge/issues[/underline blue]"
                )
            raise typer.Exit(code=1)
        except CTFBridgeError as e:
            display_error(str(e), is_json=as_json)
            raise typer.Exit(code=1)

    if as_json:
        display_probe_results_as_json(client, input_url=url, insecure=insecure)
    else:
        display_probe_results_as_table(client, insecure=insecure)
