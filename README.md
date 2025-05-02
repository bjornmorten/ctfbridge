# CTFBridge

![PyPI](https://img.shields.io/pypi/v/ctfbridge)
[![Docs](https://img.shields.io/badge/docs-readthedocs-blue.svg)](https://ctfbridge.readthedocs.io)
![License](https://img.shields.io/github/license/bjornmorten/ctfbridge)

CTFBridge is a Python library for interacting with multiple CTF platforms through a unified interface.

> ⚠️ **Under active development** – expect breaking changes.

## Overview

CTFBridge provides a simple, unified API to interact with different Capture the Flag (CTF) competition platforms like CTFd and more.

It hides platform-specific quirks and gives you consistent access to challenges, submissions, and authentication across platforms.

## Features

- 🌟 Unified API across different CTF platforms
- 📄 Fetch challenges, attachments, and challenge metadata
- 🔑 Handle logins, sessions, and authentication cleanly
- ⚡ Automatic rate-limiting and retry handling
- 🧩 Easy to extend with new platform clients
- 🧪 Demo client for quick testing without external servers

## Installation

```bash
pip install ctfbridge
```

## Basic Usage

```python
from ctfbridge import get_client

# Connect and authenticate
client = get_client("https://demo.ctfd.io")
client.login("admin", "password")

# Get challenges
challenges = client.challenges.get_all()
for chal in challenges:
    print(f"[{chal.category}] {chal.name} ({chal.value} points)")

# Submit flags
client.challenges.submit(challenge_id=1, flag="CTF{flag}")

# View the scoreboard
scoreboard = client.scoreboard.get_top(5)
for entry in scoreboard:
    print(f"[+] {entry.rank}. {entry.name} - {entry.score} points")
```

## Supported Platforms

| Platform             | Status            |
| -------------------- | ----------------- |
| CTFd                 | ✅ Supported      |
| rCTF                 | ✅ Supported      |
| Demo (Local testing) | ✅ Available      |
| _More platforms_     | 🚧 In development |

## Documentation

Full documentation: [ctfbridge.readthedocs.io](https://ctfbridge.readthedocs.io/)

## Projects Using CTFBridge

These projects use `ctfbridge`:

- [`ctf-dl`](https://github.com/bjornmorten/ctf-dl) — Automates downloading all challenges from a CTF.
- [`pwnv`](https://github.com/CarixoHD/pwnv) — Manages CTFs and challenges.

## License

MIT License © 2025 bjornmorten
