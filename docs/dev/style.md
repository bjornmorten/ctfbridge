---
title: Style Guide
description: Coding conventions and best practices for contributing to CTFBridge.
---

# 📐 Code Style Guide

This guide outlines the conventions and standards used across the CTFBridge codebase. Following these ensures consistency, readability, and ease of collaboration.

---

## 🧠 General Principles

- Be **explicit**, not implicit.
- Prefer **clarity over cleverness**.
- Keep functions and classes **short and focused**.
- Use **type annotations** consistently.
- Write **docstrings** for all public classes and methods.

---

## 🧼 Formatting and Linting

We use the following tools:

- **[ruff](https://github.com/astral-sh/ruff)** – linting (fast, multi-rule engine)
- **mypy** – type checking

To format and lint:

```bash
ruff .
mypy .
```

---

## 🧾 Naming Conventions

| Type     | Convention   | Example            |
| -------- | ------------ | ------------------ |
| Variable | `snake_case` | `challenge_name`   |
| Function | `snake_case` | `get_challenges()` |
| Class    | `PascalCase` | `ChallengeModel`   |
| Constant | `UPPER_CASE` | `DEFAULT_TIMEOUT`  |

Avoid abbreviations unless they are widely understood (`url`, `id`, etc.).

---

## ✍️ Docstrings

Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

Example:

```python
def get_flag(challenge_id: str) -> str:
    """Retrieve the flag for a given challenge ID.

    Args:
        challenge_id: The ID of the challenge.

    Returns:
        The flag string if found.
    """
```

All public methods and classes should have docstrings.

---

## 🧪 Testing Style

- Use `pytest` style assertions
- Group tests by module and use fixtures for setup
- Mock network calls, never hit real platforms
- Include both positive and negative test cases

---

## 🗂️ File Organization

- Keep files short: split modules if they grow too large
- Match structure between `src/` and `tests/`
- Avoid circular imports with careful module boundaries

---

Consistent style makes CTFBridge easier to maintain, review, and scale as a collaborative open-source project.
