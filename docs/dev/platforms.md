---
title: Platform Support
description: Guide to understanding and implementing platform-specific logic in CTFBridge.
---

# 💻 Platform Integration Guide

CTFBridge supports a range of CTF platforms through modular, pluggable platform implementations. Each platform encapsulates its own logic for authentication, challenges, and other services, while exposing a consistent API to users.

---

## 🧭 Platform Architecture

Each supported platform lives in its own subdirectory under `ctfbridge.platforms.<platform>` and includes:

- A custom client (e.g. `<PlatformName>Client`)
- Platform-specific service implementations (auth, challenges, scoreboard, etc.)
- Optional utilities, extractors, or HTTP overrides

---

## 🧱 Platform Folder Structure

```
ctfbridge/platforms/<platform>/
├── client.py
├── services/
│   ├── auth.py
│   ├── challenges.py
│   ├── scoreboard.py
│   └── ...
├── http/
├── utils/
└── __init__.py
```

Only the necessary components need to be implemented. Platform folders follow a consistent structure to ensure discoverability and ease of extension.

---

## 🔍 Platform Detection

Platform detection is handled in two steps:

### 1. `platforms/detect.py`

Contains logic to probe a target instance (usually via `/`) and return a platform identifier string like `ctfd` or `rctf`.

### 2. `platforms/registry.py`

Maps platform IDs to their client classes:

```python
PLATFORM_REGISTRY = {
    "ctfd": CTFdClient,
    "rctf": RCTFClient,
    # etc...
}
```

This lets `factory()` automatically instantiate the right implementation.

---

## 🧠 Adding a New Platform

1. Create a folder under `platforms/<new_platform>`
2. Implement `client.py` with a subclass of `CTFBridgeClient`
3. Implement the necessary services in `services/`
4. Add platform detection logic in `detect.py`
5. Register your client in `registry.py`

You can reuse base and core services or override only what's necessary.

---

## 📚 Example: Adding `examplectf`

1. `platforms/examplectf/client.py`:

```python
class ExampleCTFClient(CTFBridgeClient):
    def __init__(self, url: str):
        self.auth = ExampleAuthService(self)
        self.challenges = ExampleChallengeService(self)
        ...
```

2. `services/auth.py`, `challenges.py`, etc.
3. Add detection logic:

```python
async def static_detect(self, response: httpx.Response) -> Optional[bool]:
    if "Powered by ExampleCTF" in response.text:

```

4. Update `registry.py`:

```python
PLATFORM_REGISTRY["examplectf"] = ExampleCTFClient
```

---

This modular system allows CTFBridge to scale and adapt as new platforms emerge, with minimal duplication of logic.
