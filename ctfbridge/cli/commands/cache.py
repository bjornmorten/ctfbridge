import os
import typer
from datetime import datetime, timezone
from rich.table import Table
from ctfbridge.utils.platform_cache import CACHE_PATH, load_platform_cache
from ctfbridge.cli.ui import console, STYLES, display_error

app = typer.Typer(name="cache", help="Manage the platform detection cache.", no_args_is_help=True)


@app.command("view")
def cache_view():
    """Displays the contents of the platform cache."""
    cache = load_platform_cache()
    if not cache:
        console.print("ℹ️ Platform cache is empty.", style=STYLES["warning"])
        return

    table = Table(title="CTFBridge Platform Cache")
    table.add_column("Original URL", style="green")
    table.add_column("Detected Platform", style=STYLES["header"])
    table.add_column("Base URL", style=STYLES["info"])
    table.add_column("Cached At (UTC)", style=STYLES["warning"])

    for url, (platform, base_url, timestamp) in sorted(cache.items()):
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        table.add_row(url, platform, base_url, dt)

    console.print(table)


@app.command("clear")
def cache_clear():
    """Deletes the platform cache file."""
    try:
        if CACHE_PATH.exists():
            os.remove(CACHE_PATH)
            console.print("✅ Platform cache cleared.", style=STYLES["success"])
        else:
            console.print(
                "ℹ️ Platform cache does not exist. Nothing to do.", style=STYLES["warning"]
            )
    except Exception as e:
        display_error(f"Failed to clear cache: {e}")
        raise typer.Exit(code=1)


@app.command("path")
def cache_path():
    """Prints the absolute file path of the cache file."""
    console.print(str(CACHE_PATH.resolve()))
