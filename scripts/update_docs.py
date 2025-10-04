#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from httpx import AsyncClient

from ctfbridge.models.capability import Capabilities
from ctfbridge.platforms.registry import PLATFORM_CLIENTS, get_platform_client

# --- Configuration ---
ROOT_DIR = Path(__file__).parent.parent
README_PATH = ROOT_DIR / "README.md"
PLATFORMS_DOC_PATH = ROOT_DIR / "docs/getting-started/platforms.md"
QUICKSTART_PATH = ROOT_DIR / "examples/00_quickstart.py"

PLATFORM_METADATA = {
    "CTFd": {
        "id": "ctfd",
        "description": "A popular open-source CTF platform. [Visit CTFd.io](https://ctfd.io/) or [view on GitHub](https://github.com/CTFd/CTFd).",
    },
    "rCTF": {
        "id": "rctf",
        "description": "A open-source CTF platform developed by [redpwn](https://redpwn.net/). [View on GitHub](https://github.com/otter-sec/rctf).",
    },
    "GZCTF": {
        "id": "gzctf",
        "description": "A open-source CTF platform developed by [GZTimeWalker](https://github.com/GZTimeWalker). [View on GitHub](https://github.com/GZTimeWalker/GZCTF).",
    },
    "Berg": {
        "id": "berg",
        "description": "A closed-source CTF platform developed by [NoRelect](https://github.com/NoRelect/).",
    },
    "EPT": {
        "id": "ept",
        "description": "A closed-source CTF platform developed by [Equinor Pwn Team](https://x.com/ept_gg).",
    },
    "HTB": {
        "id": "htb",
        "description": "Hack The Box's platform for Jeopardy-style CTF events. Visit [ctf.hackthebox.com](https://ctf.hackthebox.com/)",
    },
}
PLATFORM_ORDER = ["CTFd", "rCTF", "GZCTF", "HTB", "Berg", "EPT"]

CAPABILITY_DISPLAY_MAP = {
    "🔑 Authentication & Session": {
        "login": "🔑 Login",
        "session_persistence": "🔄 Session Persistence",
    },
    "👥 Team & User Management": {
        "manage_team": "🧑‍🤝‍🧑 Manage Team",
        "view_team_information": "ℹ️ View Team Information",
        "view_user_profile": "👤 View User Profile",
    },
    "🏆 CTF Event Interaction": {
        "view_ctf_details": "📋 View CTF Details",
        "view_announcements": "📢 View Announcements",
        "view_scoreboard": "🥇 View Scoreboard",
    },
    "🧩 Challenge Interaction": {
        "view_challenges": "🗺️ View Challenges",
        "submit_flags": "🚩 Submit Flags",
        "download_attachments": "📎 Download Attachments",
        "manage_challenge_instances": "⚙️ Manage Challenge Instances",
    },
    "💾 Data Export & Archival": {
        "export_ctf_data": "🗃️ Export CTF Data",
    },
}

# --- Data Fetching ---


def get_platform_capabilities() -> Dict[str, Dict[str, bool]]:
    """
    Parses platform client files to extract their declared capabilities.
    """

    capabilities: Dict[str, Dict[str, bool]] = {}

    for platform in PLATFORM_CLIENTS.keys():
        client = get_platform_client(platform)
        client_instance = client(AsyncClient, "https://example.com")

        caps_data = client_instance.capabilities
        capabilities[client_instance.platform_name] = {
            field: getattr(caps_data, field) for field in Capabilities.model_fields
        }

    return capabilities


# --- Table Generation ---


def generate_features_table(capabilities: Dict[str, Dict[str, bool]]) -> str:
    """
    Generates a Markdown table for the README using emojis.
    """
    # MODIFIED: Simplified header generation
    headers = ["Platform", "Login", "Challenges", "Submit Flags", "Scoreboard"]
    alignment = [":---", ":---:", ":---:", ":---:", ":---:"]

    header_row = "| " + " | ".join(headers) + " |"
    align_row = "| " + " | ".join(alignment) + " |"

    table = [header_row, align_row]

    for name in PLATFORM_ORDER:
        caps = capabilities.get(name)
        if not caps:
            continue
        row = [
            f"**{name}**",
            "✅" if caps.get("login") else "❌",
            "✅" if caps.get("view_challenges") else "❌",
            "✅" if caps.get("submit_flags") else "❌",
            "✅" if caps.get("view_scoreboard") else "❌",
        ]
        table.append("| " + " | ".join(row) + " |")

    table.append("|_More..._|🚧|🚧|🚧|🚧|")

    return "\n".join(table)


def generate_platforms_page_matrix(capabilities: Dict[str, Dict[str, bool]]) -> str:
    """
    Generates the full support matrix for the documentation page using markdown shortcodes.
    """
    platforms = [p for p in PLATFORM_ORDER if p in capabilities]
    headers = ["Feature"] + [
        f"{p}[^{PLATFORM_METADATA.get(p, {}).get('id', '')}]" for p in platforms
    ]
    alignments = [":---"] + [":---:"] * len(platforms)

    table = ["| " + " | ".join(headers) + " |", "| " + " | ".join(alignments) + " |"]

    for group_name, group_caps in CAPABILITY_DISPLAY_MAP.items():
        # table.append(f"| **{group_name}** | " + " | " * len(platforms) + "|")
        for cap_key, display_name in group_caps.items():
            row = [display_name]
            any_supported = False
            for p in platforms:
                supported = capabilities.get(p, {}).get(cap_key, False)
                row.append(":white_check_mark:" if supported else ":x:")
                any_supported |= supported
            if any_supported:
                table.append("| " + " | ".join(row) + " |")

    footnotes = [""]
    for p_name, meta in PLATFORM_METADATA.items():
        if meta["id"] in PLATFORM_CLIENTS:
            footnotes.append(f"[^{meta['id']}]: **{p_name}:** {meta['description']}")

    return "\n".join(table) + "\n" + "\n".join(footnotes)


# --- File Operations ---


def update_section(file_path: Path, section_name: str, new_content: str) -> bool:
    """
    Updates a specific section in a file marked by start/end comments.
    """
    start_marker = f"<!-- {section_name}_START -->"
    end_marker = f"<!-- {section_name}_END -->"

    try:
        content = file_path.read_text()
    except FileNotFoundError:
        print(f"❌ Could not find file {file_path}. Skipping update.")
        return False

    pattern = re.compile(
        f"({re.escape(start_marker)})\n(.*?)\n({re.escape(end_marker)})", re.DOTALL
    )
    replacement = f"\\1\n{new_content}\n\\3"
    new_content_full, num_subs = re.subn(pattern, replacement, content)

    if num_subs > 0 and new_content_full != content:
        file_path.write_text(new_content_full)
        print(f"✅ Updated {section_name} section in {file_path.name}")
        return True

    print(f"ℹ️  No changes needed for {section_name} section in {file_path.name}")
    return False


# --- Main Execution ---


def main():
    """
    Main function to update the README.md file and docs.
    """
    print("🚀 Starting documentation update process...")

    changed = False
    platform_caps = get_platform_capabilities()

    # 1. Update Quickstart Example in README
    quickstart_code = QUICKSTART_PATH.read_text().strip()
    quickstart_md = f"```python\n{quickstart_code}\n```"
    changed |= update_section(README_PATH, "QUICKSTART", quickstart_md)

    # 2. Update Features Table in README
    features_table = generate_features_table(platform_caps)
    changed |= update_section(README_PATH, "PLATFORMS_TABLE", features_table)

    # 3. Update Full Support Matrix in docs
    platforms_matrix = generate_platforms_page_matrix(platform_caps)
    changed |= update_section(PLATFORMS_DOC_PATH, "PLATFORMS_MATRIX", platforms_matrix)

    if changed:
        print("\n🎉 Documentation was updated.")
    else:
        print("\n✨ Documentation is already up to date.")


if __name__ == "__main__":
    main()
