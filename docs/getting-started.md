---
title: Getting Started
description: Learn how to install and use CTFBridge, a modular Python framework for interacting with CTF platforms like CTFd and rCTF. Supports login, challenge interaction, and more.
---

## Getting Started

Install CTFBridge via pip:

```bash
pip install ctfbridge
```

Initialize a client for a supported platform:

```python
from ctfbridge import get_client

client = get_client("https://demo.ctfd.io")
client.login("admin", "password")
```

You can now begin interacting with challenges, teams, and flags.

## Requirements

Python 3.8+
