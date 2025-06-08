---
title: Usage Guide
description: Learn how to use CTFBridge to interact with supported CTF platforms. Covers setup, logging in, listing challenges, submitting flags, and more.
---

# Usage Guide

This guide provides practical examples of how to use the `ctfbridge` library for common Capture The Flag (CTF) tasks. Each section focuses on a specific aspect of the library.

<!-- prettier-ignore-start -->
??? tip "Asynchronous Code"
    All examples in this guide use `async` and `await` because CTFBridge is designed to be asynchronous. Ensure you run these within an `async` function and use `asyncio.run()` or an existing event loop.
<!-- prettier-ignore-end -->

<h2 class="no-toc">Table of Contents</h2>

- [Initializing the Client](#initializing-the-client)
- [Authentication](#authentication)
- [Working with Challenges](#working-with-challenges)
- [Handling Attachments](#handling-attachments)
- [Accessing the Scoreboard](#accessing-the-scoreboard)
- [Error Handling](#error-handling)

---

## Initializing the Client 🚀

The `create_client` function is your entry point.

### Automatic Platform Detection

This is the simplest way. CTFBridge inspects the URL to identify the platform.

```python
--8<-- "examples/01_initialize_auto.py"
```

### Specifying a Platform

If auto-detection fails or you want to be explicit:

```python
--8<-- "examples/01_initialize_specific.py"
```

---

## Authentication 🔑

Accessing challenges or submitting flags often requires logging in.

### Login with Credentials

Primarily for platforms like CTFd.

```python
--8<-- "examples/02_auth_credentials.py"
```

### Logging Out

Clears session cookies and authorization headers.

```python
--8<-- "examples/02_auth_logout.py"
```

---

## Working with Challenges 🧩

### Fetching All Challenges

```python
--8<-- "examples/03_challenges_get_all.py"
```

### Fetching a Challenge by ID

```python
--8<-- "examples/03_challenges_get_by_id.py"
```

### Filtering Challenges

Apply filters directly in `get_all()`:

```python
--8<-- "examples/03_challenges_filter.py"
```

### Submitting Flags

Requires authentication and platform support.

```python
--8<-- "examples/03_challenges_submit_flag.py"
```

---

## Handling Attachments 📂

Download files associated with challenges.

### Downloading a Single Attachment

```python
--8<-- "examples/04_attachments_download_single.py"
```

### Downloading All Attachments for a Challenge

```python
--8<-- "examples/04_attachments_download_all.py"
```

---

## Accessing the Scoreboard 🏆

View top teams or users.

```python
--8<-- "examples/05_scoreboard_get_top.py"
```

---

## Error Handling 💣

CTFBridge uses custom exceptions, all inheriting from `CTFBridgeError`. Catching these allows for more specific error management.

Always wrap your `ctfbridge` calls in appropriate `try...except` blocks for robust scripts\!

## Checking Platform Capabilities ✨

Different CTF platforms support different features. You can check what the initialized client supports before calling a function to avoid runtime errors and make your scripts more robust.

```python
--8<-- "examples/06_capabilities_check.py"
```
