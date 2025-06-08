---
title: Supported Platforms
description: Discover which CTF platforms are supported by CTFBridge. Compare features like login, challenge access, flag submission, and scoreboard viewing across CTFd, rCTF, HTB, and more.
---

# Supported Platforms

??? info "Check Capabilities Programmatically"
    This table provides a quick at-a-glance overview. For use in your code, you can check these features programmatically using the `client.capabilities` property after initializing a client. See the [Usage Guide](usage.md#checking-platform-capabilities) for an example.

| Feature                   |    CTFd[^ctfd]     |    rCTF[^rctf]     |    Berg[^berg]     |     EPT[^ept]      |     HTB[^htb]      |
| ------------------------- | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: |
| 🔐 Authentication         | :white_check_mark: | :white_check_mark: |        :x:         |        :x:         | :white_check_mark: |
| 📋 View challenges        | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| 📎 Download attachments   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| 🚩 Submit flags           | :white_check_mark: | :white_check_mark: |        :x:         |        :x:         | :white_check_mark: |
| 🏆 View scoreboard        | :white_check_mark: | :white_check_mark: |        :x:         |        :x:         | :white_check_mark: |
| 👤 View team information  |        :x:         |        :x:         |        :x:         |        :x:         |        :x:         |
| 🧭 View CTF details       |        :x:         |        :x:         |        :x:         |        :x:         |        :x:         |
| 🛠️ On-demand services     |        :x:         |        :x:         |        :x:         |        :x:         |        :x:         |

[^ctfd]: **CTFd:** A popular open-source CTF platform. [Visit CTFd.io](https://ctfd.io/) or [view on GitHub](https://github.com/CTFd/CTFd).
[^rctf]: **rCTF:** A open-source CTF platform developed by [redpwn](https://redpwn.net/). [View on GitHub](https://github.com/otter-sec/rctf).
[^berg]: **Berg:** A closed-source CTF platform developed by [NoRelect](https://github.com/NoRelect/).
[^ept]: **EPT:** A closed-source CTF platform developed by [Equinor Pwn Team](https://x.com/ept_gg).
[^htb]: **HTB:** Hack The Box's platform for Jeopardy-style CTF events. Visit [ctf.hackthebox.com](https://ctf.hackthebox.com/)
