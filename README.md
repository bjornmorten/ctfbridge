<h1 align="center">
  CTFBridge
</h1>

<h4 align="center">A unified Python interface for all major CTF platforms </h4>

<p align="center">
  <a href="https://pypi.org/project/ctfbridge/"><img src="https://img.shields.io/pypi/v/ctfbridge" alt="PyPI"></a>
  <a href="https://pypi.org/project/ctfbridge/"><img src="https://img.shields.io/pypi/pyversions/ctfbridge" alt="Python Versions"></a>
  <a href="https://ctfbridge.readthedocs.io"><img src="https://img.shields.io/badge/docs-readthedocs-blue.svg" alt="Docs"></a>
  <a href="https://github.com/bjornmorten/ctfbridge/actions/workflows/ci.yml"><img src="https://github.com/bjornmorten/ctfbridge/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
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

- ✅ **Unified API** for multiple CTF platforms
- 🧠 **Auto-detect platform type** from just a URL
- 🔐 **Clean auth flow** with support for credentials and API tokens
- 🧩 **Challenge enrichment** — parses services and attachments from descriptions
- 🔄 **Persistent sessions** — save/load session state with ease
- 🤖 **Async-first design** — perfect for scripts, tools, and automation

## 📦 Installation

```bash
pip install ctfbridge
```

## 🚀 Quickstart

<!-- QUICKSTART_START -->
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

    # Submit a flag
    await client.challenges.submit(challenge_id=1, flag="CTF{flag}")

    # View the scoreboard
    scoreboard = await client.scoreboard.get_top(5)
    for entry in scoreboard:
        print(f"[+] {entry.rank}. {entry.name} - {entry.score} points")


if __name__ == "__main__":
    asyncio.run(main())
```
<!-- QUICKSTART_END -->

## 🧩 Supported Platforms

CTFBridge works out of the box with:

<!-- PLATFORMS_TABLE_START -->
| Platform | Login | View Challenges | Submit Flags | View Scoreboard |
| :--- | :---: | :---: | :---: | :---: |
| **CTFd** | ✅ | ✅ | ✅ | ✅ |
| **rCTF** | ✅ | ✅ | ✅ | ✅ |
| **GZCTF** | ✅ | ✅ | ✅ | ✅ |
| **HTB** | ✅ | ✅ | ✅ | ✅ |
| **Berg** | ❌ | ✅ | ❌ | ❌ |
| **EPT** | ❌ | ✅ | ❌ | ❌ |
| **CryptoHack** | ✅ | ✅ | ✅ | ❌ |
| **pwnable.tw** | ✅ | ✅ | ✅ | ❌ |
| **pwnable.xyz** | ✅ | ✅ | ✅ | ❌ |
| **pwnable.kr** | ✅ | ✅ | ✅ | ❌ |
|_More..._|🚧|🚧|🚧|🚧|
<!-- PLATFORMS_TABLE_END -->

📖 See [docs](https://ctfbridge.readthedocs.io/latest/getting-started/platforms/) for details.

## 📚 Documentation

All guides and API references are available at: **[ctfbridge.readthedocs.io](https://ctfbridge.readthedocs.io/)**

## 🤝 Contributing

Contributions are welcome! We appreciate any help, from bug reports and feature requests to code enhancements and documentation improvements.

Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

## 🛠️ Projects Using CTFBridge

| Project | Description |
|---------|-------------|
| [**ctf-dl**](https://github.com/bjornmorten/ctf-dl) | 🗃️ A CTF challenge bulk downloader |
| [**ctf-sniper**](https://github.com/bjornmorten/ctf-sniper) | 🎯 An automated flag submission tool |
| [**pwnv**](https://github.com/CarixoHD/pwnv) | 🧠 A CTF workspace management tool |

Using CTFBridge in the wild? [Send a PR](https://github.com/bjornmorten/ctfbridge/edit/main/README.md) to feature it here!

## 📄 License

MIT License © 2025 [bjornmorten](https://github.com/bjornmorten)
