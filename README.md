<h1 align="center">
  CTFBridge
</h1>

<h4 align="center">A unified Python interface for all major CTF platforms </h4>

<p align="center">
  <a href="https://pypi.org/project/ctfbridge/"><img src="https://img.shields.io/pypi/v/ctfbridge" alt="PyPI"></a>
  <a href="https://pypi.org/project/ctfbridge/"><img src="https://img.shields.io/pypi/pyversions/ctfbridge" alt="Python Versions"></a>
  <a href="https://ctfbridge.readthedocs.io"><img src="https://img.shields.io/badge/docs-readthedocs-blue.svg" alt="Docs"></a>
  <a href="https://github.com/bjornmorten/ctfbridge/actions/workflows/test.yml"><img src="https://github.com/bjornmorten/ctfbridge/actions/workflows/test.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/github/license/bjornmorten/ctfbridge" alt="License">
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Install</a> •
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-documentation">Docs</a> •
  <a href="#-license">License</a>
</p>

---

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

| Platform  | &nbsp;&nbsp;&nbsp;Auth&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;Challenges&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;Flags&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;Scoreboard&nbsp;&nbsp; |
| --------- | :--------------------------------------: | :--------------------------------: | :----------------------------------------: | :--------------------------------: |
| **CTFd**  |                    ✅                    |                 ✅                 |                     ✅                     |                 ✅                 |
| **rCTF**  |                    ✅                    |                 ✅                 |                     ✅                     |                 ✅                 |
| **HTB**   |                    ✅                    |                 ✅                 |                     ✅                     |                 ✅                 |
| **Berg**  |                    ❌                    |                 ✅                 |                     ❌                     |                 ❌                 |
| **EPT**   |                    ❌                    |                 ✅                 |                     ❌                     |                 ❌                 |
| _More..._ |                    🚧                    |                 🚧                 |                     🚧                     |                 🚧                 |

📖 See [docs](https://ctfbridge.readthedocs.io/latest/getting-started/platforms/) for details.

## 📚 Documentation

All guides, API references, and platform notes are available at: **[ctfbridge.readthedocs.io](https://ctfbridge.readthedocs.io/)**

## 🤝 Contributing

Contributions are welcome! We appreciate any help, from bug reports and feature requests to code enhancements and documentation improvements.

Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

## 🛠️ Projects Using CTFBridge

These open-source projects are already using CTFBridge:

- [`ctf-dl`](https://github.com/bjornmorten/ctf-dl) — 🗃️ Download all CTF challenges in bulk
- [`pwnv`](https://github.com/CarixoHD/pwnv) — 🧠 CLI to manage CTFs and challenges

## 📄 License

MIT License © 2025 bjornmorten
