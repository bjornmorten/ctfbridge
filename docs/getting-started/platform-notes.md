---
title: Platform-Specific Notes
description: Essential guides and notes for using CTFBridge with specific platforms like CTFd, rCTF, and HTB. Find platform-specific URL formats, authentication methods, and key quirks.
---

# ✨ Platform-Specific Notes

While CTFBridge provides a unified API, each CTF platform has its own unique characteristics. This page provides essential notes to ensure a smooth experience when interacting with each supported platform. For a high-level comparison of platforms, see the [Supported Platforms](./platforms.md) page.

-----

## CTFd

??? note "Authentication"
    - **Supported Methods**: CTFd supports both **Credentials** (username/password) and **API Tokens**.
    - **API Tokens**: You can generate an API token from your profile settings on the CTFd instance.

??? info "Key Notes & Quirks"
    - Fetching detailed challenge information requires an individual API request per challenge, so using `detailed=True` in `get_all()` may be slower on instances with many challenges.

-----

## rCTF

??? warning "Authentication"
    - **Supported Method**: rCTF support is **token-only**. You must use a **Team Token** to log in.
    - **Getting Your Token**: You can pass the entire rCTF invite URL directly into the `login()` function. The library will automatically extract the token from it.
      ```python
      # The library handles this automatically
      await client.auth.login(token="https://my.rctf.com/login?token=xxxxxxxx")
      ```

-----

## Berg

??? warning "Scoreboard Support"
    - The client does **not** support fetching scoreboards, since the platform calculates and render scoreboard data entirely client-side, without exposing it through their API.
