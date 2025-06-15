---
title: Supported Platforms
description: Discover which CTF platforms are supported by CTFBridge. Compare features like login, challenge access, flag submission, and scoreboard viewing across CTFd, rCTF, HTB, and more.
---

# Supported Platforms

??? info "Check Capabilities Programmatically"
    This table provides a quick at-a-glance overview. For use in your code, you can check these features programmatically using the `client.capabilities` property after initializing a client. See the [Usage Guide](usage.md#checking-platform-capabilities) for an example.

<!-- PLATFORMS_MATRIX_START -->
| Feature | Berg[^berg] | CTFd[^ctfd] | rCTF[^rctf] |
| :--- | :---: | :---: | :---: |
| 🔑 Login | :x: | :white_check_mark: | :white_check_mark: |
| 🔄 Session Persistence | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| 🥇 View Scoreboard | :x: | :white_check_mark: | :white_check_mark: |
| 🗺️ View Challenges | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| 🚩 Submit Flags | :x: | :white_check_mark: | :white_check_mark: |
| 📎 Download Attachments | :white_check_mark: | :white_check_mark: | :white_check_mark: |

[^ctfd]: **CTFd:** A popular open-source CTF platform. [Visit CTFd.io](https://ctfd.io/) or [view on GitHub](https://github.com/CTFd/CTFd).
[^rctf]: **rCTF:** A open-source CTF platform developed by [redpwn](https://redpwn.net/). [View on GitHub](https://github.com/otter-sec/rctf).
[^berg]: **Berg:** A closed-source CTF platform developed by [NoRelect](https://github.com/NoRelect/).
<!-- PLATFORMS_MATRIX_END -->
