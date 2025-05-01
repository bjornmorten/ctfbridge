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
