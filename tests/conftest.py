import pytest


def pytest_collection_modifyitems(config, items):
    if config.option.markexpr:
        return  # Respect explicit -m filters

    skip_e2e = pytest.mark.skip(reason="Skipped by default. Run with -m e2e to include.")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)
