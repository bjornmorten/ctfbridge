name: 🧩 Platform Support Request
description: Suggest adding support for a new CTF platform
labels: ["platform", "enhancement"]
body:
  - type: input
    id: platform_name
    attributes:
      label: Platform Name
      placeholder: e.g. MetaCTF, FBCTF, Custom Internal CTF

  - type: input
    id: platform_url
    attributes:
      label: Platform URL (if public)
      placeholder: https://ctf.example.com

  - type: textarea
    id: key_features
    attributes:
      label: What key features does this platform support?
      description: Tell us what works on the platform — auth, challenges, scoreboard, etc.
      placeholder: |
        - Login with username/password
        - JSON API for challenges at /api/challenges
        - Scoreboard available at /api/scoreboard

  - type: textarea
    id: authentication
    attributes:
      label: How does authentication work?
      description: Credentials, tokens, session cookies, etc.
      placeholder: |
        Login via POST /login with username/password
        Token returned in response as JSON

  - type: textarea
    id: anything_else
    attributes:
      label: Anything else we should know?
      placeholder: API docs, example accounts, known differences from other platforms, etc.
