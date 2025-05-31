---
title: Data Models
description: Overview of the data models used in CTFBridge to represent challenges, submissions, users, and more.
---

# 🧬 Data Model Guide

CTFBridge uses typed Python classes to represent structured data returned by the client services. These classes are defined in `ctfbridge.models` and help ensure correctness, validation, and clarity across all supported platforms.

---

## 🧱 What Models Are Used For

Models represent common entities like:

- Challenges
- Users
- Submissions
- Scoreboard entries
- Attachments

They are used throughout service responses, making it easier to reason about API return values and maintain compatibility across platforms.

---

## 🧰 Where Models Live

All models are defined under `ctfbridge/models/` and typically subclass `pydantic.BaseModel`. This gives us automatic validation, type hinting, and `.json()` export capability.

Example:

```python
from pydantic import BaseModel

class Challenge(BaseModel):
    id: str
    name: str
    category: str
    value: int
    solved: bool = False
```

---

## 🔄 Platform-Agnostic Abstraction

CTFBridge normalizes platform-specific data into these unified model classes. For example:

- A CTFd challenge and a rCTF challenge will both become `Challenge` objects
- Flag submissions from any platform use the same `Submission` class

This abstraction ensures clients don’t need to worry about differences in platform API responses.

---

## 🧩 Extending Models

If a new platform introduces a field not covered by the base model:

- Extend the model in a platform-specific way only if necessary
- Prefer enriching with `processors` rather than modifying core model definitions

---

## 🧪 Model Testing

Model schemas are validated automatically via Pydantic. You can write tests using `model_instance.dict()` or `.json()` to assert serialization, or round-trip parsing of real API responses.

---

Models provide structure and consistency across services, making CTFBridge more maintainable, extensible, and easier to use from any consumer or automation tool.
