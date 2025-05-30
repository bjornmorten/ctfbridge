---
title: Getting Started
description: Learn how to install and use CTFBridge, a modular Python framework for interacting with CTF platforms like CTFd and rCTF. Supports login, challenge interaction, and more.
---

# Getting Started

Install CTFBridge via pip:

```bash
pip install ctfbridge
```

Initialize a client for a supported platform:

```python
from ctfbridge import create_client

async def main():
    client = await create_client("https://demo.ctfd.io")
    await client.auth.login(username="admin", password="password")

asyncio.run(main())
```

You can now begin interacting with challenges, scoreboards, and flags.

## Requirements

Python 3.8+
