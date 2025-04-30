# CTF Bridge

CTF Bridge is a Python library for interacting with multiple CTF platforms through a unified interface.

⚠️ This project is still in development ⚠️

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

client = get_client("https://demo.ctfd.io")
client.login("admin", "password")

challenges = client.challenges.get_all()
for chal in challenges:
    print(f"[{chal.category}] {chal.name} ({chal.value} points)")

scoreboard = client.scoreboard.get_top(5)
for entry in scoreboard:
    print(f"[+] {entry.rank}. {entry.name} - {entry.score} points")
```

## Supported Platforms

| Platform             | Status             |
| -------------------- | ------------       |
| CTFd                 | ✅ Supported       |
| rCTF                 | ✅ Supported       |
| Demo (Local testing) | ✅ Available       |
| *More platforms*     | 🚧 In development  |

## 🧩 Projects Using CTFBridge

These projects use `ctfbridge`:

- [`ctf-dl`](https://github.com/bjornmorten/ctf-dl) — Automates downloading all challenges from a CTF.
- [`pwnv`](https://github.com/CarixoHD/pwnv) — Manages CTFs and challenges.

## License

MIT License © 2025 bjornmorten
