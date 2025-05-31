---
title: Service Layer
description: Learn how to create, extend, and override services in CTFBridge to support authentication, challenges, and more.
---

# 🧵 Service Layer Guide

CTFBridge organizes platform functionality into modular **services**. These services define the logic for common tasks such as logging in, fetching challenges, submitting flags, and accessing the scoreboard.

---

## 🏗️ Base and Core Services

Base service interfaces live in `ctfbridge.base.services` and define expected methods. Core logic is implemented in `ctfbridge.core.services`, which base service classes inherit from. This split allows reuse of shared logic across platforms, while clearly defining the public interface.

Example interface (in `base.services.auth`):

```python
class AuthService:
    def login(self, username: str, password: str) -> bool:
        raise NotImplementedError
```

Common implementation (in `core.services.auth`):

```python
class AuthServiceImpl(AuthService):
    def login(self, username, password):
        # Shared POST login logic
        ...
```

Platform services can choose to inherit directly from core classes, or override specific behavior as needed.

---

## 🧬 Platform-Specific Services

Located in `ctfbridge.platforms.<platform>.services`, these classes inherit from core or base services and implement platform-specific logic. For example:

```python
class CTFdAuthService(AuthServiceImpl):
    def login(self, username, password):
        ...
```

Each platform typically includes:

- `auth.py`
- `challenges.py`
- `scoreboard.py`
- `attachments.py`
- `session.py` (if needed)

These services are composed into the client for that platform.

---

## 🧠 How They Plug Into Clients

Each platform-specific client (e.g. `CTFdClient`) is responsible for instantiating the appropriate services:

```python
class CTFdClient(CTFBridgeClient):
    def __init__(self, url: str):
        self.auth = CTFdAuthService(self)
        self.challenges = CTFdChallengeService(self)
        ...
```

This allows consumers of the library to use a **consistent interface**:

```python
client = create_client("https://myctf.io")
client.auth.login(username="admin", password="password")
chals = client.challenges.get_all()
```

---

## 📦 Shared Behavior and Utilities

If multiple platforms share similar logic, it can be factored into:

- `ctfbridge.core.services`: common service behavior
- `ctfbridge.helpers/`: smaller utility modules for reuse

---

## ✨ Adding a New Service

1. Define a base class in `base/services/` if one doesn't exist.
2. Implement shared logic in `core/services/` if reusable.
3. Implement the service in `platforms/<platform>/services/`.
4. Register it in the platform client.
5. Update the models and tests if needed.

---

Services form the backbone of CTFBridge's extensible API. They isolate logic by concern and allow clean overrides for platform-specific behavior.
