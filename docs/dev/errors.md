---
title: Error Handling
description: Learn how exceptions are structured and managed across CTFBridge services.
---

# 🧯 Error Handling Guide

CTFBridge uses custom exception classes to represent common error conditions, such as login failure, unsupported platforms, or invalid API responses. This guide explains how errors are structured and how to raise or catch them.

---

## ⚠️ Where Errors Are Defined

All custom exceptions live in `ctfbridge.exceptions`. These include:

- `CTFBridgeError` – base class for all library errors
- `PlatformNotDetectedError`
- `AuthenticationError`
- `NotFoundError`
- `InvalidResponseError`

Each one represents a specific failure scenario and provides a helpful message or context object.

---

## 🧠 Raising Errors

Service methods should raise specific exceptions when something fails:

```python
from ctfbridge.exceptions import AuthenticationError

if not response.ok:
    raise AuthenticationError("Login failed: invalid credentials")
```

This provides consistent error messaging across all platforms.

---

## 🧪 Catching Errors

Consumers of CTFBridge can catch specific exceptions or the base `CTFBridgeError` class:

```python
from ctfbridge.exceptions import CTFBridgeError

try:
    client.auth.login("wrong", "creds")
except CTFBridgeError as e:
    print("Something went wrong:", e)
```

This makes it easy to handle known failure cases and build robust CLI tools or integrations.

---

## 📦 Adding a New Exception

1. Subclass `CTFBridgeError`
2. Add a helpful docstring and constructor
3. Raise it from appropriate service or platform code

Example:

```python
class FlagSubmissionError(CTFBridgeError):
    """Raised when a flag could not be submitted successfully."""
```

---

Clear and consistent error handling ensures CTFBridge users can respond to failure scenarios programmatically, improving developer experience and automation reliability.
