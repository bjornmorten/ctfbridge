# API Overview

Welcome to the API reference section of **CTFBridge**. This section documents the public interface for interacting with CTF platforms through the unified `ctfbridge` client. It is intended for developers integrating CTFBridge into their own automation or analysis workflows.

---

## 🔧 API Structure

CTFBridge exposes its functionality through a centralized `client` object created using the `factory()` function. This object provides access to service modules grouped by functionality:

| Client Attribute     | Description                                        |
| -------------------- | -------------------------------------------------- |
| `client.auth`        | Handles login, logout, and session validation.     |
| `client.challenges`  | Lists, filters, retrieves, and submits challenges. |
| `client.attachments` | Downloads challenge-related files.                 |
| `client.scoreboard`  | Views the top teams or users.                      |
| `client.session`     | Manages cookies and session helpers.               |

Each of these modules is implemented as a **service class** (e.g. `AuthService`, `ChallengeService`) and can be interacted with using clean, typed Python methods.

---

## 🏁 Getting Started with the Client

```python
from ctfbridge import create_client

client = create_client("https://examplectf.com")
client.auth.login(username="username", password="password")

challenges = client.challenges.get_all()
for chal in challenges:
    print(chal.name, chal.points)
```

---

## 📦 Models

All returned data is strongly typed using structured Python classes defined in `ctfbridge.models`. Some key models include:

- `Challenge`
- `Submission`
- `ScoreboardEntry`
- `User`

These help ensure consistent structure and enable IDE auto-completion and static analysis.

---

## 🧠 Notes for Developers

- All services follow a consistent structure and interface.
- Internally, platform-specific behavior is abstracted away behind the scenes.
- You should generally not need to care whether you're working with CTFd, HTB, rCTF, etc.

For detailed usage of each API component, see the individual reference pages in this section:

- [⚙️ Client](client.md)
- [🧱 Models](models.md)
