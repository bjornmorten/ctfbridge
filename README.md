# CTFBridge

[![PyPI](https://img.shields.io/pypi/v/ctfbridge)](https://pypi.org/project/ctfbridge/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ctfbridge)](https://pypi.org/project/ctfbridge/)
[![Docs](https://img.shields.io/badge/docs-readthedocs-blue.svg)](https://ctfbridge.readthedocs.io)
[![CI](https://github.com/bjornmorten/ctfbridge/actions/workflows/test.yml/badge.svg)](https://github.com/bjornmorten/ctfbridge/actions/workflows/test.yml)
![License](https://img.shields.io/github/license/bjornmorten/ctfbridge)

> [!WARNING]
> **Under active development** – expect breaking changes.

## 🧠 Overview

CTFBridge is a Python library that standardizes interaction with Capture The Flag (CTF) platforms like CTFd, rCTF, and HTB — so you can focus on solving challenges, not reverse-engineering APIs.

Use a single API to:
- 🧩 Fetch challenges and metadata
- 🚩 Submit flags
- 🏆 Access scoreboards
- 🔐 Manage sessions and authentication

## ✨ Features

- ✅ **Unified API** for multiple CTF platforms — no per-platform hacks
- 🧠 **Auto-detect platform type** from just a URL
- 🔐 **Clean auth flow** with support for credentials and API tokens
- 🧩 **Challenge enrichment** — authors, categories, services, attachments
- 🔄 **Persistent sessions** — save/load session state with ease
- 🤖 **Async-first design** — perfect for scripts, tools, and automation

## 📦 Installation

```bash
pip install ctfbridge
```

## 🚀 Quickstart

```python
import asyncio
from ctfbridge import create_client

async def main():
    # Connect and authenticate
    client = await create_client("https://demo.ctfd.io")
    await client.auth.login(username="admin", password="password")

    # Get challenges
    challenges = await client.challenges.get_all()
    for chal in challenges:
        print(f"[{chal.category}] {chal.name} ({chal.value} points)")

    # Submit flags
    await client.challenges.submit(challenge_id=1, flag="CTF{flag}")

    # View the scoreboard
    scoreboard = await client.scoreboard.get_top(5)
    for entry in scoreboard:
        print(f"[+] {entry.rank}. {entry.name} - {entry.score} points")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🧩 Supported Platforms

CTFBridge works out of the box with:

| Platform             | Status            |
| -------------------- | ----------------- |
| CTFd                 | ✅ Supported      |
| rCTF                 | ✅ Supported      |
| Berg                 | ✅ Supported      |
| EPT                  | ✅ Supported      |
| HTB                  | ✅ Supported      |
| _More coming soon_   | 🚧 Planned        |

📖 See [docs.ctfbridge.io/platforms](https://ctfbridge.readthedocs.io/en/latest/platforms/) for details.

## 📚 Documentation

All guides, API references, and platform notes are available at: **[ctfbridge.readthedocs.io](https://ctfbridge.readthedocs.io/)**

Includes:

- ✅ Getting Started
- 🛠 Usage Patterns
- 🔍 API Reference

## 🛠️ Projects Using CTFBridge

These open-source projects are already using CTFBridge:

- [`ctf-dl`](https://github.com/bjornmorten/ctf-dl) — 🗃️ Download all CTF challenges in bulk
- [`pwnv`](https://github.com/CarixoHD/pwnv) — 🧠 CLI to manage CTFs and challenges

## 📄 License

MIT License © 2025 bjornmorten
