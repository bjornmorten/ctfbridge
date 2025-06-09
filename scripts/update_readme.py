#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

ROOT_DIR = Path(__file__).parent.parent
README_PATH = ROOT_DIR / "README.md"
QUICKSTART_PATH = ROOT_DIR / "examples/00_quickstart.py"
PLATFORMS_DIR = ROOT_DIR / "ctfbridge/platforms"


def get_platform_capabilities() -> Dict[str, Dict[str, bool]]:
    """
    Parses platform client files to extract their declared capabilities.

    Returns:
        A dictionary where keys are platform names and values are
        dictionaries of their capabilities (e.g., {'login': True}).
    """
    from ctfbridge.platforms.registry import PLATFORM_CLIENTS, get_platform_client
    from httpx import AsyncClient

    capabilities: Dict[str, Dict[str, bool]] = {}

    for platform in PLATFORM_CLIENTS.keys():
        client = get_platform_client(platform)
        client_instance = client(AsyncClient, "https://example.com")

        capabilities[client_instance.platform_name] = client_instance.capabilities

    return capabilities


def pad_cell(text, align, width):
    pad_count = width - len(text)
    nbsp = "&nbsp;"
    if align == "left":
        return text + nbsp * pad_count
    elif align == "center":
        left_pad = pad_count // 2
        right_pad = pad_count - left_pad
        return nbsp * left_pad + text + nbsp * right_pad
    else:
        return nbsp * pad_count + text


def generate_features_table(capabilities: Dict[str, Dict[str, bool]]) -> str:
    """
    Generates a Markdown table from the platform capabilities.

    Args:
        capabilities: A dictionary of platform capabilities.

    Returns:
        A Markdown-formatted string representing the features table.
    """
    headers = ["Platform", "Login", "Challenges", "Flags", "Scoreboard"]
    alignment = [":---", ":---:", ":---:", ":---:", ":---:"]

    max_len = max(len(h) for h in headers)

    padded_headers = [
        pad_cell(h, "left" if i == 0 else "center", max_len) for i, h in enumerate(headers)
    ]

    header_row = "| " + " | ".join(padded_headers) + " |"
    align_row = "| " + " | ".join(alignment) + " |"

    table = [header_row, align_row]

    for name, caps in sorted(capabilities.items()):
        row = [
            f"**{name}**",
            "✅" if caps.login else "❌",
            "✅" if caps.list_challenges else "❌",
            "✅" if caps.submit_flag else "❌",
            "✅" if caps.view_scoreboard else "❌",
        ]
        table.append("| " + " | ".join(row) + " |")

    table.append("|_More..._|🚧|🚧|🚧|🚧|")

    return "\n".join(table)


def update_section(file_path: Path, section_name: str, new_content: str) -> bool:
    """
    Updates a specific section in a file marked by start/end comments.

    Args:
        file_path: The path to the file to update.
        section_name: The name of the section (e.g., 'QUICKSTART').
        new_content: The new content to insert into the section.

    Returns:
        True if the file was changed, False otherwise.
    """
    start_marker = f"<!-- {section_name}_START -->"
    end_marker = f"<!-- {section_name}_END -->"

    content = file_path.read_text()

    pattern = re.compile(f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})", re.DOTALL)

    replacement = f"\\1\n{new_content}\n\\3"

    new_content_full, num_subs = re.subn(pattern, replacement, content)

    if num_subs > 0 and new_content_full != content:
        file_path.write_text(new_content_full)
        print(f"✅ Updated {section_name} section in {file_path.name}")
        return True

    print(f"ℹ️  No changes needed for {section_name} section in {file_path.name}")
    return False


def main():
    """
    Main function to update the README.md file.
    """
    print("🚀 Starting README update process...")

    changed = False

    # 1. Update Quickstart Example
    quickstart_code = QUICKSTART_PATH.read_text().strip()
    quickstart_md = f"```python\n{quickstart_code}\n```"
    changed |= update_section(README_PATH, "QUICKSTART", quickstart_md)

    # 2. Update Features Table
    platform_caps = get_platform_capabilities()
    features_table = generate_features_table(platform_caps)
    changed |= update_section(README_PATH, "PLATFORMS_TABLE", features_table)

    if changed:
        print("\n🎉 README.md was updated.")
    else:
        print("\n✨ README.md is already up to date.")


if __name__ == "__main__":
    main()
