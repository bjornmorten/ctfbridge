name: 📄 Documentation Issue
description: Report missing or unclear documentation
labels: ["documentation"]
body:
  - type: textarea
    id: area
    attributes:
      label: What part of the documentation needs improvement?
      placeholder: Examples, API Reference, Installation, etc.
      validations:
        required: true

  - type: textarea
    id: suggestion
    attributes:
      label: What would you like to see changed?
      description: Be as specific as possible.
      placeholder: Add a full example for auth with rCTF.

  - type: input
    id: link
    attributes:
      label: Link to the affected documentation
      placeholder: https://ctfbridge.readthedocs.io/en/latest/...
