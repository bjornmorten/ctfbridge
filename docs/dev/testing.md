---
title: Testing
description: How to write and run tests for CTFBridge, including unit tests, mock sessions, and integration strategies.
---

# 🧪 Testing Guide

CTFBridge includes a suite of unit and integration tests to ensure correctness across platforms and services. This guide explains how tests are structured and how to write new ones.

---

## 🧰 Tools Used

- `pytest` – test runner
- `httpx` – mock HTTP requests
- `pytest-mock` – mocking utilities
- `pydantic` – for model validation

Install dev dependencies with:

```bash
pip install -e .[dev]
```

Run all tests:

```bash
pytest
```

---

## 🧪 Test Structure

Tests are located under the `tests/` directory and mirror the structure of the main source tree:

```
tests/
├── base/
├── core/
├── platforms/
│   ├── ctfd/
│   └── ...
├── models/
└── utils/
```

Each test module focuses on a specific service or client component.

---

## 🧪 Mocking HTTP Calls

Use `httpx.MockTransport` or `pytest-mock` to simulate HTTP responses.

Example:

```python
import httpx
from httpx import Response

def test_login_success(mocker):
    def fake_post(*args, **kwargs):
        return Response(200, json={"success": True})

    mocker.patch("httpx.Client.post", side_effect=fake_post)
    ...
```

You can also define reusable fixtures for login, challenge lists, or session states.

---

## 🧩 Tips for Writing Tests

- Use `pytest.parametrize()` to cover edge cases
- Keep platform-specific mocks isolated
- Validate both happy paths and failure modes
- Always test service return types (models)

---

Tests ensure the modular architecture of CTFBridge is safe to extend and refactor. When adding new services or platforms, include both unit and integration tests to ensure compatibility.
