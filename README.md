# CTFBridge

[![PyPI](https://img.shields.io/pypi/v/ctfbridge)](https://pypi.org/project/ctfbridge/)
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

- ✅ Unified API for multiple CTF platforms — one interface, no per-platform hacks
- 🧩 Easy to extend with your own platform clients and parsers
- 📦 Challenge enrichment (authors, services, attachments) included out of the box
- 🔒 Clean authentication flow (supports credentials and API tokens)
- 🏁 Submit flags and access scoreboards with ease
- ⚙️  Platform auto-detection from just a URL — no config required
- 🔄 Session save/load support for persistent sessions
- 🤖 Designed for automation and scripting (async-first)

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
| _More platforms_     | 🚧 In development |

## 📚 Documentation

Explore the full documentation at: **[ctfbridge.readthedocs.io](https://ctfbridge.readthedocs.io/)**

Includes:
- Setup and usage guides
- Platform details
- API reference
- Contribution instructions

## 🛠️ Projects Using CTFBridge

These open-source projects are already using CTFBridge:

- [`ctf-dl`](https://github.com/bjornmorten/ctf-dl) — 🗃️ Automates downloading all challenges from a CTF.
- [`pwnv`](https://github.com/CarixoHD/pwnv) — 🧠 Manages CTFs and challenges.

## 📄 License

MIT License © 2025 bjornmorten
