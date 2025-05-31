name: 🐛 Bug Report
description: Report something that's not working correctly
labels: ["bug", "needs triage"]
body:
  - type: markdown
    attributes:
      value: |
        Please describe the issue you're experiencing. Include as much detail as possible.

  - type: textarea
    id: description
    attributes:
      label: What happened?
      description: A clear and concise description of what the bug is.
      placeholder: The `submit` function raises a 403 error when...
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce the bug?
      placeholder: |
        1. Go to '...'
        2. Run the script
        3. See the error
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: CTFBridge Version
      placeholder: e.g. 1.2.3

  - type: textarea
    id: environment
    attributes:
      label: Environment
      placeholder: OS, Python version, CTF platform, etc.
