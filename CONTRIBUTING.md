# Contributing to CTFBridge

First off, thank you for considering contributing to CTFBridge! We welcome any contributions, from bug reports and feature requests to code enhancements and documentation improvements.

This document provides a quick guide to get you started. For more detailed information on the project's architecture, how to add new platforms, and other development aspects, please refer to our full [Developer Guide](https://ctfbridge.readthedocs.io/latest/dev/).

## How Can I Contribute?

* **Reporting Bugs**: If you find a bug, please open an issue on our [GitHub Issues page](https://github.com/bjornmorten/ctfbridge/issues), providing as much detail as possible, including steps to reproduce.
* **Suggesting Enhancements**: Have an idea for a new feature or an improvement to an existing one? Feel free to open an issue to discuss it.
* **Pull Requests**: If you want to contribute code or documentation:
    * Fork the repository.
    * Create a new branch for your feature or bugfix (e.g., `feature/add-new-platform` or `fix/challenge-parsing-bug`).
    * Make your changes.
    * Submit a pull request (PR) against the `main` branch.

## Development Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/bjornmorten/ctfbridge.git
    cd ctfbridge
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    Install the project in editable mode with development dependencies:
    ```bash
    pip install -e .[dev]
    ```
    The `[dev]` dependencies are specified in `pyproject.toml` and include tools for testing, linting, and type checking.

4.  **Install pre-commit hooks**:
    CTFBridge uses pre-commit hooks for linting (Ruff) and formatting (Ruff format).
    ```bash
    pre-commit install
    ```
    These hooks will run automatically before each commit. You can also run them manually:
    ```bash
    pre-commit run --all-files
    ```

## Running Tests

Ensure all tests pass before submitting a pull request. Tests are written using `pytest` and `pytest-asyncio`.
```bash
pytest
````

## Coding Style

  * We use [Ruff](https://github.com/astral-sh/ruff) for linting and code formatting. The configuration is in `pyproject.toml`.
  * Pre-commit hooks will help ensure your code adheres to the project's style.

## Pull Request Guidelines

  * **Keep it focused**: Try to keep your PRs focused on a single feature or bugfix.
  * **Tests**: Add tests for any new code or bugfixes.
  * **Documentation**:
      * Update user documentation (in `docs/`) if your changes affect users.
      * Update developer documentation (in `docs/developer/` or relevant docstrings) if your changes affect the internal workings or how others might contribute.
      * Ensure docstrings for new public APIs are clear and comprehensive.
  * **Commit Messages**: Write clear and concise commit messages.
  * **PR Description**: Provide a good description of what your PR does and why. If it addresses an issue, link to it.

## Questions?

If you have any questions, feel free to open an issue or reach out.

Thank you for contributing to CTFBridge!
