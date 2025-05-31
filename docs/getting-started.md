---
title: Getting Started
description: Learn how to install and use CTFBridge, a modular Python framework for interacting with CTF platforms like CTFd and rCTF. Supports login, challenge interaction, and more.
---

# Getting Started

Install CTFBridge via pip:

```bash
pip install ctfbridge
```

Here's a basic example demonstrating how to authenticate, interact with challenges, submit a flag, and view the scoreboard:

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

## Requirements

Python 3.10+
