import json
from rich.console import Console
from rich.table import Table

console = Console()

STYLES = {
    "success": "bold green",
    "info": "bold cyan",
    "warning": "yellow",
    "error": "bold red",
    "path": "underline",
    "header": "magenta",
    "url": "underline blue",
}


def display_probe_results_as_table(client):
    """Formats and prints probe results using a rich table."""
    console.print(f"✅ Platform Detected: [info]{client.platform_name}[/info]")
    console.print(f"ℹ️  Resolved Base URL: [{STYLES['url']}]{client.platform_url}[/{STYLES['url']}]")

    table = Table(title="Supported Capabilities")
    table.add_column("Feature", style=STYLES["header"], no_wrap=True)
    table.add_column("Supported", style=STYLES["info"])

    for key, value in client.capabilities.model_dump().items():
        table.add_row(key.replace("_", " ").title(), "✅" if value else "❌")

    console.print(table)


def display_probe_results_as_json(client, input_url):
    """Formats and prints probe results as a JSON object."""
    result = {
        "success": True,
        "input_url": input_url,
        "platform_name": client.platform_name,
        "base_url": client.platform_url,
        "capabilities": client.capabilities.model_dump(),
    }
    console.print(json.dumps(result, indent=2))


def display_error(message: str, is_json: bool = False):
    """Displays a formatted error message."""
    if is_json:
        console.print(json.dumps({"success": False, "error": message}, indent=2))
    else:
        console.print(f"❌ Error: {message}", style=STYLES["error"])
