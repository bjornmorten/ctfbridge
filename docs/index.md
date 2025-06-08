---
title: Getting Started with CTFBridge
description: CTFBridge is a Python library that unifies interaction with CTF platforms like CTFd, rCTF, and HTB. Install the library and get started with your first script to fetch challenges and submit flags.
---

# CTFBridge

**CTFBridge** is your all-in-one Python toolkit for automating Capture The Flag (CTF) workflows — whether you're farming flags, building bots, or writing automation tools.

## ⚡ What You Can Do

- 🧩 Fetch challenges, metadata, files, and services
- 🚩 Submit flags
- 🏆 Access scoreboards, rankings, and team info
- 🔐 Manage sessions (login, API tokens, persistence)
- 🤖 Build bots, auto-solvers, or monitoring tools with async-first design

## ✨ Why CTFBridge?

- ✅ **One API for all major platforms** — CTFd, rCTF, HTB, and more
- 🧠 **Smart auto-detection** — just give a URL, and we handle the rest
- 🧩 **Challenge enrichment** — attachments, services and more built in
- 🔄 **Persistent sessions** — save & resume your session state
- 🔌 **Extensible design** — plug in your own clients or parsers
- 🚀 **Made for automation** — fully async and script-friendly

## 💻 Installation

Install CTFBridge via pip:

```bash
pip install ctfbridge
```

## 🚀 Quickstart Example

Here's a basic example demonstrating how to authenticate, interact with challenges, submit a flag, and view the scoreboard:

```python
--8<-- "examples/00_quickstart.py"
```

## 📚 Next Steps

  - See more advanced examples in the [Usage Guide](getting-started/usage.md).
  - Check which platforms are supported on the [Supported Platforms](getting-started/platforms.md) page.
  - Browse the complete [API Reference](api/index.md).
