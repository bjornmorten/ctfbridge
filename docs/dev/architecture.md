---
title: Architecture
description: High-level overview of CTFBridge's modular architecture, including its core components, service layout, and platform integration strategy.
---

# 🧩 Architecture Overview

This document provides a high-level overview of the architecture of the `ctfbridge` project. It is intended for developers contributing to the project or seeking to understand its internal structure.

---

## 🔧 Core Components

### `ctfbridge.base`

- Contains the **base client** and **service interfaces**.
- Provides shared abstractions that are platform-agnostic.
- Files:
  <!-- prettier-ignore -->
    - `client.py`: Defines the main `CTFClient` interface.
    - `services/`: Base service classes for auth, challenge, scoreboard, etc.

### `ctfbridge.core`

- Defines low-level HTTP communication and session management.
- Includes reusable logic for requests, sessions, and HTTP clients.
- Files:
  <!-- prettier-ignore -->
    - `http.py`: Core HTTP utilities.
    - `services/`: Core service implementations used by some platforms.

### `ctfbridge.models`

- Contains all data models used across services.
- Models are structured to reflect common CTF platform structures.
- Examples:
  <!-- prettier-ignore -->
    - `Challenge`, `User`, `ScoreboardEntry`, `Submission`

### `ctfbridge.create_client`

- Provides the main entry point to create the appropriate client based on the target platform.
- Handles platform detection and instantiation logic.

---

## 🧩 Platform Implementations

### `ctfbridge.platforms`

- Contains platform-specific implementations for

- Each platform folder includes:
  <!-- prettier-ignore -->
    - `client.py`: Extends the base client for that platform.
    - `services/`: Implements platform-specific services.
    - `http/`, `parsers/`, and `utils/` as needed.

### Platform Detection

- `platforms/detect.py`: Contains logic to identify the platform from a given URL or session.
- `platforms/registry.py`: Maintains mappings between platform IDs and their client implementations.

---

## 🧠 Processor Layer

### `ctfbridge.processors`

- Performs post-processing, enrichment, and extraction on data models.
- Useful for normalizing challenge categories, parsing author lists, etc.
- Submodules:

  - `extractors/`, `enrich.py`, `helpers/`

---

## 🧰 Utilities and Helpers

### `ctfbridge.utils`

- Shared utility modules such as platform caching and URL processing.

### `ctfbridge.exceptions`

- Centralized error definitions for consistent exception handling.

---

## 🎯 Flow Summary

1.  **User initializes** a client via `ctfbridge.create_client()`.
2.  **Platform detection** selects the appropriate subclass.
3.  The selected **platform client** uses:

    - Shared models
    - Core/base HTTP and services
    - Its own service overrides if needed

4.  **User calls** `client.auth`, `client.challenges`, etc., using a unified API.

---

This modular architecture ensures CTFBridge remains easy to extend to new platforms, while keeping a consistent interface for end users.
