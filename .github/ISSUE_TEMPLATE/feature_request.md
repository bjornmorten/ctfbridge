name: 💡 Feature Request
description: Suggest a new idea or enhancement
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Have a new idea? Help us understand and evaluate it!

  - type: textarea
    id: problem
    attributes:
      label: Is your feature request related to a problem?
      description: A short description of the problem you're trying to solve.
      placeholder: It's frustrating when I can't submit flags offline...

  - type: textarea
    id: solution
    attributes:
      label: Describe the solution you'd like
      description: What should the feature do?
      placeholder: Add a method to store submissions for later upload.
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: Did you consider any other solutions or workarounds?
