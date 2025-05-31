# Developer Guide

Welcome to the developer documentation for **CTFBridge**. This guide is for contributors and advanced users who want to understand how the system works under the hood, extend its capabilities, or develop new features and platform integrations.

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/bjornmorten/ctfbridge.git
cd ctfbridge
```

### Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### Run Tests

```bash
pytest
```

---

## 🧱 Project Structure

* `ctfbridge.base/` – Platform-agnostic service interfaces and base client
* `ctfbridge.core/` – Core API logic and shared services
* `ctfbridge.models/` – Data models used throughout the system
* `ctfbridge.platforms/` – Platform-specific implementations (CTFd, rCTF, HTB, etc.)
* `ctfbridge.factory.py` – Entry point for creating the right client based on target URL
* `ctfbridge.processors/` – Extractors and enrichers for processing challenges

---

## 📚 Dev Docs Overview

| Document                             | Description                                                    |
| ------------------------------------ | -------------------------------------------------------------- |
| [`architecture.md`](architecture.md) | High-level component architecture                              |
| [`platforms.md`](platforms.md)       | Guide to implementing support for a new CTF platform           |
| [`services.md`](services.md)         | How to create and extend services like auth or challenges      |
| [`models.md`](models.md)             | Details on how models are structured and validated             |
| [`errors.md`](errors.md)             | Exception types and error-handling conventions                 |
| [`testing.md`](testing.md)           | Writing unit/integration tests, mocking services               |
| [`style.md`](style.md)               | Code formatting, typing, and contribution style guidelines     |
| [`docs.md`](docs.md)                 | How the documentation system works and how to contribute to it |
